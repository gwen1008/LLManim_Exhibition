# agents/diagnoser.py
import re
from dataclasses import dataclass

@dataclass
class ErrorTriage:
    matched: bool
    is_surgical: bool
    category: str
    advice: str

class ManimDiagnoser:
    """
    Manim-specific error diagnostic system.
    Provides deterministic, immediate fixes for known error patterns (in English for better LLM comprehension).
    """
    def __init__(self):
        # Define error keywords and corresponding fix strategies
        self.knowledge_base = {
            # ========== API Deprecations ==========
            "ShowCreation": "Syntax Error: 'ShowCreation' is deprecated in ManimCE. Use 'Create' instead.",
            "TextMobject": "Syntax Error: Change 'TextMobject' to 'Text', and 'TexMobject' to 'MathTex'.",
            "TexMobject": "Syntax Error: 'TexMobject' is deprecated. Use 'MathTex' for LaTeX mathematical formulas.",
            "ShowPassingFlash": "Syntax Error: 'ShowPassingFlash' is deprecated. Use 'ShowPassingFlashAround' instead.",
            "ApplyMethod": "Syntax Error: 'ApplyMethod' is deprecated. Use the .animate syntax, e.g., self.play(obj.animate.shift(UP)).",
            
            # ========== Geometry & Positioning ==========
            "parallel": "Geometric parallel error detected. Stop using 'line_intersection' and use get_center() coordinate components to position objects instead.",
            "shift.*str": "Position Error: shift() requires a vector argument, not a string. Correct: obj.shift(3 * UP). Wrong: obj.shift('UP*3'). Convert the position string to a Manim vector constant.",
            "next_to.*str": "Position Error: next_to() direction parameter must be a vector, not a string. E.g., obj.next_to(ref, DOWN) instead of obj.next_to(ref, 'DOWN').",
            
            # ========== Indexing & Rendering ==========
            "IndexError": "IndexError detected. Common causes: (1) Out-of-bounds index when accessing MathTex/Text subobjects. Ensure the object exists. (2) Complex transforms inside always_redraw; try using manually defined Polygons instead. (3) Numerical issues in coordinate calculations; add a tiny offset (1e-6) to prevent singularities.",
            "list index out of range": "List index out of range. Check the subobject indices of MathTex, Text, or VGroup. Use len(obj) to verify length, or obj.submobjects to inspect structure.",
            "tuple index out of range": "Tuple index error. Likely an incorrect index when accessing coordinates or colors. Ensure correct usage of obj.get_center()[0/1/2] or obj.get_color().",
            
            # ========== Import Errors ==========
            "ImportError": "Import Error. Ensure 'from manim import *' is at the top of the code, and all Manim class names are spelled correctly (case-sensitive).",
            "ModuleNotFoundError": "Module not found. Check: (1) The import statement is correct. (2) Manim is properly installed. (3) You are not mistakenly using old Manim (manimlib) syntax.",
            "cannot import name": "Cannot import name. You might be using a nonexistent class or function. Check the Manim documentation for the current version.",
            
            # ========== Audio Issues ==========
            "FileNotFoundError.*audio": "Audio file not found. Verify: (1) The file path format is correct: media/audio/step_XX.mp3 (where XX is a zero-padded step number). (2) The file actually exists there. (3) The extension is correct (.mp3 or .wav).",
            "add_sound.*not found": "add_sound cannot find the audio file. Check if the file naming uses zero-padding (e.g., step_01.mp3) and the path is correct.",
            
            # ========== Transformation Errors ==========
            "Transform.*NoneType": "Transform Error: Target object is None. Ensure: (1) The object is created and stored in the objects dictionary. (2) The ID referenced in signal_action.target actually exists. (3) The object has been added to the scene via self.play() or self.add() before Transform.",
            "TransformMatchingTex.*no matching": "TransformMatchingTex found no matching elements. Ensure the source and target objects have identical LaTeX markers (e.g., '=' sign). Consider adding a key_map parameter to manually specify the mapping.",
            
            # ========== Visual Overlap ==========
            "overlap": "Visual overlap detected. Avoid using Transform() repeatedly on objects at the same position. Use ReplacementTransform() to completely replace the old object and keep the scene clean.",
            
            # ========== Object Reference Errors ==========
            "name.*is not defined": "Variable not defined. Possible causes: (1) Object was created but not stored in the objects dictionary. (2) signal_action references a nonexistent object ID. (3) Typo in variable name. Ensure all objects are stored in objects[obj_id] immediately after creation.",
            "KeyError": "Dictionary KeyError. Likely accessing a nonexistent ID in the objects dictionary. Check: (1) Is the object created and stored? (2) Does the ID spelling match the JSON exactly? (3) Are you trying to reference the object before it's created?",
            
            # ========== LaTeX Errors ==========
            "Missing \\$ inserted": "LaTeX 'Missing $ inserted' — a math-only symbol (e.g. \\odot, \\angle, \\triangle, \\times, \\frac, ^, _) appears in TEXT MODE without math delimiters. This happens in Tex(...) (text-mode) when you mix prose with bare math symbols. FIX: wrap every math symbol/expression in $...$. Example: Tex(r'(A) outside \\odot B, inside \\odot C') → Tex(r'(A) outside $\\odot B$, inside $\\odot C$'). Keep the plain English words OUTSIDE the $, keep math symbols INSIDE. Do NOT switch back to MathTex (it would re-break on the English words).",
            "LaTeX Error": "LaTeX compilation error. Common causes: (1) Syntax error (missing $ or mismatched {}). (2) Usage of undefined symbols. (3) Unescaped special characters in MathTex strings. Use raw strings r'...' or double backslashes \\\\.",
            "latexmk.*error": "LaTeX compilation failed. Check the LaTeX syntax in MathTex contents. If using special characters, ensure you use an r-string (e.g., r'\\frac{1}{2}').",
            "UnicodeDecodeError": "LaTeX Encoding Error. Avoid using Chinese characters directly in MathTex. Use Text() objects for Chinese text and MathTex() for mathematical formulas, then combine them visually using VGroup(Text(...), MathTex(...)).arrange().",
            "improper alphabetic constant": "LaTeX Error. You might have used \\text{Chinese} inside MathTex where the environment doesn't support it. Change the Chinese text to a Text() object instead.",
            
            # ========== Color Errors ==========
            "ValueError.*color": "Invalid color value. Manim colors should use predefined constants (YELLOW, RED, GREEN) or hex strings ('#FF0000'). If reading color strings from JSON, use a color mapping dictionary to convert them.",
            
            # ========== Animation Timing Errors ==========
            "wait.*negative": "wait() duration cannot be negative. Check the duration - animation_time calculation. If the result is negative, use max(0.1, remaining_time) or increase the duration value in the JSON.",
            
            # ========== Polygon Dimension Errors ==========
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

            # ========== Python 3.10+ Syntax Error (Runtime Compatibility) ==========
            "unsupported operand type.*for.*|": (
                "Python Syntax Error: The `X | Y` type union syntax requires Python 3.10+, but the runtime is Python 3.9."
                "Remove all type annotations, or use `Union[X, Y]` (requires `from typing import Union`)."
                "The safest approach is to completely omit type annotations for function parameters: use `def foo(x):` instead of `def foo(x: int | float):`."
            ),

            # ========== Attribute Error - opacity ==========
            "object has no attribute 'opacity'": (
                "Attribute Error: Manim Mobjects do not have an 'opacity' attribute."
                "Change `obj.opacity = 0.5` or `obj.opacity` to `obj.set_opacity(0.5)` or `obj.get_fill_opacity()`."
                "Similarly, 'opacity=' is NOT accepted as a constructor argument: `Circle(opacity=0.5)` → `Circle().set_opacity(0.5)`."
            ),

            # ========== Manim Render Timeout — Infinite Animation Loop ==========
            "Manim process timed out": """RENDER TIMEOUT: Your code contains an infinite or excessively long animation loop.

This is the #1 cause of timeout in dynamic scenes (unit circles, parametric curves, updaters).

PROHIBITED PATTERNS (will cause timeout):
  ❌ `while True: ...` inside construct()
  ❌ `always_redraw(lambda: ...)` on objects that are never removed
  ❌ `self.add_updater(func)` without a corresponding `self.remove_updater(func)` + `self.wait()`
  ❌ `UpdateFromFunc` with a lambda that never terminates

CORRECT PATTERNS for Synchronized Dynamic Animations:
  ✅ Use `ValueTracker` + explicit `self.play()` calls with a finite `run_time`:
     ```python
     theta = ValueTracker(0)
     dot = always_redraw(lambda: Dot(circle.point_at_angle(theta.get_value())))
     self.add(dot)
     self.play(theta.animate.set_value(2 * PI), run_time=8, rate_func=linear)
     ```
  ✅ Use a ParametricFunction for traces — do NOT use updaters to draw traces frame-by-frame:
     ```python
     sine_curve = axes.plot(lambda x: np.sin(x), x_range=[0, 2*PI], color=YELLOW)
     self.play(Create(sine_curve), run_time=5)
     ```
  ✅ If you need a synchronized sweeping plot, use `Create(curve)` with `run_time` equal to the circle animation.

REWRITE RULE: Remove ALL `while` loops and standalone `always_redraw` calls. Replace them with `ValueTracker.animate.set_value()` wrapped in `self.play()` with an explicit, finite `run_time`.""",

            # ========== Deprecated API: axes.get_graph() ==========
            "getter.*got an unexpected keyword argument": """DEPRECATED API: 'axes.get_graph()' was removed in Manim v0.18+.

Replace ALL occurrences of:
  ❌ axes.get_graph(lambda x: np.sin(x), x_range=[0, 2*PI])

With the new API:
  ✅ axes.plot(lambda x: np.sin(x), x_range=[0, 2*PI], color=YELLOW)

Other common API renames:
  - axes.get_graph(f) → axes.plot(f)
  - axes.get_graph_label(graph, label) → axes.get_graph_label(graph, label=MathTex(r"y=f(x)"))
  - graph.get_point_from_function(t) → axes.input_to_graph_point(t, graph)""",

            # ========== LayoutEngine/LayoutObject Attribute Errors (from real eval logs) ==========
            "LayoutObject.*has no attribute": (
                "LayoutEngine API Error: 'LayoutObject' does not expose Manim geometry attributes directly. "
                "Access the underlying Manim mobject via `layout_obj.mobject` (e.g., `layout_obj.mobject.get_center()`). "
                "Common mistakes: `layout_obj.center` → `layout_obj.mobject.get_center()`; "
                "`layout_obj.bounding_box` → use `layout_obj.mobject.get_bounding_box()`."
            ),
            "LayoutEngine.*has no attribute 'get_object'": (
                "LayoutEngine API Error: `layout.get_object(id)` does not exist. "
                "Access objects via `self.objects[obj_id]` (the objects dict you populated during construction). "
                "Replace `layout.get_object('foo')` with `self.objects['foo']`."
            ),
            "LayoutEngine.*has no attribute 'get'": (
                "LayoutEngine API Error: `layout.get(...)` does not exist. "
                "Do not use the LayoutEngine object as a dict. "
                "Access your scene objects via `self.objects[obj_id]`."
            ),

            # ========== AnnularSector Signature Error (from real eval logs) ==========
            "AnnularSector.*got multiple": (
                "AnnularSector Constructor Error: `AnnularSector` received multiple conflicting arguments. "
                "The correct signature is `AnnularSector(inner_radius, outer_radius, angle, start_angle, **kwargs)`. "
                "Do NOT pass both positional and keyword versions of the same argument (e.g., `AnnularSector(1, 2, PI, inner_radius=0.5)`)."
            ),

            # ========== Mobject height keyword Error (from real eval logs) ==========
            "Mobject.*got an unexpected keyword argument 'height'": (
                "Constructor Error: 'height=' is NOT a valid constructor parameter for most Manim Mobjects. "
                "Instead, set scale/size AFTER construction: `obj = SomeMobject(...); obj.scale_to_fit_height(1.5)` "
                "or `obj.set(height=1.5)` (only works on VMobject subclasses in newer Manim versions). "
                "Remove 'height=...' from the constructor call."
            ),

            # ========== Coordinate Plane Misuse (c2p missing) ==========
            "RAW_COORD_ON_PLANE": (
                "Coordinate Mapping Error: Objects (Arrow/Dot/Line/Vector) in a NumberPlane/Axes scene "
                "must use plane.c2p(x, y) to convert logical grid coordinates to Manim screen space. "
                "Raw arrays like [3, 1, 0] bypass the plane's scale and origin, causing visual misalignment. "
                "Fix ALL affected calls:\n"
                "  ❌ Arrow([0, 0, 0], [3, 1, 0])\n"
                "  ✅ Arrow(plane.c2p(0, 0), plane.c2p(3, 1))\n"
                "  ❌ dot.move_to([2, -1, 0])\n"
                "  ✅ dot.move_to(plane.c2p(2, -1))\n"
                "Also check: shift([dx, dy, 0]) → shift(plane.c2p(dx, dy) - plane.c2p(0, 0))"
            ),

            # ========== List index type mismatch (from real eval logs) ==========
            "list indices must be integers or slices, not str": (
                "Data structure mismatch: You are accessing a list with a string key (e.g., `my_list['name']`), "
                "but that only works for dicts. "
                "Check whether the variable is supposed to be a dict `{}` or a list `[]`. "
                "If it's a list of dicts, use `my_list[0]['name']`. "
                "If it's supposed to be a dict, fix the construction from `[...]` to `{...}`."
            ),
        }

    # Patterns that require full architectural rewrite — NOT safe for surgical SEARCH/REPLACE
    FULL_REWRITE_PATTERNS = [
        "timed out",
        "infinite",
        "recursion",
    ]

    # LaTeX *compilation* failures whose error message does NOT contain the broken source string.
    # SEARCH/REPLACE can't locate the bad MathTex (e.g. unclosed \sqrt{), so the LLM blindly patches
    # and often deletes the offending self.play(...) → "Called Scene.play with no animations" deadlock.
    # These MUST go full-rewrite so the whole MathTex string is regenerated. (HSAT_114_16 / 114_5 bug)
    LATEX_REWRITE_PATTERNS = [
        "undefined control sequence",
        "latex error converting to dvi",
        "latex compilation error",
        "missing $ inserted",
        "no animations",  # downstream symptom of a botched LaTeX surgical patch
    ]

    def diagnose_only(self, error_message: str) -> ErrorTriage:
        """
        Quickly check if we have a known fix for this error WITHOUT generating the full prompt.
        Returns an ErrorTriage dataclass.
        - matched=True: we know what's wrong
        - is_surgical=True: fix is a small targeted change, safe for SEARCH/REPLACE patch mode
        - category: high-level error category for injecting specific slim rules
        - advice: pre-computed targeted advice
        """
        matched = False
        advice = "Unknown error. Please check syntax and API usage."
        
        # Simple categorization heuristic
        category = "UNKNOWN"
        error_lower = error_message.lower()
        if any(kw in error_lower for kw in ["timed out", "infinite", "recursion"]):
            category = "TIMEOUT"
        elif "latex" in error_lower or "math" in error_lower or "tex" in error_lower:
            category = "LATEX"
        elif any(kw in error_lower for kw in ["deprecated", "got an unexpected keyword", "has no attribute"]):
            category = "API_DEPRECATED"
        elif any(kw in error_lower for kw in ["parallel", "shift", "next_to", "overlap", "index out of range"]):
            category = "GEOMETRY_OR_LAYOUT"
        elif "import" in error_lower or "name" in error_lower:
            category = "SYNTAX"
            
        for pattern, p_advice in self.knowledge_base.items():
            try:
                hit = re.search(pattern, error_message, re.IGNORECASE) if any(c in pattern for c in ['*', '.', '[', ']', '^', '$']) else (pattern.lower() in error_message.lower())
            except re.error:
                hit = pattern in error_message
            if hit:
                matched = True
                advice = p_advice
                break

        # LaTeX compilation failures need full rewrite regardless of knowledge_base match,
        # because SEARCH/REPLACE can't locate the broken string (see LATEX_REWRITE_PATTERNS).
        _is_latex_rewrite = any(kw in error_lower for kw in self.LATEX_REWRITE_PATTERNS)

        if not matched:
            # Unknown error is non-surgical by default; latex-compile errors stay non-surgical too.
            return ErrorTriage(matched=False, is_surgical=False, category=category, advice=advice)

        # Even if matched, timeout / architectural / latex-compile errors need full rewrite
        is_surgical = (
            not ("TIMEOUT" in category)
            and not _is_latex_rewrite
            and not any(kw in error_message.lower() for kw in self.FULL_REWRITE_PATTERNS)
        )
        return ErrorTriage(matched=matched, is_surgical=is_surgical, category=category, advice=advice)

    def generate_fix_prompt(self, error_message, original_code, script_json=None, triage_result: ErrorTriage = None, slim=False):
        if not triage_result:
            triage_result = self.diagnose_only(error_message)

        prompt = f"""
The code you generated in your previous attempt encountered an error during execution.

[ERROR MESSAGE]:
{error_message}

[DIAGNOSIS & SUGGESTION]:
{triage_result.advice}
"""
        if triage_result.matched:
            prompt += f"\n[ERROR CATEGORY]: {triage_result.category}\n"
        
        # [NEW] Opt-1 / Opt-9: Token Diet based on category
        if slim:
            from ..core.manim_api_rules import MANIM_API_STRICT_RULES, MANIM_LAYOUT_RULES, MANIM_LANGUAGE_RULES
            prompt += "\n[CRITICAL REMINDERS (SLIM MODE)]:\n"
            if triage_result.category == "API_DEPRECATED":
                prompt += MANIM_API_STRICT_RULES + "\n"
            elif triage_result.category == "GEOMETRY_OR_LAYOUT":
                prompt += MANIM_LAYOUT_RULES + "\n"
            elif triage_result.category == "SYNTAX":
                prompt += MANIM_LANGUAGE_RULES + "\n"
            else:
                prompt += "- Use Manim Community Edition (manimCE).\n- Ensure all variables are defined before use.\n- Do NOT use lambda inside get_graph, use pure functions instead.\n"

        prompt += f"\n[ORIGINAL CODE]:\n{original_code}\n"
        
        patch_mode = triage_result.is_surgical
        
        if patch_mode:
            prompt += """
Please analyze the error and the original code.
Provide a **SEARCH & REPLACE** patch to fix the error.
Do NOT rewrite the entire file.

Output Format (Strict):
<<<< SEARCH
(Exact lines to be replaced from original code)
====
  correction (New corrected lines)
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
        elif script_json and not slim:
            # [OPTIMIZATION] On iterations 2+, omit the JSON design plan (3-4k tokens).
            # The LLM already generated code from it; re-sending it on fix iterations is wasted tokens.
            prompt += f"""
[ORIGINAL DESIGN PLAN (JSON)]:
{script_json}

Based on the diagnosis and the original design plan, please rewrite the COMPLETE and BUG-FREE ManimCE code.
Ensure your code strictly implements every step described in the JSON blueprint.
"""
        elif slim:
            # slim=True + full_rewrite: no script_json, but still give the original code as anchor.
            # Without it the LLM has nothing to rewrite from — this prevents the "one-line rewrite" regression.
            prompt += (
                "\nThe original code is shown above. "
                "Based on the diagnosis, rewrite it as COMPLETE, BUG-FREE ManimCE code. "
                "Preserve the original animation intent.\n"
            )
        else:
            prompt += "\nBased on the diagnosis, please rewrite the COMPLETE and BUG-FREE ManimCE code.\n"
            
        return prompt
