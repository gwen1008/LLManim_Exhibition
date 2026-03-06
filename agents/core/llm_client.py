import os
import time
from groq import Groq  # 確保已經 pip install groq
from dotenv import load_dotenv

# 加載 .env 檔案中的環境變數
load_dotenv()

class LLMError(Exception):
    """Raised when any LLM API call fails."""
    pass

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
        
        self.client = Groq(api_key=api_key, max_retries=3, timeout=180.0)

        
        # --- DeepSeek API Support (Conservative Upgrade Path) ---
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
        if self.deepseek_api_key:
            from openai import OpenAI as _OpenAI
            self.deepseek_client = _OpenAI(
                api_key=self.deepseek_api_key,
                base_url=self.deepseek_base_url,
                timeout=180.0,
                max_retries=2,
            )
        else:
            self.deepseek_client = None
        
        # --- 多模型配置 (Role-based Model Selection) ---
        # 根據不同角色使用不同模型，優化成本與效能
        self.models = {
            "default": os.getenv("GROQ_MODEL_DEFAULT", "llama-3.3-70b-versatile"),
            "planner": os.getenv("GROQ_MODEL_PLANNER", "llama-3.3-70b-versatile"),
            "coder": "deepseek-chat",  # Switched to DeepSeek-V3 for long-context stability
            "reviewer": os.getenv("GROQ_MODEL_REVIEWER", "llama-3.1-8b-instant"),
            "vision": "gpt-4o-mini",  # Switched for cost optimization (97% cheaper)
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
            "deepseek-reasoner": {"input": 0.55, "output": 2.19},  # R1, cache miss price
            "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
            "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60}
        }
        
        self.debug = debug

    def ask(self, system_prompt, user_prompt, role="default", json_mode=False, temperature=None):
        """Route to the correct backend based on role mapping."""
        model = self.models.get(role, self.models["default"])
        
        # Determine temperature to use
        req_temp = temperature if temperature is not None else 0.1
        
        if model.startswith("deepseek-"):
            return self._call_deepseek(system_prompt, user_prompt, temperature=req_temp, json_mode=json_mode)
        elif role == "vision" or model.startswith("gpt"):
            # Text-only default fallback for standard GPT calls without images
            if not self.openai_client:
                raise LLMError("OpenAI API key not configured for vision/gpt models.")
            
            kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": req_temp
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
                
            completion = self.openai_client.chat.completions.create(**kwargs)
            return completion.choices[0].message.content
        else:
            # Groq model
            return self._call_groq(model, system_prompt, user_prompt, temperature=req_temp, json_mode=json_mode)

    def _call_groq(self, model, system_prompt, user_prompt, temperature=0.1, json_mode=False):
        """Internal method to call Groq API."""
        try:
            start_time = time.time()  # 開始計時
            
            kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "timeout": 180, # 增加至 3 分鐘，避免長上下文生成時超時
            }

            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            
            completion = self.client.chat.completions.create(**kwargs)
            
            end_time = time.time()  # 結束計時
            duration = end_time - start_time
            
            # 提取 Token 使用資訊
            usage = completion.usage
            response = completion.choices[0].message.content
            
            # Update Session Stats
            self._update_stats(model, usage.prompt_tokens, usage.completion_tokens)
            
            if self.debug:
                print(f"\n" + "-"*30)
                print(f"🤖 [模型]: {model} (Groq)")
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
            raise LLMError(error_msg) from e
    
    def _call_deepseek(self, system_prompt, user_prompt, temperature=0.1, json_mode=False):
        if not self.deepseek_client:
            raise LLMError("DeepSeek API key not configured.")

        try:
            start_time = time.time()
            
            kwargs = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": 8192,
            }
            
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            completion = self.deepseek_client.chat.completions.create(**kwargs)

            end_time = time.time()
            content = completion.choices[0].message.content
            usage = completion.usage

            self._update_stats("deepseek-chat", usage.prompt_tokens, usage.completion_tokens)

            if self.debug:
                print(f"\n" + "-"*30)
                print(f"🤖 [模型]: deepseek-chat (DeepSeek-V3, OpenAI SDK)")
                print(f"⏱️  [API 耗時]: {end_time - start_time:.2f} 秒")
                print(f"📊 [Token 統計]: 輸入 {usage.prompt_tokens} | 輸出 {usage.completion_tokens} | 總計 {usage.total_tokens}")
                print("-" * 30)

            return content

        except Exception as e:
            error_msg = f"Error connecting to DeepSeek: {str(e)}"
            print(f"❌ {error_msg}")
            raise LLMError(error_msg) from e

    def _call_deepseek_r1(self, system_prompt, user_prompt):
        """
        Call DeepSeek-R1 (deepseek-reasoner) for Tier-3 escalation.
        
        Key differences from V3:
        - system prompt merged into user prompt (R1 ignores system role reliably)
        - temperature fixed at 0.6 (R1 official recommendation)
        - max_tokens 16000 (thinking tokens also count as output)
        - <think> tags stripped by extract_code() automatically
        """
        if not self.deepseek_client:
            raise LLMError("DeepSeek API key not configured.")

        try:
            start_time = time.time()

            # Merge system prompt into user prompt for R1 reliability
            merged_user = ""
            if system_prompt and system_prompt.strip():
                merged_user = f"{system_prompt.strip()}\n\n---\n\n{user_prompt.strip()}"
            else:
                merged_user = user_prompt.strip()

            kwargs = {
                "model": "deepseek-reasoner",
                "messages": [
                    {"role": "user", "content": merged_user}
                ],
                "max_tokens": 16000,
                # temperature is NOT supported for deepseek-reasoner — omit entirely
            }

            completion = self.deepseek_client.chat.completions.create(**kwargs)

            end_time = time.time()
            content = completion.choices[0].message.content
            usage = completion.usage

            self._update_stats("deepseek-reasoner", usage.prompt_tokens, usage.completion_tokens)

            if self.debug:
                print(f"\n" + "-"*30)
                print(f"🧠 [模型]: deepseek-reasoner (DeepSeek-R1, Tier-3 Escalation)")
                print(f"⏱️  [API 耗時]: {end_time - start_time:.2f} 秒")
                print(f"📊 [Token 統計]: 輸入 {usage.prompt_tokens} | 輸出 {usage.completion_tokens} | 總計 {usage.total_tokens}")
                print("-" * 30)

            return content

        except Exception as e:
            error_msg = f"Error connecting to DeepSeek-R1: {str(e)}"
            print(f"❌ {error_msg}")
            raise LLMError(error_msg) from e

    def ask_vision(self, system_prompt, user_text, base64_image=None, detail="low", json_mode=True, temperature=0.1, max_tokens=2000):
        """
        Call OpenAI GPT-4o with image for visual audit.
        
        Args:
            base64_image: base64 encoded JPEG image (multi-frame grid)
            detail: "low" or "high". Low uses fewer tokens (85 tokens/image).
            json_mode: Whether to return strictly structured JSON.
        """
        if not self.openai_client:
            raise LLMError("OpenAI API Key not configured.")
        if not base64_image:
            raise LLMError("ask_vision requires base64_image.")

        try:
            start_time = time.time()
            model = self.models.get("vision", "gpt-4o-mini")
            
            content_parts = [{"type": "text", "text": user_text}]
            
            content_parts.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail
                }
            })
            
            
            kwargs = {
                "model": self.models.get("vision", "gpt-4o-mini"),
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content_parts}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if json_mode:
                # Need to specifically allow JSON type
                kwargs["response_format"] = {"type": "json_object"}

            completion = self.openai_client.chat.completions.create(**kwargs)

            end_time = time.time()
            duration = end_time - start_time
            
            usage = completion.usage
            response = completion.choices[0].message.content
            
            # Update Stats
            self._update_stats(model, usage.prompt_tokens, usage.completion_tokens)
            
            if self.debug:
                print(f"\n" + "-"*30)
                print(f"👁️  [模型]: {model} (Vision Audit - Image Grid)")
                print(f"⏱️  [API 耗時]: {duration:.2f} 秒")
                print(f"📊 [Token 統計]: 輸入 {usage.prompt_tokens} | 輸出 {usage.completion_tokens}")

                print("-" * 30)
                
            return response
            
        except Exception as e:
            error_msg = f"Error connecting to OpenAI Vision: {str(e)}"
            print(f"❌ {error_msg}")
            raise LLMError(error_msg) from e


    @staticmethod
    def extract_code(content: str) -> str:
        """從 markdown 內容中安全提取 Python 代碼區塊"""
        import re
        
        # 1. Strip out <think>...</think> tags if they exist (DeepSeek R1 reasoning)
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        
        # 2. Try to match ```python ... ``` or ``` ... ``` using Regex
        # This handles cases where there's extra text before or after the code block
        match = re.search(r"```(?:python)?\s*(.*?)```", content, flags=re.DOTALL)
        
        if match:
            extracted = match.group(1).strip()
            return extracted
            
        # 3. Fallback: return the cleaned content if no code blocks are found
        # (This assumes the entire response might just be code, but stripped of <think> tags)
        return content.strip()

    def ask_for_fix(self, prompt_or_system, user_prompt=None, role="coder", temperature=None, use_r1=False):
        """
        專門用於生成或修復程式碼的接口。

        支援兩種呼叫方式：
        1. ask_for_fix(full_prompt)           — 舊式單參數，全部塞 user_prompt
        2. ask_for_fix(system_prompt, user_prompt) — 新式雙參數，system 可被 DeepSeek cache

        :param role: 角色名稱，預設為 'coder'
        """
        # 向後兼容：單參數呼叫時，全部當 user_prompt。
        # Prompt Cache 的正確做法是讓 caller 顯式分離 system/user（傳入雙參數），
        # 而不是在這裡靠字串匹配猜分割點（每次 system_prompt 不同 → cache 永遠不命中）。
        if user_prompt is None:
            system_prompt = ""
            user_prompt = prompt_or_system
        else:
            system_prompt = prompt_or_system

        model = self.models.get(role, self.models["default"])

        if self.debug:
            print(f"\n🛠️  [正在處理的錯誤/要求]:")
            display_prompt = user_prompt if len(user_prompt) < 300 else user_prompt[:300] + "..."
            print(f"{display_prompt}")
            print(f"\n🧠 生成代碼中 ({model})... (System Msg Length: {len(system_prompt)})")

        _MANIM_RULES_COMPACT = (
            "CRITICAL MANIM v0.19.2 RULES (must comply — violation = immediate crash):\n"
            "- Use Text()/MathTex(), NOT TextMobject/TexMobject (deprecated)\n"
            "- Use .animate syntax: obj.animate.shift(UP)\n"
            "- self.add() BEFORE self.play(...animate...)\n"
            "- Triangle has NO height/width params — use .scale() instead\n"
            "- Sector: first arg is radius, NOT outer_radius\n"
            "- color= kwarg is INVALID for Create/Write/FadeIn — use .set_color()\n"
            "- self.wait() duration must be > 0; wrap computed durations with max(0.1, ...)\n"
        )

        is_patch_mode = ("<<<< SEARCH" in user_prompt) or ("<<<< SEARCH" in system_prompt)
        if is_patch_mode:
            system_msg_prefix = (
                "你是一個 Manim Community v0.19.2 專家。請嚴格按照 SEARCH/REPLACE 格式輸出修補內容，"
                "不要加上任何 Markdown 代碼塊（例如 ```python）。\n\n"
                + _MANIM_RULES_COMPACT
            )
        else:
            system_msg_prefix = (
                "你是一個 Manim Community v0.19.2 專家。若有 <reflection>...</reflection> 分析，"
                "請放在代碼塊之前。代碼本身請包在 ```python ... ``` 代碼塊中。\n\n"
                + _MANIM_RULES_COMPACT
            )

        full_system = system_msg_prefix + system_prompt

        if use_r1:
            content = self._call_deepseek_r1(full_system, user_prompt)
        else:
            content = self.ask(full_system, user_prompt, role=role, temperature=temperature)

        if is_patch_mode:
            import re
            content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
            return content.strip()

        return content

    def ask_for_fix_n(self, prompt_or_system, user_prompt=None, role="coder", n=3, temperature=0.5):
        """
        Runs ask_for_fix 'n' times in parallel for Self-Consistency voting.
        """
        import concurrent.futures
        
        # Using a ThreadPoolExecutor to run N parallel calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            futures = [
                executor.submit(self.ask_for_fix, prompt_or_system, user_prompt, role=role, temperature=temperature) 
                for _ in range(n)
            ]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"⚠️ [SC Worker Failed]: {e}")
            
        return results

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