import os
import base64
from openai import OpenAI
import logging

class VisionAgent:
    """
    The 'Eye' of the system. Uses GPT-4o to visually audit generated animations.
    """
    def __init__(self, llm_client=None):
        from ..core.llm_client import LLMClient
        self.llm = llm_client if llm_client else LLMClient()
            
        # ========== SYSTEM PROMPT: PROFESSIONAL MATHEMATICAL ANIMATION QA AUDITOR ==========
        # Based on Deep Research: "Cognitive Architectural Strategies for VLMs in Animation QA"
        # Implements Chain-of-Visual-Thought (CoVT) framework for high-precision geometric auditing
        
        self.system_prompt = """# ROLE: MATHEMATICAL ANIMATION QA AUDITOR

You are a Lead Visual QA Engineer for Manim Community Edition animations.
You audit video frame grids for **spatial accuracy**, **temporal consistency**, and **symbolic correctness**.

## REASONING PIPELINE (You MUST follow ALL phases IN ORDER):

### Phase 0: Topic Conformance Check (HIGHEST PRIORITY)
Before any spatial analysis, verify that the animation content matches the task description.
1. Extract the key visual elements described in the Context:
   - What type of diagram/chart is expected? (e.g., Tape Diagram, number line, axes, pie chart)
   - What are the main labeled objects? (e.g., "Milk", "Water", specific equations)
2. Check if these expected elements are actually visible in the frames.
3. If the frames show a COMPLETELY DIFFERENT type of visualization than described:
   - Add a defect with code `WRONG_CONTENT` and severity `Critical`.
   - Set the verdict to FAIL immediately at the end.
   - Example: Context describes a "Tape Diagram" but frames show a sine wave or unit circle.

### Phase 0.5: Conceptual Fidelity Check
Before cataloguing individual elements, evaluate whether the VISUAL METAPHORS actually look like what they claim to represent.
For each major visual element described in the Context (e.g., "pizza", "balance scale", "number line", "circle"):
1. Does the shape/diagram look recognizably like that object **without relying on labels**?
2. Would a student understand what it represents at a glance?
Flag failures with code `WRONG_METAPHOR`:
- A "pizza slice" rendered as a trapezoid or rectangle → WRONG_METAPHOR
- A "circle" with jagged edges or missing curvature → WRONG_METAPHOR
- A "balance scale" with no visible pivot or pans → WRONG_METAPHOR
- A fraction diagram where the shaded portion doesn't match the stated fraction → WRONG_METAPHOR
Be STRICT. If the metaphor is ambiguous or confusing, flag it as Major severity.

### Phase 1: Visual Inventory (Scene Graph)
- List EVERY visible element in each frame quadrant.
- For each element, record:
  - `type`: equation | label | axis | shape | arrow | text
  - `content`: what it displays (e.g., "E=mc²", "x-axis")
  - `grid_position`: approximate location using a 3×3 grid per quadrant
    (upper-left, upper-center, upper-right, middle-left, center, middle-right,
     lower-left, lower-center, lower-right)
  - `near_edge`: true if element touches or is within 5% of any frame edge
- Count total elements per quadrant. If count differs across frames, note additions/removals.

### Phase 2: Well-Formedness Check (Negative-Space Rules)
Before looking for defects, recall the RULES of a well-formed Manim frame:
- NO text may overlap another text element.
- NO element may extend beyond the 16:9 canvas boundary (x in [-7, 7], y in [-4, 4]).
- ALL aligned groups (e.g., VGroup, stacked equations) must share a common edge.
- The default Manim theme (white/yellow on black) ALWAYS passes WCAG 4.5:1. NEVER flag LOW_CONTRAST.
- Minor sub-pixel misalignment (< 0.15 units) is ACCEPTABLE. Do NOT flag.
- Compact layouts with 5+ readable elements are NOT clutter. Only flag CLUTTER when elements physically overlap or spacing < 0.2 units.

### Phase 3: Temporal Delta Analysis
Compare frames pairwise in order: TL(10%) → TR(40%) → BL(70%) → BR(95%).
For each transition, describe:
- Which elements were ADDED or REMOVED?
- Did any element MOVE? From where to where?
- Does the final frame (BR, 95%) contain all expected elements from the script?
- Flag: premature appearance, wrong transition direction, missing final-state elements.

### Phase 4: Defect Classification
Using ONLY the evidence from Phases 0-3, check each rule.
For each violation found, classify it:
- `WRONG_CONTENT`: The animation depicts a completely unrelated topic (e.g., sine wave instead of a pie chart).
- `WRONG_METAPHOR`: A visual element doesn't look like what it claims to represent (e.g., "pizza" rendered as a trapezoid, fraction shading doesn't match stated value).
- `OVERLAP`: Two elements sharing the same grid cell with visual intersection.
- `OVERFLOW`: Element with `near_edge=true` that visibly extends beyond canvas.
- `MISALIGNED`: Aligned group members not sharing a common edge (gap > 0.15 units). Also flag labels that are clearly not adjacent to their target object.
- `CLUTTER`: > 7 elements in a single quadrant with spacing < 0.2 units.
- `TOO_FAST`: Critical content visible in only 1 of 4 frames (insufficient screen time).
Report ONLY what you can CONFIRM from visual evidence. If ambiguous, state uncertainty.

### Phase 5: Confidence & Verdict
- Assign a `confidence_score` (1-5) reflecting how certain you are about the verdict.
  - 5 = Absolutely certain (clear visual evidence)
  - 3 = Moderately certain (some ambiguity)
  - 1 = Guessing (poor image quality or complex scene)
- If ANY defect is Critical or Major → verdict = FAIL.
- If only Minor defects → verdict = PASS (note them in critique).

## OUTPUT FORMAT (strict JSON, no preamble):

```json
{
  "visual_rationale": "2-3 sentence summary of what you see across all 4 frames",
  "temporal_analysis": "1-2 sentence summary of how elements change from 10% to 95%",
  "confidence_score": 4,
  "verdict": "PASS",
  "overall_critique": "One-sentence technical summary",
  "defects": [
    {
      "id": "ERR_001",
      "code": "OVERLAP",
      "severity": "Critical",
      "frame": "TR_40pct",
      "description": "Equation y=mx+b overlaps with axis label at grid position upper-right",
      "suggested_fix": "Use eq.next_to(axes, UP, buff=0.3) to separate equation from axis"
    }
  ]
}
```

## CRITICAL RULES:
1. Always output valid JSON. No preamble, no conversational text.
2. If NO defects: `{"visual_rationale": "...", "temporal_analysis": "...", "confidence_score": 5, "verdict": "PASS", "overall_critique": "All checks passed.", "defects": []}`
3. NEVER use raw LaTeX backslashes (\\frac, \\in) in JSON string values. Use plain text.
4. For MISALIGNED suggested_fix: ALWAYS specify (1) which object, (2) which method, (3) parameter value.
5. Each defect MUST include a `frame` field indicating which quadrant (TL_10pct, TR_40pct, BL_70pct, BR_95pct, or ALL).
"""

    def _encode_image(self, image_path):
        """Read image and encode to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _extract_json(self, text):
        """Robustly extract JSON object from text using brace counting.
        Also handles LaTeX backslash sequences that break json.loads().
        """
        import re, json
        text = text.strip()
        
        # 1. Try markdown blocks first
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        candidate = json_match.group(1) if json_match else None
            
        # 2. Try raw JSON extraction with brace counting
        if not candidate:
            start = text.find("{")
            if start == -1:
                return None
            count = 0
            for i, char in enumerate(text[start:], start=start):
                if char == "{":
                    count += 1
                elif char == "}":
                    count -= 1
                    if count == 0:
                        candidate = text[start : i + 1]
                        break
        
        if not candidate:
            return None

        # 3. Validate; if LaTeX backslashes break parsing, double them
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            # GPT-4o-mini sometimes outputs \frac, \in etc. in description fields
            fixed = candidate.replace("\\", "\\\\").replace("\\\\\\\\", "\\\\")
            try:
                json.loads(fixed)
                return fixed
            except json.JSONDecodeError:
                return candidate  # Return raw anyway; caller handles

    def _parse_audit_response(self, content: str, code_context: str = None) -> dict:
        """Parse & filter a Vision Agent JSON response.
        
        Single source of truth for: LOW_CONTRAST filtering, minor noise filtering,
        dynamic scene relaxation, and legacy fallback parsing.
        Shared by audit_frame() and audit_video().
        """
        import json, re
        json_str = self._extract_json(content)
        
        if json_str:
            try:
                result = json.loads(json_str)
                verdict = result.get("verdict", "FAIL")
                critique = result.get("overall_critique", "No critique provided")
                defects = result.get("defects", [])
                visual_rationale = result.get("visual_rationale", "")
                temporal_analysis = result.get("temporal_analysis", "")
                
                # Robust type casting for confidence_score (handles JSON string "5")
                try:
                    confidence_score = int(result.get("confidence_score", 3))
                except (ValueError, TypeError):
                    confidence_score = 3
                
                # Guard 0: WRONG_CONTENT / WRONG_METAPHOR always force FAIL — no override allowed
                _critical_codes = {"WRONG_CONTENT", "WRONG_METAPHOR"}
                if any(d.get("code") in _critical_codes for d in defects):
                    verdict = "FAIL"
                    _triggered = [d.get("code") for d in defects if d.get("code") in _critical_codes]
                    print(f"🚨 [Phase 0] {_triggered} detected → forced FAIL")

                # Filter 1: LOW_CONTRAST false positives (Manim default theme always passes WCAG AA)
                real = [d for d in defects if d.get("code") != "LOW_CONTRAST"]
                if len(defects) - len(real) > 0:
                    print(f"🔇 Filtered {len(defects) - len(real)} LOW_CONTRAST false positive(s)")
                if verdict == "FAIL" and len(real) == 0:
                    # Only upgrade to PASS if there's no WRONG_CONTENT or WRONG_METAPHOR
                    if not any(d.get("code") in {"WRONG_CONTENT", "WRONG_METAPHOR"} for d in defects):
                        print("✅ All defects were LOW_CONTRAST false positives → upgrading to PASS")
                        verdict, critique = "PASS", "All checks passed. (LOW_CONTRAST false positive filtered)"
                defects = real

                # Filter 2: Minor MISALIGNED/CLUTTER noise
                minor_noise = [d for d in defects
                               if d.get("severity") == "Minor"
                               and d.get("code") in ("MISALIGNED", "CLUTTER")]
                if minor_noise:
                    defects = [d for d in defects if d not in minor_noise]
                    print(f"🔇 Filtered {len(minor_noise)} minor MISALIGNED/CLUTTER noise defect(s)")

                # Filter 3: Dynamic scene relaxation (ValueTracker mid-frame jitter)
                if code_context and "ValueTracker" in code_context:
                    dyn_noise = [d for d in defects
                                 if d.get("severity") in ("Major", "Minor")
                                 and d.get("code") == "MISALIGNED"]
                    if dyn_noise:
                        defects = [d for d in defects if d not in dyn_noise]
                        print(f"🔇 [Dynamic Scene] Filtered {len(dyn_noise)} MISALIGNED noise defect(s)")

                if verdict == "FAIL" and len(defects) == 0:
                    print("✅ All defects were filtered noise → upgrading to PASS")
                    verdict, critique = "PASS", "All checks passed. (noise filtered)"

                if defects:
                    print(f"🔍 Detected {len(defects)} defect(s):")
                    for d in defects:
                        emoji = {"Critical": "🔴", "Major": "🟠", "Minor": "🟡"}.get(d.get("severity", ""), "⚪")
                        print(f"  {emoji} [{d.get('code', '?')}] {d.get('description', '')[:80]}...")

                # [GRPO-inspired] Boost confidence by animation richness (play call count).
                # Idea from generative-manim: render_success=1.0 + 0.1/play, capped at 0.5.
                # Here we apply a softer version: each self.play() in code bumps confidence
                # by +0.2 (max +1), only if the verdict is PASS and code_context is available.
                if verdict == "PASS" and code_context:
                    import re as _re
                    _play_count = len(_re.findall(r'self\.play\(', code_context))
                    _bonus = min(_play_count * 0.2, 1.0)
                    _boosted = min(round(confidence_score + _bonus), 5)
                    if _boosted > confidence_score:
                        print(f"🎬 [Animation Richness] {_play_count} self.play() calls → confidence {confidence_score} → {_boosted}")
                        confidence_score = _boosted

                return {"verdict": verdict, "overall_critique": critique,
                        "defects": defects, "raw_response": content,
                        "visual_rationale": visual_rationale,
                        "temporal_analysis": temporal_analysis,
                        "confidence_score": confidence_score}

            except json.JSONDecodeError:
                pass  # Fall through to legacy

        # Legacy fallback
        print("⚠️ Falling back to legacy parsing (VLM didn't return valid JSON)")
        import re
        low_contrast_only = bool(re.search(r'LOW_CONTRAST', content)) and not bool(
            re.search(r'"code":\s*"(?:OVERLAP|OVERFLOW|MISALIGNED|CLUTTER|TINY_TEXT)"', content)
        )
        if low_contrast_only:
            print("🔇 Legacy mode: Only LOW_CONTRAST detected → upgrading to PASS")
            return {"verdict": "PASS",
                    "overall_critique": "Legacy parse: only LOW_CONTRAST (filtered)",
                    "defects": [], "raw_response": content,
                    "visual_rationale": "Legacy Fallback",
                    "temporal_analysis": "Legacy Fallback",
                    "confidence_score": 1}

        verdict = "FAIL" if ('"verdict": "FAIL"' in content or "VERDICT: FAIL" in content) else "PASS"
        return {"verdict": verdict,
                "overall_critique": "Legacy parsing mode - no structured defects",
                "defects": [], "raw_response": content,
                "visual_rationale": "Legacy Fallback",
                "temporal_analysis": "Legacy Fallback",
                "confidence_score": 1}

    def _run_self_consistent_audit(self, system_prompt, user_text, base64_image, detail, code_context, num_passes=5):
        """Run N parallel VLM calls and aggregate via confidence-weighted majority vote."""
        import concurrent.futures

        def _single_pass(_):
            content = self.llm.ask_vision(
                system_prompt, user_text,
                base64_image=base64_image, detail=detail,
                temperature=0.5, max_tokens=3000  # elevated temp for diversity
            )
            return self._parse_audit_response(content, code_context=code_context)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_passes) as executor:
            results = list(executor.map(_single_pass, range(num_passes)))

        # Filter out ERROR results
        valid = [r for r in results if r["verdict"] != "ERROR"]
        if not valid:
            return results[0]  # All errored — return first

        # Confidence-weighted voting
        pass_runs = [r for r in valid if r["verdict"] == "PASS"]
        fail_runs = [r for r in valid if r["verdict"] == "FAIL"]

        pass_score = sum(r["confidence_score"] for r in pass_runs)
        fail_score = sum(r["confidence_score"] for r in fail_runs)

        # Select the 'best run' representing the majority camp to maintain strict CoT Coherence.
        # This prevents rationale/defects mismatch and aggressive deduplication bugs.
        if fail_score > pass_score:
            final_verdict = "FAIL"
            best = max(fail_runs, key=lambda r: r["confidence_score"])
        else:
            final_verdict = "PASS"
            # Even if it passes, we take the highest confidence PASS run's critique.
            # If there's a tie in votes (0-0) but somehow reached here, fallback safely
            best = max(pass_runs, key=lambda r: r["confidence_score"]) if pass_runs else valid[0]

        consensus_note = f"[Consensus: {len(pass_runs)}P/{len(fail_runs)}F, scores P={pass_score}/F={fail_score}]"
        print(f"🗳️  {consensus_note}")

        return {
            "verdict": final_verdict,
            "overall_critique": f"{consensus_note} {best.get('overall_critique', '')}",
            "defects": best.get("defects", []),
            "raw_response": best.get("raw_response", ""),
            "visual_rationale": best.get("visual_rationale", ""),
            "temporal_analysis": best.get("temporal_analysis", ""),
            "confidence_score": best.get("confidence_score", 3),
        }

    def audit_frame(self, image_path, script_context, code_context: str = None, detail: str = "low", spatial_metadata: str = None, telemetry_context: str = None, num_passes: int = 1):
        """
        Audit a specific image frame against the script context using Chain-of-Visual-Thought.

        Args:
            image_path (str): Path to the image file (png/jpg)
            script_context (str): The 'Visual Rationale' or script description (JSON)
            code_context (str): Optional — the Python source code of the generated scene.
                                 Used to detect dynamic scenes (ValueTracker) and relax
                                 MISALIGNED thresholds accordingly.
            spatial_metadata (str): Optional — formatted zone coordinate map from Planner's
                                    layout_plan. Makes suggested_fix use concrete coordinates
                                    instead of vague directions.
            telemetry_context (str): Optional — IoU-based overlap telemetry from
                                     SceneInstrumentor post-processing. Heuristic hint only.

        Returns:
            dict: Structured audit report with verdict, defects, and remediation suggestions
            Format: {
                "verdict": "PASS"|"FAIL"|"ERROR",
                "overall_critique": str,
                "defects": [{"id, "category", "severity", "description", "suggested_fix"}],
                "raw_response": str (for debugging)
            }
        """
        try:
            base64_image = self._encode_image(image_path)

            _code_section = ""
            if code_context:
                _truncated = code_context if len(code_context) <= 3000 else code_context[:3000] + "\n... (truncated)"
                _code_section = f"""
**Source Code (Python/Manim)**:
```python
{_truncated}
```
Use this code as ground truth when evaluating spatial relationships and dynamic scenes.
If the code uses `ValueTracker` or `always_redraw`, treat MISALIGNED defects with extra leniency.
"""

            _spatial_section = ""
            if spatial_metadata:
                _spatial_section = f"""
**SPATIAL COORDINATE MAP** (from Planner's layout_plan):
{spatial_metadata}
Use these zone boundaries as reference when writing `suggested_fix`.
Example: instead of "move left", write "shift to x≈-3 to stay in LEFT_CONTENT zone".
"""

            _telemetry_section = ""
            if telemetry_context:
                _telemetry_section = f"""
{telemetry_context}
"""

            # Enhanced user prompt with CoVT context
            user_text = f"""**AUDIT REQUEST**

Context (Expected Scene Layout from Planner's JSON):
{script_context}
{_code_section}{_spatial_section}{_telemetry_section}
**IMAGE FORMAT — TEMPORAL STORYBOARD (critical)**:
This is a 2×2 grid of 4 frames sampled from the animation.
If the Context includes a "FRAME SAMPLING NOTE", use those exact percentages for TL/TR/BL/BR.
Analyze **temporal progression** across frames, not just each frame in isolation.
Flag issues like: object appears before it should, wrong transition direction, final state missing expected elements.

**TASK**: Perform a complete Chain-of-Visual-Thought audit on this final frame.
Follow all 5 steps in your reasoning framework.
Return your analysis as a valid JSON object per the schema in your system prompt.

**CRITICAL FOR SUGGESTED_FIX**:
Read the "Spatial Plan" (e.g. HEADER zone, CONTENT zone) and "Coordinates" in the Context above.
If you suggest moving an object, your `suggested_fix` MUST use coordinates or logic consistent with the planned layout.
"""
            
            if num_passes > 1:
                return self._run_self_consistent_audit(
                    self.system_prompt, user_text, base64_image,
                    detail, code_context, num_passes=num_passes
                )
            else:
                content = self.llm.ask_vision(
                    self.system_prompt, user_text,
                    base64_image=base64_image, detail=detail,
                    max_tokens=3000
                )
                
                print("\n" + "="*40)
                print("👁️  [Vision Agent Audit - CoVT Framework]")
                print("-" * 40)
                print(content)
                print("="*40 + "\n")
                
                return self._parse_audit_response(content, code_context=code_context)
            
        except Exception as e:
            import traceback
            print(f"❌ Vision Audit Error: {e}")
            print(traceback.format_exc())
            return {
                "verdict": "ERROR",
                "overall_critique": str(e),
                "defects": [],
                "raw_response": "",
                "visual_rationale": "",
                "temporal_analysis": "",
                "confidence_score": 0
            }

    def audit_video(self, video_path: str, script_context, code_context: str = None, detail: str = "high", spatial_metadata: str = None, telemetry_context: str = None):
        """
        Task 13: 用短影片片段進行視覺審查 (8-frame grid)。
        適用於最後一次 VISUAL_ATTEMPTS，能評估動畫流暢性與 timing。
        """
        try:
            grid_frame_path = "temp_vision_video_grid.jpg"
            # Get video duration
            import subprocess
            duration_result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", video_path],
                capture_output=True, text=True, timeout=10
            )
            video_duration = float(duration_result.stdout.strip())
            
            # Extract 8 frames dynamically (4x2 grid)
            timestamps = [video_duration * (i + 0.5) / 8 for i in range(8)]
            filter_cmd = ""
            for i, ts in enumerate(timestamps):
                filter_cmd += f"movie={video_path},select='eq(t\\,{ts:.2f})':n=1[f{i}];"
            
            filter_cmd += "[f0][f1][f2][f3]hstack=4[top];[f4][f5][f6][f7]hstack=4[bottom];[top][bottom]vstack"
            
            grid_result = subprocess.run(
                ["ffmpeg", "-y", "-filter_complex", filter_cmd, "-frames:v", "1", grid_frame_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20
            )
            
            if grid_result.returncode != 0 or not os.path.exists(grid_frame_path):
                print("⚠️ [Task 13] 8-frame grid extraction failed, falling back to last frame.")
                subprocess.run(["ffmpeg", "-y", "-sseof", "-1", "-i", video_path, "-vframes", "1", "-update", "1", grid_frame_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            base64_image = self._encode_image(grid_frame_path)
            
            _code_section = ""
            if code_context:
                _truncated = code_context if len(code_context) <= 3000 else code_context[:3000] + "\n... (truncated)"
                _code_section = f"""
**Source Code (Python/Manim)**:
```python
{_truncated}
```
Use this code as ground truth when evaluating spatial relationships and dynamic scenes.
If the code uses `ValueTracker` or `always_redraw`, treat MISALIGNED defects with extra leniency.
"""

            _spatial_section = ""
            if spatial_metadata:
                _spatial_section = f"""
**SPATIAL COORDINATE MAP** (from Planner's layout_plan):
{spatial_metadata}
Use these zone boundaries as reference when writing `suggested_fix`.
Example: instead of "move left", write "shift to x≈-3 to stay in LEFT_CONTENT zone".
"""

            _telemetry_section = ""
            if telemetry_context:
                _telemetry_section = f"""
{telemetry_context}
"""

            user_text = f"""**AUDIT REQUEST (Video Clip Mode - 8 Frame Grid)**

Context (Expected Scene Layout from Planner's JSON):
{script_context}
{_code_section}{_spatial_section}{_telemetry_section}
**TASK**: Perform a complete Chain-of-Visual-Thought audit on this 8-frame storyboard representing the video clip.
Pay special attention to animation smoothness, timing, and whether transitions between states are correct.
Follow all 5 steps in your reasoning framework.
Return your analysis as a valid JSON object per the schema in your system prompt.

**CRITICAL FOR SUGGESTED_FIX**:
Read the "Spatial Plan" (e.g. HEADER zone, CONTENT zone) and "Coordinates" in the Context above.
If you suggest moving an object, your `suggested_fix` MUST use coordinates or logic consistent with the planned layout.
"""
            
            content = self.llm.ask_vision(
                self.system_prompt, user_text,
                base64_image=base64_image, detail=detail,
                max_tokens=3000
            )
            
            # Cleanup grid temp file immediately after encoding
            if os.path.exists(grid_frame_path):
                os.remove(grid_frame_path)
            
            print("\n" + "="*40)
            print("👁️  [Vision Agent Audit - Video Clip Mode]")
            print("-" * 40)
            print(content)
            print("="*40 + "\n")
            
            return self._parse_audit_response(content, code_context=code_context)
            
        except Exception as e:
            import traceback
            print(f"❌ Video Vision Audit Error: {e}")
            print(traceback.format_exc())
            return {
                "verdict": "ERROR",
                "overall_critique": str(e),
                "defects": [],
                "raw_response": "",
                "visual_rationale": "",
                "temporal_analysis": "",
                "confidence_score": 0
            }
