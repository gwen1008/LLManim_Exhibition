# agents/prompter.py
import re

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
            
            # ========== 顏色相關錯誤 (Color Errors) ==========
            "ValueError.*color": "顏色值錯誤。Manim 顏色應使用預定義常數（YELLOW, RED, GREEN）或十六進制字串（'#FF0000'）。如果從 JSON 讀取顏色字串，請使用 color_map 字典轉換。",
            
            # ========== 動畫時間錯誤 (Animation Timing Errors) ==========
            "wait.*negative": "wait() 時間不能為負數。檢查 duration - animation_time 的計算，確保 duration 足夠長。如果計算結果為負，使用 max(0, remaining_time) 或增加 JSON 中的 duration 值。",
        }

    def generate_fix_prompt(self, error_message, original_code, script_json=None):
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

        # Add script context (CRITICAL for preventing hallucinations)
        if script_json:
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
    def generate_initial_prompt(self, script_json, target_scene):
        return f"""You are an Expert Manim Developer serving as the \"Code Translation Engine\" (The Engineer) in a multi-agent system.
Your upstream colleague is the \"Director\" who designs Visual Rationale (JSON blueprints based on Mayer's Pedagogical Principles).
Your job is to translate the Director's JSON Plan into PRODUCTION-READY Manim Community (v0.18.0+) Python code.

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
        # ========== PHASE 1: Scene Setup (Static Objects) ==========
        # Create and display static elements from scene_setup.static_objects
        # Example:
        # title = Text("Problem Title").shift(3.5 * UP)
        # self.add(title)
        
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


### 6. OBJECT LIFETIME MANAGEMENT (CRITICAL for Signal Actions)

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