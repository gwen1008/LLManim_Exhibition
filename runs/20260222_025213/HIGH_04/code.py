'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative relationship: d/dx (0.5x^2) = x, by showing a point moving along the parabola and its dynamically updating tangent line whose slope equals the point's x-coordinate.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title (function definition)
#    - Main Content: [Center y=0] for axes and parabola
#    - Footer Region: [Bottom y=-3.5] for slope display and explanation
# 3. Anti-Overlap Check:
#    - Strategy: Use ValueTracker and always_redraw for dynamic objects (point, tangent, slope value) to keep them synchronized and prevent drift.
#    - Keep static labels (title, explanation) in their zones.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-3: Introduce function, axes, parabola.
#    - Step 4-5: Introduce moving point and tangent line concept.
#    - Step 6-7: Show dynamic slope display and animate point movement.
#    - Step 8: Display key takeaway.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = MathTex("y = 0.5x^2", color=BLUE).scale(1.2)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE}
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes

        # parabola (as a graph, not ParametricFunction for simplicity)
        parabola = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=3)
        self.objects["parabola"] = parabola

        # ValueTracker for the x-coordinate of the point of tangency
        a_tracker = ValueTracker(0)
        self.objects["a_tracker"] = a_tracker

        # point_P - will be updated via always_redraw
        point_P = always_redraw(
            lambda: Dot(
                axes.c2p(a_tracker.get_value(), 0.5 * a_tracker.get_value()**2),
                radius=0.08,
                color=WHITE
            )
        )
        self.objects["point_P"] = point_P

        # tangent_line - will be updated via always_redraw
        # For y = 0.5x^2, derivative is x. Tangent line at x=a: y = a*(x - a) + 0.5*a^2 = a*x - 0.5*a^2
        # We want a line of constant visual length (4 units wide in x).
        tangent_line = always_redraw(
            lambda: Line(
                start=axes.c2p(a_tracker.get_value() - 2, a_tracker.get_value() * (a_tracker.get_value() - 2) - 0.5 * a_tracker.get_value()**2),
                end=axes.c2p(a_tracker.get_value() + 2, a_tracker.get_value() * (a_tracker.get_value() + 2) - 0.5 * a_tracker.get_value()**2),
                color=YELLOW,
                stroke_width=3
            )
        )
        self.objects["tangent_line"] = tangent_line

        # slope_text
        slope_text = Text("Slope, m = ", color=WHITE, font_size=36).scale(0.9)
        slope_text.move_to(footer_anchor + UP * 0.5)
        self.objects["slope_text"] = slope_text

        # slope_value (DecimalNumber)
        slope_value = DecimalNumber(
            0,
            num_decimal_places=2,
            color=GREEN,
            font_size=36
        )
        slope_value.next_to(slope_text, RIGHT, buff=0.2)
        # Add updater to track the slope (which equals a)
        slope_value.add_updater(lambda d: d.set_value(a_tracker.get_value()))
        self.objects["slope_value"] = slope_value

        # slope_label VGroup
        slope_label = VGroup(slope_text, slope_value)
        self.objects["slope_label"] = slope_label

        # explanation
        explanation = Text(
            "The slope of the tangent line equals the x-coordinate of the point.",
            color=GRAY_B,
            font_size=28
        ).scale(0.7)
        explanation.next_to(slope_label, DOWN, buff=0.5)
        self.objects["explanation"] = explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "narrative": "Let's graph the quadratic function y equals one-half x squared.",
            "signal_action": {
                "type": "Indicate",
                "target": "title",
                "color": "BLUE"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "title",
                "details": "Write the function title."
            },
            "duration": 4.56,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
        }
        # Audio
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Write(self.objects["title"]))
        animation_time = 1.0  # Approximate run_time for Write
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "narrative": "We draw the coordinate axes and plot the parabola.",
            "signal_action": None,
            "visual_action": {
                "type": "Create",
                "target_id": "axes",
                "details": "Draw the x and y axes."
            },
            "duration": 3.624,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["axes"]))
        animation_time = 1.5
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "narrative": "The curve is a parabola, opening upwards.",
            "signal_action": {
                "type": "Indicate",
                "target": "parabola",
                "color": "BLUE"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "parabola",
                "details": "Draw the parabola smoothly."
            },
            "duration": 3.432,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["parabola"]))
        animation_time = 2.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "narrative": "Now, consider a point P moving along this curve. At any location, we can draw a line that just touches the curve at that single point—the tangent line.",
            "signal_action": {
                "type": "Indicate",
                "target": "point_P",
                "color": "WHITE"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "point_P",
                "details": "Show the point of tangency."
            },
            "duration": 10.224,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Add the point_P (which is an always_redraw) to the scene
        self.add(self.objects["point_P"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        animation_time = 1.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "narrative": "The slope of this tangent line is the instantaneous rate of change of the function. For our parabola, the derivative is x, so the slope equals the x-coordinate of point P.",
            "signal_action": {
                "type": "Circumscribe",
                "target": "tangent_line",
                "color": "YELLOW"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "tanglet_line",
                "details": "Draw the tangent line at the initial point (x=0)."
            },
            "duration": 11.28,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Add the tangent_line (always_redraw) to the scene
        self.add(self.objects["tangent_line"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        animation_time = 1.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "narrative": "Let's display the slope value. As P moves, the slope updates in real time.",
            "signal_action": {
                "type": "Indicate",
                "target": "slope_label",
                "color": "GREEN"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "slope_text",
                "details": "Write 'Slope, m = '."
            },
            "duration": 6.264,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Visual Action: Write slope_text (the static part)
        self.play(Write(self.objects["slope_text"]))
        # Also add the slope_value (DecimalNumber) which is already in the VGroup
        self.add(self.objects["slope_value"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        animation_time = 1.5
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        step = {
            "step": 7,
            "narrative": "Now, watch as the point moves. The tangent line transforms, and its slope—shown here—changes linearly with the x-coordinate.",
            "signal_action": None,
            "visual_action": {
                "type": "Create",
                "target_id": "slope_value",
                "details": "Write the initial slope value (0). Then, activate the animation of the point moving from x=-3 to x=3 and back, with the tangent line and slope value updating continuously."
            },
            "duration": 9.552,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_06.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # The slope_value is already added and updating via updater.
        # Animate the ValueTracker to move the point.
        # Move from -3 to 3 and back to -3 to create a complete cycle.
        run_time_per_leg = (step["duration"] - 0.5) / 2  # Split duration for two legs
        self.play(a_tracker.animate.set_value(3), run_time=run_time_per_leg, rate_func=linear)
        self.play(a_tracker.animate.set_value(-3), run_time=run_time_per_leg, rate_func=linear)
        # No extra wait needed as animation fills the duration.

        # Step 8
        step = {
            "step": 8,
            "narrative": "This demonstrates the fundamental concept: the derivative of 0.5x^2 is x, meaning the slope of the tangent at any point is precisely its x-coordinate.",
            "signal_action": {
                "type": "Indicate",
                "target": "explanation",
                "color": "LIGHT_GRAY"
            },
            "visual_action": {
                "type": "Write",
                "target_id": "explanation",
                "details": "Display the key takeaway text."
            },
            "duration": 10.176,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_07.mp3"
        }
        audio_file = step.get("audio_path")
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Visual Action
        self.play(Write(self.objects["explanation"]))
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        animation_time = 2.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))