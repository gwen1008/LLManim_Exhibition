'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually distinguish between area (space inside) and perimeter (distance around) for a 4x3 rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle, grid, and tracing
#    - Footer Region: [Bottom y=-3.5] for step explanation
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for grid and formulas. Position formulas below rectangle with buff.
#    - The rectangle and grid are centered. The step explanation is at the bottom, title at top.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    Step 1: Draw rectangle outline.
#    Step 2: Indicate rectangle, then fill with unit squares (LaggedStart).
#    Step 3: Circumscribe rectangle, fade grid.
#    Step 4: Create trace path and animate dot moving along perimeter.
#    Step 5: Indicate and write final formulas.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # step_explanation
        step_explanation = Text("Step 1: Draw a 4 by 3 rectangle.", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # rectangle (Polygon with vertices)
        rect_vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]
        rectangle = Polygon(*rect_vertices, color=BLUE, stroke_width=6, fill_opacity=0.0)
        rectangle.move_to(global_center)
        self.objects["rectangle"] = rectangle

        # grid_squares_vgroup (4x3 grid of unit squares)
        grid_squares = VGroup()
        square_side = 1.0
        for i in range(4):  # width
            for j in range(3):  # height
                sq = Square(side_length=square_side, color=GREEN, fill_opacity=0.3, stroke_width=2)
                # Position bottom-left at (-2, -1.5) and offset
                sq.move_to([-2 + i * square_side + square_side/2, -1.5 + j * square_side + square_side/2, 0])
                grid_squares.add(sq)
        grid_squares.move_to(global_center)
        self.objects["grid_squares_vgroup"] = grid_squares

        # perimeter_dot
        perimeter_dot = Dot(radius=0.1, color=YELLOW, z_index=5)
        # Place at start of rectangle path (bottom-left vertex)
        perimeter_dot.move_to(rectangle.get_start())
        self.objects["perimeter_dot"] = perimeter_dot

        # trace_path (will be created empty, then updated by dot movement)
        trace_path = TracedPath(perimeter_dot.get_center, stroke_color=YELLOW, stroke_width=3, z_index=4)
        self.objects["trace_path"] = trace_path

        # formula_group (VGroup containing area and perimeter formulas)
        area_formula = Tex(r"Area $= 4 \times 3 = 12$", color=GREEN)
        perimeter_formula = Tex(r"Perimeter $= 2\times(4+3) = 14$", color=YELLOW)
        formula_group = VGroup(area_formula, perimeter_formula)
        formula_group.arrange(RIGHT, buff=1.5)
        formula_group.next_to(rectangle, DOWN, buff=0.8)
        self.objects["area_formula"] = area_formula
        self.objects["perimeter_formula"] = perimeter_formula
        self.objects["formula_group"] = formula_group

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_4x3_rectang_c33b258356/step_00.mp3")  # [auto-injected] duration=5.16s
        _audio_dur_0 = 5.16  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1)
        self.play(Write(self.objects["step_explanation"]), run_time=1)
        # visual_action: Create rectangle
        self.play(Create(self.objects["rectangle"]), run_time=2)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # [missing audio] self.add_sound("media/audio/Create_a_4x3_rectang_c33b258356/step_01.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        # Update step explanation
        new_step_text_2 = Text("Step 2: Fill with unit squares to find area.", color=GRAY_B, font_size=24)
        new_step_text_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_step_text_2))
        self.objects["step_explanation"] = new_step_text_2
        # signal_action: Indicate rectangle
        self.play(Indicate(self.objects["rectangle"], color=GREEN, run_time=1))
        # visual_action: LaggedStart for grid squares
        self.play(LaggedStart(*[Create(sq) for sq in grid_squares], lag_ratio=0.05), run_time=3)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        # [missing audio] self.add_sound("media/audio/Create_a_4x3_rectang_c33b258356/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        new_step_text_3 = Text("Step 3: Focus on the perimeter (boundary).", color=GRAY_B, font_size=24)
        new_step_text_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_step_text_3))
        self.objects["step_explanation"] = new_step_text_3
        # signal_action: Circumscribe rectangle
        self.play(Circumscribe(self.objects["rectangle"], color=YELLOW, run_time=1))
        # visual_action: FadeToColor grid (reduce fill_opacity)
        self.play(self.objects["grid_squares_vgroup"].animate.set_fill(opacity=0.1), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        # [missing audio] self.add_sound("media/audio/Create_a_4x3_rectang_c33b258356/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        new_step_text_4 = Text("Step 4: Trace the perimeter path.", color=GRAY_B, font_size=24)
        new_step_text_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_step_text_4))
        self.objects["step_explanation"] = new_step_text_4
        # visual_action: Create trace_path and MoveAlongPath for dot
        self.add(self.objects["trace_path"])
        self.add(self.objects["perimeter_dot"])
        # Create a closed path for the dot to follow (rectangle edges)
        path = Polygon(*rect_vertices, color=WHITE, stroke_opacity=0)  # invisible path
        self.play(MoveAlongPath(self.objects["perimeter_dot"], path, run_time=4, rate_func=linear))
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        # [missing audio] self.add_sound("media/audio/Create_a_4x3_rectang_c33b258356/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        new_step_text_5 = Text("Step 5: Calculate area and perimeter.", color=GRAY_B, font_size=24)
        new_step_text_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_step_text_5))
        self.objects["step_explanation"] = new_step_text_5
        # signal_action: Indicate formula_group
        self.play(Indicate(self.objects["formula_group"], color=WHITE, run_time=1))
        # visual_action: Write formula_group
        self.play(Write(self.objects["formula_group"]), run_time=2)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))