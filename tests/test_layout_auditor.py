"""
Unit tests for LayoutAuditor + scene_instrumentor helper functions.
Pure-function tests — no Manim, no rendering.

Run: pytest tests/test_layout_auditor.py -v
"""
import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.utils.layout_auditor import LayoutAuditor, LayoutVerdict
from agents.utils.scene_instrumentor import (
    _aabb_iou, _aabb_intersection_area, _text_containment_ratio,
    _balance_offset, _is_text_type,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _mob(type_, x, y, w, h):
    return {
        "type": type_, "width": w, "height": h,
        "center": [x, y, 0], "area": round(w * h, 3),
    }


def _write_log(tmp_path: Path, snapshots: list[dict], **agg) -> Path:
    """Write a fake scene_state_log.json with given timeline + aggregated metrics."""
    p = tmp_path / "scene_state_log.json"
    payload = {
        "max_simultaneous_objects": max((s.get("n_mobjects_visible", 0) for s in snapshots), default=0),
        "max_overlap_pairs": 0,
        "steps_with_overlap": 0,
        "total_intentional_overlaps_filtered": 0,
        "peak_screen_coverage": 0,
        "overlap_iou_max": 0.0,
        "overlap_iou_worst_step": None,
        "text_occlusion_max": 0.0,
        "text_occlusion_worst_step": None,
        "crowding_max": 0.0,
        "crowding_worst_step": None,
        "balance_offset_max": 0.0,
        "balance_offset_worst_step": None,
        "timeline": snapshots,
    }
    payload.update(agg)
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


# ── Helper functions ─────────────────────────────────────────────────────────

class TestHelpers:
    def test_iou_identical_boxes(self):
        a = _mob("X", 0, 0, 2, 2)
        assert _aabb_iou(a, a) == pytest.approx(1.0)

    def test_iou_disjoint_boxes(self):
        a = _mob("X", 0, 0, 1, 1)
        b = _mob("Y", 5, 5, 1, 1)
        assert _aabb_iou(a, b) == 0.0

    def test_iou_half_overlap(self):
        # two 1x1 boxes, centers 0.5 apart on x → overlap 0.5×1 = 0.5
        # union = 1 + 1 - 0.5 = 1.5 → IoU = 1/3
        a = _mob("X", 0, 0, 1, 1)
        b = _mob("Y", 0.5, 0, 1, 1)
        assert _aabb_iou(a, b) == pytest.approx(1/3, abs=0.01)

    def test_text_containment_full(self):
        small_text = _mob("MathTex", 0, 0, 0.5, 0.3)
        big_shape  = _mob("Polygon", 0, 0, 4, 3)
        assert _text_containment_ratio(small_text, big_shape) == pytest.approx(1.0)

    def test_text_containment_zero_when_disjoint(self):
        a = _mob("MathTex", 0, 0, 1, 1)
        b = _mob("Polygon", 5, 5, 1, 1)
        assert _text_containment_ratio(a, b) == 0.0

    def test_balance_offset_centered(self):
        mobs = [_mob("X", -2, 0, 1, 1), _mob("Y", 2, 0, 1, 1)]
        assert _balance_offset(mobs) == pytest.approx(0.0)

    def test_balance_offset_far_right(self):
        mobs = [_mob("X", 5, 0, 1, 1), _mob("Y", 6, 0, 1, 1)]
        # mean x = 5.5, normalized by canvas/2 = 7 → 5.5/7 ≈ 0.786
        assert _balance_offset(mobs) == pytest.approx(0.786, abs=0.01)

    def test_is_text_type(self):
        assert _is_text_type("MathTex")
        assert _is_text_type("Text")
        assert _is_text_type("Tex")
        assert not _is_text_type("Polygon")
        assert not _is_text_type("Circle")


# ── LayoutAuditor.audit() ────────────────────────────────────────────────────

class TestAudit:
    def test_missing_log_returns_pass(self):
        result = LayoutAuditor().audit("/does/not/exist.json")
        assert result["verdict"] == LayoutVerdict.PASS
        assert result["score_1_to_5"] is None

    def test_unreadable_log_returns_pass(self, tmp_path):
        p = tmp_path / "broken.json"
        p.write_text("{not valid json")
        result = LayoutAuditor().audit(str(p))
        assert result["verdict"] == LayoutVerdict.PASS
        assert "unreadable" in result["note"]

    def test_clean_layout_passes(self, tmp_path):
        snap = {
            "step": 1,
            "mobjects": [_mob("MathTex", -3, 2, 1, 0.4), _mob("Polygon", 2, -1, 2, 2)],
            "n_mobjects_visible": 2,
            "overlap_pairs": 0,
            "overlap_iou_max": 0.0,
            "overlap_iou_worst_pair": None,
            "text_occlusion_max": 0.0,
            "text_occlusion_worst_pair": None,
            "crowding": 0.05,
            "balance_offset": 0.07,
        }
        path = _write_log(tmp_path, [snap])
        result = LayoutAuditor().audit(str(path))
        assert result["verdict"] == LayoutVerdict.PASS
        assert result["score_1_to_5"] == 5
        assert result["violations"] == []

    def test_text_occlusion_triggers_critical_fail(self, tmp_path):
        text = _mob("MathTex", 0, 0, 0.6, 0.3)
        shape = _mob("Polygon", 0, 0, 4, 3)
        snap = {
            "step": 2,
            "mobjects": [text, shape],
            "n_mobjects_visible": 2,
            "overlap_pairs": 1,
            "overlap_iou_max": 0.05,
            "overlap_iou_worst_pair": [0, 1],
            "text_occlusion_max": 1.0,
            "text_occlusion_worst_pair": [0, 1],  # text idx, other idx
            "crowding": 0.1, "balance_offset": 0.0,
        }
        path = _write_log(
            tmp_path, [snap],
            text_occlusion_max=1.0, text_occlusion_worst_step=2,
        )
        result = LayoutAuditor().audit(str(path))
        assert result["verdict"] == LayoutVerdict.FAIL
        assert result["score_1_to_5"] == 1
        violations = result["violations"]
        assert any(v["metric"] == "text_occlusion_max" and v["severity"] == "Critical"
                   for v in violations)
        # fix hint should mention next_to or move_to with concrete coords
        msg = next(v for v in violations if v["metric"] == "text_occlusion_max")
        assert "next_to" in msg["fix_hint"] or "move_to" in msg["fix_hint"]

    def test_overlap_iou_triggers_fail(self, tmp_path):
        m1 = _mob("Polygon", 0, 0, 2, 2)
        m2 = _mob("Square",  0.5, 0, 2, 2)
        snap = {
            "step": 1, "mobjects": [m1, m2], "n_mobjects_visible": 2,
            "overlap_pairs": 1,
            "overlap_iou_max": 0.6,
            "overlap_iou_worst_pair": [0, 1],
            "text_occlusion_max": 0.0, "text_occlusion_worst_pair": None,
            "crowding": 0.1, "balance_offset": 0.0,
        }
        path = _write_log(tmp_path, [snap], overlap_iou_max=0.6, overlap_iou_worst_step=1)
        result = LayoutAuditor().audit(str(path))
        assert result["verdict"] == LayoutVerdict.FAIL
        assert result["score_1_to_5"] == 2
        assert any(v["metric"] == "overlap_iou_max" for v in result["violations"])

    def test_crowding_triggers_major(self, tmp_path):
        path = _write_log(
            tmp_path, [{
                "step": 1, "mobjects": [], "n_mobjects_visible": 0,
                "overlap_pairs": 0, "overlap_iou_max": 0.0, "overlap_iou_worst_pair": None,
                "text_occlusion_max": 0.0, "text_occlusion_worst_pair": None,
                "crowding": 0.9, "balance_offset": 0.0,
            }],
            crowding_max=0.9, crowding_worst_step=1,
        )
        result = LayoutAuditor().audit(str(path))
        assert result["verdict"] == LayoutVerdict.FAIL
        violations = result["violations"]
        assert any(v["metric"] == "crowding_max" and v["severity"] == "Major"
                   for v in violations)

    def test_balance_alone_does_not_fail(self, tmp_path):
        """balance_offset is for Planner prevention only, not in veto thresholds."""
        path = _write_log(
            tmp_path, [{
                "step": 1, "mobjects": [], "n_mobjects_visible": 0,
                "overlap_pairs": 0, "overlap_iou_max": 0.0, "overlap_iou_worst_pair": None,
                "text_occlusion_max": 0.0, "text_occlusion_worst_pair": None,
                "crowding": 0.1, "balance_offset": 0.95,
            }],
            balance_offset_max=0.95, balance_offset_worst_step=1,
        )
        result = LayoutAuditor().audit(str(path))
        assert result["verdict"] == LayoutVerdict.PASS
        # but the metric should still be reported
        assert result["metrics"]["balance_offset_max"] == 0.95

    def test_score_mapping_boundaries(self):
        a = LayoutAuditor()
        assert a._score({"text_occlusion_max": 0.5, "overlap_iou_max": 0,    "crowding_max": 0})    == 1
        assert a._score({"text_occlusion_max": 0.0, "overlap_iou_max": 0.4,  "crowding_max": 0})    == 2
        assert a._score({"text_occlusion_max": 0.0, "overlap_iou_max": 0.0,  "crowding_max": 0.85}) == 2
        assert a._score({"text_occlusion_max": 0.0, "overlap_iou_max": 0.25, "crowding_max": 0})    == 3
        assert a._score({"text_occlusion_max": 0.0, "overlap_iou_max": 0.0,  "crowding_max": 0.7})  == 3
        assert a._score({"text_occlusion_max": 0.3, "overlap_iou_max": 0.0,  "crowding_max": 0})    == 4
        assert a._score({"text_occlusion_max": 0.0, "overlap_iou_max": 0.0,  "crowding_max": 0.0})  == 5

    def test_build_fix_prompt_pass_returns_empty(self):
        audit = {"verdict": LayoutVerdict.PASS, "violations": []}
        assert LayoutAuditor.build_fix_prompt(audit) == ""

    def test_build_fix_prompt_includes_actions(self):
        audit = {
            "verdict": LayoutVerdict.FAIL,
            "violations": [{
                "metric": "text_occlusion_max",
                "severity": "Critical",
                "value": 0.7, "threshold": 0.5, "step": 2,
                "details": "text 70% covered",
                "fix_hint": "use next_to with buff=0.4",
            }],
        }
        prompt = LayoutAuditor.build_fix_prompt(audit)
        assert "LAYOUT AUDIT FAILED" in prompt
        assert "text_occlusion_max" in prompt
        assert "next_to" in prompt
        assert "ACTION" in prompt
