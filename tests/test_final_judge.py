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
    # WEIGHTS = math 0.40, concept 0.15, clarity 0.15, spatial_layout 0.30
    # When spatial_layout=None it's excluded and remaining weights renormalize.
    def test_all_scores_present_correct_weighted_total(self):
        """math=5, concept=4, clarity=3, spatial=None
        → renorm over (math+concept+clarity) = 0.70
        → (5*0.4 + 4*0.15 + 3*0.15) / 0.70 = 3.05/0.70 ≈ 4.357"""
        code = {"math_score": 5, "math_justification": "", "issues": [], "summary": ""}
        visual = _make_visual(concept=4, clarity=3)
        result = _aggregate(code, visual)
        assert result["weighted_total"] == pytest.approx(4.357, abs=0.01)

    def test_scores_dict_has_all_four_dimensions(self):
        code = {"math_score": 4, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(4, 4))
        assert set(result["scores"].keys()) == {
            "math_correctness", "concept_alignment", "visual_clarity", "spatial_layout"
        }

    def test_math_none_renormalizes_to_visual_only(self):
        """math=None, spatial=None → only concept(0.15) + clarity(0.15), renorm weight=0.30
        → (4*0.15 + 3*0.15) / 0.30 = 1.05/0.30 = 3.5"""
        code = {"math_score": None, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(concept=4, clarity=3))
        assert result["weighted_total"] == pytest.approx(3.5, abs=0.01)
        assert result["scores"]["math_correctness"] is None

    def test_visual_none_keeps_concept_clarity_none(self):
        """visual_result=None → concept/clarity = None (no silent 3/5 reward).
        Only math=5 contributes; weighted = 5*0.5/0.5 = 5.0 (renormalized to math weight)."""
        code = {"math_score": 5, "issues": [], "summary": ""}
        result = _aggregate(code, None)
        assert result["scores"]["concept_alignment"] is None
        assert result["scores"]["visual_clarity"] is None
        assert result["weighted_total"] == pytest.approx(5.0, abs=0.01)
        assert result["verdict"] == "ERROR"
        assert result["veto_reason"] == "visual_api_failure"

    def test_visual_none_scores_keeps_them_none(self):
        code = {"math_score": None, "issues": [], "summary": ""}
        visual = {
            "scores": {
                "concept_alignment": {"score": None},
                "visual_clarity":    {"score": None},
            }
        }
        result = _aggregate(code, visual)
        assert result["scores"]["math_correctness"] is None
        assert result["scores"]["concept_alignment"] is None
        assert result["scores"]["visual_clarity"] is None
        assert result["weighted_total"] is None
        assert result["verdict"] == "ERROR"

    def test_all_phases_failed_returns_error(self):
        """math=None, visual=None → ERROR."""
        code = {"math_score": None, "issues": [], "summary": ""}
        result = _aggregate(code, None)
        assert result["weighted_total"] is None
        assert result["verdict"] == "ERROR"

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


# ── Verdict / hard veto logic ────────────────────────────────────────────────

class TestVerdict:
    def test_critical_code_issue_forces_fail(self):
        """Even with weighted >= threshold, a Critical issue → FAIL."""
        code = {
            "math_score": 5,
            "issues": [{"severity": "Critical", "category": "MATH_ERROR",
                        "description": "wrong formula", "fix": ""}],
            "summary": "",
        }
        result = _aggregate(code, _make_visual(5, 5))
        assert result["verdict"] == "FAIL"
        assert result["veto_reason"] == "critical_code_issue"
        # weighted_total still computed (used for trend)
        assert result["weighted_total"] == pytest.approx(5.0, abs=0.01)

    def test_dimension_floor_triggers_fail(self):
        """math=2 (<=DIMENSION_FLOOR) → FAIL even if other dims are 5."""
        code = {"math_score": 2, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(5, 5))
        assert result["verdict"] == "FAIL"
        assert result["veto_reason"] == "low_dimension_math_correctness"

    def test_below_threshold_fails(self):
        """All 3s → weighted=3.0 < 3.5 → FAIL."""
        code = {"math_score": 3, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(3, 3))
        assert result["weighted_total"] == pytest.approx(3.0, abs=0.01)
        assert result["verdict"] == "FAIL"
        assert result["veto_reason"] == "below_threshold"

    def test_above_threshold_passes(self):
        """math=4, concept=4, clarity=4 → weighted=4.0 >= 3.5 → PASS."""
        code = {"math_score": 4, "issues": [], "summary": ""}
        result = _aggregate(code, _make_visual(4, 4))
        assert result["verdict"] == "PASS"
        assert result["veto_reason"] is None

    def test_ground_truth_mismatch_forces_fail(self):
        """ground_truth_match=False → FAIL even with all 5s."""
        code = {
            "math_score": 5, "issues": [], "summary": "",
            "ground_truth_match": False,
        }
        result = _aggregate(code, _make_visual(5, 5))
        assert result["verdict"] == "FAIL"
        assert result["veto_reason"] == "ground_truth_mismatch"

    def test_ground_truth_match_true_does_not_force_pass(self):
        """gt_match=True doesn't override low scores."""
        code = {
            "math_score": 1, "issues": [], "summary": "",
            "ground_truth_match": True,
        }
        result = _aggregate(code, _make_visual(5, 5))
        # math=1 hits dimension floor
        assert result["verdict"] == "FAIL"

    def test_ground_truth_inconclusive_does_not_force_fail(self):
        """gt_match=None → no GT veto; verdict driven by scores."""
        code = {
            "math_score": 5, "issues": [], "summary": "",
            "ground_truth_match": None,
        }
        result = _aggregate(code, _make_visual(5, 5))
        assert result["verdict"] == "PASS"


