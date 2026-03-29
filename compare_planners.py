import os
import time

# 載入與環境設定相關模組
from agents.planner.planner import Planner
from agents.core.llm_client import LLMClient

TOPIC = "用兩個一樣的披薩圖形，示範為什麼 1/2 等於 2/4，並塗色對比區域。"

def check_planner(model_name: str):
    print(f"\n{'='*70}")
    print(f"🚀 啟動測試: 測試 Planner 模型 [{model_name}]")
    print(f"{'='*70}")
    
    # 動態切換環境變數
    os.environ["GROQ_MODEL_PLANNER"] = model_name
    
    # 建立全新的 LLM Client 與 Planner (強制讀取新的環境變數)
    client = LLMClient()
    planner = Planner(llm_client=client)
    
    start_time = time.time()
    try:
        script_json, thought_tree_raw = planner.plan_script(TOPIC)
        duration = time.time() - start_time
        
        print(f"\n⏱️ 最終耗時結算: {duration:.2f} 秒")
        print("\n🧠 --- Tree of Thoughts (思維樹與反思) 預覽 ---")
        print(thought_tree_raw)
        
        print("\n📜 --- 產生的 JSON 腳本 (Blueprint) ---")
        print(script_json)
        
    except Exception as e:
        print(f"\n❌ 測試過程發生嚴重錯誤: {e}")

if __name__ == "__main__":
    print(f"🎯 測試主題: {TOPIC}")
    check_planner("llama-3.3-70b-versatile")
    check_planner("deepseek-chat")
