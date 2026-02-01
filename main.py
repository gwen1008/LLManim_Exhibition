import subprocess
import os
import sys
import time
import shutil
import json
from agents.planner import Planner
from agents.prompter import ManimDiagnoser, CoderPrompter
from agents.llm_client import LLMClient
from agents.reviewer import CodeReviewer
from agents.audio_engine import AudioEngine
from agents.rag_retriever import RAGRetriever
from agents.logger import SessionLogger


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


def run_manim_task(file_path, scene_name):
    """
    執行 Manim 指令並捕獲輸出。
    加上 -p 參數可以在渲染成功後自動播放影片。
    """
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"📄 [Debug] 準備渲染檔案: {file_path} (大小: {size} bytes)")
        if size == 0:
            return False, "錯誤：渲染目標檔案為空 (0 bytes)"
    else:
        return False, f"錯誤：找不到檔案 {file_path}"

    print(f"🚀 正在啟動 Manim 引擎進行渲染...")
    # -ql: 低畫質, -v ERROR: 只顯示錯誤 (移除 -p 避免與檔案移動衝突)
    cmd = ["manim", "-v", "ERROR", "-ql", file_path, scene_name]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except FileNotFoundError:
        return False, "錯誤：找不到 'manim' 指令。請確保已安裝 Manim 且路徑正確。"

def _format_reflection_memory(reflection_memory):
    """
    格式化反思記憶以注入到 LLM prompt 中。
    
    Args:
        reflection_memory: 包含過去教訓的列表
        
    Returns:
        格式化後的字符串
    """
    if not reflection_memory:
        return ""
    
    memory_section = "\n" + "="*60 + "\n"
    memory_section += "📚 **PAST LESSONS LEARNED** (Reflexion Memory)\n"
    memory_section += "="*60 + "\n"
    memory_section += "The following are lessons from PREVIOUS FAILED attempts.\n"
    memory_section += "STRICTLY AVOID making the same mistakes:\n\n"
    
    for idx, lesson in enumerate(reflection_memory, 1):
        memory_section += f"{idx}. {lesson}\n"
    
    memory_section += "="*60 + "\n"
    
    return memory_section


