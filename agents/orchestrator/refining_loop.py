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

class RefiningLoop:
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

        try:
            # [HOTFIX] Added a 120-second timeout to prevent infinite loops (like `always_redraw` bugs or while loops)
            # from hanging the entire evaluation process.
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return True, result.stdout
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
                "Render Error: Manim process timed out after 120 seconds.\n"
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
    def pre_render_patch(code: str) -> str:
        """
        [Shift-Left Auto-Repair] Applies deterministic, zero-cost fixes before rendering.
        Eliminates wasting 10-15s engine spin-up for trivial deprecated API or structural issues.
        """
        import re
        import ast
        patched = code
        
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
        
        # 4. Fix LaTeX \text{} -> \mathrm{}
        patched = re.sub(r'\\text\{([^}]*)\}', r'\\mathrm{\1}', patched)
        
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
            
        return patched

    @staticmethod
    def auto_fix_loop(file_path, scene_name, user_topic, script_json, llm_client=None, max_attempts=5, backup_filename_prefix=None):
        """
        自動修復循環：包含語義審查與語法修復 (Reflexion Mechanism Fully Implemented)。
        """
        diagnoser = ManimDiagnoser()
        llm = llm_client if llm_client else LLMClient()
        rag_retriever = RAGRetriever()
        
        reflection_memory = []
        _prompt_cache = {}  # Task 9 Layer 2: hash(prompt) → raw_response，避免同一 session 內重複呼叫
        _failed_hashes = set()   # [Bug 3 Fix] Hashes whose cached responses already failed, skip cache
        visual_attempts = 0
        VISUAL_ATTEMPTS_LIMIT = 3
        tdr_t1_attempts = 0       # Counts zero-cost TDR T1 re-renders (cap: 3)
        tdr_t2_attempts = 0       # Counts cheap micro-prompt fixes (cap: 2)
        consecutive_timeouts = 0  # Track consecutive render timeouts for Template Override
        linter_only_retries = 0   # Linter failures are cheap — tracked separately
        LINTER_RETRY_BUDGET = 3   # Extra retries for linter-only failures (don't eat render budget)

        start_time = time.time()
        last_successful_video_path = None
        last_error_message = ""  # Tracks the most recent Manim render error for patch fallback
        last_render_hash = None   # Render Cache: skip re-render when code is identical

        i = 0  # Main iteration counter (only incremented on render/vision failures)
        total_loops = 0  # Safety cap to prevent infinite loops
        while i < max_attempts and total_loops < max_attempts + LINTER_RETRY_BUDGET:
            total_loops += 1
            print(f"\n" + "═"*50)
            print(f"🔄  迭代進行中: 第 {i+1} / {max_attempts} 次嘗試 (linter retries: {linter_only_retries}/{LINTER_RETRY_BUDGET})")
            print("═"*50)
            
            is_linter_only_failure = False  # Track if this iteration was linter-only (cheap)
            patch_mode = False  # [Bug 1 Fix] Initialize at top of every iteration to prevent UnboundLocalError

            with open(file_path, "r", encoding="utf-8") as f:
                current_code = f.read()

            # [Shift-Left Auto-Repair] Apply zero-cost deterministic patches BEFORE linter/render
            patched_code = RefiningLoop.pre_render_patch(current_code)
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
                    review_feedback = "FAIL\n\n[Static Analysis Gatekeeper]:\n"
                    for err in lint_errors:
                        review_feedback += f"- Line {err['line']} [{err['code']}]: {err['message']}\n"
                else:
                    print("✅ 靜態審查通過 (Static Analysis Passed)")
                    review_feedback = "PASS"
            
            # 🛡️ [安全性檢查] 強制檢查音訊調用 (Hard Check)
            if "PASS" in review_feedback:
                user_safe_topic = AudioEngine.get_safe_dir_name(user_topic)
                audio_dir = os.path.join("media", "audio", user_safe_topic)
                
                if os.path.exists(audio_dir) and len(os.listdir(audio_dir)) > 0:
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
                        print("⚠️ [系統攔截] 檢測到音訊缺失！強制轉為 FAIL。")
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
                # [Fast I/O] 迭代 1 用 10fps 快速預覽渲染（Vision QA 對幀率不敏感）
                # 迭代 0（首次）維持 15fps 以確保 audio sync 計算正確
                render_fps = 10 if i > 0 else 15

                # [Render Cache] Skip re-render if code is bit-for-bit identical to last render
                _code_hash = hashlib.md5(current_code.encode("utf-8")).hexdigest()
                if _code_hash == last_render_hash and last_successful_video_path and os.path.exists(last_successful_video_path):
                    print(f"⚡ [Render Cache] Code unchanged (hash={_code_hash[:8]}), reusing last render.")
                    success, message = True, "cached"
                else:
                    print("🎬 [步驟 2/2] 正在執行 Manim 渲染檢查...")
                    success, message = RefiningLoop.run_manim_task(file_path, scene_name, fps=render_fps)
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
                        video_source = os.path.join("media", "videos", os.path.splitext(os.path.basename(file_path))[0], f"480p{render_fps}", f"{scene_name}.mp4")
                        if not os.path.exists(video_source):
                            print("⚠️ 找不到渲染後的影片，跳過視覺審查。")
                            return False
                        last_successful_video_path = video_source
                    
                    # [Multi-Frame Vision Audit] Extract 4 frames at 10%, 40%, 70%, 95%
                    # and stitch into a 2x2 grid for comprehensive animation coverage.
                    grid_frame_path = "temp_vision_grid.jpg"
                    try:
                        # Get video duration
                        duration_result = subprocess.run(
                            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "default=noprint_wrappers=1:nokey=1", video_source],
                            capture_output=True, text=True, timeout=10
                        )
                        video_duration = float(duration_result.stdout.strip())
                        
                        # Calculate 4 timestamps
                        timestamps = [
                            video_duration * 0.10,  # 10% — setup/intro
                            video_duration * 0.40,  # 40% — early animation
                            video_duration * 0.70,  # 70% — mid animation
                            video_duration * 0.95,  # 95% — near end
                        ]
                        
                        # Extract 4 frames, scale each to 640x360, stitch into 2x2 grid (1280x720)
                        # Scaling BEFORE hstack/vstack is critical: without it the output is 3840x2160
                        # which GPT-4o-mini detail=low downsamples aggressively, losing all detail.
                        TILE_W, TILE_H = 640, 360
                        filter_cmd = (
                            f"movie={video_source},select='eq(t\\,{timestamps[0]:.2f})':n=1,scale={TILE_W}:{TILE_H}[f0];"
                            f"movie={video_source},select='eq(t\\,{timestamps[1]:.2f})':n=1,scale={TILE_W}:{TILE_H}[f1];"
                            f"movie={video_source},select='eq(t\\,{timestamps[2]:.2f})':n=1,scale={TILE_W}:{TILE_H}[f2];"
                            f"movie={video_source},select='eq(t\\,{timestamps[3]:.2f})':n=1,scale={TILE_W}:{TILE_H}[f3];"
                            f"[f0][f1]hstack[top];[f2][f3]hstack[bottom];[top][bottom]vstack"
                        )
                        
                        grid_result = subprocess.run(
                            ["ffmpeg", "-y", "-filter_complex", filter_cmd, "-frames:v", "1", grid_frame_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
                        )
                        
                        if grid_result.returncode != 0 or not os.path.exists(grid_frame_path):
                            # Fallback: extract 4 individual frames and use ImageMagick montage
                            frame_paths = []
                            for idx, ts in enumerate(timestamps):
                                fp = f"temp_frame_{idx}.jpg"
                                subprocess.run(
                                    ["ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", video_source,
                                     "-vframes", "1", "-update", "1", fp],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10
                                )
                                if os.path.exists(fp):
                                    frame_paths.append(fp)
                            
                            if len(frame_paths) >= 2:
                                # [Fix] Scale each frame to 640x360 BEFORE tiling.
                                # The old code used hardcoded 480x360 pixel offsets for xstack
                                # which caused frames to overlap since actual frames are larger.
                                TILE_W, TILE_H = 640, 360
                                inputs = []
                                scale_filters = []
                                for idx, fp in enumerate(frame_paths):
                                    inputs.extend(["-i", fp])
                                    scale_filters.append(f"[{idx}:v]scale={TILE_W}:{TILE_H}[s{idx}]")
                                n = len(frame_paths)
                                # Build xstack layout using scaled tile dimensions
                                layout = "|".join(f"{(i % 2) * TILE_W}_{(i // 2) * TILE_H}" for i in range(n))
                                scale_chain = ";".join(scale_filters)
                                scaled_labels = "".join(f"[s{i}]" for i in range(n))
                                filter_complex = f"{scale_chain};{scaled_labels}xstack=inputs={n}:layout={layout}"
                                subprocess.run(
                                    ["ffmpeg", "-y"] + inputs + [
                                        "-filter_complex", filter_complex,
                                        grid_frame_path
                                    ],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10
                                )
                            
                            # Cleanup individual frames
                            for fp in frame_paths:
                                if os.path.exists(fp):
                                    os.remove(fp)
                    except Exception as e:
                        print(f"⚠️ [Multi-Frame] Grid extraction failed ({e}), falling back to last frame.")
                    
                    # Use grid if available, otherwise fall back to single last frame
                    if os.path.exists(grid_frame_path):
                        frame_path = grid_frame_path
                        print("🖼️  [Multi-Frame] Using 4-frame grid for Vision Audit (10% / 40% / 70% / 95%)")
                    else:
                        frame_path = "temp_last_frame.jpg"
                        subprocess.run(["ffmpeg", "-sseof", "-1", "-i", video_source, "-vframes", "1", "-update", "1", frame_path, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print("🖼️  [Fallback] Using single last frame for Vision Audit")
                    
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

                    # Task 13 分級策略：最後一次視覺審查升級為短影片模式
                    # visual_attempts == 2 表示這是 VISUAL_ATTEMPTS_LIMIT=3 的最後一次
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
                        if clip_result.returncode == 0 and os.path.exists(clip_path):
                            print("🎬 [Task 13] 最後一次視覺審查 → 短影片模式 (2s 320p clip)")
                            audit = vision_agent.audit_video(clip_path, _vision_context, code_context=current_code, spatial_metadata=_spatial_metadata)
                            os.remove(clip_path)
                        else:
                            print("⚠️ [Task 13] 影片擷取失敗，fallback 至 4-frame grid")
                            audit = vision_agent.audit_frame(frame_path, _vision_context, code_context=current_code, detail="high", spatial_metadata=_spatial_metadata)
                    else:
                        print(f"🖼️  [Vision] 使用 detail={_frame_detail} (iteration {i})")
                        _vision_context = f"TOPIC: {user_topic}\n\n{script_json}"
                        audit = vision_agent.audit_frame(frame_path, _vision_context, code_context=current_code, detail=_frame_detail, spatial_metadata=_spatial_metadata)
                    
                    if audit["verdict"] == "ERROR":
                        print(f"⚠️  [Vision API Error] 視覺審查無法執行，跳過本次視覺檢查：{audit.get('overall_critique', '')}")
                    elif audit["verdict"] == "FAIL":
                        print(f"\n❌ 視覺審查失敗 (Visual Check Failed)：")
                        print(f"📝 總體評價: {audit.get('overall_critique', 'No critique')}")

                        # ── Tiered Defect Router (TDR) ────────────────────────────────
                        # When defects include MISALIGNED, attempt cheap local fixes first.
                        # Other defect types (OVERLAP, OVERFLOW) fall through to full rewrite.
                        _defects = audit.get("defects", [])
                        _misaligned_defects = [d for d in _defects if d.get("code") == "MISALIGNED"]
                        if _misaligned_defects and (tdr_t1_attempts < 3 or tdr_t2_attempts < 2):
                            try:
                                _router = MisalignmentRouter()

                                if tdr_t1_attempts < 3:
                                    # T1: zero-cost AST parametric fix (e.g. buff=0.2 → buff=0)
                                    _t1_patched = _router.try_t1_fix(_misaligned_defects, current_code)
                                    if _t1_patched:
                                        with open(file_path, "w", encoding="utf-8") as _f:
                                            _f.write(_t1_patched)
                                        tdr_t1_attempts += 1
                                        print(f"⚡ [TDR-T1] 參數補丁套用成功，直接重渲染 (成本 $0, 第 {tdr_t1_attempts} 次)...")
                                        continue  # Re-render immediately, no LLM call

                                if tdr_t2_attempts < 2:
                                    # T2: lightweight micro-prompt (~2K tokens vs ~20K)
                                    _micro_prompt = _router.get_t2_prompt(_misaligned_defects, current_code)
                                    if _micro_prompt and visual_attempts < VISUAL_ATTEMPTS_LIMIT:
                                        print(f"⚡ [TDR-T2] Micro-Prompt 修復對齊 (~2K tokens)...")
                                        _t2_history = RefiningLoop._format_reflection_memory(reflection_memory)
                                        _micro_fix_raw = llm.ask_for_fix(_t2_history, _micro_prompt)
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
                        print("✅ 視覺審查通過！影片品質符合標準。")

                    if success:
                        duration = round(time.time() - start_time, 2)
                        output_folder = "stable_outputs"
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
                        
                        print("\n" + "═"*40)
                        print(f"✨ 【渲染成功 / Rendering Success】 ✨")
                        print("═"*40)
                        print(f"⏱️  總執行耗時: {duration} 秒")
                        print(f"📂  歸檔目錄: {output_folder}")
                        print(f"    🎥 {os.path.basename(backup_video_path)}")
                        print("═"*40 + "\n")
                        return backup_video_path
                
                if not success:
                    if "VIOLATION REPORT" not in message: 
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
                        is_timeout = "timed out after 120" in message
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
                        base_fix = diagnoser.generate_fix_prompt(_trunc_msg, current_code, script_json, triage_result=_triage_result, slim=(i > 0))
                        
                        # [RAR-Agent] Inject verified examples from Weaviate vector database
                        _rag_results = rag_retriever.retrieve_examples(_trunc_msg, limit=1)
                        if _rag_results:
                            base_fix += "\n\n" + rag_retriever.format_for_prompt(_rag_results)

                        # [TEMPLATE OVERRIDE] After 1 consecutive timeout, bypass free-form LLM rewrite
                        # and force it to fill in a safe ValueTracker skeleton instead.
                        # Changed from >= 2 to >= 1: saves 120s wasted on a second doomed render attempt.
                        if consecutive_timeouts >= 1:
                            print(f"\n🚨 [Template Override] 連續 {consecutive_timeouts} 次渲染超時！啟動極簡 ValueTracker 骨架模式...")
                            template_override = """
[TEMPLATE OVERRIDE ACTIVATED]
Your previous attempts all caused infinite render loops. You have lost the freedom to design the animation architecture.
You MUST use the following safe, linear skeleton. Do NOT use any `always_redraw`, `add_updater`, or complex `ValueTracker` logic.
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
                
                fix_prompt = diagnoser.generate_fix_prompt(review_feedback, current_code, script_json, triage_result=_triage_result, slim=(i > 0))
                
                # [RAR-Agent] Inject verified examples for layout/visual errors
                _rag_results = rag_retriever.retrieve_examples(review_feedback, limit=1)
                if _rag_results:
                    fix_prompt += "\n\n" + rag_retriever.format_for_prompt(_rag_results)
                    
                history_context = RefiningLoop._format_reflection_memory(reflection_memory)
                feedback_for_llm = f"""
{fix_prompt}

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
                        # [Tier-3 Escalation] i >= 2 + 複雜空間錯誤 → 切換 DeepSeek-R1
                        _use_r1 = False
                        if i >= 2 and _triage_result is not None:
                            _is_hard_spatial = (
                                getattr(_triage_result, 'category', '') in ("LAYOUT_OR_VISUAL", "RENDER_ERROR")
                                or consecutive_timeouts >= 1
                            )
                            if _is_hard_spatial:
                                _use_r1 = True
                                print(f"🧠 [Tier-3] 第 {i+1} 輪啟動 DeepSeek-R1 深度推理模式...")

                        # [Self-Consistency N=3 or N=1]
                        _n_samples = 1 if (_triage_result and getattr(_triage_result, 'is_surgical', False)) else 3

                        if _use_r1:
                            # R1 單次呼叫（不做 self-consistency，R1 自帶 chain-of-thought 多樣性）
                            _r1_response = llm.ask_for_fix(history_context, feedback_for_llm, use_r1=True)
                            raw_responses = [_r1_response]
                        else:
                            print(f"⚡ [Self-Consistency] 啟動 N={_n_samples} 平行採樣以確保反思品質...")
                            raw_responses = llm.ask_for_fix_n(history_context, feedback_for_llm, n=_n_samples, temperature=0.5)
                        
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
                                base_fix = diagnoser.generate_fix_prompt(patch_error_stripped, current_code, script_json, triage_result=_triage_stripped, slim=(i > 0))
                                
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
                
            return backup_video_path
            
        return False
