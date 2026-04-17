"""Offline post-processing of SceneInstrumentor logs.

Reads scene_state_log.json (already written by the injected SceneInstrumentor)
and computes IoU-based overlap metrics.  The injected snippet is NOT modified —
all enrichment happens here, at read time.
"""

from __future__ import annotations

import json
from pathlib import Path


def _aabb_iou(m1: dict, m2: dict) -> float:
    """Compute Intersection-over-Union for two axis-aligned bounding boxes.

    Each mobject dict must have 'center' ([x, y, z]), 'width', 'height'.
    Returns 0.0 when there is no intersection.
    """
    cx1, cy1 = m1["center"][0], m1["center"][1]
    cx2, cy2 = m2["center"][0], m2["center"][1]
    hw1, hh1 = m1["width"] / 2, m1["height"] / 2
    hw2, hh2 = m2["width"] / 2, m2["height"] / 2

    # AABB extents
    left  = max(cx1 - hw1, cx2 - hw2)
    right = min(cx1 + hw1, cx2 + hw2)
    top   = min(cy1 + hh1, cy2 + hh2)
    bot   = max(cy1 - hh1, cy2 - hh2)

    if left >= right or bot >= top:
        return 0.0

    inter = (right - left) * (top - bot)
    union = m1["width"] * m1["height"] + m2["width"] * m2["height"] - inter
    if union <= 0:
        return 0.0
    return inter / union


# Intentional overlay type pairs — same whitelist as SceneInstrumentor
_INTENTIONAL_TYPE_PAIRS = {
    frozenset({"Sector", "Circle"}),
    frozenset({"AnnularSector", "Circle"}),
    frozenset({"Sector", "Arc"}),
    frozenset({"AnnularSector", "Arc"}),
}

# Text-like types: overlaps involving at least one of these are flagged.
# Everything else (Arrow↔Arrow, Line↔Circle, Dot↔Curve …) is treated as
# intentional geometric composition and silently skipped.
_TEXT_TYPES = frozenset({
    "Text", "MathTex", "Tex", "MarkupText",
    "SingleStringMathTex", "BulletedList", "Title",
})

# Overlap categories surfaced in the summary
OVERLAP_TEXT_ON_TEXT = "text_on_text"      # both objects are text
OVERLAP_TEXT_ON_OBJ  = "text_on_object"    # text covering a non-text element


def _is_intentional(m1: dict, m2: dict) -> bool:
    """Quick check: is this pair in the intentional overlay whitelist?"""
    return frozenset({m1["type"], m2["type"]}) in _INTENTIONAL_TYPE_PAIRS


def _overlap_category(m1: dict, m2: dict) -> str | None:
    """Return the overlap category for this pair, or None if it should be skipped.

    Only text-involving overlaps are flagged — all other pairs (geometric shapes,
    arrows, axes …) are assumed to be intentional composition.
    """
    t1_is_text = m1["type"] in _TEXT_TYPES
    t2_is_text = m2["type"] in _TEXT_TYPES
    if t1_is_text and t2_is_text:
        return OVERLAP_TEXT_ON_TEXT
    if t1_is_text or t2_is_text:
        return OVERLAP_TEXT_ON_OBJ
    return None  # non-text pair → skip entirely


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

IOU_THRESHOLD = 0.15  # pairs below this are noise


def choose_telemetry_midpoint_pct(
    worst_overlap_step_pct: float | None,
    *,
    fixed_mid_pct: float = 0.70,
    allowed_range: tuple[float, float] = (0.50, 0.85),
    protected_pcts: tuple[float, ...] = (0.10, 0.40, 0.95),
    min_spacing: float = 0.08,
) -> float:
    """Choose a telemetry-guided mid-frame percentage with conservative guards.

    We only replace the default 70% frame when the telemetry hotspot stays in the
    later half of the animation and is not too close to the fixed anchor frames.
    This keeps the original late-stage coverage unless telemetry provides a
    meaningfully different target.
    """
    if worst_overlap_step_pct is None:
        return fixed_mid_pct

    low, high = allowed_range
    if not (low <= worst_overlap_step_pct <= high):
        return fixed_mid_pct

    if any(abs(worst_overlap_step_pct - pct) <= min_spacing for pct in protected_pcts):
        return fixed_mid_pct

    return worst_overlap_step_pct


