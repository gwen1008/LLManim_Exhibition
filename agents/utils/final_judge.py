"""
FinalJudge — Post-render rubric-based quality evaluator.

Two-phase evaluation:
  Phase 1: Claude Opus 4.7 (via Claude Code CLI subscription) reads the generated Python code
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

    # ── Code Reviewer prompt (Claude Opus 4.7 via CLI subscription) ───────
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

**Expected visual events extraction (CRITICAL — used by vision check-list):**
Identify 3-7 *concrete, screen-visible* events that this animation should produce.
Each event must be a thing a human can confirm by looking at a frame WITHOUT reading code.

Good event examples:
- "A red Circle appears in the upper-left quadrant"
- "Two MathTex equations '1/2' and '2/4' shown side by side"
- "A blue Arrow connects the left and right shapes"
- "A right-angle marker (small square) drawn at vertex B"

Bad event examples (DO NOT EMIT — too abstract or narrative):
- "The concept of fractions is explained" (no visual to verify)
- "Student understands division" (judgement, not observable)
- "Voiceover mentions PI" (audio, not visual)
- "Wait 2 seconds" (no visual content)

Each event has a weight 1.0 (mandatory) or 0.5 (nice-to-have).
Limit to events that are actually rendered (Mobject construction + .play() / .add() / .show()).

Output ONLY valid JSON, no preamble:
{
  "math_score": <1-5>,
  "math_justification": "...",
  "final_answer_in_video": "<string or null — the answer the animation conveys>",
  "expected_visual_events": [
    {"id": "E1", "description": "...", "weight": 1.0}
  ],
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

    # ── Visual Judge prompt (event-checklist + visual_clarity) ─────────────
    _VISUAL_JUDGE_SYSTEM = """# ROLE: STRICT VISUAL FACT-CHECKER FOR MATH ANIMATION

You are checking whether an AI-generated math animation actually shows the
expected visual events. You do NOT score "concept alignment" holistically —
instead you check off each event one-by-one and answer YES/NO based ONLY on
what you can SEE in the frames.

You will receive a 2×N grid of frames (one row × multiple columns OR a 2-row
grid; each tile is a snapshot at a different timestamp of the same video) and
a list of EXPECTED VISUAL EVENTS extracted from the code.

## PROTOCOL (follow strictly):

### Step 1: Frame inventory
Briefly list every visible element across the grid (shapes, text, axes,
arrows). One short paragraph.

### Step 2: Per-event check
For EACH event in [EXPECTED EVENTS], decide:
  - present = 1 if you can SEE the event in any of the frames
  - present = 0 if the event is missing, wrong, or only inferable from labels
Be conservative: when uncertain, output 0.
Include a 1-line `evidence` field citing the frame (TL/TR/BL/BR) and what you saw.

### Step 3: Score visual_clarity ONLY (1-5)
This score is independent of the event check. Judges layout/legibility:
- 5: No overlaps, nothing off-screen, all text readable
- 4: Minor imperfection not impeding reading
- 3: Some cramping or slight overlap but still readable
- 2: Significant overlap or off-screen elements
- 1: Chaotic layout — cannot parse

