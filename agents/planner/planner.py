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
        user_content = f"Design a professional educational animation for: '{prompt}'. Include 3-5 well-structured steps. Follow the two-part output format."
        
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
        
        # 清理 Markdown 代碼塊標籤
        clean = re.sub(r"```json\n?|```", "", raw_response).strip()
        
        # 1) 直接解析
        try:
            json.loads(clean)
            return clean, thought_tree
        except json.JSONDecodeError:
            pass
        
        # 2) 若有前後文，以括號匹配擷取第一個 { ... }
        print("⚠️ 警告：Planner 產出的 JSON 格式有誤，正以括號匹配擷取 JSON 物件…")
        extracted = self._extract_first_json_object(clean)
        if extracted:
            try:
                obj = json.loads(extracted)
                return json.dumps(obj, ensure_ascii=False, indent=2), thought_tree
            except json.JSONDecodeError:
                pass
        print("⚠️ 擷取後仍無法解析，將使用原始輸出。")
        return clean, thought_tree