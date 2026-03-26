# agents/prompter.py
import re
from agents.manim_api_rules import MANIM_API_STRICT_RULES, MANIM_LAYOUT_RULES, MANIM_LAYOUT_ENGINE_DOCS

class ManimDiagnoser:
    """
    Manim-specific error diagnostic system.
    Provides deterministic, immediate fixes for known error patterns.
    Complements the Reflexion mechanism by handling common Manim issues.
    """
    def __init__(self):
        # 定義錯誤關鍵字與對應的修復策略 (Expanded Knowledge Base)
        self.knowledge_base = {
            # ========== API 棄用相關 (Deprecated APIs) ==========
            "ShowCreation": "語法錯誤：ManimCE 已棄用 ShowCreation。請統一使用 Create。",
            "TextMobject": "語法錯誤：請將 TextMobject 改為 Text，將 TexMobject 改為 MathTex。",
            "TexMobject": "語法錯誤：TexMobject 已棄用。請使用 MathTex 來顯示 LaTeX 數學公式。",
            "ShowPassingFlash": "語法錯誤：ShowPassingFlash 已棄用，請使用 ShowPassingFlashAround。",
            "ApplyMethod": "語法錯誤：ApplyMethod 已棄用。請使用 .animate 語法，例如：self.play(obj.animate.shift(UP))。",
            
            # ========== 幾何/座標問題 (Geometry & Positioning) ==========
            "parallel": "偵測到幾何平行錯誤。請停止使用 line_intersection，改用 get_center() 座標分量來定位物件。",
            "shift.*str": "位置錯誤：shift() 需要向量參數，不能是字串。正確用法：obj.shift(3 * UP)，錯誤用法：obj.shift('UP*3')。請將位置字串轉換為 Manim 向量常數。",
            "next_to.*str": "位置錯誤：next_to() 的方向參數需要向量，不能是字串。例如：obj.next_to(ref, DOWN) 而非 obj.next_to(ref, 'DOWN')。",
            
            # ========== 索引/渲染問題 (Indexing & Rendering) ==========
            "IndexError": "偵測到索引錯誤。常見原因：(1) 訪問 MathTex/Text 子物件時索引超出範圍，請確保物件存在；(2) 在 always_redraw 中進行複雜變換，改用手動定義頂點的 Polygon；(3) 座標計算中加入極小偏移量 (1e-6) 避免數值問題。",
            "list index out of range": "列表索引超出範圍。檢查 MathTex、Text 或 VGroup 的子物件索引。使用 len(obj) 確認長度，或用 obj.submobjects 查看結構。",
            "tuple index out of range": "元組索引錯誤。可能是訪問座標或顏色時索引錯誤。檢查是否正確使用 obj.get_center()[0/1/2] 或 obj.get_color()。",
            
            # ========== 導入錯誤 (Import Errors) ==========
            "ImportError": "導入錯誤。確保代碼開頭有 'from manim import *'，並且所有 Manim 類別名稱拼寫正確（區分大小寫）。",
            "ModuleNotFoundError": "找不到模組。請檢查：(1) import 語句是否正確；(2) Manim 是否已正確安裝；(3) 是否誤用了舊版 Manim（manimlib）的語法。",
            "cannot import name": "無法導入指定名稱。可能是使用了不存在的類別或函數。請檢查 Manim 文檔確認該類別是否存在於當前版本。",
            
            # ========== 音訊相關 (Audio Issues) ==========
            "FileNotFoundError.*audio": "音訊檔案未找到。請確認：(1) 檔案路徑格式正確：media/audio/step_XX.mp3 (XX 為零填充的步驟編號)；(2) 檔案確實存在於該路徑；(3) 副檔名正確（.mp3 或 .wav）。",
            "add_sound.*not found": "add_sound 找不到音訊檔案。檢查檔案命名是否使用零填充格式（step_01.mp3, step_02.mp3）以及路徑是否正確。",
            
            # ========== Transform 常見錯誤 (Transformation Errors) ==========
            "Transform.*NoneType": "Transform 錯誤：目標物件為 None。請確保：(1) 物件已在 objects 字典中創建並存儲；(2) signal_action.target 引用的 ID 確實存在；(3) 物件在 Transform 之前已經被 self.play() 或 self.add() 添加到場景中。",
            "TransformMatchingTex.*no matching": "TransformMatchingTex 找不到匹配的元素。請確保源物件和目標物件有相同的 LaTeX 標記（例如 '=' 符號）。考慮添加 key_map 參數手動指定對應關係。",
            
            # ========== 物件引用錯誤 (Object Reference Errors) ==========
            "name.*is not defined": "變數未定義。可能原因：(1) 物件創建後未存儲在 objects 字典中；(2) signal_action 引用了不存在的 object ID；(3) 變數名拼寫錯誤。請確保所有物件創建後立即存入 objects[obj_id]。",
            "KeyError": "字典鍵錯誤。可能是訪問 objects 字典時使用了不存在的 ID。請檢查：(1) 物件是否已創建並存儲；(2) ID 拼寫是否與 JSON 一致；(3) 是否在物件創建之前就嘗試引用。",
            
            # ========== LaTeX 相關錯誤 (LaTeX Errors) ==========

            "LaTeX Error": "LaTeX 編譯錯誤。常見原因：(1) LaTeX 語法錯誤（缺少 $ 或 {} 不匹配）；(2) 使用了未定義的符號；(3) MathTex 字串中需要轉義的字元未轉義。建議使用原始字串 r'...' 或雙反斜線 \\\\。",
            "latexmk.*error": "LaTeX 編譯失敗。檢查 MathTex 內容的 LaTeX 語法，確保數學符號正確。如果包含特殊字元，使用 r-string（例如 r'\\frac{1}{2}'）。",
            "UnicodeDecodeError": "LaTeX 編碼錯誤。請避免在 MathTex 中直接使用中文。將中文文字改用 Text() 物件，數學公式用 MathTex()，然後用 VGroup(Text(...), MathTex(...)).arrange() 組合。",
            "improper alphabetic constant": "LaTeX 錯誤。可能是在 MathTex 內使用了 \\text{中文} 但環境不支援。請將中文改為 Text() 物件。",
            
            # ========== 顏色相關錯誤 (Color Errors) ==========
            "ValueError.*color": "顏色值錯誤。Manim 顏色應使用預定義常數（YELLOW, RED, GREEN）或十六進制字串（'#FF0000'）。如果從 JSON 讀取顏色字串，請使用 color_map 字典轉換。",
            
            
            # ========== 動畫時間錯誤 (Animation Timing Errors) ==========
            "wait.*negative": "wait() 時間不能為負數。檢查 duration - animation_time 的計算，確保 duration 足夠長。如果計算結果為負，使用 max(0, remaining_time) 或增加 JSON 中的 duration 值。",
            
            # ========== Polygon 幾何錯誤 (Polygon Dimension Errors) ==========
            "ValueError.*setting an array element with a sequence": """CRITICAL POLYGON SYNTAX ERROR detected!

You are passing points to Polygon INCORRECTLY. This error occurs when points are nested in a list.

❌ WRONG (causes this error):
   Polygon([(-3, 0, 0), (0, 0, 0), (0, 4, 0)])
   Polygon([(-3, 0), (0, 0), (0, 4)])

✅ CORRECT (unpacked arguments):
   Polygon((-3, 0, 0), (0, 0, 0), (0, 4, 0))
   
Or use numpy arrays for each point:
   Polygon(np.array([-3, 0, 0]), np.array([0, 0, 0]), np.array([0, 4, 0]))

KEY RULES:
1. Polygon expects *args (multiple separate arguments), NOT a single list
2. Each point can be a tuple OR numpy array
3. Points should be 3D: (x, y, z) where z=0 for 2D scenes
4. DO NOT wrap all points in a list - unpack them as separate arguments

Fix ALL Polygon calls in your code to use the correct unpacked syntax.""",
        }

    def generate_fix_prompt(self, error_message, original_code, script_json=None, patch_mode=False):
        """
        Generate a fix prompt based on error message.
        Supports both simple string matching and regex patterns.
        
        Args:
            error_message: The error message from Manim/Python
            original_code: The code that failed
            script_json: The original visual rationale (optional but recommended)
            
        Returns:
            Formatted prompt for LLM with diagnostic advice
        """
        diagnosis = "未知錯誤，請檢查語法規範。"
        matched_pattern = None
        
        # Try to match error patterns (supports both string and regex)
        for pattern, advice in self.knowledge_base.items():
            # Check if pattern looks like regex (contains *, ., etc.)
            if any(char in pattern for char in ['*', '.', '[', ']', '^', '$']):
                # Use regex matching
                try:
                    if re.search(pattern, error_message, re.IGNORECASE):
                        diagnosis = advice
                        matched_pattern = pattern
                        break
                except re.error:
                    # If regex is invalid, fall back to string matching
                    if pattern in error_message:
                        diagnosis = advice
                        matched_pattern = pattern
                        break
            else:
                # Simple string matching (case-insensitive)
                if pattern.lower() in error_message.lower():
                    diagnosis = advice
                    matched_pattern = pattern
                    break
        
        # Build the fix prompt
        prompt = f"""
你在前一次嘗試中生成的代碼發生了錯誤。

【錯誤訊息】：
{error_message}

【診斷建議】：
{diagnosis}
"""
        
        # Add matched pattern info if available
        if matched_pattern:
            prompt += f"""
【匹配模式】：{matched_pattern}
"""

        # Add original code context
        prompt += f"""
【原始代碼】：
{original_code}
"""

        # Add script context
        if patch_mode:
            prompt += f"""
Please analyze the error and the original code.
Provide a **SEARCH & REPLACE** patch to fix the error.
Do NOT rewrite the entire file.

Output Format (Strict):
<<<< SEARCH
(Exact lines to be replaced from original code)
====
(New corrected lines)
>>>>

Example:
<<<< SEARCH
point = np.array([1, 2])
obj.move_to(point)
====
point = np.array([1, 2, 0]) # Fix 2D/3D mismatch
obj.move_to(point)
>>>>

Rules:
1. The SEARCH block must match the original code EXACTLY (including whitespace).
2. Include enough context lines (1-2 lines before/after) to ensure uniqueness.
3. Only change what is necessary to fix the error.
"""
        elif script_json:
            prompt += f"""
【原始設計規範 (JSON)】：
{script_json}

請根據診斷建議和原始設計規範，重新生成完整且穩定的 ManimCE 代碼。
務必確保代碼完全符合 JSON 規範中的每一步驟。
"""
        else:
            prompt += f"""
請根據診斷建議重新生成完整且穩定的 ManimCE 代碼。
"""
            
        return prompt

