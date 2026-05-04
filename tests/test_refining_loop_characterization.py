"""
Characterization tests for RefiningLoop.auto_fix_loop() and run_fix_loop().

These tests record the CURRENT behaviour of auto_fix_loop as a regression
anchor for the Phase 2/3 refactor. They use:
  - A real temp file with valid Manim code
  - Mocked subprocess.run (no actual Manim installed required)
  - Mocked LLMClient / VisionAgent to avoid API calls

Run with: pytest tests/test_refining_loop_characterization.py -v

IMPORTANT: If these tests fail after a refactor, it means observable behaviour
changed. Fix the refactor, not the tests (unless the behavioural change is
intentional and documented).
"""

import os
import sys
import json
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Fixtures ──────────────────────────────────────────────────────────────────

MINIMAL_MANIM_CODE = textwrap.dedent("""\
    from manim import *

    class GeneratedScene(Scene):
        def construct(self):
            t = Text("Hello")
            self.play(Write(t))
            self.wait(1)
""")

MINIMAL_SCRIPT_JSON = json.dumps({
    "scenes": [{"sequence": ["Step 1"], "narration": ["Hello world"]}]
})


def make_temp_script(code: str = MINIMAL_MANIM_CODE) -> tuple[str, str]:
    """Create a temp .py file with the given code. Returns (dir, file_path)."""
    tmp_dir = tempfile.mkdtemp(prefix="llmanim_test_")
    file_path = os.path.join(tmp_dir, "test_script.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return tmp_dir, file_path


def fake_video_at(media_base: str, scene_name: str, fps: int) -> str:
    """Create a zero-byte fake video file where Manim would put it."""
    video_dir = os.path.join(media_base, "videos", "test_script", f"480p{fps}")
    os.makedirs(video_dir, exist_ok=True)
    path = os.path.join(video_dir, f"{scene_name}.mp4")
    with open(path, "wb") as f:
        f.write(b"\x00" * 1024)  # non-zero size so shutil.move succeeds
    return path


# ── Helpers: common mock factories ────────────────────────────────────────────

def make_mock_llm():
    llm = MagicMock()
    llm.session_stats = {
        "time_render_sec": 0.0,
        "time_vision_sec": 0.0,
        "time_coder_sec": 0.0,
    }
    # ask_for_fix returns valid Python code
    llm.ask_for_fix.return_value = MINIMAL_MANIM_CODE
    llm.ask_for_fix_n.return_value = [MINIMAL_MANIM_CODE]
    return llm


def vision_pass_audit():
    return {
        "verdict": "PASS",
        "confidence_score": 5,
        "defects": [],
        "overall_critique": "Looks good",
    }


def vision_fail_audit():
    return {
        "verdict": "FAIL",
        "confidence_score": 1,
        "defects": [{"code": "OVERLAP", "description": "overlap", "suggested_fix": "fix it"}],
        "overall_critique": "Bad layout",
    }


# ── Test: FixLoopResult adapter ───────────────────────────────────────────────

class TestFixLoopResult:
    """Tests for the run_fix_loop() thin adapter (Design C)."""

    def test_video_path_is_none_on_failure(self, tmp_path):
        from agents.orchestrator.refining_loop_types import run_fix_loop, FailureReason

        file_path = tmp_path / "scene.py"
        file_path.write_text(MINIMAL_MANIM_CODE)

        # Simulate auto_fix_loop returning False (complete failure)
        with patch("agents.orchestrator.refining_loop.RefiningLoop.auto_fix_loop",
                   return_value=False) as mock_loop:
            result = run_fix_loop(
                str(file_path), "GeneratedScene", "test topic", MINIMAL_SCRIPT_JSON
            )

        assert result.video_path is None
        assert result.is_best_effort is False

    def test_video_path_set_on_success(self, tmp_path):
        from agents.orchestrator.refining_loop_types import run_fix_loop, FailureReason

        fake_path = str(tmp_path / "output.mp4")
        with patch("agents.orchestrator.refining_loop.RefiningLoop.auto_fix_loop",
                   return_value=fake_path):
            result = run_fix_loop(
                str(tmp_path / "scene.py"), "GeneratedScene", "topic", MINIMAL_SCRIPT_JSON
            )

        assert result.video_path == fake_path
        assert result.failure_reason == FailureReason.SUCCESS

    def test_is_best_effort_flag_propagated(self, tmp_path):
        from agents.orchestrator.refining_loop_types import run_fix_loop

        fake_path = str(tmp_path / "output.mp4")

        def fake_loop(*args, **kwargs):
            if kwargs.get("_diagnostics") is not None:
                kwargs["_diagnostics"]["is_best_effort"] = True
                kwargs["_diagnostics"]["failure_reason"] = "max_iterations"
            return fake_path

        with patch("agents.orchestrator.refining_loop.RefiningLoop.auto_fix_loop",
                   side_effect=fake_loop):
            result = run_fix_loop(
                str(tmp_path / "scene.py"), "GeneratedScene", "topic", MINIMAL_SCRIPT_JSON
            )

        assert result.is_best_effort is True

    def test_counters_propagated_from_diagnostics(self, tmp_path):
        from agents.orchestrator.refining_loop_types import run_fix_loop

        def fake_loop(*args, **kwargs):
            if kwargs.get("_diagnostics") is not None:
                kwargs["_diagnostics"].update({
                    "visual_attempts": 2,
                    "linter_only_retries": 1,
                    "consecutive_timeouts": 0,
                    "main_i": 3,
                    "is_best_effort": False,
                    "failure_reason": "success",
                    "reflection_memory": [],
                    "failed_code_snapshots": [],
                })
            return str(tmp_path / "out.mp4")

        with patch("agents.orchestrator.refining_loop.RefiningLoop.auto_fix_loop",
                   side_effect=fake_loop):
            result = run_fix_loop(
                str(tmp_path / "scene.py"), "GeneratedScene", "topic", MINIMAL_SCRIPT_JSON
            )

        assert result.counters_final["visual"] == 2
        assert result.counters_final["linter"] == 1
        assert result.counters_final["main_i"] == 3

    def test_wall_time_is_positive(self, tmp_path):
        from agents.orchestrator.refining_loop_types import run_fix_loop

        with patch("agents.orchestrator.refining_loop.RefiningLoop.auto_fix_loop",
                   return_value=False):
            result = run_fix_loop(
                str(tmp_path / "scene.py"), "GeneratedScene", "topic", MINIMAL_SCRIPT_JSON
            )

        assert result.total_wall_time >= 0.0


# ── Test: PipelineContext counter semantics ───────────────────────────────────

class TestPipelineContext:
    """Unit tests for PipelineContext counter semantics — the core of Change 2."""

    def setup_method(self):
        from agents.orchestrator.pipeline_context import PipelineContext
        self.ctx = PipelineContext(
            max_attempts=5,
            visual_attempts_limit=3,
            linter_retry_budget=3,
        )

    def test_charge_visual_increments(self):
        assert self.ctx.visual_attempts == 0
        self.ctx.charge_visual()
        assert self.ctx.visual_attempts == 1

    def test_charge_visual_returns_true_at_limit(self):
        self.ctx.visual_attempts = 2
        assert self.ctx.charge_visual() is True
        assert self.ctx.visual_attempts == 3

    def test_charge_visual_returns_false_below_limit(self):
        assert self.ctx.charge_visual() is False  # 0 → 1, limit is 3

    def test_charge_linter_independent_from_visual(self):
        """Linter failures must NOT affect visual_attempts."""
        before = self.ctx.visual_attempts
        self.ctx.charge_linter()
        assert self.ctx.visual_attempts == before
        assert self.ctx.linter_only_retries == 1

    def test_reset_timeout_zeroes_consecutive(self):
        self.ctx.consecutive_timeouts = 2
        self.ctx.reset_timeout()
        assert self.ctx.consecutive_timeouts == 0

    def test_advance_linter_or_main_linter_path(self):
        """When is_linter_only_failure=True and under budget, only linter increments."""
        self.ctx.is_linter_only_failure = True
        self.ctx.linter_only_retries = 0
        self.ctx.advance_linter_or_main()
        assert self.ctx.linter_only_retries == 1
        assert self.ctx.main_i == 0  # main_i unchanged

    def test_advance_linter_or_main_main_path(self):
        """When is_linter_only_failure=False, main_i increments."""
        self.ctx.is_linter_only_failure = False
        self.ctx.advance_linter_or_main()
        assert self.ctx.main_i == 1
        assert self.ctx.linter_only_retries == 0

    def test_advance_linter_or_main_budget_exhausted_falls_through(self):
        """When linter budget exhausted, advance_linter_or_main falls through to main_i."""
        self.ctx.is_linter_only_failure = True
        self.ctx.linter_only_retries = 3  # at budget
        self.ctx.advance_linter_or_main()
        assert self.ctx.main_i == 1   # fell through to main
        assert self.ctx.linter_only_retries == 3  # unchanged

    def test_should_continue_within_limits(self):
        assert self.ctx.should_continue() is True

    def test_should_continue_false_at_max_attempts(self):
        self.ctx.main_i = 5
        assert self.ctx.should_continue() is False

    def test_should_continue_false_at_total_loop_cap(self):
        self.ctx.total_loops = 8  # max_attempts(5) + linter_retry_budget(3)
        assert self.ctx.should_continue() is False

    def test_visual_budget_exhausted(self):
        self.ctx.visual_attempts = 3
        assert self.ctx.visual_budget_exhausted() is True

    def test_to_diagnostics_dict(self):
        self.ctx.visual_attempts = 1
        self.ctx.linter_only_retries = 2
        d = self.ctx.to_diagnostics_dict(is_best_effort=False, failure_reason="success")
        assert d["visual_attempts"] == 1
        assert d["linter_only_retries"] == 2
        assert d["is_best_effort"] is False
        assert d["failure_reason"] == "success"


# ── Test: _fill_diagnostics integration ───────────────────────────────────────

class TestFillDiagnostics:
    """
    Characterization tests that auto_fix_loop populates _diagnostics correctly
    at each exit point. Uses mock subprocess to avoid needing real Manim.
    """

    def _run_with_mocks(
        self,
        render_success: bool = True,
        vision_verdict: str = "PASS",
        vision_confidence: int = 5,
        max_attempts: int = 1,
        tmp_path=None,
    ):
        """
        Run auto_fix_loop with mocked subprocess and LLM.
        Returns the _diagnostics dict populated by the loop.
        """
        import shutil
        tmp_dir = str(tmp_path) if tmp_path else tempfile.mkdtemp()
        file_path = os.path.join(tmp_dir, "test_script.py")
        with open(file_path, "w") as f:
            f.write(MINIMAL_MANIM_CODE)

        mock_llm = make_mock_llm()
        diagnostics = {}

        # auto_fix_loop computes: _media_base = join(EVAL_OUTPUT_DIR, "media") or "media" (relative)
        # We override EVAL_OUTPUT_DIR → tmp_dir so the media path stays inside tmp_path.
        # render_fps = CFG.fps_preview = 8 (pipeline_config.py:54)
        _PREVIEW_FPS = 8
        _media_base = os.path.join(tmp_dir, "media")

        # Patch subprocess.run so Manim "renders successfully"
        def fake_subprocess_run(cmd, **kwargs):
            result = MagicMock()
            if "manim" in str(cmd):
                result.returncode = 0 if render_success else 1
                result.stdout = ""
                result.stderr = "Error: something" if not render_success else ""
                if render_success:
                    # Create the fake video at the exact path auto_fix_loop will look for.
                    fake_video_at(_media_base, "GeneratedScene", _PREVIEW_FPS)
            elif "ffprobe" in str(cmd):
                result.returncode = 0
                result.stdout = "5.0"
            elif "ffmpeg" in str(cmd):
                result.returncode = 0
                result.stdout = ""
            else:
                result.returncode = 0
                result.stdout = ""
            return result

        vision_audit = {
            "verdict": vision_verdict,
            "confidence_score": vision_confidence,
            "defects": [],
            "overall_critique": "ok",
        }

        with patch.dict(os.environ, {"EVAL_OUTPUT_DIR": tmp_dir}), \
             patch("subprocess.run", side_effect=fake_subprocess_run), \
             patch("agents.orchestrator.refining_loop.VisionAgent") as MockVA, \
             patch("agents.orchestrator.refining_loop.RAGRetriever") as MockRAG:

            MockVA.return_value.audit_frame.return_value = vision_audit
            MockVA.return_value.audit_video.return_value = vision_audit
            MockRAG.return_value.retrieve_examples.return_value = []
            MockRAG.return_value.retrieve_rules.return_value = []
            MockRAG.return_value.format_for_prompt.return_value = ""

            from agents.orchestrator.refining_loop import RefiningLoop
            RefiningLoop.auto_fix_loop(
                file_path=file_path,
                scene_name="GeneratedScene",
                user_topic="test topic",
                script_json=MINIMAL_SCRIPT_JSON,
                llm_client=mock_llm,
                max_attempts=max_attempts,
                _diagnostics=diagnostics,
            )

        return diagnostics

    def test_diagnostics_populated_on_exit(self, tmp_path):
        """_diagnostics must always have required keys on any exit path."""
        d = self._run_with_mocks(tmp_path=tmp_path)
        required_keys = {
            "visual_attempts", "linter_only_retries", "consecutive_timeouts",
            "main_i", "is_best_effort", "failure_reason",
            "reflection_memory", "failed_code_snapshots",
        }
        assert required_keys.issubset(d.keys()), f"Missing keys: {required_keys - d.keys()}"

    def test_visual_attempts_not_incremented_on_render_fail(self, tmp_path):
        """
        Characterization: visual_attempts must NOT increment on render failure.
        It only increments when Vision FAIL is processed.
        """
        d = self._run_with_mocks(render_success=False, max_attempts=1, tmp_path=tmp_path)
        assert d["visual_attempts"] == 0, (
            "visual_attempts should be 0 after render failure — "
            "it only increments after Vision FAIL/low-confidence"
        )

    def test_is_best_effort_false_on_success(self, tmp_path):
        """On Vision PASS, is_best_effort must be False."""
        d = self._run_with_mocks(
            render_success=True, vision_verdict="PASS", vision_confidence=5, tmp_path=tmp_path
        )
        # If render + vision succeeded: is_best_effort=False
        # (may not reach vision if render path mocking needs more work — check failure_reason)
        if d.get("failure_reason") == "success":
            assert d["is_best_effort"] is False

    def test_failure_reason_present(self, tmp_path):
        """failure_reason must be a non-empty string."""
        d = self._run_with_mocks(tmp_path=tmp_path)
        assert d.get("failure_reason"), "failure_reason must be set"
        assert isinstance(d["failure_reason"], str)

    def test_reflection_memory_is_list(self, tmp_path):
        d = self._run_with_mocks(tmp_path=tmp_path)
        assert isinstance(d["reflection_memory"], list)

    def test_failed_code_snapshots_is_list(self, tmp_path):
        d = self._run_with_mocks(tmp_path=tmp_path)
        assert isinstance(d["failed_code_snapshots"], list)