def auto_fix_loop(file_path, scene_name, user_topic, script_json, max_attempts=10):
    """
    自動修復循環：包含語義審查與語法修復 (Reflexion Mechanism Fully Implemented)。
    
    Core Logic:
    1. 讀取代碼 → 2. 語義審查 → 3. 渲染檢查 → 4. [失敗時] 自我反思 → 5. 修復 (注入記憶)
    """
    diagnoser = ManimDiagnoser()
    llm = LLMClient()
    reviewer = CodeReviewer()
    
    # [Reflexion] 1. 初始化長期記憶 Buffer (儲存過去的教訓)
    reflection_memory = []
    
    start_time = time.time()
    
    for i in range(max_attempts):
        print(f"\n" + "═"*50)
        print(f"🔄  迭代進行中: 第 {i+1} / {max_attempts} 次嘗試")
        print("═"*50)
        
        # 讀取當前代碼
        with open(file_path, "r", encoding="utf-8") as f:
            current_code = f.read()

        # ========== Phase 1: 語義審查 (QA Compliance Check) ==========
        print("🔍 [步驟 1/2] 正在進行代碼內容審查 (邏輯、公式、腳本一致性)...")
        review_feedback = reviewer.review_code(user_topic, current_code, script_json)
        
        # 🛡️ [安全性檢查] 強制檢查音訊調用 (Hard Check)
        # 必須在 PASS/FAIL 分支判斷之前執行，確保能正確觸發修復循環
        if "PASS" in review_feedback:
            user_safe_topic = user_topic.replace(" ", "_").replace(".", "_").replace("/", "_").replace("*", "x")
            audio_dir = os.path.join("media", "audio", user_safe_topic)
            
            # 如果音訊目錄存在且有檔案，但代碼中沒有 add_sound
            if os.path.exists(audio_dir) and len(os.listdir(audio_dir)) > 0:
                if "add_sound" not in current_code:
                    print("⚠️ [系統攔截] 檢測到 Reviewer 漏判音訊缺失！強制轉為 FAIL。")
                    review_feedback = """FAIL

[Audio Sync]: Critical Violation - Audio files generated but NOT used.
You MUST add `self.add_sound("media/audio/{}/step_XX.mp3")` for every step.
Do not verify this yourself, the system has confirmed audio files exist.
Fix this immediately.
""".format(user_safe_topic)
        
        # 現在根據最終的 review_feedback 進行分支
        if "PASS" in review_feedback:
            print("✅ 語義與佈局審查通過！執行渲染...")
            
            # ========== Phase 2: Manim 渲染檢查 (語法驗證) ==========
            print("🎬 [步驟 2/2] 正在執行 Manim 渲染檢查...")
            success, message = run_manim_task(file_path, scene_name)
            
            if success:
                # ========== Success Path: 備份成果並返回 ==========
                duration = round(time.time() - start_time, 2)
                print(f"\n✨ 【任務成功】 ✨")
                print(f"⏱️  總執行耗時: {duration} 秒")
                
                # 自動備份成果
                output_folder = "stable_outputs"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # 修正：星號及其他非法字元也需要替換，避免檔名問題
                safe_name = user_topic.replace(" ", "_").replace(".", "_")
                for char in '<>:"/\\|?*':
                    safe_name = safe_name.replace(char, "_")
                
                # 1. 備份影片檔案（先備份影片，因為這是最重要的）
                module_name = os.path.splitext(os.path.basename(file_path))[0]
                video_source = os.path.join("media", "videos", module_name, "480p15", f"{scene_name}.mp4")
                
                if os.path.exists(video_source):
                    backup_video_path = os.path.join(output_folder, f"{safe_name}.mp4")
                    # 使用 move 而非 copy，確保複製當前的影片並避免殘留
                    shutil.move(video_source, backup_video_path)
                    print(f"💾 影片已備份至: {backup_video_path}")
                    # 手動開啟影片預覽（BENCHMARK=1 時不播放，避免批量測試彈窗）
                    # 自動播放功能已停用
                    # if not os.environ.get("BENCHMARK"):
                    #     try:
                    #         print(f"▶️ 正在播放影片...")
                    #         if sys.platform == "win32":
                    #             os.startfile(backup_video_path)
                    #         else:
                    #             subprocess.run(["open", backup_video_path])
                    #     except Exception as e:
                    #         print(f"⚠️ 無法自動播放影片: {e}")
                else:
                    print(f"⚠️ 警告：未找到影片檔 {video_source}")
                    print(f"🔍 [Debug] Manim 可能未產生輸出。Manim 輸出日誌：")
                    print(message[:500] if message else "無輸出訊息")
                
                # 2. 備份 Python 程式碼
                backup_py_path = os.path.join(output_folder, f"{safe_name}.py")
                
                # 確保檔案有內容再複製（防止空檔案）
                if os.path.getsize(file_path) > 0:
                    shutil.copy(file_path, backup_py_path)
                    print(f"💾 代碼已備份至: {backup_py_path}")
                else:
                    print(f"⚠️ 警告：{file_path} 檔案為空，跳過備份")
                
                print(f"✅ 穩定版代碼與影片已歸檔至: {output_folder}/{safe_name}")

                    
                return True
            
            # ========== Rendering Failed Path ==========
            else:
                print(f"\n❌ 渲染失敗！捕捉到 Python/Manim 語法錯誤：")
                print("-" * 30)
                print(message)
                print("-" * 30)
                
                # [Reflexion] Step 2a: Self-Reflection on Rendering Failure
                print("\n🤔 [Reflexion] 正在進行自我反思 (Self-Reflection)...")
                reflection_prompt = f"""You are an expert Python/Manim Developer.

**FAILURE CONTEXT**:
You attempted to render a Manim animation but failed.

**ERROR MESSAGE**:
{message}

**YOUR TASK**:
1. Analyze the ROOT CAUSE of this error (e.g., syntax error, missing import, wrong API usage, etc.).
2. Provide a concise "Lesson Learned" (1-2 sentences) summarizing what went wrong and how to avoid it in future attempts.
3. **Do NOT generate code**. Only provide the lesson.

**OUTPUT FORMAT**:
Lesson: [Your concise lesson here]
"""
                lesson = llm.ask_for_fix(reflection_prompt)
                reflection_memory.append(f"[Rendering Error] {lesson}")
                print(f"💡 新增教訓: {lesson[:150]}...")

                # [Reflexion] Step 3: Prepare Fix Prompt with Injected Memory
                history_context = _format_reflection_memory(reflection_memory)
                feedback_for_llm = f"""
{diagnoser.generate_fix_prompt(message, current_code, script_json)}

{history_context}

**CRITICAL**: Review the "Past Lessons Learned" above and **strictly avoid** making the same mistakes again.
"""
        
        # ========== Semantic Review Failed Path ==========
        else:
            print(f"\n⚠️  語義/佈局審查未通過：")
            print("-" * 30)
            print(review_feedback)
            print("-" * 30)
            
            # [Reflexion] Step 2b: Self-Reflection on Semantic Review Failure
            print("\n🤔 [Reflexion] 正在進行自我反思 (Self-Reflection)...")
            reflection_prompt = f"""You are an expert Manim Developer.

**FAILURE CONTEXT**:
Your generated code failed the semantic review (QA Compliance Check).

**REVIEW FEEDBACK**:
{review_feedback}

**YOUR TASK**:
1. Analyze WHY the code failed the review (e.g., missing signal actions, incorrect audio sync, layout violations, etc.).
2. Provide a concise "Lesson Learned" (1-2 sentences) to avoid this in future iterations.
3. **Do NOT generate code**. Only provide the lesson.

**OUTPUT FORMAT**:
Lesson: [Your concise lesson here]
"""
            lesson = llm.ask_for_fix(reflection_prompt)
            reflection_memory.append(f"[Review Failure] {lesson}")
            print(f"💡 新增教訓: {lesson[:150]}...")
            
            # [Reflexion] Step 3: Prepare Fix Prompt with Injected Memory
            history_context = _format_reflection_memory(reflection_memory)
            feedback_for_llm = f"""
代碼審查失敗。請根據以下詳細建議修正代碼：

{review_feedback}

【參考腳本】:
{script_json}

【當前代碼】:
{current_code}

{history_context}

**CRITICAL**: Review the "Past Lessons Learned" above and **strictly avoid** making the same mistakes again.
"""

        # ========== Step 4: Request AI to Fix Code (with Memory Injection) ==========
        # ========== Step 4: Request AI to Fix Code (with Memory Injection) ==========
        print("\n🤖 正在將錯誤回傳給 AI 進行自我修正 (注入過去教訓)...")
        
        # [Fix] Retry loop for empty fix code generation
        new_code = ""
        for attempt in range(3):
            new_code = llm.ask_for_fix(feedback_for_llm)
            if new_code and len(new_code.strip()) > 0:
                break
            print(f"⚠️ [AICodeFix] 生成的修復代碼為空，正在重試 ({attempt+1}/3)...")

        if not new_code or len(new_code.strip()) == 0:
            print("❌ [Critical] 無法生成有效的修復代碼，跳過此輪修復 (保留舊代碼)。")
            continue 

        # 【強制修正】：使用 Regex 強制替換類名，確保修復後的代碼也能被 Manim 識別
        import re
        print(f"🔧 [Debug] 強制檢查並修正類名為 {target_scene} (In Fix Loop)...")
        new_code = re.sub(r'class\s+\w+\(Scene\):', f'class {target_scene}(Scene):', new_code, count=1)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_code)
            
    print(f"\n❌ 遺憾：已達到最大嘗試次數 ({max_attempts})，自動修復停止。")
    return False

