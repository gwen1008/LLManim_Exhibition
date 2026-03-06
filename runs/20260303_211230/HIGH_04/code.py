'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y=0.5x² as the slope of the tangent line, showing the rule y' = x.
# 2. Layout Strategy: Use High-Low split.
#    - Header Region: [y=3.0] for Title and Step Label.
#    - Main Content: [Center y=0] for Axes, Graph, Tangent, Dot.
#    - Footer Region: [Bottom y=-3.0] for Derivative Rule and Explanation.
# 3. Anti-Overlap Check:
#    - Title and Step Label are stacked vertically in header.
#    - Graph is centered, leaving space for slope label.
#    - Footer content is stacked vertically.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/tangent_to_parabola/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-3: Setup axes, graph, label.
#    - Step 4-5: Introduce derivative rule.
#    - Step 6-8: Show static tangent at x=2.
#    - Step 9-10: Animate point moving, updating tangent and slope.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        header_anchor = 3.0 * UP
        content_anchor = ORIGIN
        footer_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Tangent to a Parabola: y = 0.5x²", color=WHITE, font_size=36)
        title.move_to(header_anchor)
        self.objects["title"] = title

        # step_label
        step_label = Text("Step 1: The Function", color=GRAY, font_size=24)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        axes.move_to(content_anchor)
        self.objects["axes"] = axes

        # graph
        graph = axes.plot(lambda x: 0.5 * x**2, x_range=[-4, 4], color=BLUE)
        self.objects["graph"] = graph

        # func_label
        func_label = MathTex(r"y = 0.5x^2", color=BLUE)
        func_label.next_to(graph, UP, buff=0.2)
        func_label.align_to(axes.get_left(), LEFT)
        func_label.shift(RIGHT * 2)
        self.objects["func_label"] = func_label

        # derivative_rule
        derivative_rule = MathTex(r"y' = \frac{dy}{dx} = x", color=GREEN, font_size=36)
        derivative_rule.move_to(footer_anchor)
        self.objects["derivative_rule"] = derivative_rule

        # rule_explanation
        rule_explanation = Text("The slope of the tangent line equals the x-coordinate.", color=GRAY, font_size=24)
        rule_explanation.next_to(derivative_rule, DOWN, buff=0.3)
        self.objects["rule_explanation"] = rule_explanation

        # dot_t (initial static position at x=2, y=2)
        dot_t = Dot(axes.c2p(2, 2), color=RED, radius=0.08)
        self.objects["dot_t"] = dot_t

        # tan_line (initial static line, will be replaced by dynamic one)
        tan_line = Line(start=axes.c2p(0, 0), end=axes.c2p(4, 0), color=YELLOW, stroke_width=3)
        self.objects["tan_line"] = tan_line

        # slope_label (DecimalNumber)
        slope_label = DecimalNumber(2.00, num_decimal_places=2, color=YELLOW)
        # Position will be set by always_redraw later
        self.objects["slope_label"] = slope_label

        # slope_text
        slope_text = Text("Slope:", color=YELLOW, font_size=24)
        # Position will be set by always_redraw later
        self.objects["slope_text"] = slope_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/tangent_to_parabola/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/tangent_to_parabola/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["graph"], color=BLUE, run_time=1))
        self.play(Create(self.objects["graph"]), run_time=3.0)
        remaining_2 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/tangent_to_parabola/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Write(self.objects["func_label"]), run_time=1.5)
        remaining_3 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/tangent_to_parabola/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["derivative_rule"], color=GREEN, run_time=1))
        self.play(Write(self.objects["derivative_rule"]), run_time=4.0)
        remaining_4 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/tangent_to_parabola/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Write(self.objects["rule_explanation"]), run_time=3.0)
        remaining_5 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/tangent_to_parabola/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["dot_t"], color=RED, run_time=1))
        self.play(Create(self.objects["dot_t"]), run_time=3.0)
        remaining_6 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/tangent_to_parabola/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["derivative_rule"], color=GREEN, run_time=1))
        # Create a tangent line at x=2 (slope = 2)
        point = self.objects["axes"].c2p(2, 2)
        tan_line_static = Line(
            start=point - 2 * RIGHT,
            end=point + 2 * RIGHT,
            color=YELLOW,
            stroke_width=3
        )
        self.play(Create(tan_line_static), run_time=3.0)
        remaining_7 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/tangent_to_parabola/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Create slope label and text
        slope_label_static = DecimalNumber(2.00, num_decimal_places=2, color=YELLOW)
        slope_text_static = Text("Slope:", color=YELLOW, font_size=24)
        slope_label_static.next_to(tan_line_static.get_end(), UP + RIGHT, buff=0.1)
        slope_text_static.next_to(slope_label_static, LEFT, buff=0.2)
        self.play(Indicate(slope_label_static, color=YELLOW, run_time=1))
        self.play(Write(slope_text_static), Write(slope_label_static), run_time=2.5)
        remaining_8 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_08.mp3")  # [auto-injected]
        # Step 9: Setup dynamic animation
        audio_step9 = "media/audio/tangent_to_parabola/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))

        # Remove static tangent and labels
        self.remove(tan_line_static, slope_label_static, slope_text_static)

        # Create ValueTracker for x-coordinate
        x_tracker = ValueTracker(2.0)

        # Dynamic dot
        dot_dynamic = always_redraw(
            lambda: Dot(
                self.objects["axes"].c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2),
                color=RED,
                radius=0.08
            )
        )
        self.add(dot_dynamic)

        # Dynamic tangent line (segment length 4 units centered at point)
        tan_line_dynamic = always_redraw(
            lambda: Line(
                start=self.objects["axes"].c2p(
                    x_tracker.get_value() - 1,
                    0.5 * x_tracker.get_value()**2 - x_tracker.get_value()
                ),
                end=self.objects["axes"].c2p(
                    x_tracker.get_value() + 1,
                    0.5 * x_tracker.get_value()**2 + x_tracker.get_value()
                ),
                color=YELLOW,
                stroke_width=3
            )
        )
        self.add(tan_line_dynamic)

        # Dynamic slope label
        slope_label_dynamic = always_redraw(
            lambda: DecimalNumber(
                x_tracker.get_value(),
                num_decimal_places=2,
                color=YELLOW
            ).next_to(tan_line_dynamic.get_end(), UP + RIGHT, buff=0.1)
        )
        self.add(slope_label_dynamic)

        # Dynamic slope text
        slope_text_dynamic = always_redraw(
            lambda: Text("Slope:", color=YELLOW, font_size=24
            ).next_to(slope_label_dynamic, LEFT, buff=0.2)
        )
        self.add(slope_text_dynamic)

        # Update step label
        new_step_label = Text("Step 9: Dynamic Tangent", color=GRAY, font_size=24)
        new_step_label.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(Transform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label

        # Animate x_tracker from 2 to -2 and back to 2
        self.play(
            x_tracker.animate.set_value(-2),
            run_time=5,
            rate_func=linear
        )
        self.play(
            x_tracker.animate.set_value(2),
            run_time=5,
            rate_func=linear
        )
        # Wait for remaining audio
        remaining_9 = max(0.1, 10.0 - 10.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Create_a_graph_of_th_75f1d461f9/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/tangent_to_parabola/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["derivative_rule"], color=GREEN, run_time=1))
        # Hold final frame
        remaining_10 = max(0.1, 5.0 - 0.0 + 0.5)
        self.wait(max(0.1, remaining_10))