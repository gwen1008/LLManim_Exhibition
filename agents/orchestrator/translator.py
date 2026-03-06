# agents/orchestrator/translator.py
from ..core.llm_client import LLMClient

class AcademicTranslator:
    def __init__(self, llm_client=None):
        self.llm = llm_client if llm_client else LLMClient()

    def translate_to_english(self, user_topic: str) -> str:
        """
        [Agent Skill: Auto-Translation (Advanced Academic Standard)]
        Based on "Make AI Writing Better" (Reviewer Persona + Logic Check)
        """
        if not any("\u4e00" <= char <= "\u9fff" for char in user_topic):
            return user_topic

        print(f"\n🌐 [Auto-Translate] 偵測到中文輸入，啟動「學術級 Reviewer 翻譯 Agent」...")
        try:
            print("   1️⃣  [Translator] 正在進行高精度學術翻譯與邏輯審查 (Single-Pass)...")
            translation_prompt = (
                "# Role\n"
                "You are a dual-expert in Academic Research and Manim Animation Development. "
                "Your academic taste is impeccable, and you have zero tolerance for logical flaws or ambiguity.\n\n"
                "# Task\n"
                "Translate the provided [Chinese Requirement] into a precise [English Animation Specification].\n\n"
                "# Constraints\n"
                "1. Terminology: Use standard mathematical and Manim terms.\n"
                "2. Logic: Ensure the sequence of events is explicitly clear.\n"
                "3. Self-Reflection: Before outputting the final translation, think critically in a <reflection> block to ensure no semantic errors.\n"
                "4. Output: The final translated English text MUST be inside <final_translation> tags.\n"
            )
            raw_response = self.llm.ask(translation_prompt, user_topic, role="default")
            
            import re
            match = re.search(r'<final_translation>(.*?)</final_translation>', raw_response, re.DOTALL)
            if match:
                final_translation = match.group(1).strip()
                print(f"✨ [翻譯完成]: {final_translation}")
                return final_translation
            elif raw_response and not raw_response.startswith("Error"):
                print(f"⚠️ [Fallback] 無法解析 XML tag，直接使用模型輸出")
                return raw_response.strip()

            else:
                print(f"⚠️ 翻譯異常，將使用原始輸入。")
                return user_topic
                
        except Exception as e:
             print(f"⚠️ 翻譯 Agent 執行錯誤: {e}")
             return user_topic