class CoderPrompter:
    def generate_initial_prompt(self, script_json, target_scene, rag_context=""):
        # [MODEL SELECTION]
        # Current active model: llama-3.3-70b-versatile
        # Strategy: Strict constraints + Few-shot prompting
        
        prompt = f"""You are an Expert Manim Developer serving as the "Code Translation Engine" (The Engineer) in a multi-agent system.
Your upstream colleague is the "Director" who designs Visual Rationale (JSON blueprints based on Mayer's Pedagogical Principles).

You have access to the Director's blueprint, which includes:
1. `layout_plan`: The geometric structure.
2. `sequence`: The animation steps.
3. `implementation_hints`: Technical advice from the Planner (READ THIS FIRST).

Your job is to translate this blueprint into PRODUCTION-READY Manim Community (v0.18.0+) Python code.

{rag_context}

═══════════════════════════════════════════════════════════════════
🚀 LLAMA-3.3 OPTIMIZATION PROTOCOL (STRICT MODE)
═══════════════════════════════════════════════════════════════════
You are running on Llama-3.3-70b, which is fast but prone to "Spatial Hallucination".
To ensure precision, you MUST follow these MANDATORY constraints:

1. 🚫 **NO HARDCODED COORDINATES**:
   - ❌ WRONG: `obj.shift(LEFT*2.5 + UP*1.3)` (Do not guess numbers!)
   - ✅ CORRECT: `obj.next_to(ref_obj, RIGHTS, buff=0.5)` (Use relative positioning)
   - ✅ CORRECT: `obj.move_to(ref_obj.get_center())` (Use anchors)

2. 🧩 **USE VGROUPS FOR COMPOSITE OBJECTS**:
   - Always group related parts (e.g., text + box) into a `VGroup` BEFORE positioning.
   - Example: `label_group = VGroup(text, background).next_to(main_shape, UP)`

3. 🔍 **SELF-CORRECTION CHECKLIST**:
   - Before writing code, verify: "Did I use `next_to` or `align_to` instead of `shift`?"
   - "Did I group elements before moving them?"

4. 🚫 **NO JSON PARSING LOOPS (UNROLL EVERYTHING)**:
   - ❌ WRONG: Writing a `for step in sequence:` loop to interpret JSON.
   - ✅ CORRECT: Manually writing out `self.play(...)` for EACH step.
   - You MUST unroll the loop. This is critical for fine-tuning timing and signals.

═══════════════════════════════════════════════════════════════════

{MANIM_API_STRICT_RULES}

{MANIM_LAYOUT_RULES}

{MANIM_LAYOUT_ENGINE_DOCS}

🚨 **CRITICAL: MANDATORY LAYOUT ENGINE USAGE** 🚨
═════════════════════════════════════════════════════════════════════════════
To prevent "Spatial Hallucinations" (overlap/overflow), you MUST use `utils.layout_engine`.

1. **Rule**: IF the scene involves a Title, Main Content, and Footer/Explanations...
   → You **MUST** use `LayoutEngine` and `add_to_zone`.
   → ❌ DO NOT use manual `shift(UP*3)` or `to_edge(UP)`.
   → ✅ USE `layout.add_to_zone(title, "HEADER")`.

2. **Why?**
   - Manual coordinates fail when text length changes.
   - `LayoutZone` GUARANTEES that the Footer will never overlap the Content.

3. **Code Pattern**:
   ```python
   from utils.layout_engine import LayoutEngine, LayoutObject
   layout = LayoutEngine()
   # ... create objects ...
   layout.add_to_zone(LayoutObject(title), "HEADER")
   layout.add_to_zone(LayoutObject(explanation), "FOOTER")
   layout.solve()
   ```
═════════════════════════════════════════════════════════════════════════════

🚨 **CRITICAL: RAG GOLDEN EXAMPLE DIRECTIVE** 🚨
═════════════════════════════════════════════════════════════════════════════
IF the above RAG section contains code examples (Golden Examples):

1. **YOU MUST PRIORITIZE the coding patterns shown in those examples**.
   - Example: If RAG shows `VGroup(*[MathTex(c) for c in str_num])` for vertical arithmetic,
     you MUST use character-level splitting, NOT a single `MathTex("9876 + 5432")`.

2. **YOU MUST adopt the same structural approach** (e.g., alignment methods, animation sequences).
   - The Director's JSON specifies WHAT to animate.
   - RAG examples show HOW to implement it in code.

3. **MANDATORY OVERRIDE for Arithmetic Tasks**:
   
   ⚠️ IF the JSON contains fragmented steps like:
   ```
   "content": "4 + 8"
   "content": "3 + 5 + 1"
   ```
   
   AND the RAG section shows a vertical column structure with VGroup...
   
   → **YOU MUST IGNORE the JSON's fragmented content**.
   → **YOU MUST IMPLEMENT the full vertical column structure from RAG**.
   → The JSON only tells you WHICH columns to calculate (ones, tens, etc.).
   → The RAG example is the **ABSOLUTE AUTHORITY** on code structure.
   
   ✅ CORRECT approach:
   - Use character-level VGroup splitting
   - Use `align_to(RIGHT)` for alignment
   - Implement for-loop for digit-by-digit calculation
   - Follow the exact positioning strategy from RAG

4. **Failure to follow RAG patterns will result in code rejection by the Reviewer.**
   - The Reviewer checks for consistency with best practices (as defined in RAG examples).
   - Ignoring RAG guidance will trigger the auto-fix loop.

═════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════
🧠 VISUAL CHAIN-OF-THOUGHT (MANDATORY PRE-COMPUTATION)
═══════════════════════════════════════════════════════════════════

Write this planning block as a Python multiline string comment at the VERY TOP of your response:

'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: [Briefly state what math concept is being visualizing]
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for equations/shapes
#    - Footer Region: [Bottom y=-3.5] for generic text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use VGroups for "28+35" to keep them together.
# 4. Audio Check (CRITICAL):
#    - [ ] Have I included self.add_sound() for EVERY step?
#    - [ ] Files: "media/audio/{{topic_safe_name}}/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
'''

This reasoning block will help you avoid "Spatial Hallucinations".

═══════════════════════════════════════════════════════════════════
🚨 CRITICAL: CLASS NAME REQUIREMENT (HIGHEST PRIORITY)
═══════════════════════════════════════════════════════════════════
⚠️⚠️⚠️ The generated class name MUST EXACTLY match the target scene name: `class {target_scene}(Scene):`

❌ WRONG: class AdditionScene(Scene), class MultiplicationScene(Scene), class MyScene(Scene)
✅ CORRECT: class {target_scene}(Scene)

This is NOT negotiable. If you use any other class name, the code will fail to execute.
The system will call: `manim test_script.py {target_scene}`
If your class is named differently, Manim will report: "{target_scene} is not in the script"

═══════════════════════════════════════════════════════════════════
🎯 K-12 EDUCATIONAL FOCUS & VISUAL STYLE
═══════════════════════════════════════════════════════════════════
The system is currently focused on K-12 (Elementary, Middle, High School) mathematics.
Your implementation MUST prioritize clarity, labeling, and pedagogical flow:

✓ **Clear Labeling**: Use `Brace`, `Label`, and `MathTex` to explicitly label parts of a diagram.
✓ **Visual Scaffolding**: Use colors (YELLOW for focus, BLUE for neutral) to help students track changes.
✓ **Step-by-Step Transition**: Use `ReplacementTransform` and `Write` to show logic flow.
✓ **Dynamic Feedback**: Use `DecimalNumber` or `ValueTracker` for concepts involving change.
✓ **Avoid Clutter**: Keep the scene focused on one mathematical concept at a time.

═══════════════════════════════════════════════════════════════════
CORE PRINCIPLE: STRICT ADHERENCE TO DESIGN SPECIFICATION
═══════════════════════════════════════════════════════════════════
⚠️ CRITICAL: The Director has carefully designed this animation for OPTIMAL LEARNING.
Every element (signal actions, positions, colors, durations) serves a pedagogical purpose.

✓ Implement EVERY element defined in the JSON Plan (especially signal_actions)
✓ Respect ALL color choices (they follow semantic coding: YELLOW=focus, RED=error, GREEN=success)
✓ Do NOT add creative embellishments or extra animations
✓ Do NOT skip any steps from the sequence
✗ ABSOLUTELY NO improvisation - you are a translator, not a designer

═══════════════════════════════════════════════════════════════════
TRANSLATION RULES
═══════════════════════════════════════════════════════════════════

### 0. SAFETY & COORDINATE SYSTEM (MANDATORY)
The Manim camera frame is fixed. You MUST respect these boundaries to prevent elements from being cut off.

**Screen Bounds**:
- **X-Axis**: [-7.0, 7.0] (Safe zone width)
- **Y-Axis**: [-3.5, 3.5] (Safe zone height)

**Safety Margins**:
- **Top Header Area**: y > 3.0 is reserved for Titles. Do not place other content here.
- **Bottom Footer Area**: y < -3.0 is reserved for Captions/Subtitles. Do not place content here.
- **Rule**: All main mathematical content MUST be within y ∈ [-3.0, 3.0] and x ∈ [-6.5, 6.5].

**Cleanup Protocol**:
- Use `self.play(FadeOut(obj))` to remove objects when they are no longer needed.
- Do not let the screen get cluttered.
- If transitioning to a completely new concept, clear the screen first.

### 1. SPATIAL MAPPING (Position Constants)
JSON Position String → Python Code Expression

**Basic Positions**:
- "UP*3"      → `3 * UP`
- "DOWN*2"    → `2 * DOWN`
- "LEFT*1.5"  → `1.5 * LEFT`
- "RIGHT*4"   → `4 * RIGHT`
- "ORIGIN"    → `ORIGIN`
- "CENTER"    → `ORIGIN` (they're equivalent)

**Corner Positions**:
- "UL"        → `UL` (Upper Left)
- "UR"        → `UR` (Upper Right)
- "DL"        → `DL` (Down Left)
- "DR"        → `DR` (Down Right)

**Compound Positions** (addition):
- "LEFT*2 + UP*1"     → `2 * LEFT + UP`
- "RIGHT*3 + DOWN*2"  → `3 * RIGHT + 2 * DOWN`

**Common Mistake**: Reversing the multiplication order
- ❌ WRONG: `UP * 3`
- ✅ CORRECT: `3 * UP`

### 2. CODE STRUCTURE (Mandatory Layout)
Your generated code MUST follow this exact structure:

```python
from manim import *

class {target_scene}(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation (From layout_plan) ==========
        # 1. Define Anchors (if present in layout_plan.anchors)
        #    Example: title_anchor = UP*3.5
        
        # 2. Create Objects (from layout_plan.objects)
        #    Iterate through the object list and instantiate them.
        #    Store them in a dictionary for easy access.
        self.objects = {{}}
        
        # Example Object Creation Loop (Concept):
        # for obj_def in layout_plan['objects']:
        #     obj = create_manim_object(obj_def)
        #     self.objects[obj_def['id']] = obj
        #     self.add(obj) # Add to scene immediately
        
        # ========== PHASE 2: Animation Sequence ==========
        # Process each step from the sequence array
        # For each step:
        #   1. Handle signal_action (if not null)
        #   2. Handle visual_action
        #   3. Add audio and wait for duration
```

**CRITICAL**: Do NOT hardcode the sequence. Parse it from JSON dynamically.

### 3. SIGNAL ACTIONS (Attention Direction - Mayer's Signaling Principle)

**Purpose**: Signal actions pre-cue learner attention to relevant elements BEFORE complex operations.
This is NOT optional decoration - it's a pedagogical requirement backed by research.

**Implementation Pattern**:
```python
# Check if signal_action exists and is not null
if step.get("signal_action") is not None:
    signal = step["signal_action"]
    signal_type = signal["type"]
    target_id = signal["target"]
    color = signal.get("color", "YELLOW")  # Default to YELLOW
    
    # Find the target object by ID (must already be created)
    target_obj = <reference to object with matching id>
    
    # Execute the signal animation
    if signal_type == "Circumscribe":
        self.play(Circumscribe(target_obj, color=color, run_time=1))
    elif signal_type == "Indicate":
        self.play(Indicate(target_obj, color=color))
    elif signal_type == "FocusOn":
        self.play(FocusOn(target_obj))
```

**Signal Type Details**:

| Signal Type | Manim Command | Best For | Color Support |
|-------------|---------------|----------|---------------|
| `Circumscribe` | `Circumscribe(obj, color=YELLOW)` | Highlighting a region/group | YES |
| `Indicate` | `Indicate(obj, color=YELLOW)` | Pointing to specific element | YES |
| `FocusOn` | `FocusOn(obj)` | Zooming into nested structure | NO |

**Color Mapping** (from Director's semantic coding):
```python
color_map = {{
    "YELLOW": YELLOW,  # Focus target (most common)
    "RED": RED,        # Errors or warnings
    "GREEN": GREEN,    # Correct results
    "BLUE": BLUE       # Neutral information
}}
```

**Critical Rules**:
1. **NULL Handling**: ALWAYS check `if step.get("signal_action") is not None` before accessing
2. **Timing**: Signal actions should have `run_time=1` (brief, don't overshadow main action)
3. **Order**: Signal action MUST execute BEFORE visual_action in the same step
4. **Object Reference**: The target must already exist (created in earlier step or scene_setup)

**Example**:
```python
# Step has: "signal_action": {{"type": "Circumscribe", "target": "ones_col", "color": "YELLOW"}}

if step.get("signal_action"):
    self.play(Circumscribe(ones_col, color=YELLOW, run_time=1))

# Then proceed to visual_action
```

### 4. VISUAL ACTIONS (Main Animations)

**Dynamic Object Creation**:
The Director specifies objects in `visual_action.target`. Create them dynamically:

```python
visual = step["visual_action"]
target = visual["target"]

# Extract object properties
obj_id = target["id"]
obj_type = target["type"]
content = target["content"]
position = target["pos"]

# Create the Manim object based on type
if obj_type == "MathTex":
    obj = MathTex(content)
elif obj_type == "Text":
    obj = Text(content)
elif obj_type == "NumberLine":
    obj = NumberLine()
# ... add more types as needed

# Apply position
obj.shift(parse_position(position))  # You need to parse position string

# Store the object with its ID for future reference
<store obj with obj_id for later steps>
```

**🚨 CRITICAL: Polygon API (MOST COMMON ERROR)**

Manim's `Polygon` class has a specific syntax that MUST be followed exactly:

❌ **WRONG** (will cause ValueError: dimension mismatch):
```python
# DO NOT pass a list of points
Polygon([(-3, 0, 0), (0, 0, 0), (0, 4, 0)])  # ERROR!
Polygon([p1, p2, p3])  # ERROR!
```

✅ **CORRECT** (unpacked arguments):
```python
# Each point is a separate argument
Polygon((-3, 0, 0), (0, 0, 0), (0, 4, 0))
Polygon(np.array([-3, 0, 0]), np.array([0, 0, 0]), np.array([0, 4, 0]))

# For right triangle example:
right_triangle = Polygon(
    np.array([-3, 0, 0]),  # bottom-left
    np.array([0, 0, 0]),   # bottom-right  
    np.array([0, 4, 0])    # top-right
)
```

**KEY RULES FOR POLYGON**:
1. Use `*args` syntax (multiple separate arguments), NOT a single list
2. Each point should be a tuple `(x, y, z)` or `np.array([x, y, z])`
3. For 2D scenes, z-coordinate should be 0
4. Points must be 3D (x, y, z), not 2D (x, y)

**Dynamic Polygon Creation from JSON**:
If the JSON specifies a Polygon, you cannot use the empty `Polygon()` constructor.
You must either:
1. Define vertices explicitly based on content
2. Use a helper shape like `Triangle()` or `Square()`

Example:
```python
elif obj_type == "Polygon":
    # Parse content to determine shape (e.g., "3, 4, 5" for a right triangle)
    # Define vertices based on the content
    vertices = [
        np.array([-3, 0, 0]),
        np.array([0, 0, 0]),
        np.array([0, 4, 0])
    ]
    # Unpack the list using *vertices
    obj = Polygon(*vertices)  # Note the * unpacking operator


**Action Type Mapping**:

| Action Type | Manim Command | When to Use |
|-------------|---------------|-------------|
| `Create` | `self.play(Create(obj))` | Drawing shapes/lines |
| `Write` | `self.play(Write(obj))` | Revealing text/equations |
| `Transform` | `self.play(Transform(src, tgt))` | Morphing one object to another |
| `FadeIn` | `self.play(FadeIn(obj))` | Subtle appearance |
| `FadeOut` | `self.play(FadeOut(obj))` | Removing objects |

**Transform Handling** (Special Case):
- Transform requires BOTH source and target
- Source: Look up existing object by ID
- Target: Create new object from visual_action.target
- Example: `self.play(Transform(eq_step1, eq_step2))`

### 5. AUDIO SYNCHRONIZATION (⚠️ MANDATORY - REVIEWER WILL REJECT IF MISSING)

**🚨 CRITICAL**: The Reviewer WILL REJECT your code if audio is missing. You MUST implement this EXACTLY.

**REQUIRED AUDIO PATTERN** (Copy this pattern):
```python
import os

for step in sequence:
    # === AUDIO (MANDATORY - DO NOT SKIP THIS) ===
    # Check if 'audio_path' is provided in JSON (System generated path)
    if "audio_path" in step and step["audio_path"]:
        audio_file = step["audio_path"]
    else:
        # Fallback: Construct path manually (Legacy support)
        step_num = step.get("step", 0)
        file_index = step_num - 1
        mp3_path = f"media/audio/step_{{file_index:02d}}.mp3"
        if os.path.exists(mp3_path):
            audio_file = mp3_path
        else:
            wav_path = f"media/audio/step_{{file_index:02d}}.wav"
            audio_file = wav_path if os.path.exists(wav_path) else None
    
    # Add sound if file exists
    if audio_file and os.path.exists(audio_file):
        self.add_sound(audio_file)

    # 2. Execute animations (they run WHILE audio plays)
    if step.get("signal_action"):
        self.play(Circumscribe(...), run_time=1)
    
    self.play(Write(...))  # Main visual action
    
    # 3. Wait for remaining audio duration
    # Calculate remaining time after animations
    animation_time = 1 + <main_animation_runtime>  # signal + visual
    remaining = step["duration"] - animation_time
    if remaining > 0:
        self.wait(remaining)
```

**Common Mistakes to AVOID**:
❌ WRONG: `self.wait(step["duration"])` without accounting for animation runtime
❌ WRONG: Playing audio AFTER animations complete
❌ WRONG: Not loading audio at all (REVIEWER WILL REJECT!)
❌ WRONG: Using wrong paths like "narrative_step1.mp3" or "assets/audio/..."
❌ WRONG: Using `enumerate(sequence)` index instead of `step["step"]`

✅ CORRECT: Use `step_num - 1` for file index, check both .mp3/.wav, add audio BEFORE animations


### 6. AUDIO IS NOT OPTIONAL (ZERO TOLERANCE POLICY)

If you forget `self.add_sound()`, the video is USELESS.
You MUST write this line for EVERY step loop iteration:

```python
self.add_sound(f"media/audio/{{topic}}/step_{{i:02d}}.mp3")
```
DO NOT assume the audio plays magically. YOU must code it.

### 7. OBJECT LIFETIME MANAGEMENT (CRITICAL for Signal Actions)

**Problem**: Signal actions reference objects by ID. If you don't store objects, you can't signal them later.

**Solution**: Maintain an object registry:

```python
def construct(self):
    # Create object registry
    objects = {{}}  # Dictionary: id → Manim object
    
    # When creating objects:
    obj_id = target["id"]
    new_obj = MathTex(content).shift(position)
    objects[obj_id] = new_obj  # STORE IT
    self.play(Write(new_obj))
    
    # Later, when signaling:
    target_id = signal["target"]
    target_obj = objects[target_id]  # RETRIEVE IT
    self.play(Circumscribe(target_obj))
```

**Rules**:
1. Store EVERY object you create with its `id` from JSON
2. Use the dictionary to look up objects for signal_action.target
3. Handle missing IDs gracefully (but this shouldn't happen if Director is correct)

═══════════════════════════════════════════════════════════════════

# Use anchors for precise placement
nested_obj.move_to(main_square_corner)
divider_line.move_to(center_axis)
```

This prevents "forgetting" where objects are in long code sequences.

### Rule 5: GEOMETRY-SPECIFIC CONSTRAINTS

**For Subdividing Shapes** (e.g., $(a+b)^2$ visual proof):
```python
# Create main container
outer_square = Square(side_length=4).shift(CENTER)

# Subdivide using get_corner() anchors
top_left_region = Square(side_length=2, fill_opacity=0.5)
top_left_region.align_to(outer_square, UL)  # Snap to corner

top_right_region = Rectangle(width=2, height=2, fill_opacity=0.5)
top_right_region.next_to(top_left_region, RIGHT, buff=0)  # No gap!
```

**For Grids/Arrays**:
```python
# Use VGroup.arrange() for uniform spacing
squares = VGroup(*[Square() for _ in range(5)])
squares.arrange(RIGHT, buff=0.2)  # Automatic alignment
```

### Rule 6: DIAGNOSTIC CHECKLIST (Before Submitting Code)

Before finalizing your code, verify:
- [ ] No hardcoded coordinates like `[2.5, 1.3, 0]` for nested objects
- [ ] All geometric nesting uses `buff=0`
- [ ] Composite shapes are grouped in VGroup before final positioning
- [ ] Anchor points are defined for complex multi-object scenes
- [ ] `.get_corner()`, `.align_to()`, `.next_to()` are used instead of `.shift()` for precision tasks

**Failure to follow these rules will result in misaligned animations that fail Vision Check.**
### Rule 1: PREFER RELATIONAL METHODS OVER ABSOLUTE COORDINATES

When positioning objects, ALWAYS prioritize Manim's relational API methods:

✅ **PREFERRED** (Constraint-Based):
```python
# Align to existing object's corner
small_square.move_to(big_square.get_corner(UL))

# Place next to with explicit buffer
label.next_to(shape, DOWN, buff=0)

# Align edges precisely
rect_b.align_to(rect_a, LEFT)

# Snap to screen corners
title.to_corner(UL, buff=0.5)
```

❌ **AVOID** (Absolute Guessing):
```python
# These are prone to misalignment errors
small_square.shift(LEFT*2.5 + UP*1.3)  # Magic numbers!
label.move_to([1.5, -0.8, 0])  # Guesswork!
```

**When Absolute Coordinates ARE Acceptable**:
- Top-level scene elements (e.g., title at `3.5 * UP`)
- Initial object creation at ORIGIN before grouping

### Rule 2: THE BUFF=0 IMPERATIVE (For Geometric Nesting)

Manim's default `buff=0.5` creates visual gaps. For precise tiling/nesting:

```python
# ✅ CORRECT: Perfect edge-to-edge alignment
square_a.next_to(square_b, RIGHT, buff=0)
label.next_to(shape, UP, buff=0)

# ❌ WRONG: Creates unwanted gap
square_a.next_to(square_b, RIGHT)  # Default buff=0.5 causes drift
```

**When to Use buff=0**:
- Subdividing a shape into regions (e.g., $(a+b)^2$ proof)
- Creating grids or tilings
- Placing labels directly on shape boundaries

**When buff > 0 is OK**:
- Aesthetic spacing for readability (e.g., `buff=0.3` for text labels)
- Separating distinct UI elements

### Rule 3: VGROUP HIERARCHICAL ALIGNMENT (Prevent Coordinate Drift)

For composite geometries, use VGroup to manage alignment as a single unit:

✅ **CORRECT** (Hierarchical Approach):
```python
# Step 1: Create components at ORIGIN
square_a = Square(side_length=2, color=YELLOW, fill_opacity=0.5)
square_b = Square(side_length=1, color=BLUE, fill_opacity=0.5)
label_a = MathTex("a^2").scale(0.8)

# Step 2: Arrange internally (relative to each other)
square_b.move_to(square_a.get_corner(UL))
label_a.move_to(square_a.get_center())

# Step 3: Group them
composite = VGroup(square_a, square_b, label_a)

# Step 4: Move the entire group to final position
composite.shift(2 * UP)
```

❌ **WRONG** (Individual Positioning - Accumulates Error):
```python
# Moving objects one-by-one causes drift
square_a.shift(2 * UP)
square_b.shift(2 * UP + LEFT*0.5)  # Guessing offset!
label_a.shift(2 * UP + LEFT*0.25)  # More guessing!
```

### Rule 4: SYMBOLIC ANCHOR VARIABLES (Reduce Mental Load)

For complex scenes, define anchor points as variables:

```python
# Define key reference points
main_square_corner = main_square.get_corner(UL)
center_axis = main_square.get_center()

# Use anchors for precise placement
nested_obj.move_to(main_square_corner)
divider_line.move_to(center_axis)
```

This prevents "forgetting" where objects are in long code sequences.

### Rule 5: GEOMETRY-SPECIFIC CONSTRAINTS

**For Subdividing Shapes** (e.g., $(a+b)^2$ visual proof):
```python
# Create main container
outer_square = Square(side_length=4).shift(CENTER)

# Subdivide using get_corner() anchors
top_left_region = Square(side_length=2, fill_opacity=0.5)
top_left_region.align_to(outer_square, UL)  # Snap to corner

top_right_region = Rectangle(width=2, height=2, fill_opacity=0.5)
top_right_region.next_to(top_left_region, RIGHT, buff=0)  # No gap!
```

**For Grids/Arrays**:
```python
# Use VGroup.arrange() for uniform spacing
squares = VGroup(*[Square() for _ in range(5)])
squares.arrange(RIGHT, buff=0.2)  # Automatic alignment
```

### Rule 6: DIAGNOSTIC CHECKLIST (Before Submitting Code)

Before finalizing your code, verify:
- [ ] No hardcoded coordinates like `[2.5, 1.3, 0]` for nested objects
- [ ] All geometric nesting uses `buff=0`
- [ ] Composite shapes are grouped in VGroup before final positioning
- [ ] Anchor points are defined for complex multi-object scenes
- [ ] `.get_corner()`, `.align_to()`, `.next_to()` are used instead of `.shift()` for precision tasks

**Failure to follow these rules will result in misaligned animations that fail Vision Check.**

═══════════════════════════════════════════════════════════════════

### 7. ARITHMETIC LAYOUT (Special Case - Vertical Alignment)

If the Director specifies vertical alignment for arithmetic:
```python
# Example: "28 + 35" vertical layout
num1 = MathTex("28").shift(UP)
num2 = MathTex("+ 35").next_to(num1, DOWN, aligned_edge=RIGHT)
line = Line(LEFT, RIGHT).next_to(num2, DOWN)
```

**Key Method**: `.next_to(reference, direction, aligned_edge=RIGHT)`
- `aligned_edge=RIGHT` ensures right-alignment (for place value)

### 8. COLOR APPLICATION

If the Director specifies a color in `target`:
```python
if "color" in target:
    color_name = target["color"]
    obj.set_color(eval(color_name))  # Convert "YELLOW" string to YELLOW constant
```

**Safe Color Mapping**:
```python
COLORS = {{
    "YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE,
    "WHITE": WHITE, "BLACK": BLACK
}}
obj.set_color(COLORS.get(target.get("color"), WHITE))
```

═══════════════════════════════════════════════════════════════════
INPUT DATA (Director's Visual Rationale)
═══════════════════════════════════════════════════════════════════
{script_json}

═══════════════════════════════════════════════════════════════════
OUTPUT REQUIREMENTS (Strict Compliance)
═══════════════════════════════════════════════════════════════════
🚨 **MOST CRITICAL**: Class name MUST be: `class {target_scene}(Scene):`
   → DO NOT use descriptive names like AdditionScene, MultiplicationScene, etc.
   → Use EXACTLY `class {target_scene}(Scene):` with no modifications
   → Failure to comply will cause immediate runtime error

✓ Include proper imports: `from manim import *`
✓ **Include the [VISUAL REASONING] block at the top**
✓ Implement ALL steps in sequence (no skipping)
✓ Handle signal_action when present (check for null first)
✓ Create objects dynamically from JSON (don't hardcode)
✓ Store objects in a registry (dict) for later reference
✓ Ensure audio paths follow naming convention
✓ Calculate wait times correctly (duration - animation_time)
✓ Use semantic colors as specified

✗ ABSOLUTELY NO placeholder code ("# TODO", "...", "pass")
✗ NO explanatory comments (just clean executable code)
✗ NO skipping signal_actions (even if you think they're unnecessary)
✗ NO hardcoded object creation (parse from JSON)
✗ NO improvisation or additions beyond the JSON spec
✗ NO custom class names (use {target_scene} exactly)

═══════════════════════════════════════════════════════════════════
EXAMPLE OUTPUT STRUCTURE (Reference Only)
═══════════════════════════════════════════════════════════════════
```python
from manim import *
import os

class {target_scene}(Scene):
    def construct(self):
        # Object registry
        objects = {{}}
        
        # Scene setup
        title = Text("Example").shift(3.5 * UP)
        self.add(title)
        objects["title"] = title
        
        # Process sequence steps
        for i, step in enumerate(sequence):
            # Load audio with file existence check
            audio_file = None
            mp3_path = f"media/audio/step_{{i:02d}}.mp3"
            if os.path.exists(mp3_path):
                audio_file = mp3_path
            else:
                wav_path = f"media/audio/step_{{i:02d}}.wav"
                if os.path.exists(wav_path):
                    audio_file = wav_path
            
            if audio_file:
                self.add_sound(audio_file)
        
            if step.get("signal_action"):  # signal_action exists
                self.play(Circumscribe(objects["target_id"], color=YELLOW, run_time=1))
        
            obj1 = MathTex("x^2").shift(2 * UP)
            objects["obj1"] = obj1
            self.play(Write(obj1))
            self.wait(1.5)  # Remaining duration after animations
        
            # ... more steps
```

═══════════════════════════════════════════════════════════════════
FINAL REMINDER
═══════════════════════════════════════════════════════════════════
The Director has designed this animation to optimize student comprehension using Mayer's Principles.
Every signal_action, every color, every position has pedagogical justification.
Your job is FAITHFUL TRANSLATION, not creative interpretation.

If the JSON specifies a Circumscribe in YELLOW before a transformation, implement it EXACTLY.
If the JSON uses vertical alignment, implement it EXACTLY.

Trust the Director's design. Implement it perfectly.

Generate the complete, production-ready Manim code now.
"""
        return prompt


