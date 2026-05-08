import json
from pathlib import Path

# ── Canvas constants (Manim default 14×8 frame) ──────────────────────────────
CANVAS_W = 14.0
CANVAS_H = 8.0
CANVAS_AREA = CANVAS_W * CANVAS_H

# Text-like Mobject types — used for "text occlusion" detection.
_TEXT_TYPES = {"Text", "MathTex", "Tex", "MarkupText", "Title", "Paragraph",
               "SingleStringMathTex", "BulletedList"}


def _is_text_type(t: str) -> bool:
    return t in _TEXT_TYPES


def _aabb_intersection_area(m1: dict, m2: dict) -> float:
    """Axis-aligned bounding box intersection area.

    Computes the actual overlap rectangle by intersecting the two bounding
    spans on each axis, so it is correct for both partial overlap and full
    containment (it never exceeds the smaller box's edge length on any axis).
    """
    w1, h1 = m1["width"], m1["height"]
    w2, h2 = m2["width"], m2["height"]
    cx1, cy1 = m1["center"][0], m1["center"][1]
    cx2, cy2 = m2["center"][0], m2["center"][1]

    x1_lo, x1_hi = cx1 - w1 / 2, cx1 + w1 / 2
    x2_lo, x2_hi = cx2 - w2 / 2, cx2 + w2 / 2
    y1_lo, y1_hi = cy1 - h1 / 2, cy1 + h1 / 2
    y2_lo, y2_hi = cy2 - h2 / 2, cy2 + h2 / 2

    dx = min(x1_hi, x2_hi) - max(x1_lo, x2_lo)
    dy = min(y1_hi, y2_hi) - max(y1_lo, y2_lo)
    if dx <= 0 or dy <= 0:
        return 0.0
    return dx * dy


def _aabb_iou(m1: dict, m2: dict) -> float:
    """Intersection over union for two AABBs."""
    inter = _aabb_intersection_area(m1, m2)
    if inter <= 0:
        return 0.0
    union = m1["area"] + m2["area"] - inter
    if union <= 0:
        return 0.0
    return inter / union


def _text_containment_ratio(text_mob: dict, other: dict) -> float:
    """Fraction of text_mob's bbox area that is inside `other`'s bbox.
    Returns 0..1; 1.0 means text fully covered by other."""
    if text_mob["area"] <= 0:
        return 0.0
    return _aabb_intersection_area(text_mob, other) / text_mob["area"]


def _is_label_on_shape(text_mob: dict, other: dict, text_z: int, other_z: int) -> bool:
    """Detect intentional label-on-shape pattern (label drawn inside a colored shape).

    Conditions (all must hold):
      - Text is fully (>=95%) inside the other shape's bbox
      - Text bbox is much smaller than the shape (text area < 25% of shape area)
      - Text is drawn AFTER the shape (higher z-order → on top, readable)
    """
    if text_mob["area"] <= 0 or other["area"] <= 0:
        return False
    contain = _aabb_intersection_area(text_mob, other) / text_mob["area"]
    if contain < 0.95:
        return False
    if text_mob["area"] / other["area"] >= 0.25:
        return False
    # z-order: in Manim, later-added mobjects render on top.
    # `mobjects` list order ≈ z-order; bigger index = drawn last = on top.
    return text_z > other_z


def _balance_offset(mobs: list[dict]) -> float:
    """|mean(x_centers)| / (CANVAS_W/2). Range 0..1; 0=balanced, 1=fully on one edge."""
    if not mobs:
        return 0.0
    mean_x = sum(m["center"][0] for m in mobs) / len(mobs)
    return min(1.0, abs(mean_x) / (CANVAS_W / 2))


