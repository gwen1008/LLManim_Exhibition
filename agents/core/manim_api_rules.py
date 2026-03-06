# Manim Community v0.19.2 API Strict Rules
# Added as part of Conservative LLM Upgrade (Feb 2026)
# Based on deep research identifying common failure modes

MANIM_API_STRICT_RULES = """
=== CRITICAL: Manim Community v0.19.2 API Compliance ===
The following rules are MANDATORY to prevent rendering failures:

1. ✅ Use Text() and MathTex(), NOT TextMobject or TexMobject (deprecated)
2. ✅ Use class attributes, NOT CONFIG dictionary (removed in v0.19+)
3. ✅ Use .animate syntax for transformations: obj.animate.shift(UP)
4. ⚠️ Always self.add() or self.play(Create()) BEFORE self.play(...animate...)
5. 🚫 DO NOT use self.add_sound() — the system auto-injects audio after code generation

=== GEOMETRY CHEAT SHEET (Correct Signatures) ===
✅ Triangle(color=BLUE).scale(0.5)
✅ Sector(radius=2, angle=PI, start_angle=0, color=BLUE)
✅ AnnularSector(inner_radius=1, outer_radius=2, angle=PI)
✅ Rectangle(width=2, height=1, color=WHITE)
✅ RegularPolygon(n=6)
✅ Square(side_length=2, color=YELLOW)

"""

MANIM_LAYOUT_RULES = """
=== CRITICAL: LAYOUT & OVERFLOW PREVENTION ===
These rules PREVENT the #1 visual defect: equations/text overflowing the screen.

1. 🚫 **NEVER stack multiple equations vertically without cleanup**:
   - ❌ WRONG: Show step1, step2, step3... all visible at once (they overflow)
   - ✅ CORRECT: Use ReplacementTransform(old_eq, new_eq) to morph IN-PLACE.
   - ✅ CORRECT: FadeOut(old_eq) before FadeIn(new_eq).
   - 🚫 **AVOID Transform(old, new)** for text/labels. It preserves the old object's state in a way that often causes "ghosting" or "stacking" if references are mismanaged. **ReplacementTransform is the SAFE default.**

2. 📐 **SAFE ZONE & LAYOUT STRATEGY (High-Low Split)**:
   - **Math/Equations**: CENTER at ORIGIN (y=0). Max width 12 units.
   - **Explanations**: BOTTOM BANNER (y in [-3.5, -2.5]). Max width 10 units.
   - **Title**: TOP BANNER (y in [3.0, 3.5]).
   - 🚫 **AVOID Left-Right Split**: Do NOT put Eq left and Text right. Equations are WIDE!
   - 🚫 **Check Boundaries**: All content must stay within x ∈ [-6.5, 6.5], y ∈ [-3.0, 3.0].

3. 📏 **LONG EQUATION HANDLING**:
   - If a MathTex string has > 40 characters, add .scale(0.7) or .scale(0.8).
   - For multi-line equations, use aligned environment:
     MathTex(r"\\begin{aligned} ... \\end{aligned}").
   - NEVER let an equation exceed 12 units in width.

4. 🔄 **MULTI-STEP DERIVATION PATTERN** (e.g., quadratic formula):
   - Keep ONE equation anchor at ORIGIN or UP*0.5.
   - Use ReplacementTransform(eq_current, eq_next) for each step.
   - Show step label (e.g., "Step 3:") at UP*2.0, update with each step.
   - DO NOT create all equations at once; create each one right before transforming.

5. 🧹 **CLEANUP RULE**: At any given frame, there should be at most:
   - 1 title (top)
   - 1 step label (above equation)
   - 1-2 equations (current + maybe previous fading out)
   - 1 explanation line (bottom)
   - NO more than 5 total text/math objects visible simultaneously.

"""