class VisualFixPrompter:
    """
    Translates structured visual defects (JSON) into Manim code fix instructions.
    """
    def generate_visual_fix_prompt(self, audit_result, original_code, script_json=None):
        defects = audit_result.get("defects", [])
        if not defects:
            return None
            
        # Group defects by code for summarized advice
        defect_summary = {}
        for d in defects:
            code = d.get("code", "UNKNOWN")
            desc = d.get("description", "No description")
            fix = d.get("suggested_fix", "No fix suggestion")
            if code not in defect_summary:
                defect_summary[code] = []
            defect_summary[code].append(f"- {desc} (Suggestion: {fix})")
            
        # Build the Prompt using simple string concatenation to avoid f-string parsing issues
        prompt = "I have audited your previous animation frame and found specific visual defects.\\n"
        prompt += "Please modify your code to fix these issues based on the standard defect codes below.\\n\\n"
        prompt += "【VIOLATION REPORT】:\\n"

        for code, details in defect_summary.items():
            prompt += f"\\n🚨 **{code}** ({len(details)} occurrences):\\n"
            prompt += "\\n".join(details)
            
            # Append standard fix strategies for each type
            if code == "OVERLAP":
                prompt += "\\n👉 **STRATEGY**: IDs colliding? Increase `buff` in `next_to()`, use `shift()` to separate, or `scale(0.8)` if too large."
            elif code == "OVERFLOW":
                prompt += "\\n👉 **STRATEGY**: Content off-screen? Check coordinate bounds. Use `to_edge()` or `scale(0.7)` to fit within frame."
            elif code == "LOW_CONTRAST":
                prompt += "\\n👉 **STRATEGY**: Text unreadable? Change color to `WHITE` or `YELLOW` if background is dark."
            elif code == "TINY_TEXT":
                prompt += "\\n👉 **STRATEGY**: Text too small? Set `font_size >= 48` or `scale(1.5)`."
            elif code == "MISALIGNED":
                prompt += "\\n👉 **STRATEGY**: Wobbly alignment? Use `align_to()` or `VGroup.arrange()` instead of manual shifting."
            elif code == "CLUTTER":
                prompt += "\\n👉 **STRATEGY**: Too crowded? Increase `buff` parameter or spread out elements."
            elif code == "TOO_FAST":
                prompt += "\\n👉 **STRATEGY**: Flashing too fast? Increase `run_time` or `wait()` duration."

        prompt += "\\n\\n【ORIGINAL CODE】:\\n"
        prompt += str(original_code)

        if script_json:
            prompt += "\\n\\n【ORIGINAL PLAN】:\\n"
            prompt += str(script_json)

        prompt += "\\n\\n**INSTRUCTIONS**:\\n"
        prompt += "1. Analyze the specific lines of code causing these visual defects.\\n"
        prompt += "2. Apply the suggested fixes (e.g., adjust coordinates, scale, colors).\\n"
        prompt += "3. Return the COMPLETE, FIXED, and RUNNABLE Manim code.\\n"
        prompt += "4. DO NOT explain your changes, just provide the python code.\\n"

        return prompt

