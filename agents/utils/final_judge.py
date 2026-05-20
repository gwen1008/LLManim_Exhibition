"""
FinalJudge — Post-render rubric-based quality evaluator.

Two-phase evaluation:
  Phase 1: Claude 3.5 Sonnet reads the generated Python code
           → checks math logic, API correctness, structural issues
  Phase 2: GPT-4o views rendered video frames
           → receives Phase 1 code analysis as context hint
  Aggregate: weighted scoring, Python-side PASS/FAIL threshold

Never lets the LLM output PASS/FAIL directly.
Based on: G-Eval (CoT + form-filling), Prometheus (per-score rubric descriptions),
          LLM-Rubric (multi-dimension decomposition).
"""
import os
import re
import json
import base64
import subprocess


def _normalize_text(s: str) -> str:
    """Lowercase + strip whitespace + remove common punctuation/units for fuzzy match."""
    if s is None:
        return ""
    s = str(s).lower().strip()
    s = re.sub(r"[\s,，。.!?；;:：、]+", "", s)
    return s


_LATEX_FRAC_RE = re.compile(r"\\[td]?frac\s*\{\s*(-?\d+)\s*\}\s*\{\s*(-?\d+)\s*\}")


def _normalize_latex_fractions(s: str) -> str:
    r"""Rewrite \frac{a}{b} (and \dfrac{a}{b}) → a/b so _extract_numbers picks them up.

    Without this, GT '\\frac{3}{4}' is parsed as [3.0, 4.0] while extracted '3/4'
    is parsed as [0.75], and they never match. Five variant-A questions
    (Q026/Q122/Q123/Q124/Q137) failed for exactly this reason.
    """
    return _LATEX_FRAC_RE.sub(lambda m: f"{m.group(1)}/{m.group(2)}", str(s))


def _extract_numbers(s: str) -> list[float]:
    """Pull all numeric tokens (incl. fractions like 1/2) from a string as floats."""
    if s is None:
        return []
    s = _normalize_latex_fractions(s)
    nums = []
    # Fractions a/b first (so we don't double-count a and b)
    consumed = set()
    for m in re.finditer(r"(-?\d+)\s*/\s*(\d+)", str(s)):
        try:
            a, b = int(m.group(1)), int(m.group(2))
            if b != 0:
                nums.append(a / b)
                consumed.update(range(m.start(), m.end()))
        except (ValueError, ZeroDivisionError):
            pass
    # Plain decimals/integers, skipping consumed spans
    for m in re.finditer(r"-?\d+(?:\.\d+)?", str(s)):
        if m.start() in consumed:
            continue
        try:
            nums.append(float(m.group(0)))
        except ValueError:
            pass
    return nums


_REL_OP_RE = re.compile(r"(<=|>=|<|>|≤|≥|≠|=)")
# Arithmetic operators that, together with relational ops, must match in sequence
# for equation-style answers (e.g. '3^2 + 4^2 = 5^2' vs '3^2 - 4^2 = 5^2').
_STRUCT_OP_RE = re.compile(r"(<=|>=|<|>|≤|≥|≠|=|\+|\-|\*|/|\^)")


def _normalize_relational(s: str) -> str:
    """Lowercase, strip whitespace/punct except relational operators and digits/letters/fractions.

    Preserves operator order so '0.7 < 0.75 = 3/4' and '0.7 > 0.75 = 3/4' do not collapse to equal forms.
    """
    if s is None:
        return ""
    s = str(s).lower()
    # Unify unicode operators
    s = s.replace("≤", "<=").replace("≥", ">=").replace("≠", "!=")
    # Drop whitespace and most punctuation, keep digits, letters (incl. CJK), '/', '.', and operators
    s = re.sub(r"[^0-9a-z一-鿿/<>=!.\-]+", "", s)
    return s


def _is_relational(s: str) -> bool:
    """Ground truth contains a relational operator or chained equation (>=2 '=' signs)."""
    if not s:
        return False
    if re.search(r"<=|>=|<|>|≤|≥|≠", str(s)):
        return True
    # Chained equation like 'a = b = c' or '3^2 - 4^2 = 5^2' (single '=' with structure)
    if str(s).count("=") >= 1 and re.search(r"=", str(s)):
        # Has '=' AND at least one operator on either side that suggests an equation,
        # not just a labeled value like "answer = 12"
        return bool(re.search(r"[+\-*/^]\s*\d", str(s)) or str(s).count("=") >= 2)
    return False


