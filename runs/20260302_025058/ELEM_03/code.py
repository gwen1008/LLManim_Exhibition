'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the concepts of area and perimeter for a 4x3 rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for rectangle, grid, perimeter
#    - Footer Region: [Bottom y=-3.0] for formulas
# 3. Anti-Overlap Check:
#    - The rectangle, grid, and perimeter path occupy the same central space but appear sequentially.
#    - Formulas are placed at the bottom, spaced vertically.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_a_4x3_rectangle_083edf7311/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw rectangle.
#    - Step 2: Label width and height.
#    - Step 3: Show area grid.
#    - Step 4: Show area formula.
#    - Step 5: Show perimeter outline.
#    - Step 6: Trace perimeter.
#    - Step 7: Morph perimeter into straight line.
#    - Step 8: Show perimeter formula.
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
        footer_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # step_title
        step_title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        step_title.move_to(title_anchor)
        self.objects["step_title"] = step_title

        # rect_main
        rect_vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]
        rect_main = Polygon(*rect_vertices, color=BLUE, stroke_width=4, fill_opacity=0.0)
        rect_main.move_to(content_center)
        self.objects["rect_main"] = rect_main

        # dim_label_w
        dim_label_w = MathTex("4", color=YELLOW)
        dim_label_w.next_to(rect_main, DOWN, buff=0.2)
        dim_label_w.set_x(0)
        self.objects["dim_label_w"] = dim_label_w

        # dim_label_h
        dim_label_h = MathTex("3", color=YELLOW)
        dim_label_h.next_to(rect_main, RIGHT, buff=0.2)
        dim_label_h.set_y(0)
        self.objects["dim_label_h"] = dim_label_h

        # area_grid
        area_grid = VGroup()
        side_length = 1.0
        for row in range(3):  # 3 rows
            for col in range(4):  # 4 columns
                sq = Square(side_length=side_length, color=GREEN_C, fill_opacity=0.5, stroke_width=1)
                sq.move_to([-2 + col * side_length + side_length/2, -1.5 + row * side_length + side_length/2, 0])
                area_grid.add(sq)
        area_grid.move_to(content_center)
        self.objects["area_grid"] = area_grid

        # perimeter_path
        perimeter_path = Polygon(*rect_vertices, color=RED, stroke_width=6, fill_opacity=0.0)
        perimeter_path.move_to(content_center)
        self.objects["perimeter_path"] = perimeter_path

        # perimeter_line_trace
        perimeter_line_trace = Line(start=(-2, -1.5, 0), end=(-2, -1.5, 0), color=RED, stroke_width=6)
        self.objects["perimeter_line_trace"] = perimeter_line_trace

        # perimeter_line_straight
        perimeter_line_straight = Line(start=LEFT*7, end=RIGHT*7, color=RED, stroke_width=6)
        perimeter_line_straight.move_to(content_center + DOWN*2.5)
        self.objects["perimeter_line_straight"] = perimeter_line_straight

        # formula_area
        formula_area = MathTex(r"\mathrm{Area} = \mathrm{width} \times \mathrm{height} = 4 \times 3 = 12", color=GREEN_C, font_size=30)
        formula_area.move_to(footer_anchor)
        formula_area.align_to(ORIGIN, DOWN)
        self.objects["formula_area"] = formula_area

        # formula_perimeter
        formula_perimeter = MathTex(r"\mathrm{Perimeter} = 2\times(\mathrm{width}+\mathrm{height}) = 2\times(4+3)=14", color=RED, font_size=30)
        formula_perimeter.next_to(formula_area, DOWN, buff=0.5)
        self.objects["formula_perimeter"] = formula_perimeter

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["rect_main"]), run_time=1.5)
        remaining_1 = max(0.1, 4.776 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Write dim_label_w
        self.play(Write(self.objects["dim_label_w"]), run_time=1.0)
        # Visual action: Write dim_label_w (already done above, but we also need height label)
        # According to JSON, visual_action target is dim_label_w, but we also need dim_label_h.
        # The narrative says "width equals 4, height equals 3." We'll write both.
        self.play(Write(self.objects["dim_label_h"]), run_time=1.0)
        total_anim_time_step2 = 2.0
        remaining_2 = max(0.1, 5.52 - total_anim_time_step2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate rect_main with GREEN
        self.play(Indicate(self.objects["rect_main"], color=GREEN, run_time=1.0))
        # Visual action: Create area_grid
        self.play(Create(self.objects["area_grid"]), run_time=2.0)
        total_anim_time_step3 = 3.0
        remaining_3 = max(0.1, 10.008 - total_anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Circumscribe area_grid with YELLOW
        self.play(Circumscribe(self.objects["area_grid"], color=YELLOW, run_time=1.0))
        # Visual action: Write formula_area
        self.play(Write(self.objects["formula_area"]), run_time=1.5)
        total_anim_time_step4 = 2.5
        remaining_4 = max(0.1, 7.272 - total_anim_time_step4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate rect_main with RED
        self.play(Indicate(self.objects["rect_main"], color=RED, run_time=1.0))
        # Visual action: Create perimeter_path
        self.play(Create(self.objects["perimeter_path"]), run_time=1.5)
        total_anim_time_step5 = 2.5
        remaining_5 = max(0.1, 9.696 - total_anim_time_step5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: null
        # Visual action: Transform perimeter_line_trace to trace the boundary.
        # We'll animate the line growing along the rectangle's perimeter.
        # We'll create a new line that is the full perimeter path and transform the point-like line into it.
        full_perimeter_line = Polygon(*rect_vertices, color=RED, stroke_width=6, fill_opacity=0.0)
        full_perimeter_line.move_to(content_center)
        # We'll use Transform from perimeter_line_trace to full_perimeter_line.
        # But note: perimeter_line_trace is a line from (-2,-1.5) to (-2,-1.5) (a point).
        # We'll first add the trace line to the scene.
        self.add(self.objects["perimeter_line_trace"])
        self.play(Transform(self.objects["perimeter_line_trace"], full_perimeter_line), run_time=3.0)
        total_anim_time_step6 = 3.0
        remaining_6 = max(0.1, 9.216 - total_anim_time_step6 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # Signal action: Circumscribe perimeter_path with YELLOW
        self.play(Circumscribe(self.objects["perimeter_path"], color=YELLOW, run_time=1.0))
        # Visual action: ReplacementTransform perimeter_path into perimeter_line_straight
        self.play(ReplacementTransform(self.objects["perimeter_path"], self.objects["perimeter_line_straight"]), run_time=2.0)
        total_anim_time_step7 = 3.0
        remaining_7 = max(0.1, 7.2 - total_anim_time_step7 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/Draw_a_4x3_rectangle_083edf7311/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        # Signal action: Indicate perimeter_line_straight with YELLOW
        self.play(Indicate(self.objects["perimeter_line_straight"], color=YELLOW, run_time=1.0))
        # Visual action: Write formula_perimeter
        self.play(Write(self.objects["formula_perimeter"]), run_time=1.5)
        total_anim_time_step8 = 2.5
        remaining_8 = max(0.1, 7.416 - total_anim_time_step8 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Final hold
        self.wait(max(0.1, 2))