# ── Answer comparison helper ─────────────────────────────────────────────────

from agents.utils.final_judge import _compare_answer  # noqa: E402


class TestCompareAnswer:
    def test_numeric_match_exact(self):
        assert _compare_answer("9", "9") is True

    def test_numeric_match_with_units(self):
        assert _compare_answer("12 cm", "12") is True

    def test_numeric_mismatch(self):
        assert _compare_answer("8", "9") is False

    def test_multiple_numbers_all_present(self):
        # GT says 9, 8, 5 → extracted has all three
        assert _compare_answer("分別為 9、8 和 5", "面積為 9、8、5") is True

    def test_multiple_numbers_one_missing(self):
        assert _compare_answer("分別為 9 和 8", "面積為 9、8、5") is False

    def test_text_only_substring_match(self):
        assert _compare_answer("正方形面積最大", "正方形面積最大") is True

    def test_text_token_overlap(self):
        # GT has Chinese keywords; extracted contains them
        assert _compare_answer("此題答案是周長相同時正方形面積最大", "周長相同時正方形面積最大") is True

    def test_empty_inputs_inconclusive(self):
        assert _compare_answer("", "9") is None
        assert _compare_answer("9", "") is None
        assert _compare_answer(None, "9") is None

    def test_extracted_no_numbers_when_gt_has_numbers(self):
        """GT has numbers but extracted has none → inconclusive (None), NOT False."""
        assert _compare_answer("不知道", "9") is None

    def test_fraction_handled(self):
        # 1/2 = 0.5
        assert _compare_answer("0.5", "1/2") is True
        assert _compare_answer("1/2", "0.5") is True

    def test_latex_frac_vs_ascii_regression(self):
        # A-group 2026-05-20 假 FAIL regression — see commit de4cc85.
        # GT 用 \frac{a}{b}、extracted 用 a/b，舊版誤判 False，新版必須 True。
        assert _compare_answer("32/15", r"\frac{32}{15}") is True   # Q026
        assert _compare_answer("1/3", r"\frac{1}{3}") is True       # Q123
        assert _compare_answer("29/20", r"\frac{29}{20}") is True   # Q124
        assert _compare_answer("1/10", r"\frac{1}{10}") is True     # Q137

    def test_chained_equation_equivalent_forms(self):
        # Q122: extracted 同時寫了假分數跟帶分數，GT 是 \frac{49}{10}
        # _extract_numbers 會抓到 49/10 = 4.9 → 跟 GT 49/10 = 4.9 匹配
        assert _compare_answer("49/10 = 4 9/10", r"\frac{49}{10}") is True

    # ── P0-2 邊界 bug (2026-05-21) ─────────────────────────────────────────
    def test_negative_latex_fraction(self):
        # \frac{-3}{4} = -0.75；現有版本其實已 work（regex -?\d+ 涵蓋負號），
        # 鎖規格避免未來 regex 改動誤傷。
        assert _compare_answer("-0.75", r"\frac{-3}{4}") is True
        assert _compare_answer(r"\frac{-3}{4}", "-0.75") is True
        assert _compare_answer("-3/4", r"\frac{-3}{4}") is True

    def test_negative_dfrac_tfrac(self):
        assert _compare_answer("-0.5", r"\dfrac{-1}{2}") is True
        assert _compare_answer("-0.5", r"\tfrac{-1}{2}") is True

    def test_mixed_fraction_latex(self):
        # 帶分數 3\frac{1}{2} = 3.5；舊版 _extract_numbers 把 "3" 跟 "frac{1}{2}" 之間
        # 沒有分隔當成 31/2 → 15.5（bug）
        assert _compare_answer("3.5", r"3\frac{1}{2}") is True
        assert _compare_answer(r"3\frac{1}{2}", "3.5") is True
        # 負帶分數
        assert _compare_answer("-3.5", r"-3\frac{1}{2}") is True

    def test_mixed_fraction_ascii(self):
        # 3 1/2 = 3.5；舊版抓到 [0.5, 3.0] 沒合併
        assert _compare_answer("3.5", "3 1/2") is True
        assert _compare_answer("3 1/2", "3.5") is True
        # 帶分數 ↔ 假分數
        assert _compare_answer("7/2", "3 1/2") is True

    def test_scientific_notation_latex(self):
        # 1.6 × 10^1 = 16；舊版抓到 [1.6, 10, 1] 三個獨立數
        assert _compare_answer("16", r"1.6 \times 10^1") is True
        assert _compare_answer(r"1.6 \times 10^1", "16") is True
        assert _compare_answer("160", r"1.6 \times 10^2") is True
        # ASCII 形式
        assert _compare_answer("16", "1.6 * 10^1") is True
        # 負指數
        assert _compare_answer("0.16", r"1.6 \times 10^{-1}") is True