if __name__ == "__main__":
    print("\n" + "╔" + "═"*48 + "╗")
    print("║" + " "*10 + "EMA System: Multi-stage Manim Agent" + " "*9 + "║")
    print("╚" + "═"*48 + "╝")
    
    user_input = input("\n請輸入動畫主題 (或輸入已存在的 .py 檔名直接播放): ")
    
    # Initialize session logger
    logger = SessionLogger()
    
    try:
        # Start logging session
        logger.start_session(user_input)
        
        target_scene = "GeneratedScene"
        
        # 檢查是否為直接執行現有檔案
        if user_input.endswith(".py") and os.path.exists(user_input):
            print(f"\n📂 檢測到現有檔案，正在啟動播放模式...")
            success, message = run_manim_task(user_input, target_scene)
            if not success:
                print(f"❌ 執行失敗，錯誤訊息：\n{message}")
        else:
            user_topic = user_input
            target_file = "test_script.py"
        
        # 階段一：Planner 規劃腳本
        print("\n🧠 [階段 1: Planner] 正在構思教學邏輯與腳本...")
        planner = Planner()
        script_json = planner.plan_script(user_topic)
        
        try:
            parsed_script = json.loads(script_json)
            print("🎬 規劃腳本內容摘要：")
            # 兼容舊版與新版 JSON (新版使用 sequence, 舊版使用 scenes)
            if "sequence" in parsed_script:
                steps = parsed_script["sequence"]
            else:
                steps = parsed_script.get("scenes", [])
                
            for i, step in enumerate(steps):
                desc = step.get('description', '')
                if not desc and 'visual_action' in step:
                     # 新版 JSON 可能將描述放在 visual_action.details 或 narrative
                     desc = step['visual_action'].get('details', '') or step.get('narrative', '')[:20]
                print(f"  - 步驟 {i+1}: {desc}")
        except Exception as e:
            print(f"⚠️ JSON 解析失敗: {e}")
            extracted = _extract_first_json_object(script_json)
            if extracted:
                try:
                    parsed_script = json.loads(extracted)
                    print("✅ 成功從文本中提取 JSON")
                except Exception as ex:
                    print(f"❌ JSON 提取後解析失敗: {ex}")
                    print(f"📄 提取的內容: {extracted[:200]}...")
                    parsed_script = None
            else:
                print(f"❌ 無法在輸出中找到有效的 JSON 結構")
                print(f"🎬 規劃腳本內容（前 500 字元）：\n{script_json[:500]}")
                parsed_script = None

        # 成功取得 parsed_script 時，將 script_json 統一為乾淨的 JSON 字串，供 Coder / Reviewer 使用
        if parsed_script is not None and isinstance(parsed_script, dict):
            script_json = json.dumps(parsed_script, ensure_ascii=False, indent=2)

        # 階段 1.5: Audio Generation
        # 從 Director 的 Visual Rationale 中提取 sequence
        if 'parsed_script' in locals() and isinstance(parsed_script, dict):
            # 優先使用新版 sequence 結構
            if "sequence" in parsed_script:
                sequence_data = parsed_script["sequence"]
                print(f"\n🎙️ [階段 1.5: Audio Generation] 正在生成語音 (來源: Director's sequence)...")
            elif "scenes" in parsed_script:
                # 向後兼容舊版 scenes 結構
                sequence_data = parsed_script["scenes"]
                print(f"\n🎙️ [階段 1.5: Audio Generation] 正在生成語音 (來源: legacy scenes)...")
            else:
                sequence_data = None
                print(f"\n⚠️ 警告：JSON 中未找到 sequence 或 scenes 結構，跳過語音生成。")
            
            if sequence_data:
                try:
                    # 傳遞 user_topic 讓 AudioEngine 為此主題創建專屬音檔目錄
                    print(f"🔧 [Debug] 初始化 AudioEngine，topic={user_topic}")
                    audio_engine = AudioEngine(topic=user_topic)
                    print(f"🔧 [Debug] AudioEngine 已初始化，azure_enabled={audio_engine.azure_enabled}")
                    
                    # 呼叫 generate_narration 並取得更新後的列表 (含 duration) 與合併音檔路徑
                    updated_sequence, final_audio_path = audio_engine.generate_narration(sequence_data)
                    
                    # 寫回對應的鍵值
                    if "sequence" in parsed_script:
                        parsed_script["sequence"] = updated_sequence
                    else:
                        parsed_script["scenes"] = updated_sequence
                    
                    # 更新 script_json 供後續使用
                    script_json = json.dumps(parsed_script, ensure_ascii=False, indent=2)
                    
                    print(f"✅ 語音處理完成！合併音檔: {final_audio_path}")
                    print(f"📊 已根據語音時長更新 duration，準備傳遞給 Engineer (Coder)。")
                except Exception as e:
                    import traceback
                    print(f"❌ 語音生成過程發生錯誤: {e}")
                    print(f"🔍 [Debug] 錯誤詳情：")
                    print(traceback.format_exc())
                    print(f"⚠️ 將使用預設時長繼續（影片無音檔）")

        # 階段 1.8: RAG Search (Golden Examples)
        print("\n📚 [階段 1.8: RAG Retrieval] 正在搜尋黃金範例 (Golden Examples)...")
        rag_retriever = RAGRetriever()
        # 使用 user_topic 進行檢索 (未來可以改進為使用 Director 的視覺描述)
        rag_results = rag_retriever.retrieve_examples(user_topic, limit=3)
        rag_context = rag_retriever.format_for_prompt(rag_results)
        rag_retriever.close() # 查完就關，節省資源

        # 階段二：Coder 初始代碼生成
        # 【重點修改】：這裡的 Prompt 必須跟 Reviewer 的標準一致，不然一開始就會 FAIL
        print("\n✍️ [階段 2: Coder] 正在撰寫初始 Manim 程式碼...")
        llm = LLMClient()
        coder_prompter = CoderPrompter()
        # 注入 RAG Context
        initial_prompt = coder_prompter.generate_initial_prompt(script_json, target_scene, rag_context=rag_context)
        
        # [Fix] Retry loop for empty code generation
        max_retries = 3
        first_code = ""
        for attempt in range(max_retries):
            first_code = llm.ask_for_fix(initial_prompt)
            if first_code and len(first_code.strip()) > 0:
                break
            print(f"⚠️ 生成的代碼為空，正在重試 ({attempt+1}/{max_retries})...")
        
        # 【強制修正】：使用 Regex 強制替換類名，確保 Manim 能找到 GeneratedScene
        import re
        print(f"🔧 [Debug] 強制檢查並修正類名為 {target_scene}...")
        first_code = re.sub(r'class\s+\w+\(Scene\):', f'class {target_scene}(Scene):', first_code, count=1)
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(first_code)

            # 階段三：自動修復與審查循環
            print("\n🔄 [階段 3: Review & Fix] 啟動自動校對與渲染循環...")
            auto_fix_loop(target_file, target_scene, user_topic, script_json)
    
    finally:
        # Always end logging session, even if there's an error
        logger.end_session()