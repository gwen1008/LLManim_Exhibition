# main.py
import os
import sys
import json
import re
import concurrent.futures

# New Orchestrator Modules
from agents.orchestrator.translator import AcademicTranslator
from agents.orchestrator.router import TaskRouter
from agents.orchestrator.refining_loop import RefiningLoop

# Agent Modules
from agents.planner.planner import Planner
from agents.coder.prompter import CoderPrompter
from agents.core.llm_client import LLMClient
from agents.core.logger import SessionLogger
from agents.core.pipeline_config import StageTimer


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


def _inject_audio_sync(code: str, updated_sequence: list, final_audio_path: str) -> str:
    """
    [Optimization V4 / V5] Post-inject audio sync code into Coder-generated Manim code.

    因為 Coder 與 Audio 並行執行，Coder 產出的程式碼不含正確音訊路徑。
    此函數在兩者都完成後：
      1. 清除 LLM 自己寫的假音訊 block（os.path.exists 模板）— 防止 double-play
      2. 將每個 step 對應到 updated_sequence 中的 audio_path 和 duration
      3. 在 # Step N 標記前插入正確的 self.add_sound() + self.wait() padding
      4. Fallback: 若對不上 step 標記，在 construct() 開頭插入 final_narrative.mp3
    """
    import re as _re

    # === Step 0: 清除 LLM 生成的假音訊 block ===
    # 模式: audio_stepN = "..." / if os.path.exists(audio_stepN): / self.add_sound(...) / elif ...
    # 這些是 LLM 用猜測路徑寫的，會與 auto-injected 的正確路徑衝突造成 double-play 或 overlap
    fake_audio_pattern = _re.compile(
        r'[ \t]*audio_step\w+\s*=\s*["\'][^"\']+["\'][^\n]*\n'   # audio_stepN = "..."
        r'(?:[ \t]*if\s+os\.path\.exists\([^\)]+\):[^\n]*\n'      # if os.path.exists(...):
        r'[ \t]*self\.add_sound\([^\)]+\)[^\n]*\n'                 # self.add_sound(...)
        r'(?:[ \t]*elif[^\n]*\n[ \t]*self\.add_sound\([^\)]+\)[^\n]*\n)?)?',  # elif ... (optional)
        _re.MULTILINE
    )
    cleaned, n_removed = fake_audio_pattern.subn('', code)
    if n_removed > 0:
        code = cleaned
        print(f"🧹 [Audio Inject] 清除 {n_removed} 個 LLM 假音訊 block，防止 double-play")

    # 收集有 audio_path 的 steps
    audio_steps = [
        (i, s) for i, s in enumerate(updated_sequence)
        if s.get("audio_path")
    ]

    if not audio_steps:
        return code  # 沒有音訊，原樣返回

    # === Step 1: 逐步注入（匹配 # Step N 標記）===
    step_pattern = _re.compile(r'^( +)(# Step \d+)', _re.MULTILINE)
    step_markers = list(step_pattern.finditer(code))

    injected = False
    if step_markers and len(audio_steps) > 0:
        # 從後往前插入，避免 offset 位移
        n_inject = min(len(step_markers), len(audio_steps))
        for marker_idx in range(n_inject - 1, -1, -1):
            match = step_markers[marker_idx]
            indent = match.group(1)
            step_i, step_data = audio_steps[marker_idx]
            audio_path = step_data["audio_path"]
            duration = step_data.get("duration", 2.0)
            dur_var = f"_audio_dur_{marker_idx}"

            # 注入 add_sound（含實際 duration 供後面 wait 參考）
            inject_lines = (
                f'{indent}self.add_sound("{audio_path}")  # [auto-injected] duration={duration:.2f}s\n'
                f'{indent}{dur_var} = {duration:.2f}  # [audio-sync] actual TTS duration\n'
            )
            code = code[:match.start()] + inject_lines + code[match.start():]

        # === Step 2: 不替換 remaining_N 公式 ===
        # Coder 寫的 remaining_N = max(0.1, _audio_dur_{N-1} - anim_time_N + 0.5) 是正確的
        # _audio_dur_N 變數已在 Step 1 注入，Coder 的公式直接引用即可
        # 注意：不要替換成全時長，否則每步 wait = anim_time + full_audio → 影片 2x 時長

        injected = True
        print(f"🎵 [Audio Post-Inject] 成功注入 {n_inject} 個 self.add_sound()，wait 同步至實際 TTS 時長")

    # Fallback: 若 step 標記對不上，退而注入 final_narrative 在 construct() 開頭
    if not injected:
        construct_match = _re.search(r'(def construct\(self\):\s*\n)', code)
        if construct_match and final_audio_path:
            insert_pos = construct_match.end()
            next_line = code[insert_pos:insert_pos + 80]
            indent_match = _re.match(r'^(\s+)', next_line)
            indent = indent_match.group(1) if indent_match else "        "
            inject_line = f'{indent}self.add_sound("{final_audio_path}")  # [auto-injected: full narration]\n'
            code = code[:insert_pos] + inject_line + code[insert_pos:]
            print(f"🎵 [Audio Post-Inject] Fallback: 注入 final_narrative 在 construct() 開頭")
        else:
            print("⚠️ [Audio Post-Inject] 無法注入音訊同步碼（找不到 construct 或 step 標記）")

    return code

