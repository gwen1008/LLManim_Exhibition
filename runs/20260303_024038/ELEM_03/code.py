'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize area and perimeter of a 4x3 rectangle. Area is derived by counting unit squares; perimeter by tracing the boundary.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.0] for Title and Step Label
#    - Main Content: [Center y=0] for rectangle, grid, and perimeter animation
#    - Footer Region: [Bottom y=-3.0] for area and perimeter formulas
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Keep formulas at bottom left/right, far from central rectangle. Use VGroup for grid squares.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/area_perimeter_rectangle/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Draw rectangle outline, label dimensions.
#    - Fill with unit squares (grid) to show area = 12.
#    - Reveal area formula.
#    - Animate red dot tracing perimeter.
#    - Reveal perimeter formula.
#    - Final highlight of both formulas.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        title_anchor = 3.0 * UP
        content_center = ORIGIN
        formula_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # title_text
        title_text = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # step_label
        step_label = Text("Step 1: Draw the rectangle", color=YELLOW, font_size=30)
        step_label.next_to(title_text, DOWN, buff=0.5)
        self.objects["step_label"] = step_label

        # rect_outline (Polygon with vertices)
        vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]
        rect_outline = Polygon(*vertices, color=BLUE, stroke_width=6, fill_opacity=0.0)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline

        # dim_label_w
        dim_label_w = MathTex("4", color=GREEN)
        dim_label_w.next_to(rect_outline.get_bottom(), DOWN, buff=0.2)
        dim_label_w.align_to(content_center, LEFT)
        dim_label_w.shift(RIGHT * 2)
        self.objects["dim_label_w"] = dim_label_w

        # dim_label_h
        dim_label_h = MathTex("3", color=GREEN)
        dim_label_h.next_to(rect_outline.get_right(), RIGHT, buff=0.2)
        dim_label_h.align_to(content_center, UP)
        dim_label_h.shift(DOWN * 0.75)
        self.objects["dim_label_h"] = dim_label_h

        # grid_squares (12 unit squares in 4x3 grid)
        grid_squares = VGroup()
        side_length = 1.0
        for row in range(3):  # 3 rows (height)
            for col in range(4):  # 4 columns (width)
                sq = Square(side_length=side_length, color="#B8860B", stroke_width=2,
                            fill_color="#FFD700", fill_opacity=0.0, stroke_opacity=0.0)
                # Position relative to grid center
                x = (col - 1.5) * side_length
                y = (row - 1) * side_length
                sq.move_to([x, y, 0])
                grid_squares.add(sq)
        grid_squares.move_to(content_center)
        self.objects["grid_squares"] = grid_squares

        # perimeter_dot
        perimeter_dot = Dot(radius=0.08, color=RED)
        perimeter_dot.move_to((-2, -1.5, 0))
        self.objects["perimeter_dot"] = perimeter_dot

        # perimeter_path (will be created later as TracedPath)
        # We'll create it when needed in step 5.

        # formula_area
        formula_area = MathTex(r"A = 4 \times 3 = 12", color="#FFD700", font_size=36)
        formula_area.move_to(formula_anchor + LEFT * 3)
        self.objects["formula_area"] = formula_area

        # formula_perimeter
        formula_perimeter = MathTex(r"P = 2 \times (4 + 3) = 14", color=RED, font_size=36)
        formula_perimeter.move_to(formula_anchor + RIGHT * 3)
        self.objects["formula_perimeter"] = formula_perimeter

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/area_perimeter_rectangle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title_text"]), Write(self.objects["step_label"]), run_time=1.5)
        self.play(Create(self.objects["rect_outline"]), run_time=2.0)
        remaining_1 = max(0.1, 2.5 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/area_perimeter_rectangle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["rect_outline"], color=GREEN, run_time=1))
        self.play(Write(self.objects["dim_label_w"]), Write(self.objects["dim_label_h"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/area_perimeter_rectangle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # Update step label
        step_label2 = Text("Step 2: Fill with unit squares", color=YELLOW, font_size=30)
        step_label2.next_to(self.objects["title_text"], DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label2))
        self.objects["step_label"] = step_label2

        # Animate squares appearing row by row
        for i, sq in enumerate(self.objects["grid_squares"]):
            self.play(
                sq.animate.set_fill(opacity=0.5).set_stroke(opacity=1.0),
                run_time=0.2
            )
        remaining_3 = max(0.1, 5.0 - 1 - 0.2*12 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/area_perimeter_rectangle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["grid_squares"], color="#FFD700", run_time=1))
        # Update step label
        step_label3 = Text("Step 3: Area formula", color=YELLOW, font_size=30)
        step_label3.next_to(self.objects["title_text"], DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label3))
        self.objects["step_label"] = step_label3

        self.play(Write(self.objects["formula_area"]), run_time=1.5)
        remaining_4 = max(0.1, 4.0 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/area_perimeter_rectangle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["rect_outline"], color=RED, run_time=1))
        # Update step label
        step_label4 = Text("Step 4: Trace perimeter", color=YELLOW, font_size=30)
        step_label4.next_to(self.objects["title_text"], DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label4))
        self.objects["step_label"] = step_label4

        # Create perimeter_path as TracedPath
        perimeter_path = TracedPath(self.objects["perimeter_dot"].get_center,
                                    stroke_color=RED, stroke_width=4)
        self.add(perimeter_path)
        self.objects["perimeter_path"] = perimeter_path

        # Animate dot moving around rectangle (clockwise from bottom-left)
        corners = [
            (-2, -1.5, 0),  # bottom-left
            (2, -1.5, 0),   # bottom-right
            (2, 1.5, 0),    # top-right
            (-2, 1.5, 0),   # top-left
            (-2, -1.5, 0)   # back to start
        ]
        self.add(self.objects["perimeter_dot"])
        for i in range(4):
            self.play(
                self.objects["perimeter_dot"].animate.move_to(corners[i+1]),
                run_time=1.2, rate_func=linear
            )
        remaining_5 = max(0.1, 6.0 - 1 - 4*1.2 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/area_perimeter_rectangle/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["perimeter_path"], color=RED, run_time=1))
        # Update step label
        step_label5 = Text("Step 5: Perimeter formula", color=YELLOW, font_size=30)
        step_label5.next_to(self.objects["title_text"], DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label5))
        self.objects["step_label"] = step_label5

        self.play(Write(self.objects["formula_perimeter"]), run_time=1.5)
        remaining_6 = max(0.1, 4.5 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_4dd98d98e9/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/area_perimeter_rectangle/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(
            Indicate(self.objects["formula_area"], color=YELLOW, run_time=1),
            Indicate(self.objects["formula_perimeter"], color=YELLOW, run_time=1)
        )
        # Update step label
        step_label6 = Text("Step 6: Summary", color=YELLOW, font_size=30)
        step_label6.next_to(self.objects["title_text"], DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label6))
        self.objects["step_label"] = step_label6

        remaining_7 = max(0.1, 3.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_7))