from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors (from layout_plan.anchors)
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Derivative as Slope of a Tangent Line", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # step_label
        step_label = Text("Step 1: The Function", color=YELLOW, font_size=24)
        step_label.next_to(title_text, DOWN, buff=0.8)
        self.objects["step_label"] = step_label

        # axes
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes

        # graph_curve
        graph_curve = axes.plot(lambda x: 0.5 * x**2, color=BLUE)
        self.objects["graph_curve"] = graph_curve

        # func_label
        func_label = MathTex(r"y = 0.5x^2", color=BLUE)
        func_label.next_to(graph_curve, UP + RIGHT, buff=0.2)
        self.objects["func_label"] = func_label

        # moving_dot (initial position at x = -2.5)
        moving_dot = Dot(radius=0.08, color=RED)
        moving_dot.move_to(axes.c2p(-2.5, 0.5 * (-2.5)**2))
        self.objects["moving_dot"] = moving_dot

        # dot_label_p
        dot_label_p = MathTex(r"P", color=RED, font_size=24)
        dot_label_p.next_to(moving_dot, UP, buff=0.4)
        self.objects["dot_label_p"] = dot_label_p

        # tangent_line (initial dummy line, will be updated)
        tangent_line = Line(start=[-1, -1, 0], end=[1, 1, 0], color=GREEN, stroke_width=4)
        tangent_line.move_to(content_center)
        self.objects["tangent_line"] = tangent_line

        # footer_explanation
        footer_explanation = Text("The graph of the quadratic function.", color=GRAY_B, font_size=22)
        footer_explanation.move_to(footer_anchor)
        self.objects["footer_explanation"] = footer_explanation

        # slope_value_text (initial)
        slope_value_text = MathTex(r"m = ", color=GREEN, font_size=32)
        slope_value_text.next_to(footer_explanation, DOWN, buff=0.4)
        self.objects["slope_value_text"] = slope_value_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title_text"]), run_time=1.5)
        remaining_1 = max(0.1, 6.384 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Write(self.objects["step_label"]), run_time=0.8)
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_2 = max(0.1, 3.456 - (0.8 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Create(self.objects["graph_curve"]), run_time=2.0)
        remaining_3 = max(0.1, 3.264 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Write(self.objects["func_label"]), run_time=1.0)
        remaining_4 = max(0.1, 2.4 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        step_label_new_5 = Text("Step 2: The Derivative", color=YELLOW, font_size=24)
        step_label_new_5.move_to(self.objects["step_label"].get_center())
        footer_explanation_new_5 = Text("Derivative: dy/dx = x. This gives the slope at any point.", color=GRAY_B, font_size=22)
        footer_explanation_new_5.move_to(self.objects["footer_explanation"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new_5))
        self.objects["step_label"] = step_label_new_5
        self.play(ReplacementTransform(self.objects["footer_explanation"], footer_explanation_new_5))
        self.objects["footer_explanation"] = footer_explanation_new_5
        remaining_5 = max(0.1, 8.784 - (1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        step_label_new_6 = Text("Step 3: Tangent at a Point", color=YELLOW, font_size=24)
        step_label_new_6.move_to(self.objects["step_label"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new_6))
        self.objects["step_label"] = step_label_new_6
        self.play(Create(self.objects["moving_dot"]), run_time=1.5)
        remaining_6 = max(0.1, 8.352 - (1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Write(self.objects["dot_label_p"]), run_time=1.0)
        remaining_7 = max(0.1, 9.408 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Create the tangent line with correct initial slope at x = -2.5
        x0 = -2.5
        y0 = 0.5 * x0**2
        slope = x0  # derivative
        # Create a line segment centered at (x0, y0) with given slope
        line_length = 3.0
        start_point = self.objects["axes"].c2p(x0 - line_length/2, y0 + slope * (-line_length/2))
        end_point = self.objects["axes"].c2p(x0 + line_length/2, y0 + slope * (line_length/2))
        tangent_line_initial = Line(start=start_point, end=end_point, color=GREEN, stroke_width=4)
        self.play(Create(tangent_line_initial), run_time=1.5)
        self.objects["tangent_line"] = tangent_line_initial
        remaining_8 = max(0.1, 5.928 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        slope_value_text_new_9 = MathTex(r"m = -2.5", color=GREEN, font_size=32)
        slope_value_text_new_9.move_to(self.objects["slope_value_text"].get_center())
        self.play(Indicate(self.objects["slope_value_text"], color=YELLOW, run_time=1))
        self.play(TransformMatchingTex(self.objects["slope_value_text"], slope_value_text_new_9))
        self.objects["slope_value_text"] = slope_value_text_new_9
        remaining_9 = max(0.1, 6.36 - (1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        audio_step10 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        step_label_new_10 = Text("Step 4: The Moving Tangent", color=YELLOW, font_size=24)
        step_label_new_10.move_to(self.objects["step_label"].get_center())
        footer_explanation_new_10 = Text("The tangent line transforms. Its slope m updates live: m = x-coordinate of P.", color=GRAY_B, font_size=22)
        footer_explanation_new_10.move_to(self.objects["footer_explanation"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new_10))
        self.objects["step_label"] = step_label_new_10
        self.play(ReplacementTransform(self.objects["footer_explanation"], footer_explanation_new_10))
        self.objects["footer_explanation"] = footer_explanation_new_10
        remaining_10 = max(0.1, 12.36 - (1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_10))

        # Step 11
        audio_step11 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))

        # Prepare for dynamic movement: ValueTracker for x-coordinate
        x_tracker = ValueTracker(-2.5)

        # Updater for moving_dot
        def update_dot(mob):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            mob.move_to(self.objects["axes"].c2p(x, y))
        self.objects["moving_dot"].add_updater(update_dot)

        # Updater for dot_label_p (keep it next to the dot)
        def update_label(mob):
            mob.next_to(self.objects["moving_dot"], UP, buff=0.4)
        self.objects["dot_label_p"].add_updater(update_label)

        # Updater for tangent_line
        def update_tangent(mob):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x
            line_length = 3.0
            start_point = self.objects["axes"].c2p(x - line_length/2, y + slope * (-line_length/2))
            end_point = self.objects["axes"].c2p(x + line_length/2, y + slope * (line_length/2))
            mob.become(Line(start=start_point, end=end_point, color=GREEN, stroke_width=4))
        self.objects["tangent_line"].add_updater(update_tangent)

        # Updater for slope_value_text
        def update_slope_text(mob):
            x = x_tracker.get_value()
            new_text = MathTex(f"m = {x:.2f}", color=GREEN, font_size=32)
            new_text.move_to(self.objects["slope_value_text"].get_center())
            mob.become(new_text)
        self.objects["slope_value_text"].add_updater(update_slope_text)

        # ApplyWave signal
        self.play(ApplyWave(self.objects["moving_dot"]), run_time=1.0)

        # Animate the x_tracker from -2.5 to 2.5 over 8 seconds
        self.play(x_tracker.animate.set_value(2.5), run_time=8.0, rate_func=linear)

        remaining_11 = max(0.1, 10.992 - (1.0 + 8.0) + 0.5)
        self.wait(max(0.1, remaining_11))

        # Step 12
        audio_step12 = "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["tangent_line"], color=YELLOW, run_time=1))
        remaining_12 = max(0.1, 12.528 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_12))