class SceneInstrumentor:
    """
    Monkey-patches Scene.play() to log the exact state (bounding boxes, 
    visibility, overlaps) of all Mobjects after every animation step.
    Used for quantitative evaluation of the 'object stacking' problem.
    """
    def __init__(self, scene, log_path="scene_state_log.json"):
        self._scene = scene
        self._log_path = Path(log_path)
        self._log = []
        self._step = 0
        
        # Monkey-patch self.play
        self._original_play = scene.play
        scene.play = self._instrumented_play

    def _instrumented_play(self, *anims, **kwargs):
        # Execute the actual animation
        result = self._original_play(*anims, **kwargs)
        self._step += 1
        
        snapshot = {
            "step": self._step,
            "mobjects": []
        }
        
        # Collect post-animation state
        for mob in getattr(self._scene, "mobjects", []):
            # Manim v0.20.0: __getattr__ wraps deprecated getters, making hasattr() unreliable.
            # get_fill_opacity() may raise AttributeError or return None on internal mobjects.
            try:
                opacity = (mob.get_fill_opacity() or 0) + (mob.get_stroke_opacity() or 0)
            except Exception:
                opacity = 1.0  # assume visible if opacity cannot be determined
                 
            # If it's effectively invisible, skip it for visual overlap metrics
            if opacity <= 0.01:
                continue
                
            # Skip SubtitleManager backgrounds 
            if type(mob).__name__ == "BackgroundRectangle":
                continue
                
            try:
                # get_bounding_box() returns a numpy array [UP_LEFT, DOWN_RIGHT, Z_AXIS] etc.
                # but width/height is easier for simple overlap estimation
                w = mob.width
                h = mob.height
                if w * h < 0.05: # Skip tiny dots/lines 
                    continue
                    
                center = mob.get_center().tolist()
                
                snapshot["mobjects"].append({
                    "type": type(mob).__name__,
                    "width": round(w, 3),
                    "height": round(h, 3),
                    "center": [round(c, 3) for c in center],
                    "area": round(w * h, 3),
                })
            except Exception:
                pass # safely ignore objects that don't compute bboxes well
                
        snapshot["n_mobjects_visible"] = len(snapshot["mobjects"])
        
        # Rough pairwise overlap count (simple AABB intersection)
        # with intentional-overlay whitelist to suppress false positives
        overlap_count = 0
        mobs = snapshot["mobjects"]

        # Type pairs that are always intentional overlays (e.g. Sector drawn inside its Circle)
        _INTENTIONAL_TYPE_PAIRS = {
            frozenset({"Sector", "Circle"}),
            frozenset({"AnnularSector", "Circle"}),
            frozenset({"Sector", "Arc"}),
            frozenset({"AnnularSector", "Arc"}),
        }

        def _is_intentional_overlay(m1, m2):
            """Return True if this overlap should be treated as intentional."""
            # 1. Type-pair whitelist
            pair = frozenset({m1["type"], m2["type"]})
            if pair in _INTENTIONAL_TYPE_PAIRS:
                return True
            # 2. Containment check: one bbox is fully (≥90%) inside the other
            #    Uses AABB: if the smaller fits inside the larger with ≤5% margin error
            for small, large in [(m1, m2), (m2, m1)]:
                if small["width"] <= large["width"] * 1.05 and small["height"] <= large["height"] * 1.05:
                    # Check center proximity: small center within large bbox
                    dx = abs(small["center"][0] - large["center"][0])
                    dy = abs(small["center"][1] - large["center"][1])
                    if dx <= (large["width"] - small["width"]) / 2 + 0.1 and \
                       dy <= (large["height"] - small["height"]) / 2 + 0.1:
                        return True
            return False

        # Track worst (max) IoU and text-occlusion *for this step* so we can
        # produce actionable fix hints later.
        worst_iou = 0.0
        worst_iou_pair = None
        worst_occ = 0.0
        worst_occ_pair = None  # (text_idx, other_idx)

        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                m1, m2 = mobs[i], mobs[j]

                # Check horizontal overlap
                h_overlap = (abs(m1["center"][0] - m2["center"][0]) * 2 < (m1["width"] + m2["width"]))
                # Check vertical overlap
                v_overlap = (abs(m1["center"][1] - m2["center"][1]) * 2 < (m1["height"] + m2["height"]))

                if not (h_overlap and v_overlap):
                    continue

                if _is_intentional_overlay(m1, m2):
                    snapshot.setdefault("intentional_overlay_pairs", 0)
                    snapshot["intentional_overlay_pairs"] += 1
                    continue

                overlap_count += 1

                # Precise IoU for ranking severity
                iou = _aabb_iou(m1, m2)
                if iou > worst_iou:
                    worst_iou = iou
                    worst_iou_pair = (i, j)

                # Text-occlusion: if exactly one side is a text type, measure
                # how much of the text bbox is contained in the non-text bbox.
                # Skip the intentional "label inside shape" pattern (e.g. area
                # label centered in a colored Rectangle) — that is a deliberate
                # design choice, not occlusion.
                t1, t2 = _is_text_type(m1["type"]), _is_text_type(m2["type"])
                if t1 ^ t2:  # exactly one is text
                    if t1:
                        text_mob, other = m1, m2
                        text_z, other_z = i, j
                        pair = (i, j)
                    else:
                        text_mob, other = m2, m1
                        text_z, other_z = j, i
                        pair = (j, i)

                    if _is_label_on_shape(text_mob, other, text_z, other_z):
                        snapshot.setdefault("label_on_shape_pairs", 0)
                        snapshot["label_on_shape_pairs"] += 1
                        continue

                    occ = _text_containment_ratio(text_mob, other)
                    if occ > worst_occ:
                        worst_occ = occ
                        worst_occ_pair = pair

        snapshot["overlap_pairs"] = overlap_count
        snapshot["total_screen_coverage"] = sum(m["area"] for m in mobs)
        snapshot["overlap_iou_max"] = round(worst_iou, 3)
        snapshot["overlap_iou_worst_pair"] = worst_iou_pair  # (i, j) or None
        snapshot["text_occlusion_max"] = round(worst_occ, 3)
        snapshot["text_occlusion_worst_pair"] = worst_occ_pair  # (text_idx, other_idx) or None
        snapshot["crowding"] = round(min(1.0, snapshot["total_screen_coverage"] / CANVAS_AREA), 3)
        snapshot["balance_offset"] = round(_balance_offset(mobs), 3)
        
        self._log.append(snapshot)
        
        # Save incrementally
        self.save_log()
        return result

    def save_log(self):
        try:
            # Aggregate per-step metrics → max across all steps
            def _argmax_step(key):
                best_idx, best_val = -1, -1.0
                for idx, s in enumerate(self._log):
                    v = s.get(key, 0) or 0
                    if v > best_val:
                        best_val, best_idx = v, idx
                return best_idx, best_val

            iou_step, iou_max = _argmax_step("overlap_iou_max")
            occ_step, occ_max = _argmax_step("text_occlusion_max")
            crd_step, crd_max = _argmax_step("crowding")
            bal_step, bal_max = _argmax_step("balance_offset")

            with open(self._log_path, "w", encoding="utf-8") as f:
                json.dump({
                    "max_simultaneous_objects": max((s["n_mobjects_visible"] for s in self._log), default=0),
                    "max_overlap_pairs": max((s["overlap_pairs"] for s in self._log), default=0),
                    "steps_with_overlap": sum(1 for s in self._log if s["overlap_pairs"] > 0),
                    "total_intentional_overlaps_filtered": sum(s.get("intentional_overlay_pairs", 0) for s in self._log),
                    "peak_screen_coverage": max((s["total_screen_coverage"] for s in self._log), default=0),
                    # ── Layout audit metrics (deterministic) ──────────────
                    "overlap_iou_max":     round(iou_max, 3) if iou_max >= 0 else 0.0,
                    "overlap_iou_worst_step": (iou_step + 1) if iou_step >= 0 else None,
                    "text_occlusion_max":  round(occ_max, 3) if occ_max >= 0 else 0.0,
                    "text_occlusion_worst_step": (occ_step + 1) if occ_step >= 0 else None,
                    "crowding_max":        round(crd_max, 3) if crd_max >= 0 else 0.0,
                    "crowding_worst_step": (crd_step + 1) if crd_step >= 0 else None,
                    "balance_offset_max":  round(bal_max, 3) if bal_max >= 0 else 0.0,
                    "balance_offset_worst_step": (bal_step + 1) if bal_step >= 0 else None,
                    "timeline": self._log
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️ SceneInstrumentor failed to save log: {e}")
