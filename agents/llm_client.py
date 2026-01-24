import os
import time
from groq import Groq  # 確保已經 pip install groq
from dotenv import load_dotenv

# 加載 .env 檔案中的環境變數
load_dotenv()

class LLMClient:
    def __init__(self, debug=True):
        """
        初始化 LLM 客戶端
        :param debug: 是否開啟調試模式，開啟後會印出更多互動細節
        """
        # 從環境變數中自動讀取 Key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ 找不到 GROQ_API_KEY，請確認 .env 檔案內容與位置是否正確")
        
        self.client = Groq(api_key=api_key)
        
        # --- 多模型配置 (Role-based Model Selection) ---
        # 根據不同角色使用不同模型，優化成本與效能
        self.models = {
            "default": os.getenv("GROQ_MODEL_DEFAULT", "llama-3.3-70b-versatile"),
            "planner": os.getenv("GROQ_MODEL_PLANNER", "llama-3.3-70b-versatile"),
            "coder": os.getenv("GROQ_MODEL_CODER", "llama-3.3-70b-versatile"),
            "reviewer": os.getenv("GROQ_MODEL_REVIEWER", "llama-3.1-8b-instant"),
        }
        
        # 保留舊的 self.model 以兼容性（作為 default）
        self.model = self.models["default"]
        
        self.debug = debug

    def ask(self, system_prompt, user_prompt, temperature=0.1, role="default"):
        """
        通用的對話接口，供 Planner (產出 JSON) 與 Reviewer (產出文字回饋) 使用
        同時記錄 Token 使用量與耗時
        
        :param role: 角色名稱 ('planner', 'coder', 'reviewer', 'default')
        """
        try:
            start_time = time.time()  # 開始計時
            
            # 根據角色選擇模型
            model = self.models.get(role, self.models["default"])
            
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
            )
            
            end_time = time.time()  # 結束計時
            duration = end_time - start_time
            
            # 提取 Token 使用資訊
            usage = completion.usage
            response = completion.choices[0].message.content
            
            if self.debug:
                print(f"\n" + "-"*30)
                print(f"🤖 [模型]: {model} (role: {role})")
                print(f"⏱️  [API 耗時]: {duration:.2f} 秒")
                print(f"📊 [Token 統計]: 輸入 {usage.prompt_tokens} | 輸出 {usage.completion_tokens} | 總計 {usage.total_tokens}")
                
                # 如果不是 PASS 且 debug 開啟，顯示完整的回饋細節
                if "PASS" not in response:
                    print(f"\n📢 [AI 審查/反饋意見]:\n{response.strip()}")
                print("-" * 30)
                
            return response
        except Exception as e:
            error_msg = f"Error connecting to Groq: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    def ask_for_fix(self, prompt, role="coder"):
        """
        專門用於生成或修復程式碼的接口。
        在此方法中，我們會先印出「為什麼需要修復」，讓你看到錯誤在哪裡。
        
        :param role: 角色名稱，預設為 'coder'
        """
        model = self.models.get(role, self.models["default"])
        
        if self.debug:
            print(f"\n🛠️  [正在處理的錯誤/要求]:")
            # 擷取 prompt 的前 300 個字，避免畫面太亂，但足以讓你看到報錯重點
            display_prompt = prompt if len(prompt) < 300 else prompt[:300] + "..."
            print(f"{display_prompt}")
            print(f"\n🧠 Groq 正在根據上述問題生成代碼 ({model})...")
        
        system_msg = "你是一個 Manim 專家。請僅輸出修復後的 Python 代碼，並確保包在 ```python ... ``` 代碼塊中。"
        
        # 調用內部的 ask 方法獲取完整內容，傳遞 role 參數
        content = self.ask(system_msg, prompt, role=role)
        
        # 執行原本強大的代碼提取邏輯
        extracted_code = content
        if "```python" in content:
            extracted_code = content.split("```python")[1].split("```")[0].strip()
        elif "```" in content:
            extracted_code = content.split("```")[1].split("```")[0].strip()
        
        return extracted_code