'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the concepts of area (as unit squares filling a rectangle) and perimeter (as the boundary line) for a 4x3 rectangle.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle and grid
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Title at top, rectangle centered, step text at bottom. Area formula appears above step text, then fades out before perimeter trace.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/area_perimeter_rectangle/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Draw rectangle outline, label dimensions.
#    - Fill with unit squares row by row.
#    - Show area formula.
#    - Fade area formula, trace perimeter.
#    - Final indication of area vs perimeter.
'''

from manim import *
import os

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
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # rect_outline
        rect_vertices = [(-1.6, -1.2, 0), (1.6, -1.2, 0), (1.6, 1.2, 0), (-1.6, 1.2, 0)]
        rect_outline = Polygon(*rect_vertices, color=BLUE, stroke_width=4, fill_opacity=0.0)
        rect_outline.move_to(global_center)
        self.objects["rect_outline"] = rect_outline
        
        # grid_of_squares (initially empty VGroup, will be populated later)
        grid_of_squares = VGroup()
        grid_of_squares.move_to(global_center)
        self.objects["grid_of_squares"] = grid_of_squares
        
        # dim_label_length
        dim_label_length = MathTex("4", color=GREEN, font_size=30)
        dim_label_length.next_to(rect_outline, DOWN, buff=0.2)
        dim_label_length.align_to(rect_outline.get_center(), RIGHT)
        dim_label_length.shift(LEFT * 0.8)
        self.objects["dim_label_length"] = dim_label_length
        
        # dim_label_width
        dim_label_width = MathTex("3", color=GREEN, font_size=30)
        dim_label_width.next_to(rect_outline, RIGHT, buff=0.2)
        dim_label_width.align_to(rect_outline.get_center(), UP)
        dim_label_width.shift(DOWN * 0.6)
        self.objects["dim_label_width"] = dim_label_width
        
        # area_count_text
        area_count_text = MathTex(r"\mathrm{Area} = 4 \times 3 = 12 \mathrm{ unit squares}", color=YELLOW, font_size=35)
        area_count_text.move_to(explanation_anchor + UP * 0.5)
        self.objects["area_count_text"] = area_count_text
        
        # perimeter_line
        perimeter_line = Polygon(*rect_vertices, color=RED, stroke_width=6, fill_opacity=0.0)
        perimeter_line.move_to(global_center)
        perimeter_line.set_z_index(1)
        self.objects["perimeter_line"] = perimeter_line
        
        # step_explanation
        step_explanation = Text("Step 1: Draw the rectangle.", color=GRAY_C, font_size=30)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/area_perimeter_rectangle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["rect_outline"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 2.5 - 1.0 - 1.5 + 0.5)))
        
        # Step 2
        audio_step2 = "media/audio/area_perimeter_rectangle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["dim_label_length"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 2.0 - 1.0 + 0.5)))
        
        # Step 3
        audio_step3 = "media/audio/area_perimeter_rectangle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["dim_label_width"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 1.5 - 1.0 + 0.5)))
        
        # Step 4
        audio_step4 = "media/audio/area_perimeter_rectangle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["rect_outline"], color=YELLOW, run_time=1))
        new_step_text = Text("Step 2: Fill with unit squares to show area.", color=GRAY_C, font_size=30)
        new_step_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_step_text), run_time=1.0)
        self.wait(max(0.1, max(0.1, 3.5 - 1.0 - 1.0 + 0.5)))
        
        # Step 5: Create grid rows
        audio_step5 = "media/audio/area_perimeter_rectangle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Build the grid of squares
        unit = 0.8
        squares = VGroup()
        for row in range(3):  # 3 rows
            row_squares = VGroup()
            for col in range(4):  # 4 columns
                sq = Square(side_length=unit, stroke_width=1, stroke_color=WHITE, fill_opacity=0.0)
                sq.move_to([-1.6 + col * unit + unit/2, -1.2 + row * unit + unit/2, 0])
                row_squares.add(sq)
            squares.add(row_squares)
        
        # Animate rows appearing
        anim_time_per_row = 1.0
        for i, row in enumerate(squares):
            for sq in row:
                sq.set_fill(BLUE_C, opacity=0.3)
            self.play(LaggedStart(*[Create(sq) for sq in row], lag_ratio=0.1), run_time=anim_time_per_row)
            self.objects["grid_of_squares"].add(*row)
        self.wait(max(0.1, max(0.1, 4.0 - 3 * anim_time_per_row + 0.5)))
        
        # Step 6
        audio_step6 = "media/audio/area_perimeter_rectangle/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["grid_of_squares"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["area_count_text"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 4.0 - 1.0 - 1.5 + 0.5)))
        
        # Step 7
        audio_step7 = "media/audio/area_perimeter_rectangle/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        new_step_text2 = Text("Step 3: Trace the perimeter.", color=GRAY_C, font_size=30)
        new_step_text2.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_step_text2), run_time=1.0)
        self.play(FadeOut(self.objects["area_count_text"]), run_time=0.5)
        self.wait(max(0.1, max(0.1, 3.0 - 1.0 - 0.5 + 0.5)))
        
        # Step 8
        audio_step8 = "media/audio/area_perimeter_rectangle/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Create a thick line for the flash effect
        trace_line = self.objects["perimeter_line"].copy()
        trace_line.set_stroke(width=10, color=RED)
        self.add(trace_line)
        self.play(ShowPassingFlash(trace_line, time_width=0.5), run_time=4.0)
        self.remove(trace_line)
        self.wait(max(0.1, max(0.1, 5.0 - 4.0 + 0.5)))
        
        # Step 9
        audio_step9 = "media/audio/area_perimeter_rectangle/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["grid_of_squares"], color=BLUE, run_time=1))
        self.play(Indicate(self.objects["perimeter_line"], color=RED, run_time=1))
        self.wait(max(0.1, max(0.1, 4.0 - 1.0 - 1.0 + 0.5)))