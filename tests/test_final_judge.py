"""
TDD tests for FinalJudge._extract_scene_code() and FinalJudge._aggregate().

Both are pure functions — zero API calls, zero subprocess.
Run with: pytest tests/test_final_judge.py -v
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.utils.final_judge import FinalJudge


# ── Helpers ──────────────────────────────────────────────────────────────────

def _extract(code: str) -> str:
    return FinalJudge._extract_scene_code(code)


def _aggregate(code_analysis: dict, visual_result: dict | None) -> dict:
    # _aggregate is an instance method but only uses self.WEIGHTS (class attr)
    fj = object.__new__(FinalJudge)
    return fj._aggregate(code_analysis, visual_result)


# ── _extract_scene_code ───────────────────────────────────────────────────────

class TestExtractSceneCode:
    # tracer bullet
    def test_finds_generated_scene_class(self):
        code = "from manim import *\n\nclass GeneratedScene(Scene):\n    pass\n"
        result = _extract(code)
        assert "class GeneratedScene" in result

    def test_imports_before_class_are_preserved(self):
        code = (
            "from manim import *\n"
            "import numpy as np\n"
            "\n"
            "class GeneratedScene(Scene):\n"
            "    def construct(self): pass\n"
        )
        result = _extract(code)
        assert "from manim import *" in result
        assert "import numpy as np" in result
        assert "class GeneratedScene" in result

    def test_boilerplate_before_class_is_excluded(self):
        """Non-import lines before GeneratedScene (e.g. injected helpers) should not appear."""
        code = (
            "from manim import *\n"
            "SOME_CONSTANT = 42\n"          # not an import → should be stripped
            "def helper(): pass\n"          # not an import → should be stripped
            "\n"
            "class GeneratedScene(Scene):\n"
            "    pass\n"
        )
        result = _extract(code)
        assert "SOME_CONSTANT" not in result
        assert "def helper" not in result

    def test_no_generated_scene_short_code_returned_as_is(self):
        code = "from manim import *\n\nclass OtherScene(Scene):\n    pass\n"
        result = _extract(code)
        # no truncation prefix since code is short
        assert "...(start truncated)" not in result
        assert "OtherScene" in result

    def test_no_generated_scene_long_code_gets_tail(self):
        """If GeneratedScene not found and code > 6000 chars → last 6000 chars returned."""
        padding = "x = 1\n" * 1100          # ~6600 chars, no GeneratedScene
        result = _extract(padding)
        assert result.startswith("...(start truncated)\n")
        # The tail should be ≤ 6000 chars (after the prefix)
        tail = result[len("...(start truncated)\n"):]
        assert len(tail) <= 6000

    def test_combined_output_truncated_at_8000(self):
        """imports + class body > 8000 → output ends with ...(truncated)."""
        imports = "from manim import *\n"
        body = "    # " + "x" * 100 + "\n"   # 107 chars per line
        long_construct = body * 80            # ~8560 chars just for body
        code = imports + "\nclass GeneratedScene(Scene):\n" + long_construct
        result = _extract(code)
        assert result.endswith("...(truncated)")

    def test_output_under_8000_has_no_truncation_marker(self):
        code = "from manim import *\n\nclass GeneratedScene(Scene):\n    pass\n"
        result = _extract(code)
        assert "...(truncated)" not in result


# ── _aggregate ────────────────────────────────────────────────────────────────

def _make_visual(concept: int, clarity: int) -> dict:
    return {
        "scores": {
            "concept_alignment": {"score": concept, "justification": "ok"},
            "visual_clarity":    {"score": clarity,  "justification": "ok"},
        },
        "frame_analysis":    "frames look fine",
        "metaphor_audit":    "metaphors good",
        "code_confirmation": "issues confirmed",
    }


class TestAggregate:
    # tracer bullet
    def test_all_scores_present_correct_weighted_total(self):
        """math*0.5 + concept*0.2 + clarity*0.3 = 5*0.5+4*0.2+3*0.3 = 4.2"""
        code = {"math_score": 5, "math_justification": "", "issues": [], "summary": ""}
        visual = _make_visual(concept=4, clarity=3)
        result = _aggregate(code, visual)
        assert result["weighted_total"] == pytest.approx(4.2, abs=0.01)

    def test_scores_dict_has_all_three_dimensions(self):
        code = {"math_score": 4, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(4, 4))
        assert set(result["scores"].keys()) == {"math_correctness", "concept_alignment", "visual_clarity"}

    def test_math_none_renormalizes_to_visual_only(self):
        """math=None → only concept(0.2) + clarity(0.3), renorm weight=0.5
        → (4*0.2 + 3*0.3) / 0.5 = 3.4"""
        code = {"math_score": None, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(concept=4, clarity=3))
        assert result["weighted_total"] == pytest.approx(3.4, abs=0.01)
        assert result["scores"]["math_correctness"] is None

    def test_visual_none_defaults_concept_clarity_to_3(self):
        """visual_result=None → concept/clarity fallback to 3.
        math=5 → 5*0.5 + 3*0.2 + 3*0.3 = 4.0"""
        code = {"math_score": 5, "issues": [], "summary": ""}
        result = _aggregate(code, None)
        assert result["scores"]["concept_alignment"] == 3
        assert result["scores"]["visual_clarity"] == 3
        assert result["weighted_total"] == pytest.approx(4.0, abs=0.01)

    def test_all_none_weighted_total_is_none(self):
        code = {"math_score": None, "issues": [], "summary": ""}
        # visual_result with None-like scores
        visual = {
            "scores": {
                "concept_alignment": {"score": None},
                "visual_clarity":    {"score": None},
            }
        }
        result = _aggregate(code, visual)
        # concept/clarity will raise ValueError on int(None) → fall back to 3
        # So weighted_total won't be None here; test the scores["math_correctness"] is None
        assert result["scores"]["math_correctness"] is None

    def test_all_scores_truly_missing_returns_none_total(self):
        """Simulate full unavailability: math=None, no visual."""
        code = {"math_score": None, "issues": [], "summary": ""}
        result = _aggregate(code, None)
        # visual=None → concept=3, clarity=3 (defaults) → NOT None
        # weighted = (3*0.2 + 3*0.3) / 0.5 = 3.0
        assert result["weighted_total"] == pytest.approx(3.0, abs=0.01)

    def test_code_issues_always_in_result(self):
        issues = [{"severity": "Critical", "category": "MATH_ERROR",
                   "description": "wrong", "line_hint": "x", "fix": "y"}]
        code = {"math_score": 3, "issues": issues, "summary": "bad"}
        result = _aggregate(code, None)
        assert result["code_issues"] == issues
        assert result["code_summary"] == "bad"

    def test_score_details_present_when_visual_provided(self):
        code = {"math_score": 4, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(4, 4))
        assert "score_details" in result
        assert "frame_analysis" in result
        assert "metaphor_audit" in result
        assert "code_confirmation" in result

    def test_score_details_absent_when_no_visual(self):
        code = {"math_score": 4, "issues": [], "summary": ""}
        result = _aggregate(code, None)
        assert "score_details" not in result
        assert "frame_analysis" not in result

    def test_perfect_score(self):
        """All 5s → weighted = 5.0"""
        code = {"math_score": 5, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(5, 5))
        assert result["weighted_total"] == pytest.approx(5.0, abs=0.01)

    def test_minimum_score(self):
        """All 1s → weighted = 1.0"""
        code = {"math_score": 1, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(1, 1))
        assert result["weighted_total"] == pytest.approx(1.0, abs=0.01)