def _compare_answer(extracted: str, ground_truth: str) -> bool | None:
    """
    Conservative answer comparison.

    Returns:
        True  — extracted answer matches ground truth (numbers all present, or text substring match).
        False — clearly does not match (numbers conflict).
        None  — inconclusive (extraction failed, or no comparable signal).
    """
    if not extracted or not ground_truth:
        return None

    gt_nums = _extract_numbers(ground_truth)
    ex_nums = _extract_numbers(extracted)

    # Numeric-priority comparison: ground truth's key numbers must all appear in extracted.
    if gt_nums:
        if not ex_nums:
            return None  # extracted had no numbers → inconclusive
        # Allow small float tolerance (0.01) and ordering-free containment.
        for gn in gt_nums:
            if not any(abs(gn - en) <= max(0.01, abs(gn) * 0.001) for en in ex_nums):
                return False

        # Relational / equation answers: numbers alone are not enough.
        # '0.7 < 0.75 = 3/4' must NOT match '0.7 > 0.75 = 3/4'.
        # Require the operator sequence to match too, else fall back to None.
        if _is_relational(ground_truth):
            # Use the *structural* op sequence (rel + arith) so equations like
            # '3^2 + 4^2 = 5^2' don't collapse-equal to '3^2 - 4^2 = 5^2'.
            gt_ops = _STRUCT_OP_RE.findall(str(ground_truth))
            ex_ops = _STRUCT_OP_RE.findall(str(extracted))
            if gt_ops:
                if gt_ops == ex_ops:
                    return True
                # Operators present in GT but mismatch in extracted → conflict, not match.
                if ex_ops and gt_ops != ex_ops:
                    return False
                # Extracted has no operators at all — can't confirm relational claim.
                return None
            # GT looks relational (e.g. equation with structured RHS) but no ops captured;
            # require normalized-string containment as a stricter check.
            gt_n = _normalize_relational(ground_truth)
            ex_n = _normalize_relational(extracted)
            if gt_n and ex_n and (gt_n in ex_n or ex_n in gt_n):
                return True
            return None

        return True

    # No numbers in GT — fall back to normalized text containment (both directions).
    gt_n = _normalize_text(ground_truth)
    ex_n = _normalize_text(extracted)
    if not gt_n or not ex_n:
        return None
    if gt_n in ex_n or ex_n in gt_n:
        return True
    # Token-overlap fallback (>=50% of GT tokens present)
    gt_tokens = [t for t in re.split(r"[^\w一-鿿]+", str(ground_truth).lower()) if len(t) >= 2]
    if gt_tokens:
        hit = sum(1 for t in gt_tokens if t in str(extracted).lower())
        if hit / len(gt_tokens) >= 0.5:
            return True
    return None  # inconclusive — don't trigger veto on fuzzy text