# ── P1-2 inter-pass agreement (2026-05-21) ──────────────────────────────────

from agents.utils.final_judge import _event_agreement, _clarity_agreement  # noqa: E402


class TestEventAgreement:
    def test_unanimous_yes(self):
        # 3 events, all 3 passes vote yes for each
        votes = {"E1": [1, 1, 1], "E2": [1, 1, 1], "E3": [1, 1, 1]}
        overall, per = _event_agreement(votes)
        assert overall == 1.0
        assert all(v == 1.0 for v in per.values())

    def test_unanimous_no(self):
        votes = {"E1": [0, 0, 0]}
        overall, per = _event_agreement(votes)
        assert overall == 1.0   # all-no also counts as unanimous
        assert per["E1"] == 1.0

    def test_split_2_1(self):
        # 2/3 majority → unanimity = 2/3 ≈ 0.667
        votes = {"E1": [1, 1, 0]}
        overall, per = _event_agreement(votes)
        assert abs(per["E1"] - 2/3) < 1e-6
        assert abs(overall - 2/3) < 1e-6

    def test_even_split(self):
        # 4 passes, 2/2 split → 0.5
        votes = {"E1": [1, 1, 0, 0]}
        overall, per = _event_agreement(votes)
        assert per["E1"] == 0.5

    def test_mixed_events(self):
        # one unanimous + one split
        votes = {"E1": [1, 1, 1], "E2": [1, 0, 0]}
        overall, per = _event_agreement(votes)
        assert per["E1"] == 1.0
        assert abs(per["E2"] - 2/3) < 1e-6
        assert abs(overall - (1.0 + 2/3) / 2) < 1e-6

    def test_empty_votes_skipped_in_overall(self):
        # event with zero votes should not drag overall to 0
        votes = {"E1": [1, 1, 1], "E2": []}
        overall, per = _event_agreement(votes)
        assert per["E2"] == 0.0
        assert overall == 1.0  # only E1 counted

    def test_no_events(self):
        overall, per = _event_agreement({})
        assert overall == 0.0
        assert per == {}


class TestClarityAgreement:
    def test_identical_scores(self):
        assert _clarity_agreement([4, 4, 4]) == 1.0

    def test_single_score(self):
        assert _clarity_agreement([5]) == 1.0

    def test_empty(self):
        assert _clarity_agreement([]) == 1.0

    def test_with_nones(self):
        # None values dropped
        assert _clarity_agreement([4, None, 4]) == 1.0

    def test_small_disagreement(self):
        # [4, 5] → mean=4.5, var=0.25, std=0.5 → 1 - 0.25 = 0.75
        a = _clarity_agreement([4, 5])
        assert 0.7 < a < 0.8

    def test_moderate_disagreement(self):
        # [3, 4, 5] → mean=4, var=2/3, std≈0.816 → ≈0.59
        a = _clarity_agreement([3, 4, 5])
        assert 0.5 < a < 0.65

    def test_extreme_disagreement(self):
        # [1, 5] → std=2.0 → 1 - 1.0 = 0.0
        assert _clarity_agreement([1, 5]) == 0.0
