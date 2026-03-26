# agents/orchestrator/router.py
import os
import re
import time
import shutil
import sys
from ..utils.audio_engine import AudioEngine
from templates.addition import generate_vertical_addition_code, generate_addition_narrative

class TaskRouter:
    @staticmethod
    def detect_arithmetic_task(topic: str):
        """
        Detect if the topic is a basic arithmetic operation.
        Returns: (is_arithmetic, num1, operator, num2)
        """
        # 排除包含向量、座標或函數特徵的字串
        blacklist = ["向量", "vector", "座標", "coordinate", "plot", "graph", "函數", "function", "(", ")"]
        if any(word in topic.lower() for word in blacklist):
            return False, None, None, None

        # 收緊匹配：必須是「數字 [+|-|*|×|/|÷|加|減|乘|除...] 數字」，且前後不能有座標括號
        pattern = r'(?<![\(\d])(\d+)\s*([+\-\*×/÷]|加|加上|減|減去|乘|乘以|除|除以)\s*(\d+)(?![\)\d])'
        match = re.search(pattern, topic)
        if match:
            num1_str, operator, num2_str = match.groups()
            return True, int(num1_str), operator, int(num2_str)
        return False, None, None, None

    @staticmethod
    def route_to_template(topic: str, num1: int, op: str, num2: int, target_scene: str, target_file: str, logger=None, llm=None):
        """
        Routes the task to a deterministic template if available.
        """
        if op in ('+', '加', '加上'):
            from templates.addition import generate_vertical_addition_code, generate_addition_narrative
            narrative_func = generate_addition_narrative
            code_func = generate_vertical_addition_code
            op_name = "addition"
        elif op in ('-', '減', '減去'):
            from templates.subtraction import generate_vertical_subtraction_code, generate_subtraction_narrative
            narrative_func = generate_subtraction_narrative
            code_func = generate_vertical_subtraction_code
            op_name = "subtraction"
        elif op in ('*', '×', '乘', '乘以'):
            from templates.multiplication import generate_vertical_multiplication_code, generate_multiplication_narrative
            narrative_func = generate_multiplication_narrative
            code_func = generate_vertical_multiplication_code
            op_name = "multiplication"
        elif op in ('/', '÷', '除', '除以'):
            from templates.division import generate_long_division_code, generate_division_narrative
            narrative_func = generate_division_narrative
            code_func = generate_long_division_code
            op_name = "division"
        else:
            return None

        print("\n" + "="*60)
        print(f"🎯 偵測到基礎算術任務：{num1} {op} {num2}")
        print("📦 使用確定性模板系統 (Deterministic Template)")
        print("   ✅ 100% 正確性保證")
        print("   ✅ 跳過 AI Pipeline (Planner + Coder)")
        print("   ✅ 包含語音旁白同步")
        print("="*60)
        
        # Step 1: Generate narrative
        print(f"📝 生成{op_name}旁白文字...")
        try:
            narrative_steps = narrative_func(num1, num2)
        except Exception as e:
            print(f"⚠️ 生成旁白失敗 ({e})，降級回 AI Pipeline。")
            return None
        
        # Step 2: Generate audio files
        print("🎙️ 生成語音檔案...")
        audio_engine = AudioEngine(topic=topic)
        audio_steps, final_audio = audio_engine.generate_narration(narrative_steps)
        
        # Step 3: Generate code using template with audio sync
        print(f"📦 生成同步{op_name}動畫代碼...")
        try:
            template_code = code_func(
                num1=num1,
                num2=num2,
                scene_name=target_scene,
                audio_steps=audio_steps
            )
        except Exception as e:
            print(f"⚠️ 生成代碼失敗 ({e})，降級回 AI Pipeline。")
            return None
        
        # Write to file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(template_code)
        
        print(f"✅ 模板代碼已生成：{target_file}")
        print("🚀 執行渲染檢查...")
        
        # Importing here to avoid circular dependencies if any
        from .refining_loop import RefiningLoop
        
        success, message = RefiningLoop.run_manim_task(target_file, target_scene)
        
        if success:
            print("\n" + "="*40)
            print("✨ 【渲染成功 / Rendering Success】 ✨")
            print("="*40)
            
            # Archive to stable_outputs
            safe_name = topic.replace(" ", "_").replace(".", "_").replace("/", "_div_").replace("÷", "_div_").replace("*", "x").replace("×", "x").replace("+", "_plus_").replace("-", "_minus_")
            stable_dir = "stable_outputs"
            os.makedirs(stable_dir, exist_ok=True)
            
            # Construct correct video path based on Manim's output structure
            script_basename = os.path.splitext(os.path.basename(target_file))[0]
            video_src = f"media/videos/{script_basename}/480p15/{target_scene}.mp4"
            
            if os.path.exists(video_src):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                video_dst = os.path.join(stable_dir, f"{safe_name}_{timestamp}.mp4")
                shutil.copy(video_src, video_dst)
                print(f"    🎥 {os.path.basename(video_dst)}")
                
                code_dst = os.path.join(stable_dir, f"{safe_name}_{timestamp}.py")
                shutil.copy(target_file, code_dst)
                print(f"    🐍 {os.path.basename(code_dst)}")
                print("="*40)
                
                if logger:
                    logger.log_session_stats(llm)
                
                return video_dst
            else:
                print(f"    ⚠️  影片未找到於: {video_src}")
        else:
            print(f"❌ 渲染失敗：{message}")
        
        if logger:
            logger.log_session_stats(llm)
        return None