MANIM_LAYOUT_ENGINE_DOCS = """
=== CRITICAL: CONSTRAINT-BASED LAYOUT ENGINE (utils.layout_engine) ===
We have a new Layout Engine to solve "Spatial Hallucinations" (objects overlapping or misaligned).
You MUST use this for complex layouts (e.g., vertical stacks, grids) instead of manual `shift` or `next_to`.

1. 📥 **IMPORT**:
   ```python
   from utils.layout_engine import LayoutEngine, LayoutObject
   ```

2. 🚀 **USAGE PATTERN**:
   ```python
   # 1. Create Objects (initially at ORIGIN)
   title = Text("Title")
   eq = MathTex("a^2 + b^2 = c^2")
   note = Text("Pythagoras")

   # 2. Init Engine & Register
   layout = LayoutEngine()
   obj_title = LayoutObject(title, "title")
   obj_eq = LayoutObject(eq, "eq")
   obj_note = LayoutObject(note, "note")
   layout.add(obj_title)
   layout.add(obj_eq)
   layout.add(obj_note)

   # 3. Use Layout Zones (Safe Regions) - HIGHLY RECOMMENDED
   # HEADER: y ∈ [3.0, 3.5] (Title only)
   # CONTENT: y ∈ [-2.5, 3.0] (Main Math)
   # FOOTER: y ∈ [-3.5, -2.5] (Captions)
   
   layout.add_to_zone(obj_title, "HEADER")
   layout.add_to_zone(obj_eq, "CONTENT")
   layout.add_to_zone(obj_note, "FOOTER")
   
   # CRITICAL: Always anchor to center_x == 0 to prevent drift
   layout.add_constraint(obj_title.center_x == 0)

   # 4. Define Relations (Optional but good for alignment)
   layout.align_to(obj_eq, obj_title, 'CENTER_X')
   layout.align_to(obj_note, obj_title, 'CENTER_X')

   # 5. SOLVE & KEEP (Apply positions to Mobjects)
   layout.solve()

   # 6. Animate
   self.play(Write(title))
   self.play(Write(eq))
   ```

3. ⚠️ **WHEN TO USE**:
   - **ALWAYS** use `add_to_zone` for Title (HEADER) and Explanations (FOOTER).
   - Use `LayoutEngine` for Vertical stacks, Aligned lists, Grids.
   - **PREFER** this over manual `next_to` chains which drift over time.

4. 🆕 **PROXY PROPERTIES (Manim-style access)**:
   LayoutObject supports familiar Manim methods:
   ```python
   obj = LayoutObject(circle, "my_circle")
   
   # Before solve(): use for constraints
   obj.center           # → [center_x, center_y] (kiwi Variables)
   obj.center_x         # → Variable (use in constraints: obj.center_x == 0)
   obj.center_y         # → Variable
   
   # After solve(): get resolved positions
   obj.get_center()     # → np.array([x, y, 0])
   obj.get_left()       # → np.array([x, y, 0])
   obj.get_right()      # → np.array([x, y, 0])
   obj.get_top()        # → np.array([x, y, 0])
   obj.get_bottom()     # → np.array([x, y, 0])
   ```
   ⚠️ Do NOT call get_center()/get_left() etc. BEFORE layout.solve()!

5. 🔍 **OBJECT LOOKUP**:
   ```python
   layout.get_object("my_circle")  # → LayoutObject by name
   layout.get("my_circle")         # → same (alias)
   ```

6. 🚫 **PROHIBITED — DO NOT USE (these methods DO NOT EXIST)**:
   ```
   ❌ layout.add(obj1, obj2, obj3)        # add() takes EXACTLY ONE argument
   ❌ layout.stack_vertically(objects)    # Does NOT exist
   ❌ layout.stack_horizontally(objects)  # Does NOT exist
   ❌ layout.center()                     # Does NOT exist
   ❌ layout.flow(objects)               # Does NOT exist
   ❌ layout.place(obj, x, y)            # Does NOT exist
   ```
   **CORRECT pattern for multiple objects**:
   ```python
   # ✅ Call add() once per object, one at a time
   layout.add(obj_title)
   layout.add(obj_eq)
   layout.add(obj_note)
   ```
"""

MANIM_LANGUAGE_RULES = """
=== CRITICAL: LANGUAGE & LOCALIZATION ===
1. 🇹🇼 **ALWAYS USE TRADITIONAL CHINESE (繁體中文)** for all user-facing text.
2. 🚫 **NEVER REVERT TO ENGLISH** unless the user explicitly requests it.
3. **Consistency**: If the conversation is in Traditional Chinese, the video MUST be in Traditional Chinese.
"""

