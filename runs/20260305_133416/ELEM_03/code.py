'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually distinguish area (2D covering) from perimeter (1D boundary) of a rectangle using distinct metaphors: filling with unit squares and tracing with a moving dot.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle, grid, and labels
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Place area label to the RIGHT of rectangle, perimeter label ABOVE rectangle. Use buff to prevent overlap.
#    - The grid will be perfectly aligned to the rectangle's bottom-left corner.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Draw rectangle outline.
#    - Step 2: Indicate rectangle, then fill with grid of squares.
#    - Step 3: Circumscribe grid, then write area formula.
#    - Step 4: Indicate rectangle, then create perimeter dot.
#    - Step 5: Animate dot moving along rectangle's perimeter.
#    - Step 6: Circumscribe dot, then write perimeter formula.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # rect_outline
        rect_outline = Rectangle(width=4, height=3, color=BLUE, stroke_width=4, fill_opacity=0.0)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline

        # grid_group - 4x3 grid of unit squares (side=0.5) to fill the rectangle
        # We'll create the grid aligned to the rectangle's bottom-left corner.
        grid_group = VGroup()
        square_side = 0.5
        width_squares = 4
        height_squares = 3
        for h in range(height_squares):
            for w in range(width_squares):
                sq = Square(side_length=square_side, color=GREEN_C, fill_opacity=0.3, stroke_width=1)
                # Position relative to (0,0) first, then move to rectangle corner
                sq.move_to([w * square_side, h * square_side, 0])
                grid_group.add(sq)
        # Align the grid's bottom-left corner to the rectangle's bottom-left corner
        grid_group.move_to(rect_outline.get_corner(DL), aligned_edge=DL)
        self.objects["grid_group"] = grid_group

        # area_label
        area_label = Tex(r"Area $= 4 \times 3 = 12$ square units", color=GREEN)
        area_label.next_to(rect_outline, RIGHT, buff=1.0)
        self.objects["area_label"] = area_label

        # perimeter_dot
        perimeter_dot = Dot(radius=0.08, color=RED)
        perimeter_dot.move_to(rect_outline.get_corner(DL))
        self.objects["perimeter_dot"] = perimeter_dot

        # perimeter_label
        perimeter_label = Tex(r"Perimeter $= 2 \times (4 + 3) = 14$ units", color=RED)
        perimeter_label.next_to(rect_outline, UP, buff=1.0)
        self.objects["perimeter_label"] = perimeter_label

        # step_explanation (initial content for Step 1)
        step_explanation = Text("Step 1: Draw a 4x3 rectangle.", color=YELLOW, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_4x3_rectangle_3baf4cde5f/step_00.mp3")  # [auto-injected] duration=4.78s
        _audio_dur_0 = 4.78  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Write(self.objects["step_explanation"]), run_time=1.0)
        self.play(Create(self.objects["rect_outline"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_3baf4cde5f/step_01.mp3")  # [auto-injected] duration=6.55s
        _audio_dur_1 = 6.55  # [audio-sync] actual TTS duration
        # Step 2
        # Update explanation text
        new_explanation_2 = Text("Step 2: Fill with unit squares to measure area.", color=YELLOW, font_size=24)
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2

        self.play(Indicate(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # Animate grid appearing row by row (or all at once for simplicity as per hint)
        self.play(Create(self.objects["grid_group"]), run_time=2.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_3baf4cde5f/step_02.mp3")  # [auto-injected] duration=6.91s
        _audio_dur_2 = 6.91  # [audio-sync] actual TTS duration
        # Step 3
        new_explanation_3 = Text("Step 3: Count squares: 4 columns × 3 rows = 12.", color=YELLOW, font_size=24)
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3

        self.play(Circumscribe(self.objects["grid_group"], color=GREEN, run_time=1))
        self.play(Write(self.objects["area_label"]), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_3baf4cde5f/step_03.mp3")  # [auto-injected] duration=5.09s
        _audio_dur_3 = 5.09  # [audio-sync] actual TTS duration
        # Step 4
        new_explanation_4 = Text("Step 4: Perimeter is the distance around the boundary.", color=YELLOW, font_size=24)
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4

        self.play(Indicate(self.objects["rect_outline"], color=RED, run_time=1))
        self.play(Create(self.objects["perimeter_dot"]), run_time=1.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_3baf4cde5f/step_04.mp3")  # [auto-injected] duration=10.03s
        _audio_dur_4 = 10.03  # [audio-sync] actual TTS duration
        # Step 5
        new_explanation_5 = Text("Step 5: Trace the boundary: 4 right, 3 up, 4 left, 3 down.", color=YELLOW, font_size=24)
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5

        # Create a path that traces the rectangle's perimeter
        # We'll use the rectangle's outline as the path
        perimeter_path = self.objects["rect_outline"].copy().set_stroke(opacity=0)  # Invisible path
        self.add(perimeter_path)
        self.play(MoveAlongPath(self.objects["perimeter_dot"], perimeter_path), run_time=5.0)
        self.remove(perimeter_path)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_3baf4cde5f/step_05.mp3")  # [auto-injected] duration=9.07s
        _audio_dur_5 = 9.07  # [audio-sync] actual TTS duration
        # Step 6
        new_explanation_6 = Text("Step 6: Perimeter = 2 × (4 + 3) = 14 units.", color=YELLOW, font_size=24)
        new_explanation_6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_6))
        self.objects["step_explanation"] = new_explanation_6

        self.play(Circumscribe(self.objects["perimeter_dot"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["perimeter_label"]), run_time=1.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))