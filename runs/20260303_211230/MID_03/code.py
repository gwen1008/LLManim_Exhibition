'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize solving the equation 2x = 6 using a concrete balance scale metaphor, demonstrating the division property of equality.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title/Equation
#    - Main Content: [Center y=0] for Balance Scale
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - The scale is centered at ORIGIN. Pans are at y=-1.5. Boxes and circles are placed on pans.
#    - Title at top, explanation at bottom. No overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/balance_scale_equation/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show equation.
#    - Step 2: Build scale and left boxes.
#    - Step 3: Add right circles.
#    - Step 4: Explain division.
#    - Step 5: Remove half from each side (animate removal and scale tilt).
#    - Step 6: Show result "one x equals three".
#    - Step 7: Update equation to x=3.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_visualize_the_equ_bad34d7636/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        title_anchor = 3.5 * UP
        scale_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title_eq_initial
        title_eq_initial = MathTex("2x = 6", color=WHITE, font_size=48)
        title_eq_initial.move_to(title_anchor)
        self.objects["title_eq_initial"] = title_eq_initial

        # scale_beam
        scale_beam = Line(start=LEFT*3, end=RIGHT*3, color=WHITE, stroke_width=6)
        scale_beam.move_to(scale_anchor)
        self.objects["scale_beam"] = scale_beam

        # scale_pivot
        scale_pivot = Circle(radius=0.15, color=GREY, fill_opacity=1.0)
        scale_pivot.move_to(scale_anchor)
        self.objects["scale_pivot"] = scale_pivot

        # left_string
        left_string = Line(start=LEFT*3, end=LEFT*3 + DOWN*1.5, color=GRAY_C)
        self.objects["left_string"] = left_string

        # right_string
        right_string = Line(start=RIGHT*3, end=RIGHT*3 + DOWN*1.5, color=GRAY_C)
        self.objects["right_string"] = right_string

        # left_pan
        left_pan = Rectangle(width=1.2, height=0.2, color=GRAY_B, fill_opacity=0.8)
        left_pan.move_to(LEFT*3 + DOWN*1.5)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Rectangle(width=1.2, height=0.2, color=GRAY_B, fill_opacity=0.8)
        right_pan.move_to(RIGHT*3 + DOWN*1.5)
        self.objects["right_pan"] = right_pan

        # box1 and box2 (position relative to left_pan)
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box1.move_to(left_pan.get_center() + UP*0.4)
        self.objects["box1"] = box1

        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box2.move_to(left_pan.get_center() + DOWN*0.4)
        self.objects["box2"] = box2

        # circles_group (6 circles arranged in 2x3 grid)
        circles = VGroup(*[Circle(radius=0.3, color=GREEN, fill_opacity=0.7) for _ in range(6)])
        circles.arrange_in_grid(rows=2, cols=3, buff=0.2)
        circles.move_to(right_pan.get_center())
        self.objects["circles_group"] = circles
        # Also store individual circles for easy access in step 5
        for i, circle in enumerate(circles):
            self.objects[f"circles_group[{i}]"] = circle

        # step_explanation (placeholder, content set in sequence)
        step_explanation = Text("", color=WHITE, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/balance_scale_equation/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Signal action: Indicate title_eq_initial
        self.play(Indicate(self.objects["title_eq_initial"], color=YELLOW, run_time=1))
        # Visual action: Create title_eq_initial
        self.play(Write(self.objects["title_eq_initial"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/balance_scale_equation/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # No signal action
        # Visual action: Create scale structure and boxes
        scale_parts = VGroup(
            self.objects["scale_beam"],
            self.objects["scale_pivot"],
            self.objects["left_string"],
            self.objects["right_string"],
            self.objects["left_pan"],
            self.objects["right_pan"]
        )
        self.play(Create(scale_parts), run_time=2.0)
        self.play(Create(self.objects["box1"]), Create(self.objects["box2"]), run_time=2.0)
        remaining_2 = max(0.1, 4.0 - (2.0 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/balance_scale_equation/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # No signal action
        # Visual action: Create circles_group
        self.play(Create(self.objects["circles_group"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/balance_scale_equation/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Circumscribe title_eq_initial
        self.play(Circumscribe(self.objects["title_eq_initial"], color=YELLOW, run_time=1))
        # Visual action: Write step_explanation with new content
        new_text = Text("Divide both sides by 2.", color=WHITE, font_size=28)
        new_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_text), run_time=1.5)
        self.objects["step_explanation"] = new_text
        remaining_4 = max(0.1, 3.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/balance_scale_equation/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate box2
        self.play(Indicate(self.objects["box2"], color=RED, run_time=1))
        # Visual action: FadeOut box2 and last three circles, animate scale tilt
        fade_outs = [
            FadeOut(self.objects["box2"]),
            FadeOut(self.objects["circles_group[3]"]),
            FadeOut(self.objects["circles_group[4]"]),
            FadeOut(self.objects["circles_group[5]"])
        ]
        # Tilt animation: rotate beam slightly clockwise then back
        beam = self.objects["scale_beam"]
        pivot = self.objects["scale_pivot"]
        left_string = self.objects["left_string"]
        right_string = self.objects["right_string"]
        left_pan = self.objects["left_pan"]
        right_pan = self.objects["right_pan"]
        box1 = self.objects["box1"]
        remaining_circles = VGroup(self.objects["circles_group[0]"], self.objects["circles_group[1]"], self.objects["circles_group[2]"])

        # Group scale parts for rotation
        scale_group = VGroup(beam, pivot, left_string, right_string, left_pan, right_pan, box1, remaining_circles)
        tilt_angle = 5 * DEGREES  # small clockwise tilt

        self.play(
            *fade_outs,
            scale_group.animate.rotate(-tilt_angle, about_point=scale_anchor),
            run_time=1.5
        )
        self.play(
            scale_group.animate.rotate(tilt_angle, about_point=scale_anchor),
            run_time=1.5
        )
        remaining_5 = max(0.1, 4.0 - (1 + 1.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/balance_scale_equation/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Indicate box1
        self.play(Indicate(self.objects["box1"], color=YELLOW, run_time=1))
        # Visual action: Update step_explanation
        new_text2 = Text("One x equals three.", color=WHITE, font_size=28)
        new_text2.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_text2), run_time=1.5)
        self.objects["step_explanation"] = new_text2
        remaining_6 = max(0.1, 3.0 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/balance_scale_equation/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # No signal action
        # Visual action: TransformMatchingTex title_eq_initial to "x = 3"
        new_eq = MathTex("x = 3", color=WHITE, font_size=48)
        new_eq.move_to(title_anchor)
        self.play(TransformMatchingTex(self.objects["title_eq_initial"], new_eq), run_time=2.0)
        self.objects["title_eq_initial"] = new_eq
        remaining_7 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Final hold
        self.wait(max(0.1, 2))