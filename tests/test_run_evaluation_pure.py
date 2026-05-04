"""
TDD tests for pure functions in run_evaluation.py:
  - run_pattern_checks(code, case)
  - compute_quality_score(render_ok, vision_ok, pattern_rate, anim_score)
  - parse_error_types(stdout)

Zero subprocess, zero LLM, zero filesystem.
Run with: pytest tests/test_run_evaluation_pure.py -v
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from run_evaluation import run_pattern_checks, compute_quality_score, parse_error_types


# ── run_pattern_checks ────────────────────────────────────────────────────────

class TestRunPatternChecks:
    # ── tracer bullet ──
    def test_all_required_patterns_match(self):
        code = "self.play(Write(text))\nself.play(FadeIn(circle))\n"
        case = {"required_patterns": [r"Write\(", r"FadeIn\("]}
        result = run_pattern_checks(code, case)
        assert result["pattern_rate"] == 1.0
        assert result["missing_patterns"] == []

    def test_no_required_patterns_rate_is_1(self):
        result = run_pattern_checks("any code", {})
        assert result["pattern_rate"] == 1.0

    def test_partial_match_rate(self):
        code = "self.play(Write(text))\n"
        case = {"required_patterns": [r"Write\(", r"FadeIn\("]}
        result = run_pattern_checks(code, case)
        assert result["pattern_rate"] == pytest.approx(0.5)
        assert r"FadeIn\(" in result["missing_patterns"]
        assert r"Write\(" in result["matched_patterns"]

    def test_zero_match_rate(self):
        code = "self.wait(1)\n"
        case = {"required_patterns": [r"Write\(", r"FadeIn\("]}
        result = run_pattern_checks(code, case)
        assert result["pattern_rate"] == 0.0
        assert len(result["missing_patterns"]) == 2

    def test_disallowed_pattern_detected(self):
        code = "LayoutObject().add_constraint()\n"
        case = {"disallowed_patterns": [r"LayoutObject"]}
        result = run_pattern_checks(code, case)
        assert r"LayoutObject" in result["disallowed_violations"]

    def test_disallowed_pattern_absent(self):
        code = "circle.next_to(square)\n"
        case = {"disallowed_patterns": [r"LayoutObject"]}
        result = run_pattern_checks(code, case)
        assert result["disallowed_violations"] == []

    # ── animation_count ──
    def test_animation_count_counts_self_play(self):
        code = "self.play(Write(a))\nself.play(FadeIn(b))\nself.play(FadeOut(c))\n"
        result = run_pattern_checks(code, {})
        assert result["animation_count"] == 3

    def test_animation_count_zero(self):
        code = "self.wait(1)\n"
        result = run_pattern_checks(code, {})
        assert result["animation_count"] == 0

    def test_anim_score_capped_at_1(self):
        """10 self.play with min_animation_count=3 → anim_score=1.0, not >1."""
        code = "self.play(x)\n" * 10
        case = {"min_animation_count": 3}
        result = run_pattern_checks(code, case)
        assert result["animation_score"] == pytest.approx(1.0)

    def test_anim_score_partial(self):
        """1 self.play with min_animation_count=4 → anim_score=0.25."""
        code = "self.play(Write(t))\n"
        case = {"min_animation_count": 4}
        result = run_pattern_checks(code, case)
        assert result["animation_score"] == pytest.approx(0.25)

    def test_min_animation_count_defaults_to_1_when_absent(self):
        """min_animation_count absent → denominator=1."""
        code = "self.play(Write(t))\n"
        result = run_pattern_checks(code, {})
        assert result["animation_score"] == pytest.approx(1.0)

    def test_result_has_required_keys(self):
        result = run_pattern_checks("", {})
        keys = {"pattern_rate", "matched_patterns", "missing_patterns",
                "disallowed_violations", "animation_count", "animation_score"}
        assert keys.issubset(result.keys())

    def test_multiline_pattern_uses_re_multiline(self):
        """required_patterns match with re.MULTILINE."""
        code = "from manim import *\nclass GeneratedScene(Scene):\n    pass\n"
        case = {"required_patterns": [r"^class GeneratedScene"]}
        result = run_pattern_checks(code, case)
        assert result["pattern_rate"] == 1.0


# ── compute_quality_score ─────────────────────────────────────────────────────

class TestComputeQualityScore:
    # ── tracer bullet ──
    def test_all_perfect_is_1(self):
        """render+vision+pattern+anim all max → 0.4+0.3+0.2+0.1 = 1.0"""
        assert compute_quality_score(True, True, 1.0, 1.0) == pytest.approx(1.0)

    def test_all_zero_is_0(self):
        assert compute_quality_score(False, False, 0.0, 0.0) == pytest.approx(0.0)

    def test_render_only(self):
        """Only render passes → 0.4"""
        assert compute_quality_score(True, False, 0.0, 0.0) == pytest.approx(0.4)

    def test_vision_only(self):
        assert compute_quality_score(False, True, 0.0, 0.0) == pytest.approx(0.3)

    def test_pattern_only(self):
        assert compute_quality_score(False, False, 1.0, 0.0) == pytest.approx(0.2)

    def test_anim_only(self):
        assert compute_quality_score(False, False, 0.0, 1.0) == pytest.approx(0.1)

    def test_weights_sum_correctly(self):
        """Verify: 0.4+0.3+0.2+0.1 = 1.0 by checking all partial combos."""
        # render+vision = 0.7
        assert compute_quality_score(True, True, 0.0, 0.0) == pytest.approx(0.7)
        # render+pattern = 0.6
        assert compute_quality_score(True, False, 1.0, 0.0) == pytest.approx(0.6)

    def test_partial_pattern_rate(self):
        result = compute_quality_score(True, True, 0.5, 1.0)
        # 0.4 + 0.3 + 0.1 + 0.1 = 0.9
        assert result == pytest.approx(0.9)

    def test_result_rounded_to_3dp(self):
        result = compute_quality_score(True, False, 1/3, 0.0)
        # 0.4 + 0 + 0.2*(1/3) + 0 ≈ 0.467
        assert len(str(result).split(".")[-1]) <= 3


# ── parse_error_types ─────────────────────────────────────────────────────────

class TestParseErrorTypes:
    # ── tracer bullet ──
    def test_no_error_returns_none(self):
        assert parse_error_types("All good, render complete") == "NONE"

    def test_syntax_error_detected(self):
        assert parse_error_types("SyntaxError: unexpected indent") == "SYNTAX"

    def test_import_error_detected(self):
        assert parse_error_types("ImportError: No module named 'foo'") == "IMPORT_ERROR"

    def test_module_not_found_detected(self):
        assert parse_error_types("ModuleNotFoundError: No module named 'manim'") == "IMPORT_ERROR"

    def test_timeout_detected(self):
        assert parse_error_types("timed out after 120 seconds") == "TIMEOUT"

    def test_linter_detected(self):
        assert parse_error_types("Static Analysis Failed on line 5") == "LINTER"

    def test_vision_fail_detected(self):
        assert parse_error_types("Visual Check Failed: overlapping text") == "VISION_FAIL"

    def test_latex_error_detected(self):
        assert parse_error_types("latex error converting to dvi") == "LATEX_ERROR"

    def test_class_not_found_detected(self):
        assert parse_error_types("GeneratedScene is not in the script") == "CLASS_NOT_FOUND"

    def test_multiple_errors_pipe_separated(self):
        stdout = "SyntaxError: bad\nVisual Check Failed: overlap"
        result = parse_error_types(stdout)
        assert "SYNTAX" in result
        assert "VISION_FAIL" in result
        assert "|" in result

    def test_order_is_stable(self):
        """Multiple errors → order is SYNTAX before VISION_FAIL (defined order)."""
        stdout = "Visual Check Failed\nSyntaxError"
        result = parse_error_types(stdout)
        parts = result.split("|")
        assert parts.index("SYNTAX") < parts.index("VISION_FAIL")

    def test_vision_fail_chinese_variant(self):
        assert parse_error_types("視覺審查失敗") == "VISION_FAIL"

    def test_linter_chinese_variant(self):
        assert parse_error_types("靜態審查失敗") == "LINTER"
