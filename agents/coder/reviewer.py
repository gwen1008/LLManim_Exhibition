from ..core.llm_client import LLMClient
from .lint_manim import lint_file
import os

class CodeReviewer:
    def __init__(self):
        # 使用通用客戶端，自動享有 Token 統計與耗時追蹤功能
        self.client = LLMClient()

    def review_code(self, topic, code, script_json=None):
        """
        執行系統設計一致性審查 (QA/Reviewer - MetaGPT Pattern)。
        :param topic: 使用者輸入的主題
        :param code: Engineer 生成的 Manim Python 代碼
        :param script_json: (必填) Director 產出的 Visual Rationale (JSON Plan)
        """
        # =========================================================
        # 1. 執行靜態代碼分析 (Gatekeeper)
        # =========================================================
        temp_file = "temp_lint_check.py"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)
        
        success, errors = lint_file(temp_file)
        if os.path.exists(temp_file):
            os.remove(temp_file)

        if not success:
            print("❌ 靜態审查失敗 (Static Analysis Failed) - 攔截 LLM 請求")
            error_report = "FAIL\n\n[Static Analysis Gatekeeper]:\n"
            for err in errors:
                error_report += f"- Line {err['line']} [{err['code']}]: {err['message']}\n"
            return error_report

        print("✅ 靜態審查通過 (Static Analysis Passed)")
        print("🕵️  正在進行深度代碼審查 (QA Compliance Check)...")
        
        # 建立審查上下文
        review_context = f"""
═══════════════════════════════════════════════════════════════════
REVIEW CONTEXT
═══════════════════════════════════════════════════════════════════
Topic: {topic}

System Design (Director's Visual Rationale):
{script_json if script_json else "⚠️ WARNING: No design specification provided!"}
"""

        system_prompt = """You are the Quality Assurance (QA) Reviewer in a professional Multi-Agent Manim System.
Your upstream colleagues are:
  - The Director (who creates Visual Rationale JSON blueprints)
  - The Engineer (who translates JSON into Python code)

Your responsibility: Enforce STRICT System Design Compliance.
Your mission: Verify that the Engineer's Implementation perfectly matches the Director's Design Specification.

═══════════════════════════════════════════════════════════════════
STANDARD OPERATING PROCEDURE (SOP)
═══════════════════════════════════════════════════════════════════

### 1. COMPLIANCE CHECK (Completeness Verification)
❓ Question: "Does the code implement EVERY step defined in the JSON sequence?"

Verification Steps:
□ Count the number of steps in JSON `sequence` array
□ Count the number of animation blocks in Python code
□ Verify 1:1 mapping between JSON steps and code blocks
□ Check that visual_action types match implemented animations

**Critical Rule**: If JSON has 5 steps, code MUST have 5 distinct animation execution blocks.

Red Flags:
✗ Missing steps (e.g., JSON has Step 3, but code skips it)
✗ Extra steps (code adds animations not in JSON)
✗ Wrong action types (JSON says "Create" but code uses "Write")

### 2. VISUAL CONSTRAINTS CHECK (Scene Setup Validation)
❓ Question: "Are all static objects from scene_setup actually created?"

Verification Steps:
□ Parse JSON `scene_setup.static_objects` array
□ Verify each object ID appears in code
□ Check positions match (e.g., JSON "UP*3.5" → code `3.5 * UP`)
□ Validate object types (Text vs MathTex vs NumberLine)

Red Flags:
✗ Missing title or background elements
✗ Position mismatches (JSON says UP, code uses DOWN)
✗ Type mismatches (JSON says Text, code uses MathTex)

### 3. PEDAGOGICAL SIGNAL CHECK (Attention Direction - Mayer's Principle)
❓ Question: "Are signal_action elements implemented?"

Verification Steps:
□ Identify steps with `signal_action` in JSON
□ Verify corresponding Circumscribe/Indicate/FocusOn in code
□ Check signal is executed BEFORE main visual_action
□ Validate color/target matches JSON specification

Red Flags:
✗ signal_action defined but not implemented
✗ Signal executed AFTER instead of BEFORE main action
✗ Wrong signal type (JSON says Circumscribe, code uses Indicate)

### 4. AUDIO SYNCHRONIZATION CHECK (Temporal Alignment)
   ❓ Question: "Does audio timing match the design?"
   
   Verification Steps:
   □ For each step: Verify `remaining_X = max(...)` calculation is present
   □ Check `self.wait(remaining_X)` matches JSON duration field
   □ Ensure wait time accounts for animation runtime
   
   Red Flags:
   ✗ Using `self.add_sound()` (ILLEGAL: System auto-injects this!)
   ✗ Duration mismatch (JSON: 4.5s, Code waits base 2s)
   ✗ No wait() after animations

### 5. MANIM SYNTAX CHECK (Hallucination Detection)
   ❓ Question: "Is the code syntactically correct for Manim CE?"
   
   Verification Steps:
   □ Check for deprecated methods (ShowCreation, TextMobject)
   □ Validate LaTeX strings use raw strings (r"...")
   □ Verify Manim imports (from manim import *)
   □ Check class name matches target scene name
   
   Red Flags:
   ✗ Using ShowCreation instead of Create
   ✗ LaTeX without r"" (will cause escape errors)
   ✗ Non-existent Manim methods
   ✗ Wrong class name

### 6. GEOMETRIC CONSISTENCY CHECK (Spatial Fact-Checking)
   ❓ Question: "Do the object positions in code match the `layout_plan` constraints?"
   
   Verification Steps:
   □ Compare code positions against `layout_plan.anchors` and `layout_plan.objects`.
   □ Verify RELATIVE positioning logic:
     - If Plan says `B` is `RIGHT` of `A`.
     - Code MUST have `B.next_to(A, RIGHT)` or equivalent.
   □ Detect "Spatial Hallucinations":
     - Code using arbitrary `shift(UP*1.23)` when Plan says `align_to`.
     - Code placing objects in the "Death Zone" (y > 3.0 or y < -3.0) unless it's Title/Footer.
     
   Red Flags:
   ✗ Hardcoded magic numbers (e.g., `shift(RIGHT*2.5)`) where relative positioning is required.
   ✗ Object A placed relative to Object B BEFORE Object B is created.
   ✗ Missing `VGroup` for composite objects defined in Plan.

═══════════════════════════════════════════════════════════════════
OUTPUT SPECIFICATION
═══════════════════════════════════════════════════════════════════

### IF ALL CHECKS PASS:
Return EXACTLY this string (nothing else):
```
PASS
```

### IF ANY CHECK FAILS:
Return a structured violation report in Chinese:
```
FAIL

[Compliance]: Missing Step 3 - JSON defines 5 steps but code only implements 4
[Visual Constraints]: Title object missing - JSON specifies title at UP*3.5 but not found in code
[Signal Action]: Step 2 signal_action not implemented - JSON requires Circumscribe but code skips it
[Audio Sync]: Step 4 duration mismatch - JSON specifies 4.5s but code waits only 2s
[Manim Syntax]: Using deprecated ShowCreation - Should use Create instead
[Geometric Consistency]: Hardcoded coordinates detected - Code uses shift(RIGHT*3) instead of next_to as required by Plan
```

═══════════════════════════════════════════════════════════════════
CRITICAL CONSTRAINTS
═══════════════════════════════════════════════════════════════════
✓ Be STRICT - This is quality control, not a suggestion system
✓ Check EVERY criteria - Do not skip any of the 5 checks
✓ Report ALL violations - Not just the first one found
✗ Do NOT give suggestions - Only report violations
✗ Do NOT be lenient - Small errors still fail the review
✗ Do NOT add explanations - Stick to the violation format
"""

        user_prompt = f"""
{review_context}

═══════════════════════════════════════════════════════════════════
IMPLEMENTATION (Engineer's Python Code)
═══════════════════════════════════════════════════════════════════
{code}

═══════════════════════════════════════════════════════════════════
EXECUTE COMPLIANCE REVIEW
═══════════════════════════════════════════════════════════════════
Perform the complete 5-step SOP check now.
Report: PASS or structured FAIL with violations.
"""
        # 呼叫 LLMClient，自動在終端機印出細節
        response = self.client.ask(system_prompt, user_prompt, role="reviewer")
        return response