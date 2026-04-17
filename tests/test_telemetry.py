"""Unit tests for agents.utils.telemetry (IoU post-processing helper)."""

import pytest
from agents.utils.telemetry import (
    _aabb_iou,
    choose_telemetry_midpoint_pct,
    compute_iou_summary,
    format_telemetry_block,
    load_and_summarize,
    IOU_THRESHOLD,
    OVERLAP_TEXT_ON_TEXT,
    OVERLAP_TEXT_ON_OBJ,
)


# ── _aabb_iou ────────────────────────────────────────────────────────────

def _mob(cx, cy, w, h, t="Rect"):
    return {"center": [cx, cy, 0], "width": w, "height": h, "type": t, "area": w * h}


def test_iou_no_overlap():
    """Two boxes far apart → IoU 0."""
    m1 = _mob(0, 0, 1, 1)
    m2 = _mob(5, 5, 1, 1)
    assert _aabb_iou(m1, m2) == 0.0


def test_iou_identical():
    """Identical boxes → IoU 1."""
    m1 = _mob(0, 0, 2, 2)
    assert _aabb_iou(m1, m1) == pytest.approx(1.0)


def test_iou_partial_overlap():
    """Two overlapping boxes → 0 < IoU < 1."""
    m1 = _mob(0, 0, 2, 2)
    m2 = _mob(1, 0, 2, 2)
    # intersection: width=1, height=2 → area=2
    # union: 4 + 4 - 2 = 6
    assert _aabb_iou(m1, m2) == pytest.approx(2.0 / 6.0)


def test_iou_touching_edge():
    """Boxes touching at an edge → IoU 0 (no area overlap)."""
    m1 = _mob(0, 0, 2, 2)
    m2 = _mob(2, 0, 2, 2)
    assert _aabb_iou(m1, m2) == 0.0


def test_iou_small_touch_below_threshold():
    """Small overlap that would be below IOU_THRESHOLD is still computed by _aabb_iou;
    filtering happens in compute_iou_summary."""
    m1 = _mob(0, 0, 2, 2)
    m2 = _mob(1.8, 0, 2, 2)  # tiny overlap
    iou = _aabb_iou(m1, m2)
    assert 0 < iou < IOU_THRESHOLD


# ── compute_iou_summary ─────────────────────────────────────────────────

def test_empty_timeline():
    """Empty timeline → zero everything."""
    s = compute_iou_summary({"timeline": []})
    assert s["iou_overlap_pairs_max"] == 0
    assert s["total_steps"] == 0
    assert s["top_overlap_pairs"] == []


def test_single_step_no_overlap():
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 1, 1, "Text"), _mob(5, 0, 1, 1, "Text")],
            "overlap_pairs": 0,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 0
    assert s["steps_with_iou_overlap"] == 0


def test_single_step_with_overlap():
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 2, 2, "Text"), _mob(0.5, 0, 2, 2, "MathTex")],
            "overlap_pairs": 1,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 1
    assert s["steps_with_iou_overlap"] == 1
    assert s["worst_overlap_step"] == 1
    assert s["worst_overlap_step_pct"] == pytest.approx(0.5)
    assert len(s["top_overlap_pairs"]) == 1


def test_intentional_overlay_filtered():
    """Sector inside Circle should be skipped."""
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 3, 3, "Circle"), _mob(0, 0, 2, 2, "Sector")],
            "overlap_pairs": 0,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 0


def test_below_threshold_filtered():
    """Overlap with IoU < 0.15 should not count."""
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 2, 2, "Text"), _mob(1.8, 0, 2, 2, "Text")],
            "overlap_pairs": 1,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 0


def test_non_text_pairs_excluded():
    """Arrow↔Arrow, Line↔Circle etc. should never be flagged regardless of IoU."""
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [
                _mob(0, 0, 2, 2, "Arrow"), _mob(0, 0, 2, 2, "Arrow"),   # IoU 1.0, non-text
                _mob(0, 0, 2, 2, "Line"),  _mob(0, 0, 2, 2, "Circle"),  # IoU 1.0, non-text
            ],
            "overlap_pairs": 0,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 0
    assert s["text_on_text_count"] == 0
    assert s["text_on_object_count"] == 0


