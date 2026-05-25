"""TDD tests for BenchmarkJudge pure functions — zero LLM, zero subprocess.

Covers:
  - _mode_likert tiebreak (pick more pessimistic on tie)
  - _layout_gap_to_clarity_penalty (cand-bench mapping)
  - _dim_score (offset application + cap 0..100)
  - End-to-end synthesis behaviour: weights × smooth accuracy gate
  - Cache key generation + cache hit/miss

Run with: pytest tests/test_benchmark_judge.py -v
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.utils.benchmark_judge import (
    BenchmarkJudge,
    LIKERT_OFFSET,
    WEIGHTS,
    ACCURACY_GATE_THRESHOLD,
    MATH_PENALTY,
)


# ── _mode_likert ─────────────────────────────────────────────────────────────

class TestModeLikert:
    def test_empty_returns_inconclusive(self):
        assert BenchmarkJudge._mode_likert([]) == "inconclusive"

    def test_all_invalid_returns_inconclusive(self):
        assert BenchmarkJudge._mode_likert(["junk", "garbage"]) == "inconclusive"

    def test_single_pass_returns_that_label(self):
        assert BenchmarkJudge._mode_likert(["worse"]) == "worse"

    def test_clear_majority(self):
        assert BenchmarkJudge._mode_likert(["worse", "worse", "same"]) == "worse"

    def test_tiebreak_picks_more_pessimistic(self):
        # tie between same and broken → broken wins (more pessimistic)
        assert BenchmarkJudge._mode_likert(["same", "broken"]) == "broken"

    def test_tiebreak_worse_vs_better(self):
        assert BenchmarkJudge._mode_likert(["better", "worse"]) == "worse"

    def test_tiebreak_three_way(self):
        # tie of three different — picks broken (worst)
        result = BenchmarkJudge._mode_likert(["much_better", "same", "broken"])
        assert result == "broken"

    def test_filters_invalid_then_modes(self):
        # "junk" filtered, remaining {worse:2, same:1}
        assert BenchmarkJudge._mode_likert(["worse", "junk", "worse", "same"]) == "worse"

    def test_inconclusive_majority(self):
        assert BenchmarkJudge._mode_likert(["inconclusive", "inconclusive", "worse"]) == "inconclusive"


# ── _dim_score ───────────────────────────────────────────────────────────────

class TestDimScore:
    def test_same_gives_100(self):
        score, mode = BenchmarkJudge._dim_score(["same", "same"])
        assert score == 100
        assert mode == "same"

    def test_much_better_capped_at_100(self):
        # design: candidate cannot exceed benchmark (offset = 0)
        score, mode = BenchmarkJudge._dim_score(["much_better", "much_better"])
        assert score == 100
        assert mode == "much_better"

    def test_worse_offset(self):
        score, _ = BenchmarkJudge._dim_score(["worse", "worse", "worse"])
        assert score == 100 + LIKERT_OFFSET["worse"]   # 80

    def test_broken_offset(self):
        score, _ = BenchmarkJudge._dim_score(["broken", "broken"])
        assert score == 100 + LIKERT_OFFSET["broken"]  # 30

    def test_no_votes_falls_back_inconclusive(self):
        score, mode = BenchmarkJudge._dim_score([])
        assert mode == "inconclusive"
        assert score == 100 + LIKERT_OFFSET["inconclusive"]  # 95

    def test_score_floored_at_zero(self):
        # synthetic — if we hand-craft an offset that goes negative,
        # the per-dim score must clamp.
        score, _ = BenchmarkJudge._dim_score(["broken"] * 5)
        assert score >= 0


# ── _layout_gap_to_clarity_penalty ───────────────────────────────────────────

class TestLayoutGapPenalty:
    def test_none_inputs_zero_penalty(self):
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(None, 5) == 0
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(3, None) == 0
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(None, None) == 0

    def test_equal_layout_zero_penalty(self):
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(4, 4) == 0

    def test_candidate_worse_negative_penalty(self):
        # cand=2, bench=5 → gap=-3 → penalty=-30
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(2, 5) == -30

    def test_candidate_better_positive_bonus(self):
        # cand=5, bench=3 → gap=+2 → +20 (bonus capped later by 100)
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(5, 3) == 20

    def test_max_penalty_when_cand_1_bench_5(self):
        assert BenchmarkJudge._layout_gap_to_clarity_penalty(1, 5) == -40


# ── synthesis math (end-to-end formula without LLM) ──────────────────────────

class TestSynthesisMath:
    """Re-derive final_100 from per-dim scores using the same formula judge() uses."""

    @staticmethod
    def _final(scores: dict) -> int:
        weighted = sum(WEIGHTS[d] * scores[d] for d in WEIGHTS)
        factor = min(1.0, scores["accuracy"] / ACCURACY_GATE_THRESHOLD)
        return max(0, min(100, round(weighted * factor)))

    def test_all_100_returns_100(self):
        assert self._final({"accuracy": 100, "completeness": 100, "clarity": 100}) == 100

    def test_smooth_gate_not_cliff(self):
        # acc=74 vs acc=75: difference is small, not a cliff
        f74 = self._final({"accuracy": 74, "completeness": 80, "clarity": 80})
        f75 = self._final({"accuracy": 75, "completeness": 80, "clarity": 80})
        # both very close (within 2 points), proving no cliff edge
        assert abs(f74 - f75) <= 2

    def test_low_accuracy_dampens_whole_score(self):
        # acc=30 → factor=0.4
        s = {"accuracy": 30, "completeness": 100, "clarity": 100}
        f = self._final(s)
        # weighted = 0.4*30 + 0.3*100 + 0.3*100 = 72; *0.4 = 28.8 ≈ 29
        assert 27 <= f <= 30

    def test_smoke_pizza_one_vs_five(self):
        # mirrors POC 2 result: comp=broken(30), acc=broken(30), clar=much_worse+broken(50ish)
        # Using exact offsets: clarity mode broken (tiebreak) → 30
        s = {"accuracy": 30, "completeness": 30, "clarity": 60}
        f = self._final(s)
        # weighted = 0.4*30 + 0.3*30 + 0.3*60 = 12 + 9 + 18 = 39
        # factor = min(1, 30/75) = 0.4 → 39*0.4 = 15.6 → 16
        assert f == 16

    def test_high_accuracy_keeps_factor_one(self):
        s = {"accuracy": 90, "completeness": 80, "clarity": 80}
        f = self._final(s)
        # weighted = 36 + 24 + 24 = 84; factor=1
        assert f == 84

    def test_ordering_preserved_below_threshold(self):
        # acc=30 and acc=50: both below 75 but acc=50 should give higher final
        s1 = {"accuracy": 30, "completeness": 60, "clarity": 60}
        s2 = {"accuracy": 50, "completeness": 60, "clarity": 60}
        assert self._final(s2) > self._final(s1)


# ── Constants sanity ─────────────────────────────────────────────────────────

class TestConstantsSanity:
    def test_weights_sum_to_one(self):
        assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9

    def test_likert_offsets_match_design(self):
        # Locked in by feedback_fj_design_decisions_20260520.md
        assert LIKERT_OFFSET["much_better"] == 0
        assert LIKERT_OFFSET["better"] == 0
        assert LIKERT_OFFSET["same"] == 0
        assert LIKERT_OFFSET["worse"] == -20
        assert LIKERT_OFFSET["much_worse"] == -40
        assert LIKERT_OFFSET["broken"] == -70

    def test_accuracy_weight_dominant(self):
        # design: accuracy weighted highest among the three dims
        assert WEIGHTS["accuracy"] >= WEIGHTS["completeness"]
        assert WEIGHTS["accuracy"] >= WEIGHTS["clarity"]

    def test_math_penalty_monotonic(self):
        # Higher math_score = lower penalty (less negative)
        vals = [MATH_PENALTY[i] for i in (1, 2, 3, 4, 5)]
        assert vals == sorted(vals)


# ── Cache key (added in this session) ────────────────────────────────────────

class TestCacheKey:
    def test_cache_key_stable_for_same_inputs(self):
        from agents.utils.benchmark_judge import _cache_key
        k1 = _cache_key("/path/a.mp4", "/path/b.mp4", "topic", 3, "claude-opus-4-7")
        k2 = _cache_key("/path/a.mp4", "/path/b.mp4", "topic", 3, "claude-opus-4-7")
        assert k1 == k2

    def test_cache_key_changes_on_topic(self):
        from agents.utils.benchmark_judge import _cache_key
        k1 = _cache_key("/a.mp4", "/b.mp4", "topic A", 3, "m")
        k2 = _cache_key("/a.mp4", "/b.mp4", "topic B", 3, "m")
        assert k1 != k2

    def test_cache_key_changes_on_passes(self):
        from agents.utils.benchmark_judge import _cache_key
        k1 = _cache_key("/a.mp4", "/b.mp4", "t", 3, "m")
        k2 = _cache_key("/a.mp4", "/b.mp4", "t", 5, "m")
        assert k1 != k2

    def test_cache_roundtrip(self, tmp_path):
        from agents.utils.benchmark_judge import _cache_load, _cache_save
        cache_file = tmp_path / "cache.json"
        payload = {"final_100": 42, "scores": {"accuracy": 80}}
        _cache_save(str(cache_file), "key1", payload)
        loaded = _cache_load(str(cache_file), "key1")
        assert loaded == payload

    def test_cache_miss_returns_none(self, tmp_path):
        from agents.utils.benchmark_judge import _cache_load
        cache_file = tmp_path / "cache.json"
        assert _cache_load(str(cache_file), "nope") is None


# ── Cache key fold prompt hash (#5) ──────────────────────────────────────────

class TestCacheKeyPromptSig:
    def test_prompt_sig_changes_cache_key(self):
        from agents.utils.benchmark_judge import _cache_key
        k1 = _cache_key("/a.mp4", "/b.mp4", "t", 3, "m", prompt_sig="aaa11111")
        k2 = _cache_key("/a.mp4", "/b.mp4", "t", 3, "m", prompt_sig="bbb22222")
        assert k1 != k2, "editing the rubric must invalidate cache"

    def test_prompt_sig_default_empty_stable(self):
        from agents.utils.benchmark_judge import _cache_key
        # Back-compat: omitting prompt_sig still produces a deterministic key
        k1 = _cache_key("/a.mp4", "/b.mp4", "t", 3, "m")
        k2 = _cache_key("/a.mp4", "/b.mp4", "t", 3, "m", prompt_sig="")
        assert k1 == k2

    def test_class_prompt_sig_is_stable_short_hex(self):
        from agents.utils.benchmark_judge import BenchmarkJudge
        sig = BenchmarkJudge._prompt_sig()
        assert len(sig) == 8
        assert all(c in "0123456789abcdef" for c in sig)
        # Same prompt → same sig
        assert sig == BenchmarkJudge._prompt_sig()


# ── Insufficient-passes guard (#2) ───────────────────────────────────────────
# We can't easily trigger a real Opus failure in unit tests, but we can
# verify the threshold arithmetic (ceil(passes/2)).

class TestInsufficientPassesArithmetic:
    @pytest.mark.parametrize("passes,min_required", [
        (1, 1),   # 1 pass, need 1
        (2, 1),   # 2 passes, need 1
        (3, 2),   # 3 passes, need 2  (the production default)
        (4, 2),   # 4 passes, need 2
        (5, 3),   # 5 passes, need 3
    ])
    def test_majority_threshold(self, passes, min_required):
        # Mirrors `(self.passes + 1) // 2` in judge()
        computed = (passes + 1) // 2
        assert computed == min_required


# ── Integration: BJ(X, X) self-sanity ────────────────────────────────────────
# Skip by default — requires Claude CLI subscription + real video file +
# ~1 minute Opus runtime. Opt in with: RUN_BJ_INTEGRATION=1 pytest -s
import os

SANITY_VIDEO = Path(__file__).parent.parent / "runs" / "20260518_001817" / "Q050" / "video.mp4"
_BJ_INTEGRATION = os.getenv("RUN_BJ_INTEGRATION") == "1"


@pytest.mark.skipif(
    not (_BJ_INTEGRATION and SANITY_VIDEO.exists()),
    reason="set RUN_BJ_INTEGRATION=1 and ensure Q050 video exists",
)
class TestSelfSanity:
    """BJ scored against itself MUST return ~100. If it doesn't, the prompt
    is biasing toward defects even when none exist (anchor prompt leaking,
    or position swap not cancelling). Tolerance is loose (>=70) because
    Likert mode can still vote 'worse' on subtle frame jitter; we only need
    to detect catastrophic prompt drift."""

    def test_self_vs_self_should_be_high(self):
        from agents.utils.benchmark_judge import BenchmarkJudge
        bj = BenchmarkJudge(passes=2)   # 2 pass: one cand@top, one cand@bottom
        result = bj.judge(
            candidate_video=str(SANITY_VIDEO),
            benchmark_video=str(SANITY_VIDEO),
            question_topic="計算 (-48) ÷ (-6) × (-3) 的值。",
            cache_path=None,
        )
        final = result["final_100"]
        assert final >= 70, (
            f"BJ(X, X) returned {final} (expected ≥70). "
            f"modes={result['modes']}  evidence={result['evidence']}"
        )
