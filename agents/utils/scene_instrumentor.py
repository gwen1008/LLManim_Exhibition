import json
from pathlib import Path

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
            # Try to filter out invisible/purely structural objects
            opacity = getattr(mob, "fill_opacity", 0) + getattr(mob, "stroke_opacity", 0)
            if hasattr(mob, "get_fill_opacity") and hasattr(mob, "get_stroke_opacity"):
                 opacity = mob.get_fill_opacity() + mob.get_stroke_opacity()
                 
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
        overlap_count = 0
        mobs = snapshot["mobjects"]
        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                m1, m2 = mobs[i], mobs[j]
                
                # Check horizontal overlap
                h_overlap = (abs(m1["center"][0] - m2["center"][0]) * 2 < (m1["width"] + m2["width"]))
                # Check vertical overlap
                v_overlap = (abs(m1["center"][1] - m2["center"][1]) * 2 < (m1["height"] + m2["height"]))
                
                if h_overlap and v_overlap:
                    overlap_count += 1
                    
        snapshot["overlap_pairs"] = overlap_count
        snapshot["total_screen_coverage"] = sum(m["area"] for m in mobs)
        
        self._log.append(snapshot)
        
        # Save incrementally
        self.save_log()
        return result

    def save_log(self):
        try:
            with open(self._log_path, "w", encoding="utf-8") as f:
                json.dump({
                    "max_simultaneous_objects": max((s["n_mobjects_visible"] for s in self._log), default=0),
                    "max_overlap_pairs": max((s["overlap_pairs"] for s in self._log), default=0),
                    "steps_with_overlap": sum(1 for s in self._log if s["overlap_pairs"] > 0),
                    "peak_screen_coverage": max((s["total_screen_coverage"] for s in self._log), default=0),
                    "timeline": self._log
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️ SceneInstrumentor failed to save log: {e}")
