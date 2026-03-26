'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Solve the linear equation 2x = 6 using a concrete balance scale model to demonstrate the principle of "doing the same operation to both sides".
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: Upper part [y=1.5] for equation, lower part [y=0 to -1] for scale
#    - Footer Region: [Bottom y=-2.8] for step explanations (not implemented as separate text per JSON, but narrative is audio)
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct vertical zones. The equation is at UP*1.5, scale at ORIGIN+DOWN*1.0, ensuring no overlap.
#    - Group boxes and circles into VGroups for easy manipulation.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/solving_2x_equals_6/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Equation 2x=6 appears.
#    - Step 3: Build scale (fulcrum, beam, pans).
#    - Step 4: Add boxes (left) and circles (right) to pans.
#    - Step 5: Show division symbol.
#    - Step 6: Remove one box.
#    - Step 7: Split circles into two groups, remove one.
#    - Step 8: Transform equation to x=3, clean up extra elements.
#    - Step 9: Final hold.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        eq_anchor = 1.5 * UP
        scale_anchor = ORIGIN + DOWN * 1.0
        explanation_anchor = 2.8 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # equation_initial
        equation_initial = MathTex("2x = 6", color=WHITE, font_size=48)
        equation_initial.move_to(eq_anchor)
        self.objects["equation_initial"] = equation_initial

        # fulcrum (Triangle)
        fulcrum_points = [(-0.5, -1, 0), (0.5, -1, 0), (0, 0.5, 0)]
        fulcrum = Polygon(*fulcrum_points, color=GRAY, fill_opacity=0.8)
        fulcrum.move_to(scale_anchor + DOWN * 0.75)
        self.objects["fulcrum"] = fulcrum

        # beam
        beam = Line(LEFT * 3, RIGHT * 3, color=GRAY, stroke_width=8)
        beam.move_to(scale_anchor)
        self.objects["beam"] = beam

        # left_pan
        left_pan = Circle(radius=0.4, color=GRAY_B, fill_opacity=0.3, stroke_width=3)
        left_pan.move_to(scale_anchor + LEFT * 3 + DOWN * 0.4)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Circle(radius=0.4, color=GRAY_B, fill_opacity=0.3, stroke_width=3)
        right_pan.move_to(scale_anchor + RIGHT * 3 + DOWN * 0.4)
        self.objects["right_pan"] = right_pan

        # box1
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.5, stroke_width=2)
        box1.move_to(left_pan.get_center() + UP * 0.1)
        self.objects["box1"] = box1

        # box2
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.5, stroke_width=2)
        box2.next_to(box1, UP, buff=0.2)
        self.objects["box2"] = box2

        # box_label (will be duplicated onto each box)
        box_label = MathTex("x", color=WHITE, font_size=30)
        box_label.move_to(box1.get_center())
        self.objects["box_label"] = box_label

        # circles_group (6 green circles in 2x3 grid)
        circles = VGroup(*[Circle(radius=0.3, color=GREEN, fill_opacity=0.6) for _ in range(6)])
        circles.arrange_in_grid(rows=2, cols=3, buff=0.3)
        circles.move_to(right_pan.get_center())
        self.objects["circles_group"] = circles

        # circle_label (will be duplicated onto each circle)
        circle_label = MathTex("1", color=WHITE, font_size=24)
        circle_label.move_to(circles[0].get_center())
        self.objects["circle_label"] = circle_label

        # equation_final (initially invisible)
        equation_final = MathTex("x = 3", color=WHITE, font_size=48)
        equation_final.move_to(eq_anchor)
        equation_final.set_opacity(0)
        self.objects["equation_final"] = equation_final

        # division_symbol (created later in step 5)
        division_symbol = MathTex(r"\div 2", color=YELLOW, font_size=72)
        division_symbol.move_to(scale_anchor + UP * 1.0)
        division_symbol.set_opacity(0)
        self.objects["division_symbol"] = division_symbol

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Audio base path
        audio_base = "media/audio/solving_2x_equals_6"

        # ========== Step 1 ==========
        audio_step1 = f"{audio_base}/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(title), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = f"{audio_base}/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Write(equation_initial), run_time=2.5)
        remaining_2 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = f"{audio_base}/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(equation_initial, color=YELLOW, run_time=1))
        self.play(Create(fulcrum), run_time=1.0)
        self.play(Create(beam), run_time=1.0)
        self.play(Create(left_pan), Create(right_pan), run_time=1.0)
        remaining_3 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = f"{audio_base}/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Create boxes and labels
        box1_copy = box1.copy()
        box2_copy = box2.copy()
        label1 = box_label.copy().move_to(box1.get_center())
        label2 = box_label.copy().move_to(box2.get_center())
        self.objects["box_label1"] = label1
        self.objects["box_label2"] = label2

        # Create circle labels
        circle_labels = VGroup()
        for circle in circles:
            lbl = circle_label.copy().move_to(circle.get_center())
            circle_labels.add(lbl)
        self.objects["circle_labels"] = circle_labels

        self.play(
            Create(box1_copy),
            Create(box2_copy),
            Write(label1),
            Write(label2),
            Create(circles),
            Write(circle_labels),
            run_time=4.0
        )
        remaining_4 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = f"{audio_base}/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Circumscribe(equation_initial, color=YELLOW, run_time=1))
        division_symbol.set_opacity(1)
        self.play(FadeIn(division_symbol), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = f"{audio_base}/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(box2_copy, color=RED, run_time=1))
        self.play(
            FadeOut(box2_copy),
            FadeOut(label2),
            box1_copy.animate.move_to(left_pan.get_center()),
            label1.animate.move_to(box1_copy.get_center()),
            run_time=1.5
        )
        remaining_6 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = f"{audio_base}/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Indicate(circles, color=RED, run_time=1))
        # Split circles into two groups
        group1 = VGroup(*circles[:3], *circle_labels[:3])
        group2 = VGroup(*circles[3:], *circle_labels[3:])
        target_pos_group2 = scale_anchor + DOWN * 2.0
        self.play(
            group2.animate.move_to(target_pos_group2),
            run_time=2.0
        )
        remaining_7 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = f"{audio_base}/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        self.play(Indicate(box1_copy, color=GREEN, run_time=1))
        # Morph equation
        self.play(
            TransformMatchingTex(equation_initial, equation_final),
            FadeOut(group2),
            FadeOut(division_symbol),
            run_time=2.5
        )
        remaining_8 = max(0.1, 3.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        audio_step9 = f"{audio_base}/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))

        self.wait(max(0.1, 3.0))