def compute_iou_summary(log: dict, iou_threshold: float = IOU_THRESHOLD) -> dict:
    """Compute IoU-enriched overlap summary from a parsed scene_state_log.

    Parameters
    ----------
    log : dict
        Parsed content of scene_state_log.json (must have "timeline" key).
    iou_threshold : float
        IoU pairs below this value are treated as noise and excluded from
        the summary counts.

    Returns
    -------
    dict with keys:
        iou_overlap_pairs_max     – max text-involving IoU-filtered pairs in any step
        steps_with_iou_overlap    – steps with at least 1 text-involving IoU pair
        worst_overlap_step        – 1-based step number with max pairs
        worst_overlap_step_pct    – worst_step / total_steps (0.0–1.0)
        top_overlap_pairs         – list of up to 3 worst {type_a, type_b, iou, category}
        total_steps               – number of steps in timeline
        text_on_text_count        – total text-on-text pair occurrences across all steps
        text_on_object_count      – total text-on-object pair occurrences across all steps
    """
    timeline = log.get("timeline", [])
    if not timeline:
        return {
            "iou_overlap_pairs_max": 0,
            "steps_with_iou_overlap": 0,
            "worst_overlap_step": 0,
            "worst_overlap_step_pct": 0.0,
            "top_overlap_pairs": [],
            "total_steps": 0,
            "text_on_text_count": 0,
            "text_on_object_count": 0,
        }

    total_steps = len(timeline)
    worst_step_idx = 0
    worst_step_count = 0
    steps_with_overlap = 0
    text_on_text_total = 0
    text_on_obj_total = 0
    # (type_a, type_b, iou, category) for top-3 selection
    all_pairs: list[tuple[str, str, float, str]] = []

    for idx, step in enumerate(timeline):
        mobs = step.get("mobjects", [])
        step_count = 0
        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                m1, m2 = mobs[i], mobs[j]
                if _is_intentional(m1, m2):
                    continue
                category = _overlap_category(m1, m2)
                if category is None:
                    continue  # non-text pair — skip
                iou = _aabb_iou(m1, m2)
                if iou >= iou_threshold:
                    step_count += 1
                    all_pairs.append((m1["type"], m2["type"], round(iou, 3), category))
                    if category == OVERLAP_TEXT_ON_TEXT:
                        text_on_text_total += 1
                    else:
                        text_on_obj_total += 1

        if step_count > 0:
            steps_with_overlap += 1
        if step_count > worst_step_count:
            worst_step_count = step_count
            worst_step_idx = idx

    # Top 3 overlap pairs by IoU (deduplicated by type pair, keep highest IoU)
    seen: dict[frozenset, tuple[float, str]] = {}
    for ta, tb, iou, cat in all_pairs:
        key = frozenset({ta, tb})
        if key not in seen or iou > seen[key][0]:
            seen[key] = (iou, cat)
    top_pairs = []
    for key, (iou, cat) in seen.items():
        pair = sorted(key)
        top_pairs.append({
            "type_a": pair[0],
            "type_b": pair[1] if len(pair) > 1 else pair[0],
            "iou": iou,
            "category": cat,
        })
    top_pairs = sorted(top_pairs, key=lambda x: x["iou"], reverse=True)[:3]

    return {
        "iou_overlap_pairs_max": worst_step_count,
        "steps_with_iou_overlap": steps_with_overlap,
        "worst_overlap_step": worst_step_idx + 1,  # 1-based
        "worst_overlap_step_pct": round((worst_step_idx + 0.5) / total_steps, 3),
        "top_overlap_pairs": top_pairs,
        "total_steps": total_steps,
        "text_on_text_count": text_on_text_total,
        "text_on_object_count": text_on_obj_total,
    }


def load_and_summarize(log_path: str | Path) -> dict | None:
    """Convenience: load scene_state_log.json and return IoU summary.

    Returns None if the file does not exist or cannot be parsed.
    """
    p = Path(log_path)
    if not p.exists():
        return None
    try:
        with open(p, encoding="utf-8") as f:
            log = json.load(f)
        return compute_iou_summary(log)
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def format_telemetry_block(summary: dict) -> str:
    """Format an IoU summary dict into a text block for Vision Agent prompts.

    The block is explicitly labeled as heuristic, so the VLM uses it as
    attention guidance rather than ground truth.
    """
    if not summary or summary.get("total_steps", 0) == 0:
        return ""

    # Only emit the block when there are actionable text overlaps
    if summary.get("iou_overlap_pairs_max", 0) == 0:
        return ""

    tot_text = summary.get("text_on_text_count", 0)
    tot_obj  = summary.get("text_on_object_count", 0)

    lines = [
        "## Render Telemetry — TEXT OVERLAP ALERT (heuristic, verify against image)",
    ]
    if tot_text:
        lines.append(f"- ⚠️  Text-on-text overlaps detected across {summary['steps_with_iou_overlap']} steps "
                     f"({tot_text} pair-occurrences total)")
    if tot_obj:
        lines.append(f"- ⚠️  Text covering non-text objects: {tot_obj} pair-occurrences")

    lines.append(f"- Worst step: {summary['worst_overlap_step']}/{summary['total_steps']} "
                 f"(~{summary['worst_overlap_step_pct']:.0%} into animation), "
                 f"{summary['iou_overlap_pairs_max']} overlapping pair(s) at that step")

    if summary["top_overlap_pairs"]:
        lines.append("- Top offending pairs:")
        cat_label = {OVERLAP_TEXT_ON_TEXT: "text-on-text", OVERLAP_TEXT_ON_OBJ: "text-on-object"}
        for p in summary["top_overlap_pairs"]:
            label = cat_label.get(p.get("category", ""), p.get("category", ""))
            lines.append(f"  • {p['type_a']} ↔ {p['type_b']}: IoU={p['iou']:.2f} [{label}]")

    lines.append("")
    lines.append(
        "These are AABB estimates — confirm visually. "
        "Non-text overlaps (Arrow↔Arrow, Line↔Axes, etc.) are intentionally excluded."
    )
    return "\n".join(lines)
