'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize area and perimeter of a rectangle. Area as covering with unit squares, perimeter as boundary length.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for rectangle, grid, and perimeter trace
#    - Footer Region: [Bottom y=-3.5] for area and perimeter formulas
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for grid and formulas. Position formulas vertically in footer.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/area_perimeter_rectangle/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw rectangle outline.
#    - Step 2: Write width and height labels.
#    - Step 3: Indicate rectangle, update step label to Area phase.
#    - Step 4: Fill rectangle with unit squares (grid).
#    - Step 5: Circumscribe grid, write area formula.
#    - Step 6: Indicate rectangle, update step label to Perimeter phase.
#    - Step 7: Create perimeter dot.
#    - Step 8: Animate dot tracing boundary with trail.
#    - Step 9: Indicate trail, write perimeter formula.
#    - Step 10: Circumscribe both formulas.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # step_label
        step_label = Text("Step 1: The Rectangle", color=GRAY, font_size=24)
        step_label.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # rect_outline
        rect_outline = Rectangle(width=4.0, height=3.0, color=BLUE, fill_opacity=0.0, stroke_width=4)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline

        # width_label
        width_label = MathTex("4", color=BLUE)
        # Position: next_to bottom side, down, aligned to right of rectangle's left? Let's parse: "align_to(rect_outline.get_right(), LEFT).shift(RIGHT*2.0)"
        # This seems to center it under the bottom. We'll place it below the midpoint of the bottom side.
        width_label.next_to(rect_outline.get_bottom(), DOWN, buff=0.2)
        width_label.align_to(rect_outline, LEFT).shift(RIGHT * 2.0)  # This centers it roughly
        self.objects["width_label"] = width_label

        # height_label
        height_label = MathTex("3", color=BLUE)
        # Position: next_to left side, right, aligned to top of rectangle's bottom? Let's parse: "align_to(rect_outline.get_top(), DOWN).shift(UP*1.5)"
        height_label.next_to(rect_outline.get_left(), RIGHT, buff=0.2)
        height_label.align_to(rect_outline, DOWN).shift(UP * 1.5)  # This centers it roughly
        self.objects["height_label"] = height_label

        # area_squares_vgroup (empty container, will be populated in step 4)
        area_squares_vgroup = VGroup()
        area_squares_vgroup.move_to(content_center)
        self.objects["area_squares_vgroup"] = area_squares_vgroup

        # perimeter_dot
        perimeter_dot = Dot(radius=0.08, color=YELLOW)
        perimeter_dot.move_to(rect_outline.get_corner(DL))
        self.objects["perimeter_dot"] = perimeter_dot

        # perimeter_trail (will be attached to dot later)
        perimeter_trail = TracedPath(perimeter_dot.get_center, stroke_color=YELLOW, stroke_width=6)
        self.objects["perimeter_trail"] = perimeter_trail

        # area_formula
        area_formula = MathTex(r"\mathrm{Area} = \mathrm{length} \times \mathrm{width} = 4 \times 3 = 12", color=TEAL, font_size=28)
        area_formula.move_to(explanation_anchor + UP * 0.5)
        self.objects["area_formula"] = area_formula

        # perimeter_formula
        perimeter_formula = MathTex(r"\mathrm{Perimeter} = 2\times(\mathrm{length}+\mathrm{width}) = 2\times(4+3)=14", color=YELLOW, font_size=28)
        perimeter_formula.next_to(area_formula, DOWN, buff=0.5)
        self.objects["perimeter_formula"] = perimeter_formula

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/area_perimeter_rectangle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title_text"]), Write(self.objects["step_label"]), Create(self.objects["rect_outline"]), run_time=2.0)
        remaining_1 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/area_perimeter_rectangle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        # signal_action: Write width_label
        self.play(Write(self.objects["width_label"]), run_time=0.5)
        # visual_action: Write height_label
        self.play(Write(self.objects["height_label"]), run_time=0.5)
        total_anim_time_step2 = 1.0
        remaining_2 = max(0.1, 2.5 - total_anim_time_step2 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/area_perimeter_rectangle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: Indicate rect_outline with color WHITE
        self.play(Indicate(self.objects["rect_outline"], color=WHITE, run_time=1))
        # visual_action: Transform step_label to new text
        step_label_new = Text("Step 2: Area as Unit Squares", color=GRAY, font_size=24)
        step_label_new.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new), run_time=1)
        self.objects["step_label"] = step_label_new
        total_anim_time_step3 = 2.0
        remaining_3 = max(0.1, 3.0 - total_anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/area_perimeter_rectangle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Build the grid of unit squares
        width = 4
        height = 3
        unit = 1.0  # side length of unit square
        squares = VGroup()
        for h in range(height):
            for w in range(width):
                sq = Square(side_length=unit, color=TEAL, fill_opacity=0.7, stroke_width=2)
                # Position relative to rectangle center
                # Rectangle center is at content_center (ORIGIN), width=4, height=3
                # We want the grid to exactly fill the rectangle outline.
                # The rectangle's bottom-left corner is at (-2, -1.5) because width=4, height=3.
                # Square's center should be at (-2 + w*unit + unit/2, -1.5 + h*unit + unit/2)
                sq.move_to([-2 + w * unit + unit/2, -1.5 + h * unit + unit/2, 0])
                squares.add(sq)
        squares.move_to(content_center)  # Ensure centered
        self.objects["area_squares_vgroup"] = squares
        # Animate creation row by row for clarity
        anims = []
        for sq in squares:
            anims.append(Create(sq))
        self.play(LaggedStart(*anims, lag_ratio=0.05), run_time=4.0)
        remaining_4 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/area_perimeter_rectangle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: Circumscribe area_squares_vgroup with color TEAL
        self.play(Circumscribe(self.objects["area_squares_vgroup"], color=TEAL, run_time=1))
        # visual_action: Write area_formula
        self.play(Write(self.objects["area_formula"]), run_time=1.5)
        total_anim_time_step5 = 2.5
        remaining_5 = max(0.1, 3.0 - total_anim_time_step5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/area_perimeter_rectangle/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: Indicate rect_outline with color YELLOW
        self.play(Indicate(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # visual_action: Transform step_label to new text
        step_label_new2 = Text("Step 3: Perimeter as Boundary Length", color=GRAY, font_size=24)
        step_label_new2.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new2), run_time=1)
        self.objects["step_label"] = step_label_new2
        total_anim_time_step6 = 2.0
        remaining_6 = max(0.1, 3.0 - total_anim_time_step6 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/area_perimeter_rectangle/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # visual_action: Create perimeter_dot
        self.play(Create(self.objects["perimeter_dot"]), run_time=1.5)
        remaining_7 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/area_perimeter_rectangle/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Add the trail to the scene
        self.add(self.objects["perimeter_trail"])
        # Animate dot moving along rectangle boundary
        # Create a path that is the rectangle's perimeter (closed loop)
        # We'll use MoveAlongPath
        path = self.objects["rect_outline"].copy().set_stroke(opacity=0)  # invisible path
        self.play(MoveAlongPath(self.objects["perimeter_dot"], path, run_time=5.0, rate_func=linear))
        remaining_8 = max(0.1, 5.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/area_perimeter_rectangle/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # signal_action: Indicate perimeter_trail with color YELLOW
        self.play(Indicate(self.objects["perimeter_trail"], color=YELLOW, run_time=1))
        # visual_action: Write perimeter_formula
        self.play(Write(self.objects["perimeter_formula"]), run_time=1.5)
        total_anim_time_step9 = 2.5
        remaining_9 = max(0.1, 3.5 - total_anim_time_step9 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Create_a_4x3_rectang_38ca83bf54/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/area_perimeter_rectangle/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # signal_action: Circumscribe area_formula with color TEAL
        self.play(Circumscribe(self.objects["area_formula"], color=TEAL, run_time=1))
        # visual_action: Circumscribe perimeter_formula with color YELLOW
        self.play(Circumscribe(self.objects["perimeter_formula"], color=YELLOW, run_time=1))
        total_anim_time_step10 = 2.0
        remaining_10 = max(0.1, 4.0 - total_anim_time_step10 + 0.5)
        self.wait(max(0.1, remaining_10))