# agents/orchestrator/refining_loop.py
import os
import time
import shutil
import subprocess
import json
import re
import tempfile
import hashlib
from ..coder.diagnoser import ManimDiagnoser
from ..coder.prompter import VisualFixPrompter
from ..coder.lint_manim import lint_file
from ..coder.misalign_fixer import MisalignmentRouter
from ..utils.vision_agent import VisionAgent
from ..utils.audio_engine import AudioEngine
from ..core.llm_client import LLMClient, LLMError
from ..core.rag_retriever import RAGRetriever
from ..core.pipeline_config import CFG
from utils.patcher import apply_patch_block

# ─────────────────────────────────────────────────────────────────────
# Shared Reflexion JSON schema (used in all 3 failure paths to avoid duplication)
# ─────────────────────────────────────────────────────────────────────
_REFLEXION_JSON_SCHEMA = """
Output a STRICT JSON object (no other text). Schema:
{{
  "score": 0,                   // 0-100 confidence score that this fix will solve the problem
  "has_issues": true,           // boolean flag, true if there is an error to fix
  "error_type": "<VISUAL|RENDER_ERROR|STATIC_OR_SEMANTIC_ERROR>",
  "bad_code":   "Exact snippet from the original code that caused the problem",
  "good_code_plan": "Pseudo-code or conceptual mapping for the fix",
  "good_code":  "Corrected snippet that fixes it",
  "rationale":  "Rubber-Duck Debugging: explain EXACTLY why the traceback or visual feedback occurred in plain English step-by-step."
}}"""

_SUBTITLE_MANAGER_SNIPPET = '''\
class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Prevents subtitle overlap and implements YT-style chunking."""
    MAX_WIDTH = 12.5

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None
        self._y = 3.2 * DOWN

    def show(self, text_str, run_time=1.0):
        import re
        FADE_IN = 0.10
        FADE_BETWEEN = 0.08

        # Break text into chunks by punctuation (keeping the punctuation)
        parts = re.split(r'([，。！？,\.!?]+)', str(text_str))
        sentences = []
        for i in range(0, len(parts)-1, 2):
            sentences.append((parts[i] + parts[i+1]).strip())
        if len(parts) % 2 == 1 and parts[-1].strip():
            sentences.append(parts[-1].strip())

        # 過濾空字串，確保 is_last 判斷正確
        sentences = [s for s in sentences if s]
        if not sentences:
            return

        total_len = sum(len(s) for s in sentences)
        n = len(sentences)

        # run_time = 字幕總存活時間（= TTS 時長），字幕要撐滿這段時間
        time_cursor = 0.0

        for idx, s in enumerate(sentences):

            text_mob = Text(s, font_size=self.font_size, color=WHITE, weight="BOLD")
            bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
            new_mob = VGroup(bg, text_mob).move_to(self._y)
            if new_mob.width > self.MAX_WIDTH:
                new_mob.scale_to_fit_width(self.MAX_WIDTH)

            is_last = (idx == n - 1)

            if self._current is None:
                self.scene.play(FadeIn(new_mob), run_time=FADE_IN)
                time_cursor += FADE_IN
            else:
                self.scene.play(
                    FadeOut(self._current, run_time=FADE_BETWEEN / 2),
                    FadeIn(new_mob, run_time=FADE_BETWEEN / 2),
                )
                time_cursor += FADE_BETWEEN

            self._current = new_mob

            if not is_last:
                # 按字數比例分配時間給非最後一句
                chunk_ratio = len(s) / max(1, total_len)
                hold = run_time * chunk_ratio - (FADE_IN if idx == 0 else FADE_BETWEEN)
                if hold > 0:
                    self.scene.wait(hold)
                    time_cursor += hold
            else:
                # 最後一句：把剩餘時間全用掉，確保字幕撐到 TTS 結束
                remaining = run_time - time_cursor
                if remaining > 0:
                    self.scene.wait(remaining)

    def clear(self, run_time=0.5):
        if self._current is not None:
            anim_time = min(0.2, run_time)
            self.scene.play(FadeOut(self._current), run_time=anim_time)
            if run_time > anim_time:
                self.scene.wait(run_time - anim_time)
            self._current = None
'''

_INSTRUMENTOR_SNIPPET = '''\
class SceneInstrumentor:
    """Auto-injected by RefiningLoop.pre_render_patch to quantitatively track object overlap."""
    def __init__(self, scene, log_path="scene_state_log.json"):
        import json
        self._scene = scene
        self._log_path = log_path
        self._log = []
        self._step = 0
        self._original_play = scene.play
        scene.play = self._instrumented_play

    def _instrumented_play(self, *anims, **kwargs):
        result = self._original_play(*anims, **kwargs)
        self._step += 1
        snapshot = {"step": self._step, "mobjects": []}

        for mob in getattr(self._scene, "mobjects", []):
            # Manim v0.20.0: __getattr__ wraps deprecated getters, making hasattr() unreliable.
            # get_fill_opacity() may raise AttributeError or return None on internal mobjects.
            # Use try/except + (val or 0) to handle both cases robustly.
            try:
                opacity = (mob.get_fill_opacity() or 0) + (mob.get_stroke_opacity() or 0)
            except Exception:
                opacity = 1.0  # assume visible if opacity cannot be determined
                 
            if opacity <= 0.01 or type(mob).__name__ == "BackgroundRectangle":
                continue
            try:
                w, h = mob.width, mob.height
                if w * h < 0.05: continue
                c = mob.get_center().tolist()
                snapshot["mobjects"].append({
                    "type": type(mob).__name__, "width": round(w, 3), "height": round(h, 3),
                    "center": [round(c[0], 3), round(c[1], 3), round(c[2], 3)], "area": round(w * h, 3)
                })
            except Exception: pass
            
        snapshot["n_mobjects_visible"] = len(snapshot["mobjects"])
        oc = 0
        mobs = snapshot["mobjects"]
        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                m1, m2 = mobs[i], mobs[j]
                ho = (abs(m1["center"][0] - m2["center"][0]) * 2 < (m1["width"] + m2["width"]))
                vo = (abs(m1["center"][1] - m2["center"][1]) * 2 < (m1["height"] + m2["height"]))
                if ho and vo: oc += 1
                
        snapshot["overlap_pairs"] = oc
        snapshot["total_screen_coverage"] = sum(m["area"] for m in mobs)
        self._log.append(snapshot)
        
        try:
            import json
            with open(self._log_path, "w", encoding="utf-8") as f:
                json.dump({
                    "max_simultaneous_objects": max((s["n_mobjects_visible"] for s in self._log), default=0),
                    "max_overlap_pairs": max((s["overlap_pairs"] for s in self._log), default=0),
                    "steps_with_overlap": sum(1 for s in self._log if s["overlap_pairs"] > 0),
                    "peak_screen_coverage": max((s["total_screen_coverage"] for s in self._log), default=0),
                    "timeline": self._log
                }, f, indent=2)
        except Exception: pass
        return result
'''