## OUTPUT FORMAT (strict JSON, no other text):
{
  "frame_inventory": "one short paragraph",
  "event_checks": [
    {"id": "E1", "present": 0|1, "evidence": "..."},
    {"id": "E2", "present": 0|1, "evidence": "..."}
    /* one entry per expected event, in same order */
  ],
  "visual_clarity": {"score": <1-5>, "justification": "..."}
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
        """Phase 1: Claude Opus reviews the Manim code."""
        print("🔬 [FinalJudge Phase 1] Code analysis (Claude Opus)...")

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
            # Sanitize expected_visual_events: drop entries without description,
            # auto-assign IDs and clamp weights.
            _raw_events = result.get("expected_visual_events") or []
            _events = []
            for i, ev in enumerate(_raw_events, 1):
                if not isinstance(ev, dict):
                    continue
                desc = str(ev.get("description", "")).strip()
                if not desc:
                    continue
                try:
                    w = float(ev.get("weight", 1.0))
                except (ValueError, TypeError):
                    w = 1.0
                w = max(0.0, min(1.0, w))
                _events.append({
                    "id":          str(ev.get("id") or f"E{i}"),
                    "description": desc,
                    "weight":      w,
                })
            result["expected_visual_events"] = _events

            # Ground-truth hard compare (only when GT.answer present and extraction succeeded)
            gt_match = None
            if ground_truth and ground_truth.get("answer") and result["final_answer_in_video"]:
                gt_match = _compare_answer(result["final_answer_in_video"], ground_truth["answer"])
            result["ground_truth_match"] = gt_match

            print(f"🔬 [Phase 1] math_score={result['math_score']} | issues={len(result['issues'])} | events={len(result['expected_visual_events'])}")
            for ev in result["expected_visual_events"]:
                print(f"  · [{ev['id']} w={ev['weight']:.1f}] {ev['description'][:70]}")
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
    def _extract_frames(self, video_path: str, script_context: str = "",
                        keep_file: bool = False) -> tuple[str | None, str | None]:
        """Extract step-based frame grid.

        Strategy: infer number of steps from Planner JSON, sample one frame
        per step at ~90% of each step's time window (captures the completed state).
        Fallback to 4 evenly-spaced frames if step count can't be determined.
        Max 6 frames arranged in a grid.

        Returns:
            (base64_string, file_path) — both may be None on failure.
            file_path is removed unless keep_file=True (Opus backend needs the
            file on disk for Claude's Read tool).
        """
        # Write to /tmp (world-readable by default on macOS) so the Opus backend
        # — which runs as a different user via `sudo -u claudealt` — can Read
        # the file. The default tempfile.gettempdir() under /var/folders/... has
        # mode 0o700 and would block cross-user access (EACCES).
        import tempfile as _tempfile
        _fd, grid_path = _tempfile.mkstemp(prefix="fj_grid_", suffix=".jpg", dir="/tmp")
        os.close(_fd)
        os.chmod(grid_path, 0o644)
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
            try:
                os.remove(grid_path)
            except OSError:
                pass
            return None, None

        if not os.path.exists(grid_path):
            return None, None
        with open(grid_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        if not keep_file:
            os.remove(grid_path)
            return b64, None
        return b64, grid_path

    def _analyze_visual(self, video_path: str, script_context: str, code_analysis: dict) -> dict:
        """Phase 2: Vision model checks events + visual_clarity.

        Backend selectable via env var FJ_VISION_BACKEND:
          - "gpt4o" (default): OpenAI GPT-4o via base64 image
          - "opus":             Claude Opus via Claude Code CLI Read tool
        """
        backend = os.getenv("FJ_VISION_BACKEND", "gpt4o").strip().lower()
        backend_label = {"gpt4o": "GPT-4o", "opus": "Claude Opus"}.get(backend, backend)
        print(f"👁️  [FinalJudge Phase 2] Visual analysis ({backend_label})...")

        keep_file = (backend == "opus")
        b64, grid_path = self._extract_frames(video_path, script_context, keep_file=keep_file)
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

        # ── Build [EXPECTED EVENTS] block from code analysis ────────────────
        events = code_analysis.get("expected_visual_events") or []
        if events:
            _events_text = "\n**[EXPECTED EVENTS — check each one]**\n"
            for ev in events:
                _events_text += f"- {ev['id']} (weight {ev['weight']:.1f}): {ev['description']}\n"
        else:
            _events_text = ""

        user_text = f"""**FINAL QUALITY AUDIT**

**Animation Context** (from Planner):
{str(script_context)[:800]}
{_gt_block}{_code_issues_text}{_code_math}{_events_text}
**Storyboard**: Each frame captures the completed state of one animation step (sampled at ~90% of each step window). Frames are arranged left-to-right, top-to-bottom in chronological order.

Follow the protocol in your system prompt. Output ONLY the JSON object."""

        # ── Self-consistency: n parallel passes ─────────────────────────────
        n_passes = int(os.getenv("LLMANIM_FJ_PASSES", "3"))
        n_passes = max(1, min(n_passes, 5))

        def _gpt4o_pass(_idx):
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

        def _opus_pass(_idx):
            # Opus reads the grid image via Claude Code CLI's Read tool.
            # Pattern mirrors agents/utils/pairwise_judge.py::_call_opus_read.
            import shutil as _shutil, time as _time, subprocess as _sp
            claude_bin = (
                os.getenv("CLAUDE_BIN")
                or _shutil.which("claude")
                or "/Users/liaozhenting/.local/bin/claude"
            )
            run_as = os.getenv("CLAUDE_RUN_AS_USER", "claudealt")
            model  = os.getenv("FJ_OPUS_MODEL", "claude-opus-4-7")
            grid_abs = os.path.abspath(grid_path)
            opus_prompt = (
                f"{user_text}\n\n"
                f"The frame grid is at: {grid_abs}\n"
                f"Use the Read tool to view the image before answering. "
                f"Then output ONLY the JSON described in your system prompt."
            )
            cmd_inner = [
                claude_bin, "-p", opus_prompt.strip(),
                "--model", model,
                "--output-format", "json",
                "--no-session-persistence",
                "--tools", "Read",
                "--add-dir", os.path.dirname(grid_abs),
                "--system-prompt", self._VISUAL_JUDGE_SYSTEM,
                "--strict-mcp-config",
                "--disable-slash-commands",
            ]
            cmd = (["sudo", "-u", run_as, "-i"] + cmd_inner) if run_as else cmd_inner
            try:
                t0 = _time.time()
                r = _sp.run(cmd, capture_output=True, text=True, timeout=300)
                elapsed = _time.time() - t0
                if r.returncode != 0:
                    print(f"⚠️ [FinalJudge Phase 2 pass {_idx}] Opus CLI rc={r.returncode}: {r.stderr.strip()[-300:]}")
                    return None
                data = json.loads(r.stdout)
                usage = data.get("usage", {}) or {}
                in_tok = (usage.get("input_tokens", 0)
                          + usage.get("cache_read_input_tokens", 0)
                          + usage.get("cache_creation_input_tokens", 0))
                out_tok = usage.get("output_tokens", 0)
                try:
                    self.llm._update_stats(f"anthropic/{model}", in_tok, out_tok)
                except Exception:
                    pass
                print(f"  [pass {_idx}] Opus {elapsed:.1f}s in={in_tok} out={out_tok}")
                raw = data.get("result", "")
                s, e = raw.find("{"), raw.rfind("}") + 1
                if s == -1 or e <= 0:
                    print(f"⚠️ [FinalJudge Phase 2 pass {_idx}] no JSON in Opus output")
                    return None
                return json.loads(raw[s:e])
            except Exception as _e:
                print(f"⚠️ [FinalJudge Phase 2 pass {_idx}] Opus failed: {_e}")
                return None

        _single_pass = _opus_pass if backend == "opus" else _gpt4o_pass

        if n_passes == 1:
            results = [_single_pass(0)]
        else:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=n_passes) as ex:
                results = list(ex.map(_single_pass, range(n_passes)))

        # Cleanup Opus grid file
        if grid_path and os.path.exists(grid_path):
            try:
                os.remove(grid_path)
            except OSError:
                pass

        valid = [r for r in results if r and ("event_checks" in r or "visual_clarity" in r)]
        min_required = 2 if n_passes >= 2 else 1
        if len(valid) < min_required:
            print(f"❌ [FinalJudge Phase 2] Only {len(valid)}/{n_passes} passes succeeded — visual unavailable")
            return None

        # ── Per-event majority vote ─────────────────────────────────────────
        # For each expected event id, gather present votes across passes; >= ceil(n/2)
        # of present=1 means that event is considered confirmed.
        event_id_to_meta = {ev["id"]: ev for ev in events}
        event_votes = {ev["id"]: [] for ev in events}
        event_evidence = {ev["id"]: [] for ev in events}
        for r in valid:
            for chk in r.get("event_checks") or []:
                eid = str(chk.get("id", "")).strip()
                if eid not in event_votes:
                    continue
                try:
                    p = int(chk.get("present", 0))
                except (ValueError, TypeError):
                    p = 0
                event_votes[eid].append(1 if p else 0)
                ev_text = str(chk.get("evidence", "")).strip()
                if ev_text:
                    event_evidence[eid].append(ev_text[:100])

        # Confirmed events: per-event majority (>= ceil(votes/2)).
        confirmed = {}
        for eid, votes in event_votes.items():
            if not votes:
                confirmed[eid] = 0  # event never voted on → treat as missing
                continue
            need = (len(votes) + 1) // 2
            confirmed[eid] = 1 if sum(votes) >= need else 0

        # Alignment = Σ w·p / Σ w
        if events:
            total_w = sum(ev["weight"] for ev in events) or 1.0
            alignment = sum(event_id_to_meta[eid]["weight"] * p for eid, p in confirmed.items()) / total_w
        else:
            alignment = None

        # ── Map alignment → 1-5 concept_alignment with concave curve ─────────
        # score = round(1 + 4 * alignment^1.5)  →  alignment=1.0 → 5, 0.9 → 4, 0.7 → 3
        # Hard cap: 5 only if alignment == 1.0 AND #events >= 3 (prevents 1-event saturation)
        if alignment is None:
            concept_score = None
        else:
            raw = 1 + 4 * (alignment ** 1.5)
            concept_score = int(round(raw))
            if concept_score == 5 and (alignment < 0.999 or len(events) < 3):
                concept_score = 4
            concept_score = max(1, min(5, concept_score))

        # ── visual_clarity: median of per-pass scores (unchanged dim) ───────
        def _extract_clarity(r):
            s = r.get("visual_clarity") or {}
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

        clarity_raw = [_extract_clarity(r) for r in valid]
        clarity_score = _median(clarity_raw)

        # ── Build aggregated dict in same shape as old code ─────────────────
        agg_scores = {
            "concept_alignment": {
                "score": concept_score,
                "justification": (
                    f"event-checklist: {sum(confirmed.values())}/{len(events)} events confirmed "
                    f"(alignment={alignment:.2f})" if events else "no events"
                ),
                "raw_alignment": alignment,
                "event_votes": event_votes,
                "event_confirmed": confirmed,
            },
            "visual_clarity": {
                "score": clarity_score,
                "justification": " | ".join(
                    str((r.get("visual_clarity") or {}).get("justification", ""))[:120]
                    for r in valid
                )[:400],
                "raw_scores": clarity_raw,
            },
        }

        primary = valid[0]
        consensus_note = (
            f"[{len(valid)}/{n_passes} passes; events={sum(confirmed.values())}/{len(events)} "
            f"confirmed → concept={concept_score}; clarity={clarity_raw} → median={clarity_score}]"
        )
        print(f"\n--- FinalJudge Visual Consensus ---\n{consensus_note}")
        for eid in event_votes:
            votes = event_votes[eid]
            mark = "✅" if confirmed[eid] else "❌"
            desc = event_id_to_meta[eid]["description"][:60]
            print(f"  {mark} {eid} votes={votes} — {desc}")
        print(f"concept_alignment = {concept_score} (alignment={alignment})")
        print(f"visual_clarity    = {clarity_score}")
        print("-----------------------------------\n")

        return {
            "scores": agg_scores,
            "frame_inventory": primary.get("frame_inventory", ""),
            "consensus": consensus_note,
            "alignment_value": alignment,
            "events_total": len(events),
            "events_confirmed": sum(confirmed.values()) if events else 0,
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
            result["frame_inventory"]    = visual_result.get("frame_inventory", "")
            result["alignment_value"]    = visual_result.get("alignment_value")
            result["events_total"]       = visual_result.get("events_total", 0)
            result["events_confirmed"]   = visual_result.get("events_confirmed", 0)
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
