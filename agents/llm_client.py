import os
import time
import requests  # For DeepSeek API
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
        
        # --- DeepSeek API Support (Conservative Upgrade Path) ---
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
        
        # --- 多模型配置 (Role-based Model Selection) ---
        # 根據不同角色使用不同模型，優化成本與效能
        self.models = {
            "default": os.getenv("GROQ_MODEL_DEFAULT", "llama-3.3-70b-versatile"),
            "planner": os.getenv("GROQ_MODEL_PLANNER", "llama-3.3-70b-versatile"),
            "coder": os.getenv("GROQ_MODEL_CODER", "llama-3.3-70b-versatile"),
            "reviewer": os.getenv("GROQ_MODEL_REVIEWER", "llama-3.1-8b-instant"),
            "vision": "gpt-4o",
        }
        
        # --- Native OpenAI Support (for Vision) ---
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
        
        self.model = self.models["default"]
        
        # --- Session Tracking (Token Usage and Cost) ---
        self.session_stats = {
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost_usd": 0.0,
            "calls": []
        }
        
        # Pricing per 1M tokens (USD) - Industry standard Feb 2026
        self.pricing = {
            "deepseek-chat": {"input": 0.14, "output": 0.28},
            "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
            "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
            "gpt-4o": {"input": 2.50, "output": 10.00}
        }
        
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
            
            # 🔀 Route to DeepSeek API if model is 'deepseek-*'
            if "deepseek" in model.lower():
                return self._call_deepseek(system_prompt, user_prompt, temperature)
            
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
            
            # Update Session Stats
            self._update_stats(model, usage.prompt_tokens, usage.completion_tokens)
            
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
    
    def _call_deepseek(self, system_prompt, user_prompt, temperature=0.1):
        """
        Call DeepSeek API directly for models specified as 'deepseek-*'
        """
        try:
            start_time = time.time()
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature
            }
            
            response = requests.post(
                f"{self.deepseek_base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            end_time = time.time()
            duration = end_time - start_time
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            
            # Update Session Stats
            self._update_stats("deepseek-chat", usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))
            
            if self.debug:
                print(f"\n" + "-"*30)
                print(f"🤖 [模型]: deepseek-chat (DeepSeek-V3)")
                print(f"⏱️  [API 耗時]: {duration:.2f} 秒")
                print(f"📊 [Token 統計]: 輸入 {usage.get('prompt_tokens', 'N/A')} | 輸出 {usage.get('completion_tokens', 'N/A')} | 總計 {usage.get('total_tokens', 'N/A')}")
                print("-" * 30)
            
            return content
            
        except Exception as e:
            error_msg = f"Error connecting to DeepSeek: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg

    def ask_vision(self, system_prompt, user_text, base64_image):
        """
        Call OpenAI GPT-4o with image for visual audit.
        """
        if not self.openai_client:
            return "ERROR: OpenAI API Key not configured."

        try:
            start_time = time.time()
            model = "gpt-4o"
            
            completion = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            usage = completion.usage
            response = completion.choices[0].message.content
            
            # Update Stats
            self._update_stats(model, usage.prompt_tokens, usage.completion_tokens)
            
            if self.debug:
                print(f"\n" + "-"*30)
                print(f"👁️  [模型]: {model} (Vision Audit)")
                print(f"⏱️  [API 耗時]: {duration:.2f} 秒")
                print(f"📊 [Token 統計]: 輸入 {usage.prompt_tokens} | 輸出 {usage.completion_tokens}")
                print("-" * 30)
                
            return response
            
        except Exception as e:
            error_msg = f"Error connecting to OpenAI Vision: {str(e)}"
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

    def _update_stats(self, model_name, prompt_tokens, completion_tokens):
        """Update the internal session statistics counters."""
        self.session_stats["total_prompt_tokens"] += prompt_tokens
        self.session_stats["total_completion_tokens"] += completion_tokens
        
        # Calculate cost
        price = self.pricing.get(model_name, self.pricing["llama-3.3-70b-versatile"])
        cost = (prompt_tokens / 1_000_000 * price["input"]) + (completion_tokens / 1_000_000 * price["output"])
        self.session_stats["total_cost_usd"] += cost
        
        # Log call for debugging
        self.session_stats["calls"].append({
            "model": model_name,
            "prompt": prompt_tokens,
            "completion": completion_tokens,
            "cost": cost
        })

    def get_session_report(self):
        """Return a formatted string summarizing the session usage."""
        stats = self.session_stats
        total_tokens = stats["total_prompt_tokens"] + stats["total_completion_tokens"]
        
        report = "\n" + "="*40 + "\n"
        report += "📊 **LLM USAGE SESSION REPORT**\n"
        report += "="*40 + "\n"
        report += f"Total Calls: {len(stats['calls'])}\n"
        report += f"Total Tokens: {total_tokens:,}\n"
        report += f"  - Prompt: {stats['total_prompt_tokens']:,}\n"
        report += f"  - Completion: {stats['total_completion_tokens']:,}\n"
        report += "-"*40 + "\n"
        # 轉換為台幣預算 (假設 1 USD = 31 TWD)
        cost_twd = stats["total_cost_usd"] * 31
        report += f"Estimated Cost: ${stats['total_cost_usd']:.6f} USD\n"
        report += f"約合台幣: NT$ {cost_twd:.4f}\n"
        report += "="*40 + "\n"
        
        return report

    def close(self):
        """Close the underlying API clients to release resources."""
        try:
            if hasattr(self, 'client') and hasattr(self.client, 'close'):
                self.client.close()
        except Exception as e:
            if self.debug:
                print(f"⚠️ Error closing LLMClient: {e}")