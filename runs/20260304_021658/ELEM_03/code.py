'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the area and perimeter of a 4x3 rectangle. Area is shown by tiling unit squares, perimeter by tracing the boundary.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for rectangle, grid, squares, and tracer
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for composite objects (rectangle, grid, squares). Position them at content_center (ORIGIN). Step label and explanation text are placed relative to title and footer anchor.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/area_perimeter_rectangle/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Draw rectangle.
#    Step 2: Highlight rectangle, draw interior grid.
#    Step 3: Fill unit squares sequentially.
#    Step 4: Indicate rectangle, show tracer dot.
#    Step 5: Move tracer dot along perimeter.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_a_4x3_rectangle_5debffc0c0/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor + UP*0.2)
        self.objects["title"] = title

        # Create step_label (initial content)
        step_label = Text("Step 1: Draw the 4x3 rectangle", color=YELLOW, font_size=28)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # Create rectangle VGroup (as a Polygon for easy path)
        rect_vertices = [
            np.array([-2, -1.5, 0]),
            np.array([2, -1.5, 0]),
            np.array([2, 1.5, 0]),
            np.array([-2, 1.5, 0])
        ]
        rect_poly = Polygon(*rect_vertices, color=BLUE, stroke_width=4)
        rect_poly.move_to(content_center)
        self.objects["rect_vgroup"] = rect_poly  # Storing as a single Polygon for simplicity

        # Create grid lines VGroup
        grid_lines = VGroup()
        # Vertical lines at x = -1.5, -0.5, 0.5, 1.5
        for x in [-1.5, -0.5, 0.5, 1.5]:
            line = Line([x, -1.5, 0], [x, 1.5, 0], color=WHITE, stroke_width=2, stroke_opacity=0.7)
            grid_lines.add(line)
        # Horizontal lines at y = -1, 0, 1
        for y in [-1, 0, 1]:
            line = Line([-2, y, 0], [2, y, 0], color=WHITE, stroke_width=2, stroke_opacity=0.7)
            grid_lines.add(line)
        grid_lines.move_to(content_center)
        self.objects["grid_lines_vgroup"] = grid_lines

        # Create unit squares VGroup (12 squares)
        unit_squares = VGroup()
        for i in range(4):  # columns (x direction)
            for j in range(3):  # rows (y direction)
                # Square centered at ( -1.5 + i*1.0, -1.0 + j*1.0 )
                center_x = -1.5 + i * 1.0 + 0.5
                center_y = -1.0 + j * 1.0 + 0.5
                sq = Square(side_length=1.0, color=GREEN, fill_opacity=0.0, stroke_width=0)
                sq.move_to([center_x, center_y, 0])
                unit_squares.add(sq)
        unit_squares.move_to(content_center)
        self.objects["unit_squares_vgroup"] = unit_squares

        # Create tracer dot
        tracer_dot = Dot(radius=0.08, color=RED)
        # Place at start of rectangle path (bottom-left vertex)
        tracer_dot.move_to(rect_vertices[0])
        self.objects["tracer_dot"] = tracer_dot

        # Create perimeter path (same as rectangle)
        perimeter_path = Polygon(*rect_vertices, color=WHITE, stroke_opacity=0, stroke_width=0)
        perimeter_path.move_to(content_center)
        self.objects["perimeter_path"] = perimeter_path

        # Create explanation text
        explanation_text = Text("We start with a rectangle of width 4 and height 3.", color=GRAY_C, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/area_perimeter_rectangle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Visual action: Create rectangle
        self.play(Write(self.objects["title"]), run_time=0.5)
        self.play(Write(self.objects["step_label"]), run_time=0.5)
        self.play(Create(self.objects["rect_vgroup"]), run_time=2.0)
        self.play(Write(self.objects["explanation_text"]), run_time=0.5)
        remaining_1 = max(0.1, 3.0 - (0.5+0.5+2.0+0.5) + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/area_perimeter_rectangle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Circumscribe rectangle
        self.play(Circumscribe(self.objects["rect_vgroup"], color=YELLOW, run_time=1))
        # Update step label
        step_label2 = Text("Step 2: Partition into unit squares", color=YELLOW, font_size=28)
        step_label2.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label2))
        self.objects["step_label"] = step_label2
        # Update explanation text
        explanation_text2 = Text("We partition the rectangle into a 4 by 3 grid of unit squares.", color=GRAY_C, font_size=24)
        explanation_text2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], explanation_text2))
        self.objects["explanation_text"] = explanation_text2
        # Visual action: Create grid lines
        self.play(Create(self.objects["grid_lines_vgroup"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - (1.0+2.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/area_perimeter_rectangle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # No signal action
        # Update step label
        step_label3 = Text("Step 3: Fill squares to count area", color=YELLOW, font_size=28)
        step_label3.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label3))
        self.objects["step_label"] = step_label3
        # Update explanation text
        explanation_text3 = Text("Area = number of unit squares = 4 × 3 = 12.", color=GRAY_C, font_size=24)
        explanation_text3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], explanation_text3))
        self.objects["explanation_text"] = explanation_text3
        # Visual action: Fill squares sequentially
        anims = []
        for sq in self.objects["unit_squares_vgroup"]:
            anims.append(sq.animate.set_fill(opacity=0.5))
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=3.0)
        remaining_3 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/area_perimeter_rectangle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate rectangle
        self.play(Indicate(self.objects["rect_vgroup"], color=RED, run_time=1))
        # Update step label
        step_label4 = Text("Step 4: Trace the perimeter", color=YELLOW, font_size=28)
        step_label4.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label4))
        self.objects["step_label"] = step_label4
        # Update explanation text
        explanation_text4 = Text("Perimeter is the total distance around the outside.", color=GRAY_C, font_size=24)
        explanation_text4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], explanation_text4))
        self.objects["explanation_text"] = explanation_text4
        # Visual action: Create tracer dot
        self.play(FadeIn(self.objects["tracer_dot"]), run_time=1.0)
        remaining_4 = max(0.1, 2.5 - (1.0+1.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/area_perimeter_rectangle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # No signal action
        # Update step label
        step_label5 = Text("Step 5: Perimeter = 4 + 3 + 4 + 3 = 14", color=YELLOW, font_size=28)
        step_label5.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label5))
        self.objects["step_label"] = step_label5
        # Update explanation text
        explanation_text5 = Text("Perimeter = 4 + 3 + 4 + 3 = 14 units.", color=GRAY_C, font_size=24)
        explanation_text5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], explanation_text5))
        self.objects["explanation_text"] = explanation_text5
        # Visual action: Move tracer along perimeter
        self.play(MoveAlongPath(self.objects["tracer_dot"], self.objects["perimeter_path"]), run_time=4.0)
        remaining_5 = max(0.1, 4.5 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))