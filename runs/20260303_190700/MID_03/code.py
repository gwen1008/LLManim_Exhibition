'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize solving the equation 2x = 6 using a concrete balance scale model. Show that dividing both sides by 2 corresponds to removing half the weight from each pan.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the scale, pans, boxes, circles, and equation.
#    - Footer Region: [Bottom y=-3.5] for step explanation text.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for composite objects (boxes, circles). Position scale at content_center (ORIGIN). Keep equation above (UP*2) and explanation below (DOWN*2.5). Ensure objects do not extend beyond safe zones.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/solving_2x_equals_6_with_a_balance_scale/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title.
#    - Step 2: Build the scale structure and add two boxes to left pan.
#    - Step 3: Add six circles to right pan, show equation and initial explanation.
#    - Step 4: Highlight equation, update explanation to "Divide both sides by 2".
#    - Step 5: Remove one box and three circles, animate beam tilt.
#    - Step 6: Highlight remaining box, transform equation to x=3, update final explanation.
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
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # scale_base (Triangle)
        base_points = [(-0.5, -1.5, 0), (0, -0.5, 0), (0.5, -1.5, 0)]
        scale_base = Polygon(*base_points, color=GRAY_B, fill_opacity=0.8)
        scale_base.move_to(content_center + 2 * DOWN)
        self.objects["scale_base"] = scale_base

        # scale_beam
        scale_beam = Line(start=3 * LEFT, end=3 * RIGHT, color=GRAY_B, stroke_width=8)
        scale_beam.move_to(content_center + 0.5 * UP)
        self.objects["scale_beam"] = scale_beam

        # left_pan
        left_pan = Circle(radius=0.5, color=GRAY, fill_opacity=0.3)
        left_pan.move_to(scale_beam.get_start() + DOWN)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Circle(radius=0.5, color=GRAY, fill_opacity=0.3)
        right_pan.move_to(scale_beam.get_end() + DOWN)
        self.objects["right_pan"] = right_pan

        # connector_left
        connector_left = Line(start=scale_beam.get_start(), end=left_pan.get_top(), color=GRAY, stroke_width=4)
        self.objects["connector_left"] = connector_left

        # connector_right
        connector_right = Line(start=scale_beam.get_end(), end=right_pan.get_top(), color=GRAY, stroke_width=4)
        self.objects["connector_right"] = connector_right

        # box_template (VGroup: Square + 'x' label)
        box_sq = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        box_label = MathTex("x", color=WHITE, font_size=30)
        box_label.move_to(box_sq.get_center())
        box_template = VGroup(box_sq, box_label)
        self.objects["box_template"] = box_template  # store template, not shown

        # box1 (copy of template)
        box1 = box_template.copy()
        box1.move_to(left_pan.get_center() + 0.6 * LEFT)
        self.objects["box1"] = box1

        # box2 (copy of template)
        box2 = box_template.copy()
        box2.move_to(left_pan.get_center() + 0.6 * RIGHT)
        self.objects["box2"] = box2

        # circle_template
        circle_template = Circle(radius=0.3, color=GREEN, fill_opacity=0.7)
        self.objects["circle_template"] = circle_template  # template, not shown

        # circles_group (six circles arranged in 2 rows of 3)
        circles = VGroup()
        for i in range(6):
            circ = circle_template.copy()
            circles.add(circ)
        # Arrange in 2 rows, 3 columns, centered on right pan
        circles.arrange_in_grid(rows=2, cols=3, buff=0.2)
        circles.move_to(right_pan.get_center())
        self.objects["circles_group"] = circles

        # Create a subgroup of three circles for removal (step 5)
        # We'll pick the first three circles (top row) for simplicity
        three_circles = VGroup(*circles[:3])
        self.objects["three_circles"] = three_circles

        # equation
        equation = MathTex("2x = 6", color=YELLOW, font_size=48)
        equation.move_to(content_center + 2 * UP)
        self.objects["equation"] = equation

        # step_explanation (initial)
        step_explanation = Text("The scale is balanced: two boxes equal six circles.", color=GRAY_B, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Create updated explanation texts for later steps
        step4_text = Text("Divide both sides by 2: Remove half from each side.", color=GRAY_B, font_size=28)
        step4_text.move_to(explanation_anchor)
        self.objects["step4_text"] = step4_text

        step6_text = Text("Therefore, x = 3.", color=GRAY_B, font_size=28)
        step6_text.move_to(explanation_anchor)
        self.objects["step6_text"] = step6_text

        # Create final equation x = 3 for step 6
        final_eq = MathTex("x = 3", color=YELLOW, font_size=48)
        final_eq.move_to(equation.get_center())
        self.objects["final_eq"] = final_eq

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/To_visualize_the_equ_32e762e472/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/solving_2x_equals_6_with_a_balance_scale/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/To_visualize_the_equ_32e762e472/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/solving_2x_equals_6_with_a_balance_scale/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        scale_parts = [self.objects["scale_base"], self.objects["scale_beam"], self.objects["connector_left"],
                       self.objects["connector_right"], self.objects["left_pan"], self.objects["right_pan"]]
        self.play(LaggedStart(*[Create(part) for part in scale_parts], lag_ratio=0.1), run_time=3.0)
        self.play(FadeIn(self.objects["box1"]), FadeIn(self.objects["box2"]), run_time=1.5)
        remaining_2 = max(0.1, 5.0 - (3.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/To_visualize_the_equ_32e762e472/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/solving_2x_equals_6_with_a_balance_scale/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["circles_group"], color=GREEN, run_time=1))
        self.play(FadeIn(self.objects["circles_group"]), run_time=1.5)
        self.play(Write(self.objects["equation"]), Write(self.objects["step_explanation"]), run_time=1.5)
        remaining_3 = max(0.1, 4.0 - (1 + 1.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/To_visualize_the_equ_32e762e472/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/solving_2x_equals_6_with_a_balance_scale/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["equation"], color=YELLOW, run_time=1))
        self.play(ReplacementTransform(self.objects["step_explanation"], self.objects["step4_text"]), run_time=1.5)
        remaining_4 = max(0.1, 4.0 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/To_visualize_the_equ_32e762e472/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/solving_2x_equals_6_with_a_balance_scale/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["box2"], color=RED, run_time=1))
        # Animate beam tilting slightly (rotate about its center)
        beam = self.objects["scale_beam"]
        self.play(Rotate(beam, angle=-0.1 * PI, about_point=beam.get_center()), run_time=0.5)
        self.play(FadeOut(self.objects["box2"]), FadeOut(self.objects["three_circles"]), run_time=1.0)
        self.play(Rotate(beam, angle=0.1 * PI, about_point=beam.get_center()), run_time=0.5)
        remaining_5 = max(0.1, 3.0 - (1 + 0.5 + 1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/To_visualize_the_equ_32e762e472/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/solving_2x_equals_6_with_a_balance_scale/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["box1"], color=BLUE, run_time=1))
        self.play(ReplacementTransform(self.objects["equation"], self.objects["final_eq"]),
                  ReplacementTransform(self.objects["step4_text"], self.objects["step6_text"]), run_time=1.5)
        remaining_6 = max(0.1, 4.0 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_6))