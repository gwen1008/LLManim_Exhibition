from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout zones
        title_anchor = 3.5 * UP
        circle_anchor = 4 * LEFT  # Left of center
        unfolded_line_anchor = 4 * RIGHT  # Right of center
        comparison_anchor = unfolded_line_anchor + 2 * DOWN  # Below the C line
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Unfolding a Circle's Circumference", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(circle_anchor + 2 * LEFT, circle_anchor + 2 * RIGHT, color=YELLOW, stroke_width=6)
        self.objects["diameter_line"] = diameter_line

        # label_D
        label_D = MathTex("D", color=YELLOW)
        label_D.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_D"] = label_D

        # dashed_circumference
        base_circle = Circle(radius=2, color=GREEN, stroke_width=4)
        dashed_circumference = DashedVMobject(base_circle, num_dashes=50, color=GREEN)
        dashed_circumference.move_to(circle_anchor)
        self.objects["dashed_circumference"] = dashed_circumference

        # unfolded_line
        unfolded_line = Line(unfolded_line_anchor + PI * 2 * LEFT, unfolded_line_anchor + PI * 2 * RIGHT, color=GREEN, stroke_width=6)
        unfolded_line.set_opacity(0)  # Start invisible
        self.objects["unfolded_line"] = unfolded_line

        # label_C
        label_C = MathTex("C", color=GREEN)
        label_C.next_to(unfolded_line, UP, buff=0.2)
        self.objects["label_C"] = label_C

        # comparison_line_3D
        comparison_line_3D = Line(comparison_anchor, comparison_anchor + 12 * RIGHT, color=RED, stroke_width=6)
        self.objects["comparison_line_3D"] = comparison_line_3D

        # label_3D
        label_3D = MathTex("3D", color=RED)
        label_3D.next_to(comparison_line_3D, DOWN, buff=0.2)
        self.objects["label_3D"] = label_3D

        # formula_text
        formula_text = MathTex(r"C = \pi D \quad > \quad 3D", color=WHITE, font_size=36)
        formula_text.move_to(explanation_anchor)
        self.objects["formula_text"] = formula_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/unfolding_circle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/unfolding_circle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["diameter_line"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/unfolding_circle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: Write label_D
        self.play(Write(self.objects["label_D"]), run_time=1.0)
        remaining_3 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/unfolding_circle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Create(self.objects["dashed_circumference"]), run_time=2.0)
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/unfolding_circle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: Indicate dashed_circumference
        self.play(Indicate(self.objects["dashed_circumference"], color=GREEN, run_time=1))
        # Custom unfold animation: rotate and translate
        start_center = circle_anchor
        end_center = unfolded_line_anchor
        r = 2
        # We'll animate the dashed_circumference moving and rotating
        self.play(
            self.objects["dashed_circumference"].animate.move_to(end_center).rotate(-PI/2, about_point=end_center).stretch_to_fit_width(TAU * r),
            run_time=3.0
        )
        remaining_5 = max(0.1, 4.0 - 1 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/unfolding_circle/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Make unfolded_line visible and replace
        self.objects["unfolded_line"].set_opacity(1)
        self.play(
            ReplacementTransform(self.objects["dashed_circumference"], self.objects["unfolded_line"]),
            run_time=1.5
        )
        remaining_6 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/unfolding_circle/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # signal_action: Write label_C
        self.play(Write(self.objects["label_C"]), run_time=1.0)
        remaining_7 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/unfolding_circle/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # signal_action: Indicate diameter_line
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["comparison_line_3D"]), run_time=1.5)
        remaining_8 = max(0.1, 2.5 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/unfolding_circle/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # signal_action: Write label_3D
        self.play(Write(self.objects["label_3D"]), run_time=1.0)
        remaining_9 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/unfolding_circle/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # signal_action: Indicate unfolded_line
        self.play(Indicate(self.objects["unfolded_line"], color=GREEN, run_time=1))
        # Visual_action: Indicate comparison_line_3D
        self.play(Indicate(self.objects["comparison_line_3D"], color=RED, run_time=1))
        # Highlight the gap
        gap_start = self.objects["comparison_line_3D"].get_end()
        gap_end = self.objects["unfolded_line"].get_end()
        gap_line = Line(gap_start, gap_end, color=YELLOW, stroke_width=8)
        self.play(Create(gap_line), run_time=1.0)
        self.play(FadeOut(gap_line), run_time=0.5)
        remaining_10 = max(0.1, 3.0 - 1 - 1 - 1.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_10.mp3")  # [auto-injected]
        # Step 11
        audio_step11 = "media/audio/unfolding_circle/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        self.play(Write(self.objects["formula_text"]), run_time=2.0)
        remaining_11 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_11))

        self.add_sound("media/audio/The_animation_begins_96a2e6efe2/step_11.mp3")  # [auto-injected]
        # Step 12
        audio_step12 = "media/audio/unfolding_circle/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        # signal_action: Circumscribe formula_text
        self.play(Circumscribe(self.objects["formula_text"], color=YELLOW, run_time=1))
        remaining_12 = max(0.1, 3.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_12))