MANIM_BANNED_APIS = """
=== BANNED: Colors & Attributes That DO NOT Exist in Manim v0.19.2 ===
Using any of the following will cause an immediate NameError or TypeError at render time:

## Banned Color Constants → Use the replacement shown:
❌ LIGHT_BLUE     → ✅ BLUE_C or BLUE_B
❌ LIGHT_GREEN    → ✅ GREEN_C or GREEN_B
❌ LIGHT_RED      → ✅ RED_C
❌ DARK_GREEN     → ✅ GREEN_D or GREEN_E
❌ DARK_BLUE      → ✅ BLUE_D or BLUE_E
❌ LIGHT_GRAY     → ✅ GRAY_B or GRAY_C
❌ DARK_GRAY      → ✅ GRAY_D or GRAY_E
❌ LIGHT_YELLOW   → ✅ YELLOW_C
❌ ORANGE_RED     → ✅ ORANGE or RED

## Banned Mobject Constructor Arguments:
- `opacity` is NEVER a valid constructor argument. Always use `.set_opacity()` AFTER creation.
✅ Circle().set_opacity(0.5)
✅ fill_color=RED  (use Manim constants, not strings)

## Banned VGroup Methods (DO NOT EXIST in v0.19):
- `arrange_in_circle` does NOT exist. Use `vgroup.arrange(RIGHT, buff=0.5)` or manual positioning.

## Wait Duration Safety Rule:
✅ self.wait(max(0.1, audio_duration - animation_time))  # ALWAYS wrap with max(0.1, ...) to prevent negative → CRASH

## BANNED: add_updater + become() — Causes 120s Render Timeout
- `become()` inside an updater reconstructs the entire Manim object every frame → TIMEOUT.
- The linter will BLOCK this with error UPDATER_BECOME_RISK.

✅ CORRECT PATTERN — use always_redraw + ValueTracker:
   theta = ValueTracker(0)
   curve = always_redraw(lambda: ParametricFunction(..., t_range=[0, theta.get_value()]))
   dot   = always_redraw(lambda: Dot(circle_center + 2*np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0])))
   self.add(curve, dot)
   self.play(theta.animate.set_value(2 * PI), run_time=8, rate_func=linear)

## BANNED: MathTex Array Indexing — Causes IndexError
- NEVER use `eq[n]` hardcoded index on MathTex/Tex. Linter will BLOCK with HARDCODED_MOBJECT_INDEX.
✅ eq.get_part_by_tex("substring").set_color(RED)
✅ eq.set_color_by_tex("substring", RED)

## BANNED: \\mathrm{} inside MathTex — crashes LaTeX with "Missing } inserted"
- Confirmed crash in Manim v0.19/v0.20. Linter will BLOCK with MATHRM_IN_MATHTEX.
✅ MathTex(r"m = \\frac{\\Delta y}{\\Delta x} = \\frac{2}{1} = 2")   # no \\mathrm needed
✅ Tex(r"slope $= \\frac{rise}{run} = \\frac{2}{1} = 2$")           # mixed text+math
✅ Text("slope = rise / run = 2")                                   # pure text

## BANNED: set_stroke(dash=...) — NOT supported in ManimCE
- `set_stroke()` only accepts: color, width, opacity, background, family. No dash parameter.
✅ DashedLine(start, end, dash_length=0.1)
✅ DashedVMobject(original_mobject, num_dashes=15)

## BANNED: TransformMatchingTex/TransformMatchingShapes with non-MathTex args — AssertionError
- Both args MUST be MathTex/Tex instances. Group/VGroup/Text will crash (no .tex_string attribute).
✅ ReplacementTransform(old_group, new_group)   # Works with any Mobject
✅ FadeTransform(old_group, new_group)          # Works with any Mobject
✅ ONLY use TransformMatchingTex when BOTH args are a single MathTex/Tex directly:
   self.play(TransformMatchingTex(MathTex(r"y = x"), MathTex(r"y = 2x - 1")))
"""

