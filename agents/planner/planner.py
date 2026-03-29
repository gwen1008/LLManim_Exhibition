# agents/planner.py
import json
import re
from ..core.llm_client import LLMClient
from .templates import PLANNER_SYSTEM_PROMPT

class Planner:
    def __init__(self, llm_client=None):
        self.client = llm_client if llm_client else LLMClient()
        self.system_prompt = PLANNER_SYSTEM_PROMPT

    @staticmethod
    def _extract_first_json_object(text: str) -> str | None:
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

    def plan_script(self, topic: str):
        """
        Legacy method for backward compatibility.
        """
        return self.plan_script_from_prompt(topic)

    def plan_script_from_prompt(self, prompt: str, file_path: str = None) -> tuple[str, str]:
        """
        Plans a script based on a text prompt and optional file context (PDF).
        """
        # Default text-only prompt
        user_content = f"Design a professional educational animation for: '{prompt}'. Include 3-5 well-structured steps. You MUST output all THREE parts: PART 1 (thought_tree XML), PART 2 (reasoning XML), and PART 3 (JSON blueprint). Do NOT stop after PART 2."
        
        if file_path:
            try:
                from ..utils.pdf_processor import process_local_pdf
                pdf_b64 = process_local_pdf(file_path)
                user_content = [
                    {"type": "text", "text": f"Design a professional educational animation for: '{prompt}'. Include 3-5 well-structured steps."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:application/pdf;base64,{pdf_b64}"
                        }
                    }
                ]
                print(f"📄 Added PDF context from: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to process PDF: {e}")

        raw_response = self.client.ask(self.system_prompt, user_content, role="planner")
        return self._process_response(raw_response)

    @staticmethod
    def _repair_manim_json(text: str):
        """嘗試用 eval 解析含有 Python 表達式（如 90 * DEGREES 或 RED）的髒 JSON"""
        import math
        safe_dict = {
            "__builtins__": {},
            "true": True, "false": False, "null": None,
        }
        # 注入常見數學變數，讓 90 * DEGREES 可以直接算出小數
        safe_dict.update({
            "PI": math.pi, "TAU": math.tau, "DEGREES": math.pi / 180,
        })
        # 注入常見 Manim 常數（直接轉為同名字串，讓 JSON dump 出來還看得懂）
        constants = [
            "UP", "DOWN", "LEFT", "RIGHT", "ORIGIN", "UR", "UL", "DR", "DL",
            "WHITE", "BLACK", "RED", "BLUE", "GREEN", "YELLOW", "ORANGE", 
            "PURPLE", "PINK", "TEAL", "GOLD", "GREY", "GRAY"
        ]
        for c in constants:
            safe_dict[c] = c

        return eval(text, safe_dict)

    def _process_response(self, raw_response: str) -> tuple[str, str]:
        # Extract Thought Tree block if present
        thought_tree = ""
        if "<thought_tree>" in raw_response and "</thought_tree>" in raw_response:
            start = raw_response.find("<thought_tree>") + len("<thought_tree>")
            end = raw_response.find("</thought_tree>")
            thought_tree = raw_response[start:end].strip()
            # Remove thought tree block from response for JSON extraction
            raw_response = raw_response[end + len("</thought_tree>"):].strip()
            if thought_tree:
                print("\n" + "="*60)
                print("🌳 **VISUAL TREE OF THOUGHTS (ToT)**")
                print("="*60)
                print(thought_tree)
                print("="*60 + "\n")

        # Extract reasoning block if present
        reasoning = ""
        if "<reasoning>" in raw_response and "</reasoning>" in raw_response:
            start = raw_response.find("<reasoning>") + len("<reasoning>")
            end = raw_response.find("</reasoning>")
            reasoning = raw_response[start:end].strip()
            # Remove reasoning block from response for JSON extraction
            raw_response = raw_response[end + len("</reasoning>"):].strip()
            if reasoning:
                print("\n" + "="*60)
                print("🧠 **SPATIAL REASONING**")
                print("="*60)
                print(reasoning)
                print("="*60 + "\n")
        
        def _try_parse(content: str):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                try:
                    return self._repair_manim_json(content)
                except Exception:
                    return None

        # 0) 優先從 <json_blueprint> 標記提取
        if "<json_blueprint>" in raw_response and "</json_blueprint>" in raw_response:
            start = raw_response.find("<json_blueprint>") + len("<json_blueprint>")
            end = raw_response.find("</json_blueprint>")
            blueprint_content = raw_response[start:end].strip()
            
            obj = _try_parse(blueprint_content)
            if obj:
                return json.dumps(obj, ensure_ascii=False, indent=2), thought_tree
            else:
                raw_response = blueprint_content  # 繼續往下用這個內容解析

        # 清理 Markdown 代碼塊標籤
        clean = re.sub(r"```json\n?|```", "", raw_response).strip()
        
        # 1) 直接解析
        obj = _try_parse(clean)
        if obj:
            return json.dumps(obj, ensure_ascii=False, indent=2), thought_tree
        
        # 2) 若有前後文，以括號匹配擷取第一個 { ... }
        print("⚠️ 警告：Planner 產出的 JSON 格式有誤，正啟動髒資料修復解析 (Dirty JSON Parse)…")
        extracted = self._extract_first_json_object(clean)
        if extracted:
            obj = _try_parse(extracted)
            if obj:
                print("✅ 髒資料修復成功！已將 Llama 的 Python 變數硬轉為標準 JSON。")
                return json.dumps(obj, ensure_ascii=False, indent=2), thought_tree

        print("⚠️ 擷取後仍無法解析，將使用原始輸出。")
        return clean, thought_tree