class RefiningLoop:
    @staticmethod
    def strip_injected_snippets(code: str) -> str:
        """Strip auto-injected SubtitleManager/SceneInstrumentor classes and their init lines.

        Called before sending code back to LLM for reflexion, so the model never sees
        these infrastructure classes and won't attempt to reproduce/compress them
        (which causes try=/except Exception= syntax corruption).
        """
        # Remove the full class definitions (they start with the class docstring marker)
        code = re.sub(
            r'^class SubtitleManager:.*?(?=\nclass |\n[^ \n])',
            '', code, count=1, flags=re.DOTALL | re.MULTILINE
        )
        code = re.sub(
            r'^class SceneInstrumentor:.*?(?=\nclass |\n[^ \n])',
            '', code, count=1, flags=re.DOTALL | re.MULTILINE
        )
        # Remove the init lines injected into construct()
        code = re.sub(r'^[ \t]*self\._sm = SubtitleManager\(self\)\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'^[ \t]*self\.set_subtitle = self\._sm\.show\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'^[ \t]*self\._instrumentor = SceneInstrumentor\(self.*\)\n', '', code, flags=re.MULTILINE)
        # Clean up excess blank lines left behind
        code = re.sub(r'\n{3,}', '\n\n', code)
        return code.strip() + '\n'

    @staticmethod
    def _extract_reflection_from_response(response: str) -> tuple[str, dict|None]:
        """從合併回覆中分離 reflection JSON 和代碼。"""
        match = re.search(r'<reflection>(.*?)</reflection>', response, re.DOTALL)
        reflection = None
        if match:
            try:
                reflection = json.loads(match.group(1).strip())
            except: pass
            response = response[:match.start()] + response[match.end():]
        return response.strip(), reflection

    @staticmethod
    def _extract_first_json_object(text: str):
        """從可能含前後文的字串中，以括號匹配擷取第一個完整 JSON 物件。"""
        i = text.find("{")
        if i == -1:
            return None
        depth = 0
        for j, c in enumerate(text[i:], start=i):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[i : j + 1]
        return None

    @staticmethod
    def run_manim_task(file_path, scene_name, fps: int = 15):
        """
        執行 Manim 指令並捕獲輸出。

        Args:
            fps: 渲染幀率。15 = 正常品質；10 = 快速預覽模式（Vision QA 結果相同）。
                 解析度固定 480p (-ql)，Vision Agent 不感知 fps 差異。
        """
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"📄 [Debug] 準備渲染檔案: {file_path} (大小: {size} bytes)")
            if size == 0:
                return False, "錯誤：渲染目標檔案為空 (0 bytes)"
        else:
            return False, f"錯誤：找不到檔案 {file_path}"

        fps_label = f"{fps}fps" if fps != 15 else "標準"
        print(f"🚀 正在啟動 Manim 引擎進行渲染 ({fps_label})...")
        cmd = ["manim", "-v", "ERROR", "-ql", "--fps", str(fps), file_path, scene_name]
        # [Parallel Eval Fix] If running under eval worker, isolate Manim's media output
        # to the worker's tmpdir so concurrent renders don't overwrite each other's videos.
        _eval_dir = os.environ.get("EVAL_OUTPUT_DIR")
        if _eval_dir:
            _media_dir = os.path.join(_eval_dir, "media")
            os.makedirs(_media_dir, exist_ok=True)
            cmd += ["--media_dir", _media_dir]

        try:
            # [HOTFIX] Added a 120-second timeout to prevent infinite loops (like `always_redraw` bugs or while loops)
            # from hanging the entire evaluation process.
            _r_start = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=CFG.render_timeout_sec)
            _r_dur = time.time() - _r_start
            
            if result.returncode == 0:
                return True, result.stdout, _r_dur
            else:
                # Manim routes LaTeX error details (! Undefined control sequence, etc.)
                # to stdout via print_all_tex_errors(), not stderr. Combine both so LLM
                # sees the actual LaTeX failure reason instead of just the generic wrapper.
                combined_error = result.stderr
                if result.stdout:
                    combined_error = result.stdout + "\n" + combined_error

                # If it's a latex→dvi error, also try to read the .log file Manim leaves behind.
                # The .log contains the full LaTeX compiler output with line/column info.
                if "latex error converting to" in combined_error:
                    import re as _re
                    log_match = _re.search(r'the log file:\s*(\S+\.log)', combined_error)
                    if log_match:
                        tex_log_path = log_match.group(1)
                        try:
                            with open(tex_log_path, "r", encoding="utf-8", errors="replace") as _f:
                                tex_log_raw = _f.read()
                            # Extract the relevant error section (lines starting with !)
                            error_lines = [
                                l for l in tex_log_raw.splitlines()
                                if l.startswith("!") or l.startswith("l.") or "Undefined" in l or "Missing" in l or "Emergency" in l
                            ]
                            if error_lines:
                                latex_detail = "\n".join(error_lines[:30])
                                combined_error += f"\n\n[LaTeX Compiler Output]:\n{latex_detail}"
                        except (OSError, IOError):
                            pass  # log file may have been cleaned up, not critical

                return False, combined_error
        except subprocess.TimeoutExpired:
            error_msg = (
                f"Render Error: Manim process timed out after {CFG.render_timeout_sec} seconds.\n"
                "ROOT CAUSE: Almost certainly add_updater(lambda m: m.become(...)) "
                "rebuilding a complex object (ParametricFunction, DashedLine, MathTex) every frame.\n"
                "MANDATORY FIX — Replace ALL add_updater+become with always_redraw:\n"
                "  REMOVE: obj.add_updater(lambda m: m.become(HeavyObject(...)))\n"
                "  REPLACE:\n"
                "    tracker = ValueTracker(0)\n"
                "    obj = always_redraw(lambda: HeavyObject(...))\n"
                "    self.add(obj)\n"
                "    self.play(tracker.animate.set_value(TARGET), run_time=N, rate_func=linear)\n"
                "Search your code for ALL .add_updater( calls where the lambda contains .become(). "
                "Replace every one. See MANIM_API_RULES Rule 7."
            )
            return False, error_msg
        except FileNotFoundError:
            return False, "錯誤：找不到 'manim' 指令。請確保已安裝 Manim 且路徑正確。"

    @staticmethod
    def _truncate_error(message, max_chars=6000):
        """Sandwich truncation: preserve head (File/line info) + tail (Exception type).
        
        A plain tail-only truncation drops 'File "x.py", line N' context when
        tracebacks exceed 2000 chars. We keep 300 chars of head and 1680 chars
        of tail so both the error location and the exception class are visible.
        """
        if len(message) <= max_chars:
            return message
        head = message[:300]
        tail_size = max_chars - 300 - 20  # 20 chars for the separator line
        tail = message[-tail_size:]
        skipped = len(message) - max_chars
        return f"{head}\n... ({skipped} chars truncated) ...\n{tail}"

    @staticmethod
    def _dedup_reflection(memory: list, new_entry) -> bool:
        """回傳 True = 已存在相同簽名，跳過 append。"""
        if not isinstance(new_entry, dict):
            return False
        import difflib
        new_err = new_entry.get("error_type", "")
        new_code = new_entry.get("bad_code", "")
        for existing in memory:
            if isinstance(existing, dict):
                if new_err == existing.get("error_type", ""):
                    ratio = difflib.SequenceMatcher(None, new_code, existing.get("bad_code", "")).ratio()
                    if ratio > 0.7:
                        return True
        return False

    @staticmethod
    def _render_memory_entry(idx: int, entry) -> str:
        """將單條 reflection memory 格式化為字串（供預算計算使用）。"""
        if isinstance(entry, dict):
            bad_code = entry.get('bad_code', 'N/A')
            # [Improvement] bad_code truncated to 80 chars: just enough to identify the anti-pattern.
            # The Coder doesn't need to re-read the full bad snippet; rationale + good_code are what matter.
            bad_code_truncated = bad_code if len(bad_code) <= 80 else bad_code[:80] + "... (see rationale)"
            good_code = entry.get('good_code', 'N/A')
            # good_code stays at 500 — Coder needs enough context to copy-adapt it
            good_code_truncated = good_code if len(good_code) <= 500 else good_code[:500] + "... (truncated)"
            return (
                f"[{idx}] ⛔ ERROR TYPE: {entry.get('error_type', 'Unknown')}\n"
                f"    ❌ BAD CODE (DO NOT USE): {bad_code_truncated}\n"
                f"    ✅ GOOD CODE (USE THIS INSTEAD):\n    {good_code_truncated.replace(chr(10), chr(10)+'    ')}\n"
                f"    🧠 RATIONALE: {entry.get('rationale', 'N/A')}\n\n"
            )
        else:
            return f"[{idx}] {entry}\n\n"

    @staticmethod
    def _format_reflection_memory(reflection_memory, budget_chars=2000, max_entries=3):
        """
        格式化反思記憶以注入到 LLM prompt 中。
        結合 Sliding Window (Omega=3) 與 Token 預算制：
        從最新記憶往舊的填入，最多 3 筆，且不超過 budget_chars。
        """
        if not reflection_memory:
            return ""

        header = (
            "\n" + "="*60 + "\n"
            "📚 **PAST LESSONS LEARNED** (Reflexion Memory)\n"
            + "="*60 + "\n"
            "The following are lessons from PREVIOUS FAILED attempts.\n"
            "STRICTLY AVOID making the same mistakes:\n\n"
        )
        footer = "="*60 + "\n"

        # Fill from newest → oldest, stop when budget or max_entries exceeded
        selected = []
        used_chars = len(header) + len(footer)
        for entry in reversed(reflection_memory):
            if len(selected) >= max_entries:
                break
            rendered = RefiningLoop._render_memory_entry(len(selected) + 1, entry)
            if used_chars + len(rendered) > budget_chars:
                break
            selected.append(rendered)
            used_chars += len(rendered)

        if not selected:
            return ""

        # Re-number in chronological order (oldest first)
        selected.reverse()
        body = "".join(
            RefiningLoop._render_memory_entry(idx + 1, entry)
            for idx, entry in enumerate(
                # recover original entries for proper re-numbering
                reflection_memory[-(len(selected)):]
            )
        )
        return header + body + footer

    @staticmethod
    def pre_render_patch(code: str, log_path: str = None, scene_name: str = None, script_json: dict = None) -> str:
        """
        [Shift-Left Auto-Repair] Applies deterministic, zero-cost fixes before rendering.
        Eliminates wasting 10-15s engine spin-up for trivial deprecated API or structural issues.
        """
        import re
        import ast
        patched = code

        # 0a. [Import Guarantee] Ensure `from manim import *` is always present.
        # LLM occasionally omits it, causing immediate ImportError at render time.
        if 'from manim import' not in patched and 'import manim' not in patched:
            patched = 'from manim import *\n' + patched
            print("🔧 [Shift-Left] Added missing 'from manim import *'")

        # 0b. [Class Name Normalization] Ensure Scene subclass name matches scene_name.
        # Prevents CLASS_NOT_FOUND errors when Coder uses a different name than Planner specified.
        if scene_name:
            _cls_pattern = r'class\s+(\w+)\s*\(\s*(?:MovingCamera|ThreeD|Zoomed|Vector)?Scene\s*\)'
            _cls_match = re.search(_cls_pattern, patched)
            if _cls_match and _cls_match.group(1) != scene_name:
                _old_name = _cls_match.group(1)
                patched = re.sub(
                    rf'(?<!\w){re.escape(_old_name)}(?!\w)',
                    scene_name,
                    patched,
                    count=1
                )
                print(f"🔧 [Shift-Left] Class name normalized: {_old_name} → {scene_name}")

        # 1. Fix get_graph -> plot
        patched = patched.replace(".get_graph(", ".plot(")
        patched = patched.replace(".get_lines()", ".get_vertices()")
        
        # 2. Fix non-existent light/dark color names
        color_replacements = {
            "LIGHT_BLUE": "BLUE_C", "DARK_BLUE": "BLUE_E",
            "LIGHT_GREEN": "GREEN_C", "DARK_GREEN": "GREEN_E",
            "LIGHT_RED": "RED_C", "DARK_RED": "RED_E",
            "LIGHT_GRAY": "GRAY_C", "DARK_GRAY": "GRAY_E",
            "LIGHT_PINK": "PINK",
        }
        for bad_color, good_color in color_replacements.items():
            patched = patched.replace(bad_color, good_color)
            
        # 3. Fix Python 3.10+ type union syntax (X | Y)
        # Strip return type annotations: def foo() -> int | None:  →  def foo():
        if " | " in patched and ("->" in patched or ": " in patched):
            patched = re.sub(r'\)\s*->\s*[^:]+:', '):', patched)
            # Strip param type annotations: (x: int | None, y: str = "a")  →  (x, y = "a")
            patched = re.sub(r'(\w+)\s*:\s*(?:[\w\[\], |]+)(\s*[=,)])', r'\1\2', patched)
        
        # 4. Strip \mathrm{} and \text{} — keep content, remove command.
        # Both commands crash Manim v0.19/v0.20 with "Missing } inserted" (LaTeX brace splitter bug).
        # \text{} additionally requires amsmath which is not loaded by Manim's default template.
        # Fix: strip both X -> X so they never reach the LaTeX compiler.
        # This prevents LATEX_TEXT_CMD lint errors from triggering the LLM fix path,
        # which was causing syntax-error deadlocks that exhausted the linter budget.
        patched = re.sub(r'\\mathrm\{([^}]*)\}', r'\1', patched)
        patched = re.sub(r'\\text\{([^}]*)\}', r'\1', patched)

        # 4b. [REMOVED] add_updater+become → always_redraw transform was removed.
        # Reason: regex rewrite only updates the local variable (obj = always_redraw(...))
        # but does NOT update prior self.add(obj) / VGroup(obj, ...) references, so the
        # new always_redraw object is never added to the scene and the animation silently
        # stops updating. UPDATER_BECOME_RISK is left for the LLM refining loop to handle
        # with full context of surrounding self.add() calls.

        # 4c. Fix Sector(outer_radius=X) -> Sector(radius=X)
        # Manim v0.20 Sector.__init__ uses 'radius', not 'outer_radius'.
        # Passing outer_radius= causes "got multiple values for keyword argument 'outer_radius'".
        patched = re.sub(r'Sector\(outer_radius=', 'Sector(radius=', patched)

        # 4d. Fix invalid "if VAR is [not] None= EXPR" syntax.
        # LLM generates this when trying to conditionally cap a value inside custom Animation
        # subclasses (e.g. interpolate_mobject). Pattern observed in ELEM_03/HIGH_04/MID_04/MID_05.
        # Also covers "is None=" variant (observed in HIGH_04 ablation session 20260402_102257).
        # Transforms:  if self._current is not None= min(0.2, run_time)
        #           →  if self._current is not None:
        #                  self._current = min(0.2, run_time)
        # Transforms:  if fill_op is None= 0
        #           →  if fill_op is None:
        #                  fill_op = 0
        _before_4d = patched
        patched = re.sub(
            r'^([ \t]*)if\s+(\S+)\s+is\s+(not\s+)?None=\s*(.+)$',
            lambda m: (
                f"{m.group(1)}if {m.group(2)} is {m.group(3) or ''}None:\n"
                f"{m.group(1)}    {m.group(2)} = {m.group(4)}"
            ),
            patched,
            flags=re.MULTILINE
        )
        if patched != _before_4d:
            print("🔧 [Shift-Left] Fixed 'is [not] None=' invalid syntax → expanded to if block")

        # 4e. Fix invalid keyword-as-assignment syntax.
        # LLM collapses the SceneInstrumentor's try/except opacity pattern into pseudo-lines.
        # Observed variants across eval sessions:
        #   try= (mob.get_fill_opacity() or 0) + ...        (ELEM_03/ELEM_05/MID_04)
        #   except Exception= 1.0                            (HIGH_01, session 20260402_102257)
        #   except= some_value
        #   finally= cleanup_val
        # Regex captures optional classname/args between keyword and '=' to handle
        # both "except= X" and "except Exception= X".
        _before_4e = patched
        _KW_AS_ASSIGN = re.compile(
            r'^([ \t]*)(try|except|finally|with)(?:\s+\w+)?\s*=\s*(.+)$',
            re.MULTILINE
        )
        def _fix_kw_assign(m: re.Match) -> str:
            indent, kw, expr = m.group(1), m.group(2), m.group(3)
            if kw == 'try':
                return (
                    f"{indent}try:\n"
                    f"{indent}    opacity = {expr}\n"
                    f"{indent}except Exception:\n"
                    f"{indent}    opacity = 1.0"
                )
            if kw == 'except':
                # "except Exception= 1.0" → restore the full except block
                return (
                    f"{indent}except Exception:\n"
                    f"{indent}    opacity = {expr}"
                )
            # For finally=/with= just demote to a plain assignment so AST can parse
            return f"{indent}_tmp = {expr}"
        patched = _KW_AS_ASSIGN.sub(_fix_kw_assign, patched)
        if patched != _before_4e:
            print("🔧 [Shift-Left] Fixed keyword-as-assignment syntax → valid block")

        # 5. [Enforce Final Wait] Ensure the construct method ends with a wait operation
        try:
            tree = ast.parse(patched)
            construct_node = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == 'construct':
                    construct_node = node
                    break
                    
            if construct_node and construct_node.body:
                last_stmt = construct_node.body[-1]
                has_wait = False
                if isinstance(last_stmt, ast.Expr) and isinstance(last_stmt.value, ast.Call):
                    func = last_stmt.value.func
                    if isinstance(func, ast.Attribute) and func.attr == 'wait':
                        has_wait = True
                
                if not has_wait and not isinstance(last_stmt, ast.Return):
                    lines = patched.splitlines()
                    end_line = getattr(last_stmt, 'end_lineno', last_stmt.lineno)
                    indent = " " * getattr(last_stmt, 'col_offset', 8)
                    lines.insert(end_line, f"{indent}self.wait(3)  # [Auto-injected by Shift-Left Repair]")
                    patched = "\n".join(lines)
        except Exception as e:
            print(f"⚠️ [Shift-Left] AST parsing failed during pre-render patch: {e}")

        # 5b. [Empty Animation Guard] Detect code with no self.play() or self.wait() calls.
        # Such code renders a 0-second blank video — catch before wasting a full render cycle.
        try:
            _tree = ast.parse(patched)
            _has_animation = False
            for _node in ast.walk(_tree):
                if isinstance(_node, ast.Expr) and isinstance(_node.value, ast.Call):
                    _func = _node.value.func
                    if isinstance(_func, ast.Attribute) and _func.attr in ('play', 'wait'):
                        _has_animation = True
                        break
            if not _has_animation:
                # Auto-inject a placeholder wait so Manim doesn't crash with 0-second render.
                # This is better than failing outright — the LLM likely forgot to add animations.
                _construct_match = re.search(r'(def construct\(self\):[ \t]*\n)(\s+)', patched)
                if _construct_match:
                    _indent = _construct_match.group(2)
                    patched = patched.rstrip() + f"\n{_indent}self.wait(1)  # [Auto-injected: no self.play() found]\n"
                    print("⚠️ [Shift-Left] No self.play()/self.wait() detected — injected fallback self.wait(1). LLM forgot animations.")
        except Exception:
            pass  # AST parse failed; skip this guard, render will catch it

        # 6. [LayoutEngine Neutralizer] Neutralize incorrectly-used LayoutEngine/LayoutObject blocks.
        # utils/layout_engine.py EXISTS in this project, but LLM almost always:
        #   (a) omits `from utils.layout_engine import LayoutEngine, LayoutObject`
        #   (b) calls non-existent methods like place_below() / place_above()
        #   (c) passes string args to add_constraint() instead of kiwisolver expressions
        # Only trigger when the import is missing (= LLM hallucinated incorrect usage).
        # If properly imported, leave the code alone — it's a valid benchmark-style solution.
        _has_layout_import = (
            'from utils.layout_engine import' in patched
            or 'from utils import layout_engine' in patched
        )
        try:
            _layout_cls_pat = re.compile(
                r'^([ \t]*)(\w+)\s*=\s*(?:LayoutEngine|LayoutObject|LayoutSolver)\s*\(', re.MULTILINE
            )
            _layout_match = _layout_cls_pat.search(patched)
            if _layout_match and not _has_layout_import:
                _layout_var = _layout_match.group(2)
                _method_pat = re.compile(
                    rf'^[ \t]*{re.escape(_layout_var)}\s*\.'
                    r'(?:add_constraint|place_below|place_right_of|place_above|place_at|solve|apply|add)\s*\(',
                    re.MULTILINE
                )
                # Collect object names from method call arguments (first identifier in each call)
                _obj_names = []
                for _m in _method_pat.finditer(patched):
                    # grab the full line to extract first identifier argument
                    _line_end = patched.find('\n', _m.start())
                    _line = patched[_m.start():_line_end if _line_end != -1 else len(patched)]
                    _args = re.findall(r'\b([a-zA-Z_]\w*)\b', _line)
                    # skip the var name itself and common keywords
                    _skip = {_layout_var, 'LEFT', 'RIGHT', 'UP', 'DOWN', 'CENTER', 'ORIGIN', 'True', 'False'}
                    for _a in _args[1:]:  # [0] is the method name
                        if _a not in _skip and not _a.startswith('_'):
                            _obj_names.append(_a)
                            break
                _obj_names = list(dict.fromkeys(_obj_names))  # dedupe, preserve order

                # Delete instantiation line + all method-call lines
                patched = _layout_cls_pat.sub('', patched)
                patched = _method_pat.sub('', patched)

                # Insert VGroup.arrange() before first self.play() as positional fallback
                if _obj_names:
                    _indent = _layout_match.group(1) or '        '
                    _arrange_line = f"{_indent}VGroup({', '.join(_obj_names)}).arrange(DOWN, buff=0.5)\n"
                    patched = re.sub(r'([ \t]*self\.play\()', _arrange_line + r'\1', patched, count=1)
                    print(f"🔧 [Shift-Left] LayoutEngine neutralized → VGroup({', '.join(_obj_names)}).arrange(DOWN)")
                else:
                    print("🔧 [Shift-Left] LayoutEngine neutralized (no objects extracted, layout lines removed)")
        except Exception as e:
            print(f"⚠️ [Shift-Left] LayoutEngine patch failed: {e}")

        # 7. [SubtitleManager] Inject to prevent subtitle overlap
        if 'SubtitleManager' not in patched:
            class_match = re.search(r'^class\s+\w+\s*\(Scene\)\s*:', patched, re.MULTILINE)
            if class_match:
                pos = class_match.start()
                patched = patched[:pos] + _SUBTITLE_MANAGER_SNIPPET + '\n\n' + patched[pos:]
            else:
                patched = _SUBTITLE_MANAGER_SNIPPET + '\n\n' + patched
            # Inject self._sm + self.set_subtitle at the top of construct()
            patched = re.sub(
                r'(def construct\(self\):[ \t]*\n)(\s+)',
                lambda m: (
                    m.group(1)
                    + m.group(2) + 'self._sm = SubtitleManager(self)\n'
                    + m.group(2) + 'self.set_subtitle = self._sm.show\n'
                    + m.group(2)
                ),
                patched, count=1
            )

        # 8. [SceneInstrumentor] Auto-inject collision/overlap tracking mechanism
        if 'SceneInstrumentor' not in patched:
            class_match = re.search(r'^class\s+\w+\s*\(Scene\)\s*:', patched, re.MULTILINE)
            if class_match:
                pos = class_match.start()
                patched = patched[:pos] + _INSTRUMENTOR_SNIPPET + '\n\n' + patched[pos:]
            else:
                patched = _INSTRUMENTOR_SNIPPET + '\n\n' + patched
            
            # Inject self._instrumentor at the top of construct()
            instrumentor_init = f"self._instrumentor = SceneInstrumentor(self, log_path='{log_path}')\n" if log_path else "self._instrumentor = SceneInstrumentor(self)\n"
            patched = re.sub(
                r'(def construct\(self\):[ \t]*\n)(\s+)',
                lambda m: (
                    m.group(1)
                    + m.group(2) + instrumentor_init
                    + m.group(2)
                ),
                patched, count=1
            )

        # 9. [Title Zone Protection] Only one object may use .to_edge(UP) — the title.
        # Multiple .to_edge(UP) calls stack objects at the top, causing title overlap (HIGH_02 pattern).
        # Strategy: keep the first occurrence (title), shift all subsequent ones down by 1.8 units.
        # Result: 2nd+ objects land at y ≈ 1.9, safely below the title zone (y ≥ 2.5).
        try:
            _edge_up_re = re.compile(r'\.to_edge\s*\(\s*UP[^)]*\)')
            _edge_up_lines = [(i, ln) for i, ln in enumerate(patched.splitlines()) if _edge_up_re.search(ln)]
            if len(_edge_up_lines) > 1:
                _lines = patched.splitlines()
                _shifted = 0
                for _idx, (_lno, _ln) in enumerate(_edge_up_lines):
                    if _idx == 0:
                        continue  # keep first (title)
                    _lines[_lno] = _edge_up_re.sub(lambda m: m.group(0) + '.shift(DOWN * 1.8)', _lines[_lno])
                    _shifted += 1
                patched = '\n'.join(_lines)
                print(f"🔧 [Shift-Left] Title Zone: shifted {_shifted} non-title .to_edge(UP) call(s) down 1.8 units")
        except Exception as _e9:
            print(f"⚠️ [Shift-Left] Title Zone patch failed: {_e9}")

        # 10. [Audio Dur Fallback Replace] Deterministic truncation
        try:
            _sj = script_json if isinstance(script_json, dict) else (json.loads(script_json) if script_json else None)
        except (json.JSONDecodeError, TypeError):
            _sj = None
        if _sj and 'scenes' in _sj and len(_sj['scenes']) > 0:
            seq = _sj['scenes'][0].get('sequence', [])
            max_injected = max(0, len(seq) - 1)
            refs = [int(m) for m in re.findall(r'_audio_dur_(\d+)', patched)]
            for n in set(refs):
                if n > max_injected:
                    patched = re.sub(rf'_audio_dur_{n}\b', f'_audio_dur_{max_injected}', patched)

        return patched

    @staticmethod
    def auto_fix_loop(file_path, scene_name, user_topic, script_json, llm_client=None, max_attempts=5, backup_filename_prefix=None, _diagnostics=None):
        """
        自動修復循環：包含語義審查與語法修復 (Reflexion Mechanism Fully Implemented)。

        Args:
            _diagnostics: Optional dict. If provided, counter state is written into it at
                every exit point so callers can build structured results without parsing logs.
                Keys written: visual_attempts, linter_only_retries, consecutive_timeouts,
                main_i, is_best_effort, failure_reason, reflection_memory, failed_code_snapshots.
                See agents/orchestrator/refining_loop_types.py for the adapter.
        """
        diagnoser = ManimDiagnoser()
        llm = llm_client if llm_client else LLMClient()
        rag_retriever = RAGRetriever()

        # [Parallel Eval Fix] Use isolated media dir when running under eval worker.
        _eval_dir = os.environ.get("EVAL_OUTPUT_DIR")
        _media_base = os.path.join(_eval_dir, "media") if _eval_dir else "media"

        reflection_memory = []
        _failed_code_snapshots = []  # [(attempt_num, failure_type, code)] for OSF/debug archiving
        _prompt_cache = {}  # Task 9 Layer 2: hash(prompt) → raw_response，避免同一 session 內重複呼叫
        _failed_hashes = set()   # [Bug 3 Fix] Hashes whose cached responses already failed, skip cache
        _syntax_rollback = False  # [Bug 4 Fix] Set when SyntaxError rollback occurs, poisons next prompt hash
        visual_attempts = 0
        VISUAL_ATTEMPTS_LIMIT = CFG.visual_attempts_limit
        tdr_t1_attempts = 0       # Counts zero-cost TDR T1 re-renders (cap: CFG.tdr_t1_cap)
        tdr_t2_attempts = 0       # Counts cheap micro-prompt fixes (cap: CFG.tdr_t2_cap)
        consecutive_timeouts = 0  # Track consecutive render timeouts for Template Override
        linter_only_retries = 0   # Linter failures are cheap — tracked separately
        LINTER_RETRY_BUDGET = CFG.linter_retry_budget
        layout_only_retries = 0   # Deterministic layout-audit failures — independent budget
        LAYOUT_RETRY_BUDGET = 2   # Cap to avoid burning visual_attempts on layout fixes

        start_time = time.time()

        def _fill_diagnostics(is_best_effort: bool, failure_reason):
            """Fill _diagnostics out-param at every exit point (no-op when _diagnostics is None)."""
            if _diagnostics is None:
                return
            _diagnostics.update({
                "visual_attempts": visual_attempts,
                "linter_only_retries": linter_only_retries,
                "layout_only_retries": layout_only_retries,
                "consecutive_timeouts": consecutive_timeouts,
                "main_i": i,
                "is_best_effort": is_best_effort,
                "failure_reason": failure_reason,
                "reflection_memory": list(reflection_memory),
                "failed_code_snapshots": list(_failed_code_snapshots),
            })

        last_successful_video_path = None
        last_error_message = ""  # Tracks the most recent Manim render error for patch fallback
        last_render_hash = None   # Render Cache: skip re-render when code is identical

        i = 0  # Main iteration counter (only incremented on render/vision failures)
        total_loops = 0  # Safety cap to prevent infinite loops
        while i < max_attempts and total_loops < max_attempts + LINTER_RETRY_BUDGET + LAYOUT_RETRY_BUDGET:
            total_loops += 1
            print(f"\n" + "═"*50)
            print(f"🔄  迭代進行中: 第 {i+1} / {max_attempts} 次嘗試 (linter retries: {linter_only_retries}/{LINTER_RETRY_BUDGET} | layout retries: {layout_only_retries}/{LAYOUT_RETRY_BUDGET})")
            print("═"*50)
            
            is_linter_only_failure = False  # Track if this iteration was linter-only (cheap)
            patch_mode = False  # [Bug 1 Fix] Initialize at top of every iteration to prevent UnboundLocalError

            with open(file_path, "r", encoding="utf-8") as f:
                current_code = f.read()

            # [Shift-Left Auto-Repair] Apply zero-cost deterministic patches BEFORE linter/render
            log_path = os.path.join(os.path.dirname(os.path.abspath(file_path)), "scene_state_log.json")
            patched_code = RefiningLoop.pre_render_patch(current_code, log_path=log_path, scene_name=scene_name, script_json=script_json)
            if patched_code != current_code:
                current_code = patched_code
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(current_code)
                    
            _triage_result = None  # Global triage result for deciding Dynamic N

            # ========== Phase 1: Static Analysis Gatekeeper (Linter Only) ==========
            # [OPTIMIZATION] Removed the LLM Reviewer (llama-3.1-8b) which was ~3s + 7k tokens
            # per iteration but almost always returned PASS. The Linter catches the critical
            # issues (deprecated APIs, hallucinated methods, syntax errors) deterministically.
            syntax_error = None
            try:
                compile(current_code, file_path, 'exec')
            except SyntaxError as e:
                syntax_error = f"FAIL\n\n[Syntax Error] (Local Check): {e}\nLine {e.lineno}: {e.text}"
                print(f"❌ [Syntax Check] Local compilation failed: {e}")

            if syntax_error:
                review_feedback = syntax_error
                # SyntaxError already caught above — no need to create tempfile for linter
            else:
                print("🔍 [步驟 1/2] 正在進行靜態代碼分析 (Linter Gatekeeper)...")
                # Run Linter directly (no LLM call)
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".py", encoding="utf-8", delete=False
                ) as _lf:
                    _lf.write(current_code)
                    temp_lint_file = _lf.name
                try:
                    lint_ok, lint_errors = lint_file(temp_lint_file)
                finally:
                    if os.path.exists(temp_lint_file):
                        os.remove(temp_lint_file)
                
                if not lint_ok:
                    print("❌ 靜態審查失敗 (Static Analysis Failed) - 攔截渲染")
                    _failed_code_snapshots.append((i + 1, "LINTER", current_code))
                    review_feedback = "FAIL\n\n[Static Analysis Gatekeeper]:\n"
                    for err in lint_errors:
                        review_feedback += f"- Line {err['line']} [{err['code']}]: {err['message']}\n"
                else:
                    print("✅ 靜態審查通過 (Static Analysis Passed)")
                    review_feedback = "PASS"
            
            # 🛡️ [安全性檢查] 強制檢查音訊調用 (Hard Check)
            if "PASS" in review_feedback:
                user_safe_topic = AudioEngine.get_safe_dir_name(user_topic)
                audio_dir = os.path.join(_media_base, "audio", user_safe_topic)
                
                _audio_mp3s = [f for f in os.listdir(audio_dir) if f.endswith(".mp3") and os.path.getsize(os.path.join(audio_dir, f)) >= 1024] if os.path.exists(audio_dir) else []
                if _audio_mp3s:
                    import ast
                    has_add_sound = False
                    try:
                        tree = ast.parse(current_code)
                        has_add_sound = any(
                            isinstance(n, ast.Call)
                            and isinstance(n.func, ast.Attribute)
                            and n.func.attr == 'add_sound'
                            for n in ast.walk(tree)
                        )
                    except SyntaxError:
                        has_add_sound = True  # fallback: if code can compile but not parse, don't brutally crash
                        
                    if not has_add_sound:
                        print("⚠️ [系統攔截] 檢測���音訊缺失！強制轉為 FAIL。")
                        review_feedback = """FAIL

[Audio Sync]: Critical Violation - Audio files generated but NOT used.
You MUST add `self.add_sound("media/audio/{}/step_XX.mp3")` for every step.
Do not verify this yourself, the system has confirmed audio files exist.
Fix this immediately.
""".format(user_safe_topic)
                    else:
                        print("🔧 [System] Disabling caching to ensure audio sync (Issue #4005 workaround)")
                        import sys
                        if "--disable_caching" not in sys.argv:
                            sys.argv.append("--disable_caching")
            
            # === Pre-flight Audio File Check ===
            # Checks both existence AND integrity (file size < 1KB = corrupted Azure TTS output)
            if "PASS" in review_feedback:
                _sound_refs = re.findall(r'^[^#\n]*self\.add_sound\(["\']([^"\']+)["\']', current_code, re.MULTILINE)
                _missing = [
                    p for p in _sound_refs
                    if not os.path.exists(p) or os.path.getsize(p) < 1024
                ]
                if _missing:
                    _missing_detail = [
                        f"{p} ({'missing' if not os.path.exists(p) else f'{os.path.getsize(p)}B corrupted'})"
                        for p in _missing
                    ]
                    print(f"⚠️ [Pre-flight] {len(_missing)} 個音訊問題（缺失或損壞），自動注解: {_missing_detail}")
                    _patched = current_code
                    for _p in _missing:
                        _patched = re.sub(
                            r'(\s*)(self\.add_sound\(["\']' + re.escape(_p) + r'["\'][^)]*\))',
                            r'\1# [missing audio] \2',
                            _patched
                        )
                    if _patched != current_code:
                        current_code = _patched
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(current_code)
                        print("✅ [Pre-flight] 缺失/損壞音訊已註解，繼續渲染")

            if "PASS" in review_feedback:
                print("✅ 靜態審查通過！執行渲染...")

                # ========== Phase 2: Manim 渲染檢查 (語法驗證) ==========
                # [Fast I/O] 使用低 fps 快速預覽渲染（Vision QA 對幀率不敏感）
                render_fps = CFG.fps_preview

                # [Render Cache] Skip re-render if code is bit-for-bit identical to last render
                _code_hash = hashlib.md5(current_code.encode("utf-8")).hexdigest()
                if _code_hash == last_render_hash and last_successful_video_path and os.path.exists(last_successful_video_path):
                    print(f"⚡ [Render Cache] Code unchanged (hash={_code_hash[:8]}), reusing last render.")
                    success, message, r_dur = True, "cached", 0.0
                else:
                    print("🎬 [步驟 2/2] 正在執行 Manim 渲染檢查...")
                    ret = RefiningLoop.run_manim_task(file_path, scene_name, fps=render_fps)
                    # Handled both return signatures to be safe, ret is tuple (success, msg, [dur])
                    if len(ret) == 3:
                        success, message, r_dur = ret
                    else:
                        success, message = ret
                        r_dur = 0.0
                    
                    llm.session_stats["time_render_sec"] += r_dur
                    if success:
                        last_render_hash = _code_hash
                
                if success:
                    consecutive_timeouts = 0  # Reset on successful render
                    # ========== Phase 3: Vision QA Check (Visual Auto-Fix) ==========
                    print("👁️ [步驟 3/3] 正在執行視覺 QA 審查 (Vision Audit)...")

                    # [Render Cache fix] If cache hit, video_source = last_successful_video_path (already correct path).
                    # If fresh render, compute path from current render_fps.
                    if message == "cached" and last_successful_video_path and os.path.exists(last_successful_video_path):
                        video_source = last_successful_video_path
                    else:
                        video_source = os.path.join(_media_base, "videos", os.path.splitext(os.path.basename(file_path))[0], f"480p{render_fps}", f"{scene_name}.mp4")
                        if not os.path.exists(video_source):
                            print("⚠️ 找不到渲染後的影片，跳過視覺審查。")
                            _fill_diagnostics(False, "video_not_found")
                            return False
                        last_successful_video_path = video_source
                    
                    # [Multi-Frame Vision Audit] Extract 4 frames at 10%, 40%, 70%, 95%
                    # and stitch into a 2x2 grid for comprehensive animation coverage.
                    grid_frame_path = "temp_vision_grid.jpg"
                    try:
                        # Get video duration
                        duration_result = subprocess.run(
                            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                             "-of", "default=noprint_wrappers=1:nokey=1", video_source],
                            capture_output=True, text=True, timeout=10
                        )
                        _dur_str = duration_result.stdout.strip()
                        if not _dur_str or _dur_str == "N/A":
                            # fallback: container duration（可能含音軌，但至少不崩潰）
                            duration_result = subprocess.run(
                                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "default=noprint_wrappers=1:nokey=1", video_source],
                                capture_output=True, text=True, timeout=10
                            )
                            _dur_str = duration_result.stdout.strip()
                        video_duration = float(_dur_str)
                        
                        # [Smart Frame Selection] Sample using a single ffmpeg command to save overhead
                        CANDIDATE_COUNT = 20
                        TILE_W, TILE_H = 640, 360
                        timestamps = None
                        try:
                            import numpy as np
                            from PIL import Image as _PILImage
                            
                            temp_dir = tempfile.mkdtemp(prefix="llmanim_frames_")
                            # Extract ~20 frames evenly spaced using fps filter
                            fps_val = max(0.5, CANDIDATE_COUNT / max(0.1, video_duration))
                            subprocess.run(
                                ["ffmpeg", "-y", "-i", video_source, 
                                 "-vf", f"fps={fps_val},scale=160:90", 
                                 os.path.join(temp_dir, "frame_%03d.jpg")],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
                            )
                            
                            _candidates = []
                            for f_name in sorted(os.listdir(temp_dir)):
                                if not f_name.endswith(".jpg"): continue
                                _cfp = os.path.join(temp_dir, f_name)
                                # Estimate timestamp from file index
                                idx = int(f_name.split("_")[1].split(".")[0]) - 1
                                _ts = (idx + 0.5) / fps_val
                                
                                _img = np.array(_PILImage.open(_cfp).convert("RGB"))
                                _candidates.append((_ts, float(np.std(_img)), _img))
                                
                            shutil.rmtree(temp_dir, ignore_errors=True)

                            # 去重：從複雜度高的幀開始挑，MAD < 8 視為同一畫面跳過
                            _candidates.sort(key=lambda x: x[1], reverse=True)
                            _unique = []
                            for cand in _candidates:
                                if not any(
                                    np.mean(np.abs(cand[2].astype(float) - u[2].astype(float))) < 8.0
                                    for u in _unique
                                ):
                                    _unique.append(cand)
                                if len(_unique) >= 4:
                                    break

                            if len(_unique) >= 4:
                                timestamps = sorted([c[0] for c in _unique[:4]])
                                print(f"🧮 [Smart Frame] 4 unique timestamps: {[f'{t:.1f}s' for t in timestamps]}")
                        except Exception as _ve:
                            print(f"⚠️ [Smart Frame] Variance selection failed ({_ve}), falling back to fixed %")

                        if not timestamps:
                            # Telemetry-guided dynamic frame: conservatively replace 70% only
                            # when the overlap hotspot remains in the later half and stays away
                            # from the fixed anchor frames.
                            _mid_pct = 0.70
                            try:
                                from ..utils.telemetry import (
                                    choose_telemetry_midpoint_pct as _choose_mid_pct,
                                    load_and_summarize as _tel_load,
                                )
                                _tel_sum = _tel_load(log_path)
                                if _tel_sum and _tel_sum.get("iou_overlap_pairs_max", 0) > 0:
                                    _wpct = _tel_sum.get("worst_overlap_step_pct")
                                    _mid_pct = _choose_mid_pct(_wpct)
                                    if _mid_pct != 0.70:
                                        print(f"🎯 [Telemetry Frame] Replacing 70% with worst-overlap step at {_mid_pct:.0%}")
                            except Exception:
                                pass
                            timestamps = [
                                video_duration * 0.10,  # 10% — setup/intro
                                video_duration * 0.40,  # 40% — early animation
                                video_duration * _mid_pct,  # dynamic — mid/worst-overlap
                                video_duration * 0.95,  # 95% — near end
                            ]

                        # [Optimization] Single ffmpeg command: 4x fast-seek inputs → scale + xstack → grid
                        # Replaces 4 individual extractions + 1 composite = 5 subprocess calls with 1
                        try:
                            TILE_W, TILE_H = 640, 360
                            n = len(timestamps)
                            inputs = []
                            scale_filters = []
                            for idx, ts in enumerate(timestamps):
                                inputs.extend(["-ss", f"{ts:.2f}", "-i", video_source])
                                scale_filters.append(f"[{idx}:v]scale={TILE_W}:{TILE_H},setpts=PTS-STARTPTS[s{idx}]")
                            layout = "|".join(f"{(k % 2) * TILE_W}_{(k // 2) * TILE_H}" for k in range(n))
                            scale_chain = ";".join(scale_filters)
                            scaled_labels = "".join(f"[s{k}]" for k in range(n))
                            filter_complex = f"{scale_chain};{scaled_labels}xstack=inputs={n}:layout={layout}"
                            subprocess.run(
                                ["ffmpeg", "-y"] + inputs + [
                                    "-filter_complex", filter_complex,
                                    "-frames:v", "1",
                                    grid_frame_path
                                ],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
                            )
                        except Exception as e:
                            print(f"⚠️ [Multi-Frame] Grid extraction failed ({e}), falling back to single frame.")

                    except Exception as e:
                        print(f"⚠️ [Multi-Frame] Grid extraction failed ({e}), falling back to last frame.")
                    
                    _frame_sampling_note = ""
                    if timestamps:
                        _pcts = [round((t / video_duration) * 100) for t in timestamps]
                        _frame_sampling_note = (
                            "FRAME SAMPLING NOTE:\n"
                            f"- TL = {_pcts[0]}% of video\n"
                            f"- TR = {_pcts[1]}% of video\n"
                            f"- BL = {_pcts[2]}% of video\n"
                            f"- BR = {_pcts[3]}% of video"
                        )

                    # Use grid if available, otherwise fall back to single last frame
                    if os.path.exists(grid_frame_path):
                        frame_path = grid_frame_path
                        ts_str = " / ".join([f"{t:.1f}s" for t in timestamps])
                        print(f"🖼️  [Multi-Frame] Using 4-frame grid for Vision Audit ({ts_str})")
                    else:
                        frame_path = "temp_last_frame.jpg"
                        subprocess.run(["ffmpeg", "-sseof", "-1", "-i", video_source, "-vframes", "1", "-update", "1", frame_path, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print("🖼️  [Fallback] Using single last frame for Vision Audit")
                    
                    # ── [Layout Gate] Deterministic layout audit BEFORE Vision LLM call ──
                    # Reads SceneInstrumentor's scene_state_log.json, checks for text-occlusion,
                    # excessive overlap, crowding. If FAILED, feed fix prompt to Coder and skip
                    # this iteration's Vision audit (saves tokens + targets the real problem).
                    # Has its own budget (LAYOUT_RETRY_BUDGET) to avoid burning visual_attempts.
                    if layout_only_retries < LAYOUT_RETRY_BUDGET:
                        try:
                            from ..utils.layout_auditor import LayoutAuditor, LayoutVerdict
                            _layout_audit = LayoutAuditor().audit(log_path)
                            if _layout_audit["verdict"] == LayoutVerdict.FAIL:
                                _layout_fix_prompt = LayoutAuditor.build_fix_prompt(_layout_audit)
                                print(f"\n📐 [Layout Gate] FAILED — {len(_layout_audit['violations'])} violations detected")
                                for _v in _layout_audit["violations"]:
                                    print(f"   ❌ [{_v['severity']}] {_v['metric']}={_v['value']} (step {_v['step']})")
                                print(f"   Layout retry {layout_only_retries+1}/{LAYOUT_RETRY_BUDGET} — feeding fix prompt to Coder...")
                                review_feedback = "FAIL\n\n" + _layout_fix_prompt
                                success = False
                                layout_only_retries += 1
                                # Skip Vision audit — let Coder fix layout first, re-render next iteration.
                                # i is NOT incremented because layout retries use independent budget.
                                continue
                            else:
                                print(f"📐 [Layout Gate] PASS (score={_layout_audit.get('score_1_to_5')})")
                        except Exception as _lg_err:
                            print(f"⚠️ [Layout Gate] audit failed: {_lg_err} — skipping gate")
                    else:
                        print(f"📐 [Layout Gate] budget exhausted ({layout_only_retries}/{LAYOUT_RETRY_BUDGET}) — proceeding to Vision audit")

                    vision_agent = VisionAgent(llm_client=llm)

                    # P2-3: Extract layout_plan zone coordinates from script_json for Vision hints
                    _spatial_metadata = None
                    try:
                        _parsed = json.loads(script_json) if isinstance(script_json, str) else script_json
                        _layout = _parsed.get("layout_plan", {})
                        if _layout:
                            _lines = []
                            for zone_name, zone_val in _layout.items():
                                if isinstance(zone_val, dict):
                                    _coords = zone_val.get("coordinates") or zone_val.get("position") or zone_val.get("region")
                                    _desc = zone_val.get("description", "")
                                    _lines.append(f"  {zone_name}: coords={_coords} | {_desc}")
                                else:
                                    _lines.append(f"  {zone_name}: {zone_val}")
                            if _lines:
                                _spatial_metadata = "Zones:\n" + "\n".join(_lines)
                    except Exception:
                        pass

                    # Telemetry: read SceneInstrumentor log and compute IoU summary
                    _telemetry_context = None
                    try:
                        from ..utils.telemetry import load_and_summarize, format_telemetry_block
                        _iou_summary = load_and_summarize(log_path)
                        if _iou_summary and _iou_summary.get("iou_overlap_pairs_max", 0) > 0:
                            _telemetry_context = format_telemetry_block(_iou_summary)
                            print(f"📊 [Telemetry] IoU overlap: max_pairs={_iou_summary['iou_overlap_pairs_max']}, "
                                  f"worst_step={_iou_summary['worst_overlap_step']}/{_iou_summary['total_steps']} "
                                  f"({_iou_summary['worst_overlap_step_pct']:.0%})")
                    except Exception as _tel_err:
                        print(f"⚠️  [Telemetry] Failed to load overlap summary: {_tel_err}")

                    # Task 13 分級策略：最後一次視覺審查升級為短影片模式
                    # visual_attempts == 2 表示這是 VISUAL_ATTEMPTS_LIMIT=3 的最後一���
                    use_video_audit = (visual_attempts >= VISUAL_ATTEMPTS_LIMIT - 1)

                    # [Opt] Adaptive detail: i==0 (first audit) → high detail for max accuracy.
                    # Subsequent audits drop to low to save Vision API tokens.
                    # First-pass verdict is the most consequential: false negative = wasted LLM iteration.
                    _frame_detail = "high" if i == 0 else "low"

                    if use_video_audit:
                        # 擷取中段 2 秒片段（320p，去音軌降低 base64 大小）
                        clip_path = "temp_vision_clip.mp4"
                        mid = video_duration * 0.5
                        clip_result = subprocess.run([
                            "ffmpeg", "-y",
                            "-ss", str(max(0, mid - 1)),
                            "-i", video_source,
                            "-t", "2",
                            "-vf", "scale=320:-2",
                            "-an",  # 去音軌，省 token
                            clip_path
                        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)

                        # Prepend user_topic so Vision Agent's Phase 0 anchor always fires
                        _vision_context = f"TOPIC: {user_topic}\n\n{script_json}"
                        if _frame_sampling_note:
                            _vision_context += f"\n\n{_frame_sampling_note}"
                        if clip_result.returncode == 0 and os.path.exists(clip_path):
                            print("🎬 [Task 13] 最後一次視覺審查 → 短影片模式 (2s 320p clip)")
                            _vstart = time.time()
                            audit = vision_agent.audit_video(clip_path, _vision_context, code_context=current_code, spatial_metadata=_spatial_metadata, telemetry_context=_telemetry_context)
                            llm.session_stats["time_vision_sec"] += (time.time() - _vstart)
                            os.remove(clip_path)
                        else:
                            print("⚠️ [Task 13] 影片擷取失敗，fallback 至 4-frame grid")
                            _vstart = time.time()
                            audit = vision_agent.audit_frame(frame_path, _vision_context, code_context=current_code, detail="high", spatial_metadata=_spatial_metadata, telemetry_context=_telemetry_context)
                            llm.session_stats["time_vision_sec"] += (time.time() - _vstart)
                    else:
                        print(f"🖼️  [Vision] 使用 detail={_frame_detail} (iteration {i})")
                        _vision_context = f"TOPIC: {user_topic}\n\n{script_json}"
                        if _frame_sampling_note:
                            _vision_context += f"\n\n{_frame_sampling_note}"
                        _vstart = time.time()
                        audit = vision_agent.audit_frame(frame_path, _vision_context, code_context=current_code, detail=_frame_detail, spatial_metadata=_spatial_metadata, telemetry_context=_telemetry_context)
                        llm.session_stats["time_vision_sec"] += (time.time() - _vstart)
                    
                    if audit["verdict"] == "ERROR":
                        print(f"⚠️  [Vision API Error] 視覺審查無法執行，跳過本次視覺檢查：{audit.get('overall_critique', '')}")
                    elif audit["verdict"] == "FAIL":
                        print(f"\n❌ 視覺審查失敗 (Visual Check Failed)：")
                        print(f"📝 總體評價: {audit.get('overall_critique', 'No critique')}")

                        # ── Tiered Defect Router (TDR) ────────────────────────────────
                        # OVERLAP T1: if overlap involves the title zone, attempt zero-cost AST fix first.
                        # MISALIGNED T1/T2: cheap local fixes for alignment issues.
                        # Other defect types fall through to full rewrite.
                        _defects = audit.get("defects", [])

                        # OVERLAP T1: title zone collision → shift offending .to_edge(UP) down (zero cost)
                        _overlap_defects = [d for d in _defects if d.get("code") == "OVERLAP"]
                        _title_overlap = any(
                            "title" in (d.get("description", "") + d.get("suggested_fix", "")).lower()
                            for d in _overlap_defects
                        )
                        if _title_overlap and tdr_t1_attempts < CFG.tdr_t1_cap:
                            try:
                                import re as _re9
                                _eu_re = _re9.compile(r'\.to_edge\s*\(\s*UP[^)]*\)')
                                _eu_lines = [(i, ln) for i, ln in enumerate(current_code.splitlines()) if _eu_re.search(ln)]
                                if len(_eu_lines) > 1:
                                    _t1_lines = current_code.splitlines()
                                    for _idx, (_lno, _) in enumerate(_eu_lines):
                                        if _idx == 0:
                                            continue
                                        _t1_lines[_lno] = _eu_re.sub(lambda m: m.group(0) + '.shift(DOWN * 1.8)', _t1_lines[_lno])
                                    _t1_code = '\n'.join(_t1_lines)
                                    with open(file_path, "w", encoding="utf-8") as _f:
                                        _f.write(_t1_code)
                                    tdr_t1_attempts += 1
                                    print(f"⚡ [TDR-T1] Title OVERLAP: shifted non-title .to_edge(UP) down 1.8 units (成本 $0)...")
                                    continue
                            except Exception as _ov_err:
                                print(f"⚠️  [TDR-T1] Title overlap patch failed: {_ov_err}")

                        _misaligned_defects = [d for d in _defects if d.get("code") == "MISALIGNED"]
                        if _misaligned_defects and (tdr_t1_attempts < CFG.tdr_t1_cap or tdr_t2_attempts < CFG.tdr_t2_cap):
                            try:
                                _router = MisalignmentRouter()

                                if tdr_t1_attempts < CFG.tdr_t1_cap:
                                    # T1: zero-cost AST parametric fix (e.g. buff=0.2 → buff=0)
                                    _t1_patched = _router.try_t1_fix(_misaligned_defects, current_code)
                                    if _t1_patched:
                                        with open(file_path, "w", encoding="utf-8") as _f:
                                            _f.write(_t1_patched)
                                        tdr_t1_attempts += 1
                                        print(f"⚡ [TDR-T1] 參數補丁套用成功，直接重渲染 (成本 $0, 第 {tdr_t1_attempts} 次)...")
                                        continue  # Re-render immediately, no LLM call

                                if tdr_t2_attempts < CFG.tdr_t2_cap:
                                    # T2: lightweight micro-prompt (~2K tokens vs ~20K)
                                    _micro_prompt = _router.get_t2_prompt(_misaligned_defects, current_code)
                                    if _micro_prompt and visual_attempts < VISUAL_ATTEMPTS_LIMIT:
                                        print(f"⚡ [TDR-T2] Micro-Prompt 修復對齊 (~2K tokens)...")
                                        _t2_history = RefiningLoop._format_reflection_memory(reflection_memory)
                                        
                                        _cstart = time.time()
                                        _micro_fix_raw = llm.ask_for_fix(_t2_history, _micro_prompt)
                                        llm.session_stats["time_coder_sec"] += (time.time() - _cstart)
                                        
                                        _micro_fix = LLMClient.extract_code(_micro_fix_raw)
                                        _t2_patched = apply_patch_block(current_code, _micro_fix)
                                        if _t2_patched:
                                            with open(file_path, "w", encoding="utf-8") as _f:
                                                _f.write(_t2_patched)
                                            tdr_t2_attempts += 1
                                            visual_attempts += 1
                                            print(f"⚡ [TDR-T2] 補丁套用成功，重渲染...")
                                            continue

                            except Exception as _tdr_err:
                                print(f"⚠️  [TDR] 路由器異常 ({_tdr_err})，fallback 至標準流程")
                        # ── End TDR ───────────────────────────────────────────────────

                        if visual_attempts >= VISUAL_ATTEMPTS_LIMIT:
                            print(f"\n⚠️  視覺修復次數已達上限 ({VISUAL_ATTEMPTS_LIMIT})。代碼未變更，停止迴圈以避免重複渲染浪費。")
                            break  # Code unchanged — re-rendering would waste render + Vision API calls
                        else:
                            visual_prompter = VisualFixPrompter()
                            visual_fix_instruction = visual_prompter.generate_visual_fix_prompt(audit, current_code, script_json, slim=(i > 0))
                            
                            if visual_fix_instruction:
                                print(f"🤖 正在生成視覺修復代碼 (Visual Auto-Fix) [Attempt {visual_attempts+1}/{VISUAL_ATTEMPTS_LIMIT}]...")
                                review_feedback = visual_fix_instruction
                                success = False 
                                message = visual_fix_instruction 
                                visual_attempts += 1
                                
                                history_context = RefiningLoop._format_reflection_memory(reflection_memory)
                                patch_mode = False  # Visual fixes need full-code rewrite; patch mode causes apply failures
                                
                                # feedback_for_llm = dynamic user content (defect report + code)
                                # history_context = static Reflexion Memory → goes to system_prompt for DeepSeek Cache
                                feedback_for_llm = f"""
{visual_fix_instruction}

**CRITICAL**: Review the 'Past Lessons Learned' in your system context and **strictly avoid** making the same mistakes again.

**BEFORE writing code**, first analyze this failure in a <reflection> block:
<reflection>
{_REFLEXION_JSON_SCHEMA}
</reflection>

Then provide the corrected code.
"""
                            else:
                                # [HOTFIX] If VisualFixPrompter returns None, it means all defects
                                # were filtered (e.g., only LOW_CONTRAST). Treat as PASS.
                                # Previously, this fallback dumped raw_response (containing "LOW_CONTRAST")
                                # back to the Coder, causing it to "fix" a non-existent problem.
                                print("✅ [Filter] 所有視覺缺陷已被過濾（假陽性），視為通過。")
                                # Don't set success=False, let it continue as if passed
                                patch_mode = False 
                    
                    else:
                        # ── Vision Confidence Gradient Decision ───────────────────────
                        # confidence_score 1-5 from VisionAgent.
                        # Grade policy (thresholds from CFG):
                        #   >= vision_conf_accept  → high confidence PASS → break immediately
                        #   == vision_conf_soft_fail and budget exhausted → accept with warning
                        #   == vision_conf_soft_fail and budget remains   → soft-FAIL, one more fix
                        #   <  vision_conf_soft_fail                      → treat as FAIL
                        _conf = audit.get("confidence_score", 5) if audit.get("verdict") != "ERROR" else 5
                        _budget_exhausted = (i >= max_attempts - 2) or (visual_attempts >= VISUAL_ATTEMPTS_LIMIT - 1)

                        if _conf >= CFG.vision_conf_accept:
                            print(f"✅ 視覺審查通過！影片品質符合標準。(confidence={_conf}/5)")
                        elif _conf == CFG.vision_conf_soft_fail and _budget_exhausted:
                            print(f"⚠️  [Vision Gradient] confidence={_conf}/5，但已接近預算上限，接受此結果。")
                        elif _conf < CFG.vision_conf_soft_fail and not _budget_exhausted:
                            # Low-confidence PASS → downgrade, request another visual fix
                            print(f"⚠️  [Vision Gradient] confidence={_conf}/5 過低，視為 soft-FAIL，要求額外修復...")
                            success = False
                            _low_conf_critique = audit.get("overall_critique", "Low confidence in visual quality.")
                            review_feedback = (
                                f"Visual check returned PASS but with very low confidence (score {_conf}/5). "
                                f"The model is uncertain. Critique: {_low_conf_critique}\n\n"
                                "Please review the code carefully for subtle visual issues: "
                                "overlapping labels, off-screen elements, missing objects, or unclear layout."
                            )
                            visual_attempts += 1
                        else:
                            # _conf == vision_conf_soft_fail with budget remaining → same soft-FAIL path
                            print(f"⚠️  [Vision Gradient] confidence={_conf}/5，尚有修復預算，嘗試進一步改善...")
                            success = False
                            _low_conf_critique = audit.get("overall_critique", "Moderate confidence in visual quality.")
                            review_feedback = (
                                f"Visual check returned PASS but with moderate confidence (score {_conf}/5). "
                                f"Critique: {_low_conf_critique}\n\n"
                                "Please improve visual clarity: ensure all labels are readable, "
                                "no objects overlap unintentionally, and the layout matches the topic requirements."
                            )
                            visual_attempts += 1
                        # ── End Vision Confidence Gradient ────────────────────────────

                    if success:
                        if render_fps != CFG.fps_final:
                            print(f"🌟 [High-Quality Render] 預覽驗證無誤，啟動最終高品質 {CFG.fps_final}fps 算繪...")
                            ret_15 = RefiningLoop.run_manim_task(file_path, scene_name, fps=CFG.fps_final)
                            success_15 = ret_15[0]
                            if success_15:
                                # Compute the actual 15fps video path (run_manim_task returns stdout, not path)
                                video_source_15 = os.path.join(
                                    _media_base, "videos",
                                    os.path.splitext(os.path.basename(file_path))[0],
                                    f"480p{CFG.fps_final}", f"{scene_name}.mp4"
                                )
                                if os.path.exists(video_source_15):
                                    video_source = video_source_15
                                else:
                                    print(f"⚠️ 15fps 影片路徑不存在，退回使用 {render_fps}fps 版本。")
                            else:
                                print(f"⚠️ 最終高品質算繪失敗，退回使用 {render_fps}fps 版本。:\n{ret_15[1]}")

                        duration = round(time.time() - start_time, 2)
                        output_folder = os.environ.get("EVAL_OUTPUT_DIR", "stable_outputs")
                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder)

                        name_source = backup_filename_prefix if backup_filename_prefix else user_topic
                        safe_name = name_source.replace(" ", "_").replace(".", "_").replace("/", "_").replace("*", "x").replace("+", "_plus_").replace("-", "_minus_")
                        for char in '<>:"/\\|?*()':
                            safe_name = safe_name.replace(char, "_")
                        safe_name = safe_name[:50]
                        
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        backup_video_path = os.path.join(output_folder, f"{safe_name}_{timestamp}.mp4")
                        shutil.move(video_source, backup_video_path)
                        
                        if os.path.getsize(file_path) > 0:
                            backup_py_path = os.path.join(output_folder, f"{safe_name}_{timestamp}.py")
                            shutil.copy(file_path, backup_py_path)

                        # Save failed code snapshots for debugging / OSF supplementary material
                        for snap_num, snap_type, snap_code in _failed_code_snapshots[:5]:
                            snap_path = os.path.join(output_folder, f"{safe_name}_{timestamp}_attempt_{snap_num}_{snap_type}.py")
                            with open(snap_path, "w", encoding="utf-8") as _sf:
                                _sf.write(snap_code)
                        if _failed_code_snapshots:
                            print(f"📸 [Snapshot] 已儲存 {len(_failed_code_snapshots)} 個失敗版本至 {output_folder}/")

                        # ── DPO Training Pairs ────────────────────────────────────────
                        # Only emit pairs when there are actual failed attempts to contrast with.
                        # Format: one JSONL record per (rejected, chosen) pair.
                        # - prompt    : topic + visual plan JSON (task description, model-agnostic)
                        # - rejected  : broken code from each failed attempt
                        # - chosen    : final working code (this file_path content)
                        # - metadata  : defect type, iteration number, topic
                        if _failed_code_snapshots and backup_py_path and os.path.exists(backup_py_path):
                            dpo_path = os.path.join(output_folder, f"{safe_name}_{timestamp}_dpo.jsonl")
                            _dpo_prompt = f"TOPIC: {user_topic}\n\nVISUAL PLAN:\n{script_json}"
                            try:
                                with open(dpo_path, "w", encoding="utf-8") as _dpo_f:
                                    for _snap_num, _snap_type, _snap_code in _failed_code_snapshots:
                                        _pair = {
                                            "prompt":    _dpo_prompt,
                                            "rejected":  _snap_code,
                                            "chosen":    current_code,
                                            "metadata": {
                                                "topic":          user_topic,
                                                "attempt":        _snap_num,
                                                "failure_type":   _snap_type,
                                                "total_attempts": i + 1,
                                            }
                                        }
                                        _dpo_f.write(json.dumps(_pair, ensure_ascii=False) + "\n")
                                print(f"🧬 [DPO] 已儲存 {len(_failed_code_snapshots)} 個訓練對至 {os.path.basename(dpo_path)}")
                            except Exception as _dpo_err:
                                print(f"⚠️  [DPO] 儲存失敗（不影響主流程）: {_dpo_err}")
                        # ── End DPO Training Pairs ────────────────────────────────────

                        print("\n" + "═"*40)
                        print(f"✨ 【渲染成功 / Rendering Success】 ✨")
                        print("═"*40)
                        print(f"⏱️  總執行耗時: {duration} 秒")
                        print(f"📂  歸檔目錄: {output_folder}")
                        print(f"    🎥 {os.path.basename(backup_video_path)}")
                        print("═"*40 + "\n")
                        _fill_diagnostics(False, "success")
                        return backup_video_path

                if not success:
                    if "VIOLATION REPORT" not in message:
                        _failed_code_snapshots.append((i + 1, "RENDER", current_code))
                        print(f"\n❌ 渲染失敗！捕捉到 Python/Manim 語法錯誤：\n{message}")
                        
                        # [NEW] Static Linter Interceptor
                        # Catch low-level color parameter misplacement errors before burning LLM tokens.
                        # We strip all whitespace/newlines from message because Manim's rich traceback randomly word-wraps errors.
                        clean_msg = message.replace('\n', '').replace('\r', '').replace(' ', '')
                        is_color_kwarg_error = "unexpectedkeywordargument'color'" in clean_msg
                        is_set_color_error = "hasnoattribute'set_color'" in clean_msg
                        
                        if is_color_kwarg_error or is_set_color_error:
                            
                            print("⚡ [Static Linter] 偵測到低級 'color' 參數錯置，啟動自動 Regex 修復 (成本 $0)...")
                            
                            def remove_color_kwarg(match):
                                anim = match.group(1)
                                inner = match.group(2)
                                color_match = re.search(r',\s*color\s*=\s*([^,)]+)', inner)
                                if not color_match:
                                    return match.group(0)
                                color_val = color_match.group(1)
                                new_inner = re.sub(r',\s*color\s*=\s*[^,)]+', '', inner)
                                return f"{anim}({new_inner.strip()}.set_color({color_val}))"

                            patched_code = re.sub(r'(Create|Write|FadeIn|DrawBorderThenFill)\((.+?)\)', remove_color_kwarg, current_code)
                            patched_code = re.sub(r'(Create|Write|FadeIn|DrawBorderThenFill)\((.+?)\)\.set_color\((.+?)\)', r'\1(\2.set_color(\3))', patched_code)
                            
                            if patched_code != current_code:
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write(patched_code)
                                print("✅ [Static Linter] `color=` 語法修補完成，重新提交渲染...")
                                continue # Skip the LLM prompt and directly retry the loop!
                                
                        # [NEW] Opt-5 Auto-Fixes: opacity and 2D/3D mismatches
                        is_opacity_error = "unexpectedkeywordargument'opacity'" in clean_msg
                        is_2d_3d_error = "tupleindexoutofrange" in clean_msg or "settinganarrayelementwithasequence" in clean_msg

                        if is_opacity_error or is_2d_3d_error:
                            print("⚡ [Static Linter] 偵測到可自動修復的過時 API，嘗試 regex 替換...")
                            patched_code = current_code

                            # 1. Fix opacity=0.5 -> .set_opacity(0.5)
                            if is_opacity_error:
                                patched_code = re.sub(r'([A-Z][a-zA-Z0-9_]*)(?:\(([^)]*?)(?:,\s*)?)?opacity\s*=\s*([^,)]+)([^)]*)\)',
                                                      r'\1(\2\4).set_opacity(\3)', patched_code)

                            # 2. Fix 2D to 3D point mismatch
                            if is_2d_3d_error:
                                patched_code = re.sub(r'(move_to|shift|next_to)(\(\s*\[\s*[^,]+,\s*[^,]+)(\s*\]\s*\))', r'\1\2, 0\3', patched_code)

                            if patched_code != current_code:
                                with open(file_path, "w", encoding="utf-8") as f:
                                    f.write(patched_code)
                                print("✅ [Static Linter] API/Kwarg regex 語法修補完成，重新提交渲染...")
                                continue  # Skip the LLM prompt and directly retry the loop!

                        # Track consecutive timeouts for Template Override escalation
                        is_timeout = f"timed out after {CFG.render_timeout_sec}" in message
                        if is_timeout:
                            consecutive_timeouts += 1
                        else:
                            consecutive_timeouts = 0

                        print("\n🤔 [Reflexion] 準備進行自我反思 (Self-Reflection) 與修復...")
                        _trunc_msg = RefiningLoop._truncate_error(message)
                        
                        # [Smart Patch Routing] Use SEARCH/REPLACE only for targeted known fixes.
                        # Full rewrite is only used for unknown or architectural errors (e.g. timeouts).
                        _triage_result = diagnoser.diagnose_only(message)
                        patch_mode = _triage_result.is_surgical  # True = 外科手術式修改, False = 全部重寫
                        if patch_mode:
                            print(f"🔬 [Smart Patch] 已識別為局部可修復錯誤 ({_triage_result.category}) → 切換為 SEARCH/REPLACE 模式（保護完好代碼）")
                        else:
                            print(f"🔄 [Full Rewrite] 需架構重寫 ({_triage_result.category}) → 使用完整代碼重寫")

                        last_error_message = message  # Save for patch fallback (Bug #9)
                        history_context = RefiningLoop._format_reflection_memory(reflection_memory)
                        _code_for_llm = RefiningLoop.strip_injected_snippets(current_code)
                        base_fix = diagnoser.generate_fix_prompt(_trunc_msg, _code_for_llm, script_json, triage_result=_triage_result, slim=(i > 0))

                        # [RAR-Agent] Inject verified examples + API rules from Weaviate
                        # Use user_topic (not error traceback) — topic gives semantically relevant examples
                        _rag_results = rag_retriever.retrieve_examples(user_topic, limit=2)
                        _rag_results += rag_retriever.retrieve_rules(_trunc_msg, limit=2)
                        if _rag_results:
                            base_fix += "\n\n" + rag_retriever.format_for_prompt(_rag_results)

                        # [TIERED TEMPLATE OVERRIDE]
                        # Timeout Tier 1 (1st timeout): Safe dynamic skeleton - allows always_redraw + ValueTracker
                        #   but BANS add_updater+become which is the actual cause of infinite loops.
                        # Timeout Tier 2 (2nd+ timeout): Nuclear linear-only skeleton - bans everything dynamic.
                        # This graduated approach fixes the deadlock where dynamic animations (e.g. Unit Circle Sync)
                        # NEED always_redraw/ValueTracker to work but the old single override banned them completely.
                        if consecutive_timeouts == 1:
                            print(f"\n🚨 [Template Override Tier 1] 第 1 次渲染超時！啟動安全動態骨架（允許 always_redraw + ValueTracker）...")
                            print(f"\n🚨 [Template Override Tier 1] 第 1 次渲染超時！注入完整的安全動態代碼模板（強制取代 add_updater 架構）...")
                            # Strategy: Instead of giving an empty skeleton (which LLM ignores),
                            # inject a full WORKING code example using the correct always_redraw + ValueTracker pattern.
                            # LLM is ONLY allowed to ADAPT this code (change labels, layout, audio),
                            # NOT to replace the core animation architecture.
                            _sine_wave_golden = open(
                                "knowledge_base/geometry/SineWaveConstruction.py", "r", encoding="utf-8"
                            ).read() if __import__("os").path.exists("knowledge_base/geometry/SineWaveConstruction.py") else ""

                            _golden_injection = ""
                            if _sine_wave_golden:
                                _golden_injection = f"""
--- MANDATORY STARTING POINT (Full Working Code) ---
The following code uses the CORRECT always_redraw + ValueTracker architecture and renders in < 10 seconds.
You MUST use this exact architecture as your starting point.
You are ONLY allowed to: rename labels, adjust layout coordinates, add audio calls.
You are NOT allowed to: replace `always_redraw` with `add_updater`, add `become()`, or rebuild core animation logic.

```python
{_sine_wave_golden}
```
--- END OF MANDATORY STARTING POINT ---
"""

                            template_override = f"""
[TEMPLATE OVERRIDE — TIER 1: INJECT WORKING CODE]
Your previous attempt caused a timeout because it used `add_updater(lambda m: m.become(...))` which rebuilds expensive objects every frame.

This pattern is PERMANENTLY BANNED. The ONLY correct approach for dynamic animations is:
  ✅ `always_redraw(lambda: LightObject(...))` — for Dot, Line, Arc, DashedLine ONLY
  ✅ One `ValueTracker` drives ALL movement via `self.play(tracker.animate.set_value(TARGET))`
  ✅ `TracedPath(obj.get_center)` for curves
  ❌ `add_updater(lambda m: m.become(...))` — FATAL timeout
  ❌ `ParametricFunction` / `MathTex` inside any lambda — too expensive
{_golden_injection}"""

                            feedback_for_llm = f"""
{template_override}

═══════════════════════════════════════════════════════════
ORIGINAL TASK — YOU MUST IMPLEMENT THIS, NOT SOMETHING ELSE
═══════════════════════════════════════════════════════════
{script_json}
═══════════════════════════════════════════════════════════

{history_context}

**BEFORE writing code**, first analyze this failure in a <reflection> block:
<reflection>
{_REFLEXION_JSON_SCHEMA}
</reflection>

Then provide the corrected code.
"""
                        elif consecutive_timeouts >= 2:
                            print(f"\n🚨 [Template Override Tier 2] 連續 {consecutive_timeouts} 次渲染超時！啟動極簡線性骨架模式（禁止所有動態機制）...")
                            template_override = """
[TEMPLATE OVERRIDE — TIER 2: LINEAR-ONLY SKELETON]
Your previous attempts ALL caused infinite render loops even with dynamic patterns.
You have lost ALL freedom to design the animation architecture.
You MUST use the following safe, linear skeleton. Do NOT use ANY `always_redraw`, `add_updater`, or `ValueTracker` logic.
Build the scene sequentially using simple `Create`, `Write`, `FadeIn`, and `play` commands:

```python
from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # 1. Create static elements
        # (e.g. titles, axes, base geometry)
        
        # 2. Build the main diagram step-by-step
        # ... your code here ...
        
        # 3. Animate changes linearly (no updaters)
        # ... your code here ...
        
        self.wait(1)
```

You MUST strip away all complex updaters and rebuild the requested animation using this safe, step-by-step linear approach.
"""
                            feedback_for_llm = f"""
{template_override}

═══════════════════════════════════════════════════════════
ORIGINAL TASK — YOU MUST IMPLEMENT THIS, NOT SOMETHING ELSE
═══════════════════════════════════════════════════════════
{script_json}
═══════════════════════════════════════════════════════════

{history_context}

**BEFORE writing code**, first analyze this failure in a <reflection> block:
<reflection>
{_REFLEXION_JSON_SCHEMA}
</reflection>

Then provide the corrected code.
"""
                        else:
                            feedback_for_llm = f"""
{base_fix}

{history_context}

**CRITICAL**: Review the 'Past Lessons Learned' above and **strictly avoid** making the same mistakes again.

**BEFORE writing code**, first analyze this failure in a <reflection> block:
<reflection>
{_REFLEXION_JSON_SCHEMA}
</reflection>

Then provide the corrected code.
"""
            
            else:
                is_linter_only_failure = True  # Linter failures are cheap — use separate budget
                print(f"\n⚠️  語義/佈局審查未通過：\n{review_feedback}")

                print("\n🤔 [Reflexion] 準備進行自我反思 (Self-Reflection) 與修復...")
                
                # Vision analysis doesn't undergo static triage, manually create triage
                from ..coder.diagnoser import ErrorTriage
                is_static_error = "[Static Analysis Gatekeeper]" in review_feedback
                
                # Pre-triage visual errors or static layout errors
                _vision_cat = "LAYOUT_OR_VISUAL" if not is_static_error else "STATIC_API"
                _triage_result = ErrorTriage(matched=True, is_surgical=is_static_error, category=_vision_cat, advice=review_feedback)
                patch_mode = _triage_result.is_surgical  # [Bug Fix] Ensure patch_mode matches the prompt for linter errors!
                
                _code_for_llm = RefiningLoop.strip_injected_snippets(current_code)
                fix_prompt = diagnoser.generate_fix_prompt(review_feedback, _code_for_llm, script_json, triage_result=_triage_result, slim=(i > 0))

                # [RAR-Agent] Inject verified examples + API rules for layout/visual errors
                # Use user_topic (not review feedback) — topic gives semantically relevant examples
                _rag_results = rag_retriever.retrieve_examples(user_topic, limit=2)
                _rag_results += rag_retriever.retrieve_rules(review_feedback, limit=2)
                if _rag_results:
                    fix_prompt += "\n\n" + rag_retriever.format_for_prompt(_rag_results)

                history_context = RefiningLoop._format_reflection_memory(reflection_memory)
                # [Bug 4 Fix] If the last attempt ended with a SyntaxError rollback, inject that
                # signal into the prompt so the hash differs and cache deadlock is broken.
                _syntax_prefix = ""
                if _syntax_rollback:
                    _syntax_prefix = (
                        f"⚠️ PREVIOUS REPAIR CAUSED SYNTAX ERROR: {last_error_message}\n"
                        f"The current code still has the original static-analysis issue below. "
                        f"Your previous fix introduced a Python syntax error — ensure the new code is "
                        f"syntactically valid before addressing the linter issue.\n\n"
                    )
                    _syntax_rollback = False  # consume the flag
                feedback_for_llm = f"""
{_syntax_prefix}{fix_prompt}

{history_context}

**CRITICAL**: Review the 'Past Lessons Learned' above and **strictly avoid** making the same mistakes again.

**BEFORE writing code**, first analyze this failure in a <reflection> block:
<reflection>
{_REFLEXION_JSON_SCHEMA}
</reflection>

Then provide the corrected code.
"""

            print("\n🤖 正在將錯誤回傳給 AI 進行自我修正 (注入過去教訓)...")
            
            try:
                new_code = ""
                for attempt in range(3):
                    # Task 9 Layer 2: 相同 prompt hash 直接用快取，跳過重複 LLM call
                    prompt_hash = hashlib.md5(feedback_for_llm.encode()).hexdigest()[:16]
                    if prompt_hash in _prompt_cache:
                        # [Bug 3 Fix] If this prompt's cached response already caused a failure, skip it
                        if prompt_hash in _failed_hashes:
                            print(f"⚡ [Cache Skip] 此 prompt 的 cached 回應上次已失敗，重新呼叫 LLM")
                            del _prompt_cache[prompt_hash]
                            _failed_hashes.discard(prompt_hash)
                        else:
                            print(f"⚡ [Cache Hit] 相同 prompt 已呼叫過，跳過重複 LLM call")
                            raw_response = _prompt_cache[prompt_hash]
                            # Cache hit：直接提取代碼後跳出 retry loop，避免用同一個回應重複嘗試 3 次
                            new_code_raw, reflection = RefiningLoop._extract_reflection_from_response(raw_response)
                            new_code = LLMClient.extract_code(new_code_raw) or new_code_raw
                            break
                    else:
                        # [Tier-3 Escalation] Disabled: user wants to stay on primary model (e.g. Opus 4.7)
                        _use_r1 = False
                        _is_repeated = any(isinstance(e, dict) and str(e.get("error_type", "")).startswith("REPEATED_") for e in reflection_memory)
                        _is_surgical = getattr(_triage_result, 'is_surgical', False) if _triage_result else patch_mode
                        
                        if _is_repeated and not _is_surgical:
                            # print(f"🧠 [Tier-3] 檢測到相同錯誤簽名，但根據設定維持主模型模式...")
                            _use_r1 = False
                        elif i >= 2 and _triage_result is not None:
                            _is_hard_spatial = (
                                getattr(_triage_result, 'category', '') in ("LAYOUT_OR_VISUAL", "RENDER_ERROR")
                                or consecutive_timeouts >= 1
                            )
                            if _is_hard_spatial:
                                # print(f"🧠 [Tier-3] 進入第 {i+1} 輪，維持主模型進行深度修復...")
                                _use_r1 = False

                        # [Self-Consistency] Adaptive N: surgical=1, first iteration=2, subsequent=1
                        # Reflection memory already guides later iterations, N>1 adds latency without proportional gain
                        if _triage_result and getattr(_triage_result, 'is_surgical', False):
                            _n_samples = 1
                        elif i == 0:
                            _n_samples = 2
                        else:
                            _n_samples = 1

                        _cstart = time.time()
                        if _use_r1:
                            # R1 單次呼叫（不做 self-consistency，R1 自帶 chain-of-thought 多樣性）
                            _r1_response = llm.ask_for_fix(history_context, feedback_for_llm, use_r1=True)
                            raw_responses = [_r1_response]
                        else:
                            print(f"⚡ [Self-Consistency] 啟動 N={_n_samples} 平行採樣以確保反思品質...")
                            raw_responses = llm.ask_for_fix_n(history_context, feedback_for_llm, n=_n_samples, temperature=0.5)
                        llm.session_stats["time_coder_sec"] += (time.time() - _cstart)
                        
                        candidates = []
                        for resp in raw_responses:
                            code_raw, ref = RefiningLoop._extract_reflection_from_response(resp)
                            code = LLMClient.extract_code(code_raw) or code_raw
                            if not code and code_raw:
                                code = code_raw
                            candidates.append({
                                "raw_response": resp,
                                "new_code": code,
                                "reflection": ref
                            })
                        
                        if not candidates:
                            print("⚠️ [Self-Consistency] 所有 worker 連線失敗（candidates 為空），中止本輪修復。")
                            break

                        valid_refs = [c for c in candidates if c["reflection"]]
                        if not valid_refs:
                            best_candidate = candidates[0]
                            print("⚠️ [Self-Consistency] 未取得有效的反思 JSON，降級使用第一個結果。")
                        else:
                            from collections import Counter
                            targets = [c["reflection"].get("bad_code", "").strip() for c in valid_refs]
                            most_common_target, count = Counter(targets).most_common(1)[0]
                            
                            if len(valid_refs) == 1:
                                best_candidate = valid_refs[0]
                            elif count >= 2:
                                print(f"🎯 [Self-Consistency] 達成共識 (票數 {count}/{len(valid_refs)}) 鎖定錯誤代碼: {most_common_target[:30]}...")
                                best_candidate = next(c for c in valid_refs if c["reflection"].get("bad_code", "").strip() == most_common_target)
                            else:
                                print("⚠️ [Self-Consistency] 意見分歧，選擇 rationale 寫得最長的候選者。")
                                best_candidate = max(valid_refs, key=lambda c: len(c["reflection"].get("rationale", "")))
                        
                        raw_response = best_candidate["raw_response"]
                        new_code = best_candidate["new_code"]
                        reflection = best_candidate["reflection"]
                        
                        _prompt_cache[prompt_hash] = raw_response

                    # Task 9 Layer 1: 去重後 append
                    if reflection:
                        if not RefiningLoop._dedup_reflection(reflection_memory, reflection):
                            reflection_memory.append(reflection)
                        else:
                            # [Dedup Fix] LLM generated the same bad pattern again.
                            # Don't append the duplicate — but DO inject a redirect entry so the
                            # next iteration sees fresh signal instead of identical history_context
                            # (which causes prompt_cache hit → same output again).
                            _err_type = reflection.get("error_type", "UNKNOWN")
                            _bad_snip = str(reflection.get("bad_code", ""))[:80]
                            _redirect = {
                                "error_type": f"REPEATED_{_err_type}",
                                "bad_code": _bad_snip,
                                "good_code": "⚠️ You have generated this same error MULTIPLE TIMES. "
                                             "The approach is fundamentally broken. "
                                             "You MUST choose a completely different implementation strategy. "
                                             "Do NOT use the same pattern again.",
                                "rationale": f"Dedup triggered: same error_type='{_err_type}' and bad_code signature seen again. "
                                             "Switch to an entirely different approach.",
                            }
                            reflection_memory.append(_redirect)
                            print(f"⚡ [Reflection Dedup] 相同簽名已存在，注入 REPEATED redirect 強制換方向")
                    elif raw_response and "<reflection>" not in raw_response:
                        reflection_memory.append(f"[Failed to parse JSON reflection] {raw_response[:200]}")
                    
                    if new_code and len(new_code.strip()) > 0:
                        if patch_mode:
                            print("🩹 [Patching] Applying unified diff patch...")
                            patched_code = apply_patch_block(current_code, new_code)
                            if patched_code:
                                new_code = patched_code
                                break
                            else:
                                # Bug #9: If patch fails, fallback to full rewrite
                                # First, strip the code block from the error message to avoid LLM hallucinating
                                # on its own code.
                                code_block_pattern = re.compile(
                                    r"```(?:python)?\n"  # Start of code block
                                    r"(.*?)"  # Non-greedy match for content
                                    r"```",  # End of code block
                                    re.DOTALL
                                )
                                # Remove it from the fallback prompt
                                patch_error_stripped = re.sub(code_block_pattern, "", last_error_message)
                                
                                # Re-triage the stripped error message to get the correct patch_mode
                                _triage_stripped = diagnoser.diagnose_only(patch_error_stripped)
                                
                                print("🔄 [Fallback Rewrite] SEARCH/REPLACE failed. Switching to Full Rewrite mode.")
                                patch_mode = False  # [Bug 2 Fix] Force full rewrite — do NOT let patch_mode carry over
                                _code_for_llm = RefiningLoop.strip_injected_snippets(current_code)
                                base_fix = diagnoser.generate_fix_prompt(patch_error_stripped, _code_for_llm, script_json, triage_result=_triage_stripped, slim=(i > 0))
                                
                                feedback_for_llm = f"""
{base_fix}

{history_context}

**CRITICAL**: Review the 'Past Lessons Learned' above and **strictly avoid** making the same mistakes again.

**BEFORE writing code**, first analyze this failure in a <reflection> block:
<reflection>
{_REFLEXION_JSON_SCHEMA}
</reflection>

Then provide the corrected code.
"""
                                continue
                        else:
                            break
            except LLMError as e:
                print(f"❌ [LLM Failure] API 呼叫失敗，跳過本次迭代：{e}")
                i += 1
                continue
            
            if not new_code or len(new_code.strip()) == 0:
                i += 1
                continue

            if not patch_mode: 
                new_code = re.sub(r'class\s+\w+\(Scene\):', f'class {scene_name}(Scene):', new_code, count=1)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_code)

            # [Bug 2 Fix] Post-write sanity check — reject gibberish writes (e.g., raw <<< SEARCH blocks)
            _syntax_rollback = False
            try:
                compile(new_code, file_path, 'exec')
            except SyntaxError as _sanity_err:
                print(f"🛡️ [Safety] 新代碼語法無效 ({_sanity_err})，回滾至上一版本並清除 cache...")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(current_code)
                # [Bug 3 Fix] Mark this prompt hash as failed so cache won't reuse it
                _failed_hashes.add(prompt_hash)
                if prompt_hash in _prompt_cache:
                    del _prompt_cache[prompt_hash]
                # [Bug 4 Fix] Poison the next iteration's feedback so it doesn't produce the same
                # broken output again (same prompt → same LLM output → infinite SyntaxError loop).
                _syntax_rollback = True
                last_error_message = (
                    f"SyntaxError in generated code: {_sanity_err}\n"
                    f"The previous repair attempt produced code that failed Python's compile() check at "
                    f"line {_sanity_err.lineno}: {_sanity_err.msg}. "
                    f"The offending snippet: {repr(_sanity_err.text)}. "
                    f"You must write syntactically valid Python. Start fresh — do NOT reuse "
                    f"the broken structure from the previous attempt."
                )

            # Increment the appropriate counter
            if is_linter_only_failure and linter_only_retries < LINTER_RETRY_BUDGET:
                linter_only_retries += 1
                print(f"🔁 [Linter Budget] 使用 linter 額外重試額度 ({linter_only_retries}/{LINTER_RETRY_BUDGET})，不消耗渲染預算")
            else:
                i += 1

        print(f"\n❌ 遺憾：已達到最大嘗試次數 ({max_attempts})，自動修復停止。")
        
        # [Fallback] Even if we didn't get a perfect Visual PASS, archive the latest successful render
        # so that run_evaluation.py doesn't fail with FileNotFoundError.
        if last_successful_video_path and os.path.exists(last_successful_video_path):
            print("📦 [Fallback] Archiving 'Best Effort' video to stable_outputs for evaluation.")
            output_folder = "stable_outputs"
            os.makedirs(output_folder, exist_ok=True)
            
            name_source = backup_filename_prefix if backup_filename_prefix else user_topic
            safe_name = "".join([c if c.isalnum() or c in "._-" else "_" for c in name_source])[:50]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            backup_video_path = os.path.join(output_folder, f"{safe_name}_{timestamp}.mp4")
            shutil.copy2(last_successful_video_path, backup_video_path)
            
            if os.path.getsize(file_path) > 0:
                backup_py_path = os.path.join(output_folder, f"{safe_name}_{timestamp}.py")
                shutil.copy2(file_path, backup_py_path)
                
            rag_retriever.close()
            _fill_diagnostics(True, "max_iterations")
            return backup_video_path

        rag_retriever.close()
        _fill_diagnostics(False, "max_iterations")
        return False