if __name__ == "__main__":
    print("\n" + "╔" + "═"*48 + "╗")
    print("║" + " "*10 + "EMA System: Multi-stage Manim Agent" + " "*9 + "║")
    print("╚" + "═"*48 + "╝")
    
    user_input = input("\n請輸入動畫主題 (或輸入已存在的 .py 檔名直接播放): ")
    
    # Initialize session logger
    logger = SessionLogger(max_files=1000, max_age_days=30)
    
    try:
        # Start logging session
        logger.start_session(user_input)
        
        target_scene = "GeneratedScene"
        target_file = "test_script.py"
        
        # 共享 LLMClient 以統計總 Token 與成本
        llm = LLMClient()

        # 1. 檢查是否為直接執行現有檔案
        if user_input.endswith(".py") and os.path.exists(user_input):
            print(f"\n📂 檢測到現有檔案，正在啟動播放模式...")
            success, message = RefiningLoop.run_manim_task(user_input, target_scene)
            if not success:
                print(f"❌ 執行失敗，錯誤訊息：\n{message}")
            sys.exit(0)

        # 2. 智能路由 (Smart Task Router)
        # 暫時註解掉，確保 run_evaluation.py 所有的題目都會跑完整的 LLM 流程
        # router = TaskRouter()
        # is_arithmetic, num1, op, num2 = router.detect_arithmetic_task(user_input)
        # if is_arithmetic:
        #     video_path = router.route_to_template(user_input, num1, op, num2, target_scene, target_file, logger, llm)
        #     if video_path:
        #         sys.exit(0)

        # 3. 自動翻譯 (Academic Translator Agent)
        translator = AcademicTranslator(llm_client=llm)
        user_topic = translator.translate_to_english(user_input)

        # ========== 🎬 Original AI Pipeline (Planner + Coder) ==========

        # [Optimization V5] Start RAG task in parallel with Planner
        def _rag_task():
            print("\n📚 [階段 1.8: RAG Retrieval 並行中] 正在搜尋黃金範例...")
            from agents.core.rag_retriever import RAGRetriever as _RAG
            with StageTimer("RAG", llm.session_stats, "time_rag_sec"):
                _rag = _RAG()
                _results = _rag.retrieve_examples(user_topic, limit=2)
                _results += _rag.retrieve_rules(user_topic, limit=2)
                _ctx = _rag.format_for_prompt(_results)
                _rag.close()
            return _ctx
            
        _pipeline_executor = concurrent.futures.ThreadPoolExecutor(max_workers=6)
        _rag_future = _pipeline_executor.submit(_rag_task)

        # 階段一：Director 規劃 (Planner)
        print("\n🎬 [階段 1: Director] 正在規劃動畫腳本...")
        from agents.core.llm_client import LLMError
        planner = Planner(llm_client=llm)
        _solution = os.environ.get("LLMANIM_SOLUTION", "").strip() or None
        _answer   = os.environ.get("LLMANIM_ANSWER",   "").strip() or None
        _ground_truth = {"answer": _answer, "solution": _solution} if (_answer or _solution) else None
        if _solution:
            print("📋 [Planner] Solution context provided — skipping math derivation.")
        with StageTimer("Planner", llm.session_stats, "time_planner_sec"):
            try:
                script_json, thought_tree_raw = planner.plan_script_from_prompt(user_topic, solution=_solution)
            except LLMError as e:
                print(f"❌ [Fatal] Planner LLM 完全失敗：{e}")
                sys.exit(1)

        # Planner compliance check: verify solution keywords appear in thought_tree (Route C only)
        if _solution and thought_tree_raw:
            _sol_keywords = [w for w in _solution.split() if len(w) > 3 and w.replace("$","").replace("\\","").strip()][:20]
            _matched = sum(1 for kw in _sol_keywords if kw in thought_tree_raw)
            _compliance = round(_matched / len(_sol_keywords), 2) if _sol_keywords else 0.0
            llm.session_stats["planner_solution_compliance"] = _compliance
            print(f"📊 [Planner Compliance] {_matched}/{len(_sol_keywords)} solution keywords found in thought_tree → {_compliance:.0%}")
        
        # [Optimization] Strip XML thought/reasoning blocks before parsing
        script_json_clean = re.sub(r'<thought_tree>.*?</thought_tree>', '', script_json, flags=re.DOTALL)
        script_json_clean = re.sub(r'<reasoning>.*?</reasoning>', '', script_json_clean, flags=re.DOTALL).strip()
        
        try:
            parsed_script = json.loads(script_json_clean)
        except Exception:
            extracted = _extract_first_json_object(script_json_clean)
            try:
                parsed_script = json.loads(extracted) if extracted else None
            except Exception:
                parsed_script = None
                print("⚠️  最終解析失敗，嘗試使用原始輸出做為上下文。")

        if parsed_script:
            script_json = json.dumps(parsed_script, ensure_ascii=False, indent=2)
            print(f"📉 [Compression] Planner Context Reduced: {len(script_json)} chars")
            
            # [Feature] Save the blueprint JSON for human review
            try:
                _out_dir = os.environ.get("EVAL_OUTPUT_DIR", "stable_outputs")
                os.makedirs(_out_dir, exist_ok=True)
                with open(os.path.join(_out_dir, "blueprint.json"), "w", encoding="utf-8") as f:
                    f.write(script_json)
                print(f"📄 [Blueprint] 已儲存完整劇本至: {os.path.join(_out_dir, 'blueprint.json')}")
            except Exception as e:
                print(f"⚠️ [Blueprint] Unable to save blueprint.json: {e}")

            # Task 11: Audio (Step 1.5) 與 RAG (Step 1.8) 並行執行，節省 15-28s
            from agents.utils.audio_engine import AudioEngine
            sequence_data = parsed_script.get("sequence") or parsed_script.get("scenes")

            def _audio_task():
                if not sequence_data:
                    return None, None
                print(f"\n🎙️ [階段 1.5: Audio Generation 並行中] 正在生成語音...")
                try:
                    audio_engine = AudioEngine(topic=user_topic)
                    return audio_engine.generate_narration(sequence_data)
                except Exception as e:
                    print(f"❌ 語音生成發生錯誤: {e}")
                    return None, None

            # [Optimization V4] Audio ‖ RAG ‖ Coder 三路並行。
            # Coder 內部先 block 等 RAG（~5-10s），拿到 rag_context 後立即呼叫 LLM。
            # Audio 並行跑，結果在 Coder 完成後才取用（Audio ~15-25s << Coder ~60-90s）。
            # spatial_hints 需在 Coder 啟動前算好（純 CPU，幾乎零耗時）
            if thought_tree_raw:
                _tt_truncated = thought_tree_raw[:500].strip()
                _tt_suffix = "\n... (truncated)" if len(thought_tree_raw) > 500 else ""
                spatial_hints = f"PLANNER SPATIAL HINTS:\n{_tt_truncated}{_tt_suffix}"
            else:
                spatial_hints = ""

            _audio_future = _pipeline_executor.submit(_audio_task)

            def _coder_task():
                """等 RAG 完成後立即啟動 Coder（T=0.3），不等 Audio。"""
                _rag_ctx = _rag_future.result()
                print("\n👨‍💻 [階段 2: Coder] 正在生成動畫程式碼...")
                coder_prompter = CoderPrompter()
                _cs, _cu = coder_prompter.generate_initial_prompt(
                    script_json, target_scene, rag_context=_rag_ctx, spatial_hints=spatial_hints
                )
                
                with StageTimer("Coder", llm.session_stats, "time_coder_sec", silent=True):
                    raw = llm.ask_for_fix(_cs, _cu, temperature=0.3)
                
                code = LLMClient.extract_code(raw)

                code = re.sub(r'class\s+\w+\(Scene\):', f'class {target_scene}(Scene):', code, count=1)
                code = re.sub(r'self\.wait\(([^)]+)\)', lambda m: f'self.wait(max(0.1, {m.group(1)}))', code)
                try:
                    compile(code, "<coder>", "exec")
                    print("✅ [Coder] T=0.3 通過編譯檢查")
                except SyntaxError as _se:
                    print(f"⚠️ [Coder] T=0.3 編譯失敗: {_se}，進入修復循環")
                return code

            _coder_future = _pipeline_executor.submit(_coder_task)

            try:
                first_code = _coder_future.result()
                updated_sequence, final_audio_path = _audio_future.result()
                rag_context = _rag_future.result()  # already resolved
            finally:
                _pipeline_executor.shutdown(wait=False)

            # [Optimization V4] Post-inject audio sync code into Coder's output.
            # Coder ran in parallel with Audio (no audio info in prompt), so we
            # retroactively inject self.add_sound() calls at each # Step marker.
            if updated_sequence is not None:
                key = "sequence" if "sequence" in parsed_script else "scenes"
                parsed_script[key] = updated_sequence
                script_json = json.dumps(parsed_script, ensure_ascii=False, indent=2)
                print(f"✅ 語音處理完成！合併音檔: {final_audio_path}")

                first_code = _inject_audio_sync(first_code, updated_sequence, final_audio_path)
        else:
            # [#7] Planner JSON parse failed — inject minimal fallback so Coder always
            # receives valid JSON instead of garbled raw Planner output.
            _raw_hint = script_json[:500] if isinstance(script_json, str) else ""
            _fallback = {
                "title": user_topic,
                "target_scene": target_scene,
                "notes": "Planner JSON parse failed. Generate animation from topic title only.",
                "raw_planner_hint": _raw_hint,
            }
            script_json = json.dumps(_fallback, ensure_ascii=False, indent=2)
            print("⚠️  [Fallback] Planner 解析失敗，已注入最小 fallback JSON")

            # [Optimization V5] RAG already submitted in parallel with Planner — reuse it
            print("\n📚 [階段 1.8: RAG Retrieval] 等待已提交的 RAG 結果...")
            rag_context = _rag_future.result()

            # Fallback path: no Audio, Coder runs after RAG
            print("\n👨‍💻 [階段 2: Coder] 正在生成動畫程式碼 (Best-of-3 並行)...")
            if thought_tree_raw:
                _tt_truncated = thought_tree_raw[:500].strip()
                _tt_suffix = "\n... (truncated)" if len(thought_tree_raw) > 500 else ""
                spatial_hints = f"PLANNER SPATIAL HINTS:\n{_tt_truncated}{_tt_suffix}"
            else:
                spatial_hints = ""
            coder_prompter = CoderPrompter()
            coder_system, coder_user = coder_prompter.generate_initial_prompt(
                script_json, target_scene, rag_context=rag_context, spatial_hints=spatial_hints
            )

            def _generate_candidate(temperature):
                with StageTimer("Coder", llm.session_stats, "time_coder_sec", silent=True):
                    raw = llm.ask_for_fix(coder_system, coder_user, temperature=temperature)
                
                code = LLMClient.extract_code(raw)
                code = re.sub(r'class\s+\w+\(Scene\):', f'class {target_scene}(Scene):', code, count=1)
                code = re.sub(
                    r'self\.wait\(([^)]+)\)',
                    lambda m: f'self.wait(max(0.1, {m.group(1)}))',
                    code
                )
                return code

            first_code = _generate_candidate(0.3)
            try:
                compile(first_code, "<coder>", "exec")
                print("✅ [Coder] T=0.3 通過編譯檢查")
            except SyntaxError as _se:
                print(f"⚠️ [Coder] T=0.3 編譯失敗: {_se}，進入修復循環")

            _pipeline_executor.shutdown(wait=False)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(first_code)

        # 階段三：自動修復與審查循環
        print("\n🔄 [階段 3: Review & Fix] 啟動自動校對與渲染循環...")
        from agents.core.llm_client import LLMError
        from agents.orchestrator.refining_loop_types import run_fix_loop
        try:
            loop_result = run_fix_loop(target_file, target_scene, user_topic, script_json, llm_client=llm, backup_filename_prefix=user_input)
            result = loop_result.video_path
        except LLMError as e:
            print(f"❌ [Fatal] LLM API 完全失敗：{e}")
            sys.exit(1)
            
        # ── 階段四：FinalJudge 兩階段品質評分 ─────────────────────────────
        if result and os.path.exists(str(result)):
            print("\n🏛️  [階段 4: FinalJudge] 啟動兩階段品質評分...")
            try:
                from agents.utils.final_judge import FinalJudge
                with open(target_file, "r", encoding="utf-8") as _cf:
                    _final_code = _cf.read()
                _fj = FinalJudge(llm_client=llm)
                _fj_result = _fj.judge(str(result), script_json, _final_code, ground_truth=_ground_truth)
                # Attach to session_stats so it's saved in cost_report.json
                llm.session_stats["final_judge"] = {
                    "weighted_total": _fj_result.get("weighted_total"),
                    "scores":         _fj_result.get("scores", {}),
                    "code_issues":    _fj_result.get("code_issues", []),
                }
            except Exception as _fj_err:
                print(f"⚠️  [FinalJudge] 評分失敗，不影響影片輸出：{_fj_err}")
        # ── 最終統計報告 ────────────────────────────────────────────────────
        print(llm.get_session_report())
        
    finally:
        logger.end_session()
        if 'llm' in locals():
            # [Improvement] Always save cost_report.json, even on failure.
            # Previously written only inside try block, so LLMError / timeout / crash would skip it,
            # making failed tasks show '—' in the cost dashboard instead of their true token cost.
            try:
                stable_out_dir = os.environ.get("EVAL_OUTPUT_DIR", "stable_outputs")
                os.makedirs(stable_out_dir, exist_ok=True)
                with open(os.path.join(stable_out_dir, "cost_report.json"), "w", encoding="utf-8") as f:
                    json.dump(llm.session_stats, f, indent=2)
            except Exception:
                pass  # Best-effort — don't let a logging failure crash the cleanup
            llm.close()