class FinalJudge:
    # ── Weights (must sum to 1.0) ──────────────────────────────────────────
    # math_correctness: Claude reads code (most reliable text signal)
    # concept_alignment + visual_clarity: GPT-4o views frames (LLM, noisy)
    # spatial_layout: deterministic from SceneInstrumentor (highest trust)
    WEIGHTS = {
        "math_correctness":  0.40,  # Claude only
        "concept_alignment": 0.15,  # GPT-4o only
        "visual_clarity":    0.15,  # GPT-4o only
        "spatial_layout":    0.30,  # deterministic — see LayoutAuditor
    }

    # Verdict thresholds — calibrate against golden_set after collecting labels.
    PASS_THRESHOLD = 3.5      # weighted_total below this → FAIL
    DIMENSION_FLOOR = 2       # any single dimension <= this → FAIL (hard veto)

    # ── Code Reviewer prompt (Claude 3.5 Sonnet) ──────────────────────────
    _CODE_REVIEW_SYSTEM = """You are an expert Manim Community Edition (CE) code reviewer.
You analyze generated Manim Python code to find mathematical and logical problems.

Check ONLY these categories (ignore style/formatting):

1. **Math Logic Errors**
   - Formulas or values that are mathematically wrong
   - Fraction diagrams where shaded count ≠ stated fraction
   - Angle drawn with wrong radian value vs stated degrees
   - Number line range that doesn't include key plotted points

2. **Visual Metaphor Mismatch**
   - Code claims to draw X but actually draws something unrecognizable
   - e.g., "pizza" drawn as Polygon with 4 sides, not a Circle with Sector

3. **Manim API Errors**
   - Methods that don't exist in Manim CE (hallucinated API)
   - `.move_to()` / `.next_to()` called on empty VGroup() before adding children
   - Wrong argument names for known methods

4. **Coordinate / Layout Issues**
   - Objects clearly placed off-screen (|x| > 6.5 or |y| > 3.8)
   - Double-offset: using both start=/end= AND .move_to() on same Line/Arrow

**math_score rubric (be strict — default to the lower score when in doubt):**
- 5: Every formula, value, geometric shape, and coordinate is mathematically correct.
- 4: One minor imprecision (e.g., approximate value) that does not mislead a student.
- 3: Noticeable error (e.g., wrong fraction region, off-by-one coordinate) that could confuse but concept is still recognizable.
- 2: One critical error that actively teaches incorrect mathematics (wrong formula, wrong shape used).
- 1: Fundamentally wrong — multiple critical errors or the core concept is misrepresented.

**Final answer extraction:**
If a [GROUND TRUTH] block is provided, infer what numerical or short-text answer the
animation will display to the student at the end (e.g., "9", "12 cm", "x = 3", "周長相同時正方形面積最大").
Pull this from MathTex/Text contents, final highlighted values, or the conclusion screen.
If you cannot determine it, set the field to null. Do not invent.

Output ONLY valid JSON, no preamble:
{
  "math_score": <1-5>,
  "math_justification": "...",
  "final_answer_in_video": "<string or null — the answer the animation conveys>",
  "issues": [
    {
      "severity": "Critical" | "Major" | "Minor",
      "category": "MATH_ERROR" | "METAPHOR_MISMATCH" | "API_ERROR" | "LAYOUT_ERROR",
      "description": "what is wrong",
      "line_hint": "approximate code snippet",
      "fix": "how to fix"
    }
  ],
  "summary": "one sentence overall assessment"
}"""

    # ── Visual Judge prompt (GPT-4o) ───────────────────────────────────────
    _VISUAL_JUDGE_SYSTEM = """# ROLE: STRICT MATHEMATICAL ANIMATION CRITIC

You are an uncompromising expert judge for AI-generated math educational animations.
You NEVER rubber-stamp. You actively seek out problems.
A score of 5 means FLAWLESS — only give it when there are truly no issues.

## MANDATORY EVALUATION PROTOCOL (follow IN ORDER):

### Step 1: Frame-by-Frame Inventory
For each of the 4 frames (TL=10%, TR=35%, BL=65%, BR=90%):
- List every visible element (text, shapes, labels, axes)
- Note any overlapping elements
- Note any elements near/outside the canvas edge

### Step 2: Visual Metaphor Audit
For each named visual concept in the Context (e.g., "pizza", "balance scale"):
- Does the shape LOOK LIKE that object WITHOUT relying on labels?
- Would a 10-year-old student recognize it instantly?
- Flag any metaphor that requires a label to be understood.

### Step 3: Code Issue Confirmation
Review the [Code Analysis] section. For each issue found there:
- Can you SEE evidence of that problem in the frames?
- Note which issues are visible vs invisible in the frames.

### Step 4: Score TWO dimensions only (1-5 scale)

**concept_alignment** — Does the animation represent the intended concept visually?
- 5: Perfect. Visual metaphors are immediately recognizable without labels.
- 4: Good alignment, minor ambiguity.
- 3: Concept conveyed but requires labels to understand.
- 2: Visual metaphors are confusing or misleading.
- 1: Animation does not represent the intended concept.

**visual_clarity** — Layout, legibility, absence of overlap/overflow:
- 5: Perfect. No overlaps, nothing off-screen, all text readable.
- 4: Minor imperfection not impeding reading.
- 3: Some cramping or slight overlap but still readable.
- 2: Significant overlap or off-screen elements blocking comprehension.
- 1: Chaotic layout. Cannot parse the visual.

## OUTPUT FORMAT (strict JSON, no other text):
{
  "frame_analysis": "2-3 sentences describing what you see across all 4 frames",
  "metaphor_audit": "assessment of each visual metaphor — does it look like what it claims?",
  "code_confirmation": "which code issues are visible in the frames, which are not",
  "scores": {
    "concept_alignment": {"score": X, "justification": "..."},
    "visual_clarity":    {"score": X, "justification": "..."}
  }
}"""

    def __init__(self, llm_client=None):
        from ..core.llm_client import LLMClient
        self.llm = llm_client if llm_client else LLMClient()

    # ──────────────────────────────────────────────────────────────────────
    # Phase 1: Code Analysis
    # ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def _extract_scene_code(code: str) -> str:
        """
        Extract the GeneratedScene class body from injected code.
        SceneInstrumentor / SubtitleManager boilerplate is prepended by RefiningLoop
        and can push GeneratedScene past the truncation limit.
        Strategy: find 'class GeneratedScene' and take from there.
        Fallback: if not found, return last 6000 chars (scene is likely at the end).
        """
        marker = "class GeneratedScene"
        idx = code.find(marker)
        if idx != -1:
            # Collect import lines before the class using byte-offset tracking
            # (avoids code.find(line) bug when identical import appears twice)
            import_lines = []
            offset = 0
            for line in code[:idx].splitlines(keepends=True):
                if line.lstrip().startswith("from manim") or line.lstrip().startswith("import "):
                    import_lines.append(line.rstrip())
                offset += len(line)
            imports_block = "\n".join(import_lines)
            scene_block = code[idx:]
            combined = imports_block + "\n\n" + scene_block
            # Cap at 8000 chars — enough for any reasonable scene
            return combined[:8000] + ("\n...(truncated)" if len(combined) > 8000 else "")
        # Fallback: last 6000 chars
        if len(code) > 6000:
            return "...(start truncated)\n" + code[-6000:]
        return code

    def _analyze_code(self, code: str, script_context: str, ground_truth: dict = None) -> dict:
        """Phase 1: Claude Sonnet reviews the Manim code."""
        print("🔬 [FinalJudge Phase 1] Code analysis (Claude Sonnet)...")

        _scene_code = self._extract_scene_code(code)
        _ctx = f"\nAnimation context: {str(script_context)[:600]}\n" if script_context else ""

        _gt_block = ""
        if ground_truth:
            _ans = ground_truth.get("answer", "")
            _sol = ground_truth.get("solution", "")
            if _ans or _sol:
                _gt_block = "\n**[GROUND TRUTH — USE THIS TO VERIFY math_score]**\n"
                if _ans:
                    _gt_block += f"Correct answer: {_ans}\n"
                if _sol:
                    _gt_block += f"Solution steps:\n{_sol[:800]}\n"
                _gt_block += "Check whether the code's mathematical steps and final result match the ground truth above.\n"

        user_prompt = f"""{_ctx}{_gt_block}
**Manim Python Code**:
```python
{_scene_code}
```
Review for mathematical and logical correctness. Output JSON only."""

        try:
            raw = self.llm._call_claude_code(
                self._CODE_REVIEW_SYSTEM,
                user_prompt,
            )
        except Exception as e:
            print(f"⚠️ [FinalJudge Phase 1] Claude API error: {e} — math_score unavailable")
            return {
                "math_score": None,
                "math_justification": f"Code review unavailable: {e}",
                "issues": [], "summary": "Code review skipped due to API error.",
                "final_answer_in_video": None,
                "ground_truth_match": None,
            }

        try:
            start = raw.find("{")
            end = raw.rfind("}") + 1
            result = json.loads(raw[start:end])
            result.setdefault("math_score", None)
            result.setdefault("math_justification", "")
            result.setdefault("issues", [])
            result.setdefault("summary", "")
            result.setdefault("final_answer_in_video", None)

            # Ground-truth hard compare (only when GT.answer present and extraction succeeded)
            gt_match = None
            if ground_truth and ground_truth.get("answer") and result["final_answer_in_video"]:
                gt_match = _compare_answer(result["final_answer_in_video"], ground_truth["answer"])
            result["ground_truth_match"] = gt_match

            print(f"🔬 [Phase 1] math_score={result['math_score']} | issues={len(result['issues'])}")
            if result["final_answer_in_video"] is not None:
                _gt_icon = {True: "✅", False: "❌", None: "❓"}[gt_match]
                print(f"  {_gt_icon} extracted_answer={result['final_answer_in_video']!r} (gt_match={gt_match})")
            for iss in result["issues"]:
                sev_icon = {"Critical": "🔴", "Major": "🟠", "Minor": "🟡"}.get(iss.get("severity", ""), "⚪")
                print(f"  {sev_icon} [{iss.get('category')}] {iss.get('description', '')[:80]}")
            return result

        except Exception as e:
            print(f"⚠️ [FinalJudge Phase 1] JSON parse failed: {e}")
            return {"math_score": None, "math_justification": "Parse failed", "issues": [], "summary": "Parse failed"}

    # ──────────────────────────────────────────────────────────────────────
    # Phase 2: Visual Analysis
    # ──────────────────────────────────────────────────────────────────────
    def _extract_frames(self, video_path: str, script_context: str = "") -> str | None:
        """Extract step-based frame grid → base64 string.

        Strategy: infer number of steps from Planner JSON, sample one frame
        per step at ~90% of each step's time window (captures the completed state).
        Fallback to 4 evenly-spaced frames if step count can't be determined.
        Max 6 frames arranged in a grid.
        """
        grid_path = "temp_final_judge_grid.jpg"
        try:
            dur_result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", video_path],
                capture_output=True, text=True, timeout=10
            )
            dur = float(dur_result.stdout.strip())

            # ── Infer step count from Planner JSON ──────────────────────────
            n_steps = 0
            try:
                ctx = script_context if isinstance(script_context, dict) else json.loads(str(script_context))
                # Planner outputs "sequence" as the top-level step array
                steps = ctx.get("sequence") or ctx.get("steps") or ctx.get("animation_steps") or []
                n_steps = len(steps)
            except Exception:
                pass

            MAX_FRAMES = 6
            if n_steps >= 2:
                # One frame per step, sampled at 90% of each step window
                n = min(n_steps, MAX_FRAMES)
                step_dur = dur / n_steps
                timestamps = sorted([
                    step_dur * i + step_dur * 0.90
                    for i in range(n_steps)
                ][:n])
                print(f"📐 [FinalJudge] Step-based sampling: {n_steps} steps → {len(timestamps)} frames")
            else:
                # Fallback: evenly spaced, skip first 5% (often black)
                n = 4
                timestamps = [dur * p for p in [0.15, 0.38, 0.62, 0.88]]
                print(f"📐 [FinalJudge] Fixed sampling (no step info): {len(timestamps)} frames")

            n = len(timestamps)
            # Grid layout: 2 columns
            cols = 2
            rows = (n + 1) // cols
            TILE_W, TILE_H = 640, 360

            inputs = []
            scale_filters = []
            for idx, ts in enumerate(timestamps):
                inputs.extend(["-ss", f"{ts:.2f}", "-i", video_path])
                scale_filters.append(
                    f"[{idx}:v]scale={TILE_W}:{TILE_H},setpts=PTS-STARTPTS[s{idx}]"
                )

            # Pad to even count for xstack
            if n % 2 != 0:
                # Duplicate last frame as padding
                inputs.extend(["-ss", f"{timestamps[-1]:.2f}", "-i", video_path])
                scale_filters.append(
                    f"[{n}:v]scale={TILE_W}:{TILE_H},setpts=PTS-STARTPTS[s{n}]"
                )
                n += 1

            layout = "|".join(
                f"{(k % cols) * TILE_W}_{(k // cols) * TILE_H}" for k in range(n)
            )
            fc = (
                ";".join(scale_filters) + ";"
                + "".join(f"[s{k}]" for k in range(n))
                + f"xstack=inputs={n}:layout={layout}"
            )
            subprocess.run(
                ["ffmpeg", "-y"] + inputs + ["-filter_complex", fc, "-frames:v", "1", grid_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
            )
        except Exception as e:
            print(f"⚠️ [FinalJudge Phase 2] Frame extraction failed: {e}")
            return None

        if not os.path.exists(grid_path):
            return None
        with open(grid_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        os.remove(grid_path)
        return b64

    def _analyze_visual(self, video_path: str, script_context: str, code_analysis: dict) -> dict:
        """Phase 2: GPT-4o analyzes frames with code analysis as context."""
        print("👁️  [FinalJudge Phase 2] Visual analysis (GPT-4o)...")

        b64 = self._extract_frames(video_path, script_context)
        if not b64:
            print("⚠️ [FinalJudge Phase 2] No frames — defaulting to code-only scores")
            return None

        # Format code analysis context for Vision
        _code_issues_text = ""
        if code_analysis.get("issues"):
            _code_issues_text = "\n**[Code Analysis] Issues found by static reviewer:**\n"
            for iss in code_analysis["issues"]:
                _code_issues_text += (
                    f"- [{iss.get('severity')}] {iss.get('category')}: "
                    f"{iss.get('description')} → Fix: {iss.get('fix')}\n"
                )
        else:
            _code_issues_text = "\n**[Code Analysis]**: No issues found in code.\n"

        _code_math = (
            f"\n**[Code Math Score]**: {code_analysis.get('math_score')}/5 — "
            f"{code_analysis.get('math_justification', '')}\n"
        )

        _gt_block = ""
        if hasattr(self, "_ground_truth") and self._ground_truth:
            _ans = self._ground_truth.get("answer", "")
            _sol = self._ground_truth.get("solution", "")
            if _ans or _sol:
                _gt_block = "\n**[GROUND TRUTH]**\n"
                if _ans:
                    _gt_block += f"Correct answer: {_ans}\n"
                if _sol:
                    _gt_block += f"Solution steps: {_sol[:400]}\n"
                _gt_block += "Use this to verify concept_alignment: does the animation show the correct mathematical process?\n"

        user_text = f"""**FINAL QUALITY AUDIT**

**Animation Context** (from Planner):
{str(script_context)[:1000]}
{_gt_block}{_code_issues_text}{_code_math}
**Storyboard**: Each frame captures the completed state of one animation step (sampled at ~90% of each step window). Frames are arranged left-to-right, top-to-bottom in chronological order.

Follow the 4-step protocol in your system prompt.
Output ONLY the JSON object."""

        # ── Self-consistency: n parallel passes, median of scores ───────────
        n_passes = int(os.getenv("LLMANIM_FJ_PASSES", "3"))
        n_passes = max(1, min(n_passes, 5))

        def _single_pass(_idx):
            try:
                content = self.llm.ask_vision(
                    self._VISUAL_JUDGE_SYSTEM, user_text,
                    base64_image=b64, detail="high",
                    max_tokens=2000,
                    temperature=0.5 if n_passes > 1 else 0.1,
                    json_mode=True
                )
                start = content.find("{")
                end = content.rfind("}") + 1
                return json.loads(content[start:end])
            except Exception as _e:
                print(f"⚠️ [FinalJudge Phase 2 pass {_idx}] failed: {_e}")
                return None

        if n_passes == 1:
            results = [_single_pass(0)]
        else:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=n_passes) as ex:
                results = list(ex.map(_single_pass, range(n_passes)))

        valid = [r for r in results if r and "scores" in r]
        # Require at least 2 successful passes for self-consistency mode (n>=2)
        # Otherwise variance is too high; treat as visual-API failure.
        min_required = 2 if n_passes >= 2 else 1
        if len(valid) < min_required:
            print(f"❌ [FinalJudge Phase 2] Only {len(valid)}/{n_passes} passes succeeded — visual unavailable")
            return None

        # Median per-dimension score, attach justification from highest-confidence pass
        def _extract_score(r, dim):
            s = r["scores"].get(dim, {})
            try:
                return int(s.get("score") if isinstance(s, dict) else s)
            except (ValueError, TypeError):
                return None

        def _median(vals):
            vals = sorted(v for v in vals if v is not None)
            if not vals:
                return None
            mid = len(vals) // 2
            return vals[mid] if len(vals) % 2 else (vals[mid - 1] + vals[mid]) // 2

        agg_scores = {}
        for dim in ("concept_alignment", "visual_clarity"):
            dim_scores = [_extract_score(r, dim) for r in valid]
            agg_scores[dim] = {
                "score": _median(dim_scores),
                "justification": " | ".join(
                    str(r["scores"].get(dim, {}).get("justification", ""))[:120]
                    for r in valid if r["scores"].get(dim)
                )[:400],
                "raw_scores": dim_scores,
            }

        # Use first valid pass for textual fields (frame_analysis etc.)
        primary = valid[0]
        consensus_note = f"[{len(valid)}/{n_passes} passes; concept={agg_scores['concept_alignment']['raw_scores']}, clarity={agg_scores['visual_clarity']['raw_scores']}]"
        print(f"\n--- FinalJudge Visual Consensus ---\n{consensus_note}")
        print(f"concept_alignment median = {agg_scores['concept_alignment']['score']}")
        print(f"visual_clarity    median = {agg_scores['visual_clarity']['score']}")
        print("-----------------------------------\n")

        return {
            "scores": agg_scores,
            "frame_analysis": primary.get("frame_analysis", ""),
            "metaphor_audit": primary.get("metaphor_audit", ""),
            "code_confirmation": primary.get("code_confirmation", ""),
            "consensus": consensus_note,
        }

    # ──────────────────────────────────────────────────────────────────────
    # Aggregate
    # ──────────────────────────────────────────────────────────────────────
    def _aggregate(self, code_analysis: dict, visual_result: dict | None,
                   layout_audit: dict | None = None) -> dict:
        """Compute weighted score across all dimensions.

        math_correctness  → Claude code review (sole source of truth)
        concept_alignment → GPT-4o visual frames
        visual_clarity    → GPT-4o visual frames
        spatial_layout    → LayoutAuditor (deterministic from SceneInstrumentor log)
        """
        scores = {}

        # math: Claude is the only judge — None means review was unavailable
        _raw_math = code_analysis.get("math_score")
        scores["math_correctness"] = int(_raw_math) if _raw_math is not None else None

        # spatial_layout: deterministic; None when log unavailable (don't auto-fail)
        if layout_audit and layout_audit.get("score_1_to_5") is not None:
            scores["spatial_layout"] = int(layout_audit["score_1_to_5"])
        else:
            scores["spatial_layout"] = None

        if visual_result and "scores" in visual_result:
            v_scores = visual_result["scores"]
            for dim in ("concept_alignment", "visual_clarity"):
                entry = v_scores.get(dim, {})
                _raw = entry.get("score") if isinstance(entry, dict) else entry
                try:
                    scores[dim] = int(_raw) if _raw is not None else None
                except (ValueError, TypeError):
                    scores[dim] = None
        else:
            # Visual API unavailable — do NOT default to 3 (that silently rewards failures).
            # Mark as None so verdict logic can flag this as ERROR / api_failure.
            scores["concept_alignment"] = None
            scores["visual_clarity"] = None

        # Weighted total — skip dimensions with None score, renormalize weights
        available = {d: scores[d] for d in self.WEIGHTS if scores.get(d) is not None}
        if available:
            total_weight = sum(self.WEIGHTS[d] for d in available)
            weighted = round(sum(scores[d] * self.WEIGHTS[d] / total_weight for d in available), 3)
        else:
            weighted = None

        # ── Verdict decision (hard veto > thresholds > overall score) ────────
        verdict, veto_reason = self._decide_verdict(code_analysis, scores, weighted)

        score_str = " | ".join(f"{d}={scores.get(d, 'N/A')}" for d in self.WEIGHTS)
        print(f"\n{'='*50}")
        print(f"🏛️  [FinalJudge] {score_str}")
        print(f"🏛️  [FinalJudge] Weighted Total: {weighted}")
        print(f"🏛️  [FinalJudge] Verdict: {verdict}" + (f" (reason: {veto_reason})" if veto_reason else ""))
        print(f"{'='*50}\n")

        result = {
            "verdict": verdict,
            "veto_reason": veto_reason,
            "weighted_total": weighted,
            "scores": scores,
            "ground_truth_match": code_analysis.get("ground_truth_match"),
        }

        # Add per-dimension justifications
        if visual_result and "scores" in visual_result:
            result["score_details"] = {
                d: visual_result["scores"].get(d, {}).get("justification", "")
                for d in self.WEIGHTS
            }
            result["frame_analysis"] = visual_result.get("frame_analysis", "")
            result["metaphor_audit"] = visual_result.get("metaphor_audit", "")
            result["code_confirmation"] = visual_result.get("code_confirmation", "")
            result["consensus"] = visual_result.get("consensus", "")

        result["code_issues"] = code_analysis.get("issues", [])
        result["code_summary"] = code_analysis.get("summary", "")
        result["final_answer_in_video"] = code_analysis.get("final_answer_in_video")

        if layout_audit:
            result["layout_audit"] = {
                "verdict":      layout_audit.get("verdict"),
                "score":        layout_audit.get("score_1_to_5"),
                "metrics":      layout_audit.get("metrics", {}),
                "violations":   layout_audit.get("violations", []),
            }

        return result

    def _decide_verdict(self, code_analysis: dict, scores: dict, weighted: float | None) -> tuple[str, str | None]:
        """Return (verdict, veto_reason). veto_reason is None when verdict == PASS."""
        # 1. Critical code issue → instant FAIL (regardless of weighted score)
        for iss in code_analysis.get("issues", []):
            if str(iss.get("severity", "")).lower() == "critical":
                return "FAIL", "critical_code_issue"

        # 2. Ground truth hard mismatch (only fires when comparison was conclusive)
        if code_analysis.get("ground_truth_match") is False:
            return "FAIL", "ground_truth_mismatch"

        # 3. Visual API totally failed → cannot judge → ERROR (not silent PASS)
        if scores.get("concept_alignment") is None and scores.get("visual_clarity") is None:
            return "ERROR", "visual_api_failure"

        # 4. Math review unavailable AND no other strong signal → ERROR
        if scores.get("math_correctness") is None and weighted is None:
            return "ERROR", "all_phases_failed"

        # 5. Any single dimension at or below floor → FAIL (no rescue by other dims)
        for dim, val in scores.items():
            if val is not None and val <= self.DIMENSION_FLOOR:
                return "FAIL", f"low_dimension_{dim}"

        # 6. Overall threshold
        if weighted is None or weighted < self.PASS_THRESHOLD:
            return "FAIL", "below_threshold"

        return "PASS", None

    # ──────────────────────────────────────────────────────────────────────
    # Public entry point
    # ──────────────────────────────────────────────────────────────────────
    def judge(self, video_path: str, script_context: str, code: str,
              ground_truth: dict = None,
              scene_state_log_path: str = None) -> dict:
        """
        Run full multi-phase evaluation.

        Args:
            video_path:           Path to rendered .mp4
            script_context:       Planner JSON string (or dict) describing the animation
            code:                 Generated Manim Python source code
            ground_truth:         Optional dict with keys "answer" and/or "solution"
                                  Used to verify math_correctness against known correct answer
            scene_state_log_path: Optional path to SceneInstrumentor's scene_state_log.json
                                  Used to compute the deterministic `spatial_layout` dimension

        Returns:
            dict with verdict, weighted_total, scores, score_details, code_issues, layout_audit
        """
        print("\n" + "="*50)
        print("🏛️  [FinalJudge] Starting multi-phase quality evaluation")
        if ground_truth:
            print(f"🎯 [FinalJudge] Ground truth provided (answer={bool(ground_truth.get('answer'))}, solution={bool(ground_truth.get('solution'))})")
        if scene_state_log_path:
            print(f"📐 [FinalJudge] Scene-state log provided: {scene_state_log_path}")
        print("="*50)

        # Store ground_truth for use in _analyze_visual
        self._ground_truth = ground_truth

        # Phase 1: Code review
        code_analysis = self._analyze_code(code, script_context, ground_truth=ground_truth)

        # Phase 2: Visual review
        visual_result = self._analyze_visual(video_path, script_context, code_analysis)

        # Phase 3: Layout audit (deterministic, ~10ms, $0)
        layout_audit = None
        if scene_state_log_path:
            try:
                from .layout_auditor import LayoutAuditor
                layout_audit = LayoutAuditor().audit(scene_state_log_path)
                _ls = layout_audit.get("score_1_to_5")
                _v = layout_audit.get("verdict")
                _vio = len(layout_audit.get("violations", []))
                print(f"📐 [FinalJudge Phase 3] Layout {_v} | score={_ls} | violations={_vio}")
            except Exception as e:
                print(f"⚠️ [FinalJudge Phase 3] Layout audit failed: {e}")

        # Aggregate
        return self._aggregate(code_analysis, visual_result, layout_audit)
