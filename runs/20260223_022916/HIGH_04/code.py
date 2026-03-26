from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        derivation_anchor = 4 * LEFT + 2.5 * UP

        # Create objects from layout_plan
        # title
        title = Text("Derivative as Slope: y = 0.5x²", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            axis_config={"include_numbers": True},
            color=GRAY_B
        ).scale(0.9).move_to(content_center)
        self.objects["axes"] = axes

        # graph (parabola)
        graph = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=4)
        self.objects["graph"] = graph

        # moving_dot (initial position at x = -3.5)
        moving_dot = Dot(radius=0.08, color=YELLOW)
        moving_dot.move_to(axes.c2p(-3.5, 0.5 * (-3.5)**2))
        self.objects["moving_dot"] = moving_dot

        # tangent_line (initial dummy line, will be updated via always_redraw)
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=3)
        self.objects["tangent_line"] = tangent_line

        # slope_label (initial text, will be updated via always_redraw)
        slope_label = MathTex("m = -3.50", color=GREEN, font_size=30)
        self.objects["slope_label"] = slope_label

        # step_explanation
        step_explanation = Text("Step 1: The function y = 0.5x²", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # derivation_tex
        derivation_tex = MathTex("y = 0.5x^2", color=WHITE).scale(0.8).move_to(derivation_anchor)
        self.objects["derivation_tex"] = derivation_tex

        # Create ValueTracker for x-coordinate
        t_tracker = ValueTracker(-3.5)

        # Define dynamic objects using always_redraw
        # moving_dot updater
        moving_dot.add_updater(lambda d: d.move_to(axes.c2p(t_tracker.get_value(), 0.5 * t_tracker.get_value()**2)))

        # tangent_line updater: line through point with slope = x (derivative)
        # Constrain endpoints to stay within x in [-7, 7] and y in [-3.5, 3.5]
        tangent_line = always_redraw(lambda: Line(
            start=axes.c2p(t_tracker.get_value() - 1.2, 0.5 * t_tracker.get_value()**2 - 1.2 * t_tracker.get_value()),
            end=axes.c2p(t_tracker.get_value() + 1.2, 0.5 * t_tracker.get_value()**2 + 1.2 * t_tracker.get_value()),
            color=RED,
            stroke_width=3
        ))
        self.objects["tangent_line"] = tangent_line

        # slope_label updater: text and position
        slope_label = always_redraw(lambda: MathTex(
            f"m = {t_tracker.get_value():.2f}",
            color=GREEN,
            font_size=30
        ).next_to(
            axes.c2p(t_tracker.get_value(), 0.5 * t_tracker.get_value()**2),
            UP+RIGHT,
            buff=0.15
        ))
        self.objects["slope_label"] = slope_label

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 5.04 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_2 = max(0.1, 3.48 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["graph"], color=BLUE, run_time=1))
        self.play(Create(self.objects["graph"]), run_time=1.5)
        remaining_3 = max(0.1, 2.208 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Write(self.objects["derivation_tex"]), run_time=2.0)
        remaining_4 = max(0.1, 11.352 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        derivation_tex2 = MathTex(r"y' = 0.5 \cdot 2x^{1}", color=WHITE).scale(0.8).move_to(derivation_anchor)
        derivation_tex3 = MathTex(r"y' = x", color=WHITE).scale(0.8).move_to(derivation_anchor)
        self.play(TransformMatchingTex(self.objects["derivation_tex"], derivation_tex2))
        self.wait(max(0.1, 0.5))
        self.play(TransformMatchingTex(derivation_tex2, derivation_tex3))
        self.objects["derivation_tex"] = derivation_tex3
        remaining_5 = max(0.1, 6.24 - 2.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["derivation_tex"], color=YELLOW, run_time=1))
        self.play(FadeOut(self.objects["derivation_tex"]), run_time=1.0)
        remaining_6 = max(0.1, 9.24 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["moving_dot"], color=YELLOW, run_time=1))
        self.add(self.objects["moving_dot"])
        self.play(Create(self.objects["moving_dot"]), run_time=1.5)
        remaining_7 = max(0.1, 9.864 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.add(self.objects["tangent_line"])
        self.play(Create(self.objects["tangent_line"]), run_time=2.0)
        remaining_8 = max(0.1, 10.008 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["slope_label"], color=GREEN, run_time=1))
        self.add(self.objects["slope_label"])
        self.play(Write(self.objects["slope_label"]), run_time=1.5)
        remaining_9 = max(0.1, 3.12 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        audio_step10 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(t_tracker.animate.set_value(3.5), run_time=8, rate_func=smooth)
        remaining_10 = max(0.1, 22.248 - 8.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final wait
        self.wait(max(0.1, 2))