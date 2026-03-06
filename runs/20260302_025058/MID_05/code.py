'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between a circle's circumference (C) and its diameter (D) to discover Pi (π). Show that C is slightly longer than 3D.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] Left side for circle, right side for unrolled line and comparison.
#    - Footer Region: [Bottom y=-2.8] for final formula.
# 3. Anti-Overlap Check:
#    - Strategy: Use defined anchors to position objects. Keep left and right sides separate. Use VGroup for three diameters.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Present_a_circle_wit_fc0a36e6ef/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show circle.
#    - Step 2: Highlight circumference.
#    - Step 3: Unroll circumference into a vertical line.
#    - Step 4: Create three diameter copies.
#    - Step 5: Align three diameters below the unrolled line.
#    - Step 6: Show the gap (C - 3D).
#    - Step 7: Show final formula C = πD.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        circle_anchor = np.array([-3.5, 0, 0])
        line_anchor = np.array([3.5, 0, 0])
        diameter_store = np.array([3.5, 2.5, 0])
        formula_anchor = np.array([0, -2.8, 0])

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Unrolling a Circle: Discovering Pi", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(circle_anchor + LEFT*2, circle_anchor + RIGHT*2, color=RED, stroke_width=6)
        self.objects["diameter_line"] = diameter_line

        # label_D
        label_D = MathTex("D", color=RED)
        label_D.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_D"] = label_D

        # circumference_highlight
        circumference_highlight = Arc(radius=2.0, angle=TAU, color=YELLOW, stroke_width=8, stroke_opacity=0.7)
        circumference_highlight.move_to(circle_anchor)
        self.objects["circumference_highlight"] = circumference_highlight

        # unrolled_line
        unrolled_line = Line(line_anchor + DOWN*1.273, line_anchor + UP*1.273, color=YELLOW, stroke_width=8)
        self.objects["unrolled_line"] = unrolled_line

        # label_C
        label_C = MathTex("C", color=YELLOW)
        label_C.next_to(unrolled_line, RIGHT, buff=0.2)
        self.objects["label_C"] = label_C

        # diameter_copy_1
        diameter_copy_1 = Line(ORIGIN, RIGHT*4.0, color=RED, stroke_width=4)
        diameter_copy_1.move_to(diameter_store)
        self.objects["diameter_copy_1"] = diameter_copy_1

        # diameter_copy_2
        diameter_copy_2 = Line(ORIGIN, RIGHT*4.0, color=RED, stroke_width=4)
        diameter_copy_2.next_to(diameter_copy_1, RIGHT, buff=0.0)
        self.objects["diameter_copy_2"] = diameter_copy_2

        # diameter_copy_3
        diameter_copy_3 = Line(ORIGIN, RIGHT*4.0, color=RED, stroke_width=4)
        diameter_copy_3.next_to(diameter_copy_2, RIGHT, buff=0.0)
        self.objects["diameter_copy_3"] = diameter_copy_3

        # VGroup for three diameters
        three_diameters = VGroup(diameter_copy_1, diameter_copy_2, diameter_copy_3)
        self.objects["three_diameters"] = three_diameters

        # three_D_line (dashed line for comparison)
        three_D_line = DashedLine(line_anchor + DOWN*1.273 + LEFT*6.0, line_anchor + DOWN*1.273 + LEFT*6.0 + RIGHT*12.0, color=RED, stroke_width=4, stroke_opacity=0.5)
        self.objects["three_D_line"] = three_D_line

        # label_3D
        label_3D = MathTex("3D", color=RED)
        label_3D.next_to(three_D_line, DOWN, buff=0.2)
        self.objects["label_3D"] = label_3D

        # gap_line (will be created dynamically later)
        # We'll create it when needed in step 6.

        # label_gap
        label_gap = MathTex(r"C - 3D \approx 0.28D", color=GREEN, font_size=30)
        # Position will be set relative to gap_line later
        self.objects["label_gap"] = label_gap

        # formula_text
        formula_text = MathTex(r"C = \pi D \quad\mathrm{and}\quad \pi \approx 3.14159...", color=WHITE, font_size=35)
        formula_text.move_to(formula_anchor)
        self.objects["formula_text"] = formula_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Signal action: Create circle (as per JSON, signal_action type Create target circle)
        # But circle is the main visual action. We'll combine.
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = max(0.1, 6.912 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Create circumference_highlight
        self.play(Create(self.objects["circumference_highlight"]), run_time=1.5)
        remaining_2 = max(0.1, 4.8 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # No signal action. Transform circumference_highlight into unrolled_line.
        # Also create label_C.
        self.play(
            Transform(self.objects["circumference_highlight"], self.objects["unrolled_line"]),
            Write(self.objects["label_C"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 4.44 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate diameter_line
        self.play(Indicate(self.objects["diameter_line"], color=RED, run_time=1))
        # Visual action: Create three diameter copies at storage area.
        self.play(
            Create(self.objects["diameter_copy_1"]),
            Create(self.objects["diameter_copy_2"]),
            Create(self.objects["diameter_copy_3"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 5.52 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # No signal action. Move three diameters down and create dashed line.
        # Align start of first diameter with start of unrolled line.
        start_unrolled = self.objects["unrolled_line"].get_start()
        target_position = start_unrolled + DOWN*1.273  # This is the start of the dashed line
        # We'll move the VGroup
        self.play(
            self.objects["three_diameters"].animate.move_to(target_position + RIGHT*6.0),  # Center of group at middle of line
            Create(self.objects["three_D_line"]),
            Write(self.objects["label_3D"]),
            run_time=3.0
        )
        remaining_5 = max(0.1, 7.584 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Create gap_line
        # Create the gap_line dynamically
        gap_line = Line(
            self.objects["three_D_line"].get_end(),
            self.objects["unrolled_line"].get_end(),
            color=GREEN,
            stroke_width=6
        )
        self.objects["gap_line"] = gap_line
        # Position label_gap
        self.objects["label_gap"].next_to(gap_line, RIGHT, buff=0.2)

        self.play(
            Create(gap_line),
            Write(self.objects["label_gap"]),
            run_time=2.0
        )
        remaining_6 = max(0.1, 5.016 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/Present_a_circle_wit_fc0a36e6ef/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # Signal action: Write formula_text
        self.play(Write(self.objects["formula_text"]), run_time=3.0)
        remaining_7 = max(0.1, 8.976 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))