def test_text_on_text_counted():
    """Two overlapping text objects → text_on_text_count > 0."""
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 2, 2, "Text"), _mob(0, 0, 2, 2, "MathTex")],
            "overlap_pairs": 1,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 1
    assert s["text_on_text_count"] == 1
    assert s["text_on_object_count"] == 0
    assert s["top_overlap_pairs"][0]["category"] == OVERLAP_TEXT_ON_TEXT


def test_text_on_object_counted():
    """Text overlapping a non-text object → text_on_object_count > 0."""
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 2, 2, "MathTex"), _mob(0, 0, 2, 2, "Rectangle")],
            "overlap_pairs": 1,
        }]
    })
    assert s["iou_overlap_pairs_max"] == 1
    assert s["text_on_text_count"] == 0
    assert s["text_on_object_count"] == 1
    assert s["top_overlap_pairs"][0]["category"] == OVERLAP_TEXT_ON_OBJ


def test_multi_step_worst_step():
    """Worst step is the one with most text-involving IoU-filtered pairs."""
    s = compute_iou_summary({
        "timeline": [
            {"step": 1, "mobjects": [_mob(0, 0, 1, 1, "Text")], "overlap_pairs": 0},
            {"step": 2, "mobjects": [
                _mob(0, 0, 2, 2, "Text"), _mob(0, 0, 2, 2, "MathTex"),  # IoU 1.0, text-on-text
            ], "overlap_pairs": 1},
            {"step": 3, "mobjects": [_mob(0, 0, 1, 1, "Text")], "overlap_pairs": 0},
        ]
    })
    assert s["worst_overlap_step"] == 2
    assert s["worst_overlap_step_pct"] == pytest.approx((1 + 0.5) / 3, abs=0.01)


def test_top_pairs_are_sorted_by_iou():
    """top_overlap_pairs should be sorted descending by IoU."""
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [
                _mob(0, 0, 2, 2, "MathTex"),
                _mob(0, 0, 2, 2, "Text"),      # IoU 1.0 with MathTex
                _mob(0.5, 0, 2, 2, "MathTex"), # IoU < 1.0 with first MathTex
            ],
            "overlap_pairs": 3,
        }]
    })
    ious = [p["iou"] for p in s["top_overlap_pairs"]]
    assert ious == sorted(ious, reverse=True)


# ── choose_telemetry_midpoint_pct ───────────────────────────────────────

def test_choose_midpoint_none_keeps_default():
    assert choose_telemetry_midpoint_pct(None) == pytest.approx(0.70)


def test_choose_midpoint_outside_range_keeps_default():
    assert choose_telemetry_midpoint_pct(0.31) == pytest.approx(0.70)
    assert choose_telemetry_midpoint_pct(0.91) == pytest.approx(0.70)


def test_choose_midpoint_too_close_to_anchor_keeps_default():
    assert choose_telemetry_midpoint_pct(0.46) == pytest.approx(0.70)
    assert choose_telemetry_midpoint_pct(0.89) == pytest.approx(0.70)


def test_choose_midpoint_valid_hotspot_replaces_default():
    assert choose_telemetry_midpoint_pct(0.73) == pytest.approx(0.73)


# ── format_telemetry_block ───────────────────────────────────────────────

def test_format_empty():
    assert format_telemetry_block(None) == ""
    assert format_telemetry_block({"total_steps": 0}) == ""


def test_format_contains_heuristic_warning():
    s = compute_iou_summary({
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 2, 2, "Text"), _mob(0.5, 0, 2, 2, "MathTex")],
            "overlap_pairs": 1,
        }]
    })
    block = format_telemetry_block(s)
    assert "heuristic" in block.lower()
    assert "AABB" in block
    assert "IoU" in block


# ── load_and_summarize ───────────────────────────────────────────────────

def test_load_missing_file(tmp_path):
    assert load_and_summarize(tmp_path / "nonexistent.json") is None


def test_load_valid_file(tmp_path):
    import json
    log = {
        "timeline": [{
            "step": 1,
            "mobjects": [_mob(0, 0, 2, 2, "Text"), _mob(0, 0, 2, 2, "MathTex")],
            "overlap_pairs": 1,
        }]
    }
    p = tmp_path / "scene_state_log.json"
    p.write_text(json.dumps(log))
    s = load_and_summarize(p)
    assert s is not None
    assert s["iou_overlap_pairs_max"] == 1
