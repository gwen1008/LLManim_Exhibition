"""
LayoutAuditor — deterministic post-render layout quality check.

Reads SceneInstrumentor's scene_state_log.json and produces:
  - verdict: PASS / FAIL
  - violations: list of (metric, value, threshold, step, details, fix_hint)
  - metrics: raw indicator values
  - score_1_to_5: maps to FinalJudge's `spatial_layout` dimension

Cost: ~10ms, $0.

Used by:
  1. RefiningLoop (in-loop quality gate → next iteration's fix prompt)
  2. FinalJudge (post-render `spatial_layout` dimension)
"""
import json
from pathlib import Path
from typing import Optional


class LayoutVerdict:
    PASS = "PASS"
    FAIL = "FAIL"


class LayoutAuditor:
    # Conservative thresholds — prefer false-negative over false-positive.
    # Calibrate after running on first 30 cases.
    THRESHOLDS = {
        "text_occlusion_max": 0.5,   # user's #1 concern: text obscured by shapes
        "overlap_iou_max":    0.4,   # objects mutually obscuring each other
        "crowding_max":       0.85,  # canvas too cramped
    }

    SEVERITY = {
        "text_occlusion_max": "Critical",
        "overlap_iou_max":    "Critical",
        "crowding_max":       "Major",
    }

    def audit(self, scene_state_log_path: str) -> dict:
        """Read instrumentor log and return audit dict."""
        path = Path(scene_state_log_path)
        if not path.exists():
            return {
                "verdict": LayoutVerdict.PASS,  # cannot audit → don't block
                "violations": [],
                "metrics": {},
                "score_1_to_5": None,
                "note": f"log not found: {path}",
            }

        try:
            with open(path, encoding="utf-8") as f:
                log = json.load(f)
        except Exception as e:
            return {
                "verdict": LayoutVerdict.PASS,
                "violations": [],
                "metrics": {},
                "score_1_to_5": None,
                "note": f"log unreadable: {e}",
            }

        metrics = {
            "text_occlusion_max": float(log.get("text_occlusion_max", 0.0) or 0.0),
            "overlap_iou_max":    float(log.get("overlap_iou_max", 0.0) or 0.0),
            "crowding_max":       float(log.get("crowding_max", 0.0) or 0.0),
            "balance_offset_max": float(log.get("balance_offset_max", 0.0) or 0.0),
        }

        violations = []
        for metric, threshold in self.THRESHOLDS.items():
            val = metrics[metric]
            if val >= threshold:
                step = log.get(f"{metric.replace('_max','')}_worst_step")
                violations.append({
                    "metric": metric,
                    "severity": self.SEVERITY[metric],
                    "value": round(val, 3),
                    "threshold": threshold,
                    "step": step,
                    "details": self._describe_violation(metric, val, step, log),
                    "fix_hint": self._fix_hint(metric, val, step, log),
                })

        verdict = LayoutVerdict.FAIL if violations else LayoutVerdict.PASS
        score = self._score(metrics)

        return {
            "verdict": verdict,
            "violations": violations,
            "metrics": metrics,
            "score_1_to_5": score,
        }

    def _score(self, metrics: dict) -> int:
        """Map metrics → 1..5 dimension score for FinalJudge."""
        occ = metrics["text_occlusion_max"]
        iou = metrics["overlap_iou_max"]
        crd = metrics["crowding_max"]

        if occ >= 0.5:
            return 1
        if iou >= 0.4:
            return 2
        if crd >= 0.85:
            return 2
        if iou >= 0.25:
            return 3
        if crd >= 0.7:
            return 3
        if occ >= 0.25 or iou >= 0.1:
            return 4
        return 5

    # ── Violation description / fix hint ─────────────────────────────────────

    def _lookup_pair(self, log: dict, step: Optional[int], pair_key: str):
        """Get the worst-pair Mobjects from timeline at given 1-based step."""
        if not step:
            return None, None
        try:
            snap = log["timeline"][step - 1]
            pair = snap.get(pair_key)
            if not pair:
                return None, None
            i, j = pair
            mobs = snap["mobjects"]
            return mobs[i], mobs[j]
        except (KeyError, IndexError, TypeError):
            return None, None

    def _describe_violation(self, metric, val, step, log):
        if metric == "text_occlusion_max":
            text_mob, other = self._lookup_pair(log, step, "text_occlusion_worst_pair")
            if text_mob and other:
                return (f"Step {step}: text {text_mob['type']} at "
                        f"({text_mob['center'][0]:.1f},{text_mob['center'][1]:.1f}) "
                        f"is {int(val*100)}% covered by {other['type']} "
                        f"at ({other['center'][0]:.1f},{other['center'][1]:.1f}).")
            return f"Step {step}: text occluded {int(val*100)}%."
        if metric == "overlap_iou_max":
            m1, m2 = self._lookup_pair(log, step, "overlap_iou_worst_pair")
            if m1 and m2:
                return (f"Step {step}: {m1['type']} and {m2['type']} overlap "
                        f"with IoU={val:.2f} (centers "
                        f"{m1['center'][:2]} & {m2['center'][:2]}).")
            return f"Step {step}: overlap IoU={val:.2f}."
        if metric == "crowding_max":
            return f"Step {step}: canvas {int(val*100)}% covered — too crowded."
        return f"Step {step}: {metric}={val:.2f}"

    def _fix_hint(self, metric, val, step, log):
        if metric == "text_occlusion_max":
            text_mob, other = self._lookup_pair(log, step, "text_occlusion_worst_pair")
            if text_mob and other:
                # Suggest moving text to the side opposite the obscuring shape
                ox, oy = other["center"][0], other["center"][1]
                # Pick the side with most free space
                if oy >= 0:
                    target = "DOWN"
                    ty = max(-3.0, oy - other["height"]/2 - 0.5)
                    tx = ox
                else:
                    target = "UP"
                    ty = min(3.0, oy + other["height"]/2 + 0.5)
                    tx = ox
                return (f"Move the text out of {other['type']}: use "
                        f"`text.next_to(<other_id>, {target}, buff=0.4)` "
                        f"or `text.move_to([{tx:.1f}, {ty:.1f}, 0])`.")
            return ("Re-position the occluded text using .next_to(shape, UP/DOWN, buff=0.4) "
                    "instead of overlapping move_to.")
        if metric == "overlap_iou_max":
            return ("Separate the two overlapping mobjects: use .next_to() with buff>=0.4, "
                    "or shift one with .shift(LEFT*1.5) / .shift(RIGHT*1.5).")
        if metric == "crowding_max":
            return ("Reduce on-screen objects: FadeOut earlier-step mobjects before adding "
                    "new ones, or split into more steps.")
        return "Re-layout this step to satisfy the threshold."

    # ── Build a fix-prompt block for RefiningLoop ────────────────────────────

    @staticmethod
    def build_fix_prompt(audit: dict) -> str:
        """Produce a natural-language fix prompt block for the Coder."""
        if audit["verdict"] != LayoutVerdict.FAIL:
            return ""
        lines = ["[LAYOUT AUDIT FAILED — fix the following before re-rendering]"]
        for v in audit["violations"]:
            lines.append(
                f"- ❌ [{v['severity']}] {v['metric']} = {v['value']} "
                f"(threshold {v['threshold']})"
            )
            lines.append(f"  {v['details']}")
            lines.append(f"  ACTION: {v['fix_hint']}")
        lines.append("")
        lines.append("RULES:")
        lines.append("- Use .next_to(other, DIRECTION, buff>=0.4) instead of overlapping move_to.")
        lines.append("- For text near shapes, place text OUTSIDE the shape's bbox with buff>=0.3.")
        lines.append("- If too crowded: FadeOut older mobjects before introducing new ones.")
        lines.append("- Keep all unaffected steps unchanged. Re-emit the full GeneratedScene class.")
        return "\n".join(lines)
