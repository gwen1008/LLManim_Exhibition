from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors based on layout_plan
        title_anchor = 3.5 * UP
        circle_panel_center = 3 * LEFT
        graph_panel_center = 3 * RIGHT
        parameter_display_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = Text("Sine Function from the Unit Circle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle_axes
        circle_axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": False}
        )
        circle_axes.move_to(circle_panel_center)
        self.objects["circle_axes"] = circle_axes

        # unit_circle
        unit_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        unit_circle.move_to(circle_panel_center)
        self.objects["unit_circle"] = unit_circle

        # circle_dot
        circle_dot = Dot(radius=0.08, color=TEAL)
        circle_dot.move_to(circle_panel_center + 2 * RIGHT)
        self.objects["circle_dot"] = circle_dot

        # graph_axes
        graph_axes = Axes(
            x_range=[0, 6.283, 1.5708],
            y_range=[-1.2, 1.2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True}
        )
        graph_axes.move_to(graph_panel_center)
        self.objects["graph_axes"] = graph_axes

        # sine_curve_static
        sine_curve_static = graph_axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2 * PI],
            color=GREY,
            stroke_width=1
        )
        sine_curve_static.set_stroke(opacity=0.5)
        sine_curve_static.move_to(graph_panel_center)
        self.objects["sine_curve_static"] = sine_curve_static

        # sine_curve_dynamic (starts empty)
        sine_curve_dynamic = VMobject(stroke_color=TEAL, stroke_width=4)
        sine_curve_dynamic.move_to(graph_panel_center)
        self.objects["sine_curve_dynamic"] = sine_curve_dynamic

        # graph_dot
        graph_dot = Dot(radius=0.06, color=TEAL)
        graph_dot.move_to(graph_panel_center)
        self.objects["graph_dot"] = graph_dot

        # parameter_text
        parameter_text = MathTex(
            "t = 0.00,\\quad P = (\\cos t,\\ \\sin t) = (1.00,\\ 0.00)",
            font_size=30
        )
        parameter_text.move_to(parameter_display_anchor)
        self.objects["parameter_text"] = parameter_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        step = {
            "step": 1,
            "duration": 8.76,
            "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_00.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Create(self.objects["circle_axes"]))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Create", "target": "unit_circle", "color": "YELLOW"},
            "duration": 8.712,
            "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_01.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else WHITE
            target_obj.set_color(color)
            self.play(Create(target_obj))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "duration": 6.216,
            "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_02.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Create(self.objects["graph_axes"]))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "FadeIn", "target": "sine_curve_static", "color": None},
            "duration": 8.808,
            "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_03.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            self.play(FadeIn(target_obj))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "circle_dot", "color": "TEAL"},
            "duration": 9.888,
            "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_04.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])

        # Setup for synchronized animation
        theta = ValueTracker(0)

        # Update circle_dot position
        circle_dot.add_updater(
            lambda m: m.move_to(
                circle_panel_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0])
            )
        )

        # Update graph_dot position
        graph_dot.add_updater(
            lambda m: m.move_to(
                graph_axes.c2p(theta.get_value(), np.sin(theta.get_value()))
            )
        )

        # Build sine_curve_dynamic using a TracedPath (simpler than manual VMobject)
        # We'll create a new traced path that follows graph_dot
        trace = TracedPath(graph_dot.get_center, stroke_color=TEAL, stroke_width=4)
        self.add(trace)

        # Update parameter_text
        def update_parameter_text(m):
            t_val = theta.get_value()
            cos_t = np.cos(t_val)
            sin_t = np.sin(t_val)
            new_text = MathTex(
                f"t = {t_val:.2f},\\quad P = (\\cos t,\\ \\sin t) = ({cos_t:.2f},\\ {sin_t:.2f})",
                font_size=30
            )
            new_text.move_to(parameter_display_anchor)
            m.become(new_text)

        parameter_text.add_updater(update_parameter_text)

        # Add all objects that will be animated
        self.add(
            self.objects["title"],
            self.objects["circle_axes"],
            self.objects["unit_circle"],
            self.objects["circle_dot"],
            self.objects["graph_axes"],
            self.objects["sine_curve_static"],
            self.objects["graph_dot"],
            self.objects["parameter_text"]
        )

        # Execute signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = TEAL if signal.get("color") == "TEAL" else YELLOW
            self.play(Indicate(target_obj, color=color))

        # Start the main synchronized animation
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=8,
            rate_func=linear
        )

        # Remove updaters
        circle_dot.clear_updaters()
        graph_dot.clear_updaters()
        parameter_text.clear_updaters()

        # Final wait
        animation_time = 8.0 + 1.0  # main animation + indicate
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))