MANIM_GEOMETRY_RULES = """
=== GEOMETRY POSITIONING: 6 GOLDEN RULES (Anti-Misalignment) ===
These rules prevent the #2 visual defect: MISALIGNED objects and coordinate drift.

## Rule 1: RELATIONAL > ABSOLUTE (No Magic Numbers)
❌ obj.shift(LEFT*2.5 + UP*1.3)           # Guessing coordinates → MISALIGNED
❌ label.move_to([1.5, -0.8, 0])          # Hardcoded → breaks when text length changes
✅ obj.next_to(ref_obj, RIGHT, buff=0.5)  # Relative to reference
✅ obj.move_to(ref_obj.get_center())      # Anchored to another object
✅ obj.align_to(ref_obj, LEFT)            # Edge-aligned
- Only use absolute coords for top-level elements (e.g., title at 3.5 * UP).

## Rule 2: buff=0 FOR GEOMETRIC NESTING (Tile/Grid Layouts)
❌ square_a.next_to(square_b, RIGHT)       # Default buff=0.5 → visible gap!
✅ square_a.next_to(square_b, RIGHT, buff=0)  # Edge-to-edge, no gap
- Use buff=0 when: subdividing shapes, creating grids, placing labels ON boundaries.
- Use buff > 0 when: aesthetic spacing between unrelated elements.

## Rule 3: VGroup BEFORE MOVE (Prevent Coordinate Drift)
❌ Moving objects one-by-one (each shift accumulates floating-point error):
   square_a.shift(2*UP); square_b.shift(2*UP + LEFT*0.5)  # Drift!
✅ Group first, move once:
   composite = VGroup(square_a, square_b, label)
   composite.shift(2*UP)  # All children move together, zero drift

## Rule 4: ANCHOR VARIABLES (For Complex Scenes)
✅ corner = main_square.get_corner(UL)
   nested_obj.move_to(corner)        # Precise, readable, reusable
❌ nested_obj.shift(LEFT*2 + UP*2)   # Guessing where UL corner is

## Rule 5: Polygon UNPACKED ARGS (Most Common Crash)
❌ Polygon([A, B, C])              # TypeError: dimension mismatch!
✅ Polygon(A, B, C)                # Each point is a separate argument
✅ Polygon(*vertices)              # Unpack a list with *
- Each point must be 3D: (x, y, 0). NOT 2D (x, y).

## Rule 6: PRE-SUBMISSION CHECKLIST
Before finalizing code, verify:
- [ ] No hardcoded coordinates like [2.5, 1.3, 0] for nested objects
- [ ] All geometric nesting uses buff=0
- [ ] Composite shapes are grouped in VGroup BEFORE final positioning
- [ ] .get_corner()/.align_to()/.next_to() used instead of .shift() for precision
- [ ] All Polygon() calls use unpacked args, not a single list

## Rule 7: DYNAMIC SYNC SCENES — ValueTracker Pattern (MANDATORY)
For scenes where a point moves on one object (e.g., unit circle) and must synchronize with a point on another (e.g., sine graph), you MUST use a shared ValueTracker.

❌ WRONG — Using two independent updaters causes drift and MISALIGNED:
   circle_dot.add_updater(lambda m, dt: m.move_to(circle.point_at_angle(t)))
   graph_dot.add_updater(lambda m, dt: m.move_to(axes.c2p(t, np.sin(t))))
   # ↑ These 't' values diverge over time → GUARANTEED MISALIGNED

✅ CORRECT — One shared ValueTracker, all projections computed from it:
   theta = ValueTracker(0)

   # All geometry derived from the SAME theta.get_value()
   circle_dot = always_redraw(
       lambda: Dot(circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]))
   )
   proj_line = always_redraw(
       lambda: DashedLine(
           circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
           axes.c2p(theta.get_value(), np.sin(theta.get_value()))
       )
   )
   graph_dot = always_redraw(
       lambda: Dot(axes.c2p(theta.get_value(), np.sin(theta.get_value())), color=YELLOW)
   )

   self.add(circle_dot, proj_line, graph_dot)
   self.play(theta.animate.set_value(2 * PI), run_time=8, rate_func=linear)

KEY RULES:
- ONE ValueTracker → ALL synchronized objects read from it
- All `always_redraw` lambdas reference the SAME ValueTracker getter
- Animate ONLY the ValueTracker; never animate the dots directly
- The projection line endpoints MUST be computed from theta.get_value() on BOTH ends

## Rule 8: TOPOLOGICAL RECTIFICATION (Arc ↔ Line Morphing / Rolling Circle)
When animating a circle unrolling into a line, or any arc-to-line morph:

### 8a. Arc-to-Line Morphing — The "Rectification Pattern"
❌ Transform(Arc(...), Line(...))
   # FAILS: Arc has many bezier points, Line has 2 → "path jumping" / distortion glitch

✅ CORRECT — Initialize target as a near-zero angle Arc, then stretch it:
   target = Arc(radius=r, angle=0.001)         # Same internal structure as source Arc
   target.stretch_to_fit_width(TAU * r)        # Morphs cleanly, matching point counts
   self.play(Transform(arc, target))

"""
