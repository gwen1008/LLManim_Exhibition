'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the connection between circular motion on the unit circle and the sine wave graph.
# 2. Layout Strategy: Use LayoutEngine for a dual-panel layout with Title, Content, and Footer zones.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] split into left (circle) and right (sine graph) panels.
#    - Footer Region: [Bottom y=-3.5] for explanatory text.
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep Title, Content, and Footer separated. Left and right panels will be positioned relative to anchors.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using the provided audio_path.
#    - [x] Files: "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_XX.mp3"
# 5. Animation Flow: Setup title and axes, create the moving point and projection, animate the point around the circle while plotting the sine wave in real-time.
'''

from manim import *
import numpy as np
import os
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}  # Registry for objects referenced by ID

        # ========== PHASE 1: Layout & Object Creation ==========
        layout = LayoutEngine()

        # Create anchors as LayoutObjects with specific positions
        title_anchor_obj = LayoutObject(Dot(ORIGIN, radius=0), "title_anchor")
        layout.add(title_anchor_obj)
        layout.add_to_zone(title_anchor_obj, "HEADER")

        left_anchor_obj = LayoutObject(Dot(ORIGIN, radius=0), "left_anchor")
        layout.add(left_anchor_obj)
        layout.add_to_zone(left_anchor_obj, "CONTENT")
        layout.add_constraint(left_anchor_obj.center_x == -3.5)

        right_anchor_obj = LayoutObject(Dot(ORIGIN, radius=0), "right_anchor")
        layout.add(right_anchor_obj)
        layout.add_to_zone(right_anchor_obj, "CONTENT")
        layout.add_constraint(right_anchor_obj.center_x == 3.5)

        footer_anchor_obj = LayoutObject(Dot(ORIGIN, radius=0), "footer_anchor")
        layout.add(footer_anchor_obj)
        layout.add_to_zone(footer_anchor_obj, "FOOTER")

        layout.solve()  # Solve to get anchor positions
        title_anchor = title_anchor_obj.get_center()
        left_anchor = left_anchor_obj.get_center()
        right_anchor = right_anchor_obj.get_center()
        footer_anchor = footer_anchor_obj.get_center()

        # Create objects from layout_plan
        # title
        title = Text("Sine Wave from the Unit Circle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle_axes
        circle_axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True, "color": GREY},
            tips=False
        ).move_to(left_anchor)
        self.objects["circle_axes"] = circle_axes

        # unit_circle
        unit_circle = Circle(radius=2, color=BLUE, stroke_width=3).move_to(left_anchor)
        self.objects["unit_circle"] = unit_circle

        # circle_label
        circle_label = MathTex("x^2 + y^2 = 1", color=BLUE, font_size=30).next_to(unit_circle, UP, buff=0.2)
        self.objects["circle_label"] = circle_label

        # moving_dot - initial position at (2,0) relative to left_anchor
        moving_dot = Dot(radius=0.08, color=PINK).move_to(left_anchor + np.array([2, 0, 0]))
        self.objects["moving_dot"] = moving_dot

        # dot_label
        dot_label = MathTex(r"P(\cos(t), \sin(t))", color=PINK, font_size=24).next_to(moving_dot, UR, buff=0.1)
        self.objects["dot_label"] = dot_label

        # sine_axes
        sine_axes = Axes(
            x_range=[0, 2 * PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "color": GREY},
            tips=False
        ).move_to(right_anchor)
        self.objects["sine_axes"] = sine_axes

        # sine_axes_labels
        sine_axes_labels = VGroup(
            MathTex("t").next_to(sine_axes.x_axis, RIGHT),
            MathTex(r"\sin(t)").next_to(sine_axes.y_axis, UP)
        )
        self.objects["sine_axes_labels"] = sine_axes_labels

        # sine_wave_dots - initially empty VGroup
        sine_wave_dots = VGroup()
        sine_wave_dots.move_to(right_anchor)
        self.objects["sine_wave_dots"] = sine_wave_dots

        # projection_line - will be updated via always_redraw
        # Create a placeholder line, its updater will be set later
        projection_line = DashedLine(
            start=left_anchor,
            end=left_anchor,
            color=YELLOW,
            stroke_width=2,
            dash_length=0.05
        )
        self.objects["projection_line"] = projection_line

        # footer_text
        footer_text = Text(
            "The y-coordinate of the point on the circle is plotted against the angle t.",
            color=GRAY_B,
            font_size=24
        ).move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # ValueTracker for the angle parameter t
        t_tracker = ValueTracker(0)
        self.t_tracker = t_tracker

        # Updater for moving_dot position
        def update_moving_dot(mob):
            t = t_tracker.get_value()
            mob.move_to(left_anchor + np.array([2 * np.cos(t), 2 * np.sin(t), 0]))
        moving_dot.add_updater(update_moving_dot)

        # Updater for dot_label to follow the dot
        dot_label.add_updater(lambda m: m.next_to(moving_dot, UR, buff=0.1))

        # Updater for projection_line (horizontal dashed line from dot to sine graph)
        def update_projection_line(mob):
            t = t_tracker.get_value()
            dot_pos = left_anchor + np.array([2 * np.cos(t), 2 * np.sin(t), 0])
            # Project horizontally to the vertical line x = right_anchor's x - 3 (left edge of sine axes)
            # The sine graph's x-coordinate for angle t is: right_anchor's x - 3 + (t / (2*PI)) * 6
            # But for the line, we want to connect to the vertical axis at x = right_anchor's x - 3
            target_x = right_anchor[0] - 3
            line_end = np.array([target_x, dot_pos[1], 0])
            mob.become(DashedLine(
                start=dot_pos,
                end=line_end,
                color=YELLOW,
                stroke_width=2,
                dash_length=0.05
            ))
        projection_line.add_updater(update_projection_line)

        # Function to add a dot to sine_wave_dots at current (t, sin(t))
        def add_sine_dot():
            t = t_tracker.get_value()
            if t <= 2 * PI:
                dot_pos = sine_axes.c2p(t, np.sin(t))
                dot = Dot(point=dot_pos, color=GREEN, radius=0.04)
                sine_wave_dots.add(dot)
                return dot
            return None

        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.extract_sequence()  # This would be parsed from JSON, but we'll simulate it with the steps provided.

        # Step 1
        step = sequence[0]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeIn(self.objects["title"]))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = sequence[1]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects["circle_axes"], color=WHITE))
        self.play(Create(self.objects["circle_axes"]))
        animation_time = 2.0  # Approximate for Indicate + Create
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = sequence[2]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects["sine_axes"], color=WHITE))
        self.play(Create(self.objects["sine_axes"]))
        self.play(FadeIn(self.objects["sine_axes_labels"]))
        animation_time = 2.5
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = sequence[3]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["unit_circle"]))
        self.play(Write(self.objects["circle_label"]))
        if step.get("signal_action") is not None:
            self.play(Circumscribe(self.objects["dot_label"], color=YELLOW))
        self.play(FadeIn(self.objects["moving_dot"]))
        self.play(FadeIn(self.objects["dot_label"]))
        animation_time = 4.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = sequence[4]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            self.play(Indicate(self.objects["projection_line"], color=YELLOW))
        self.play(Create(self.objects["projection_line"]))
        self.play(FadeIn(self.objects["footer_text"]))
        animation_time = 2.5
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = sequence[5]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Animate t from 0 to 2π over 10 seconds
        # We'll use a custom animation that updates the tracker and adds dots
        run_time = 10.0
        def update_t_and_dots(t):
            t_tracker.set_value(t)
            add_sine_dot()
        self.play(
            UpdateFromAlphaFunc(
                t_tracker,
                lambda mob, alpha: update_t_and_dots(alpha * 2 * PI),
                run_time=run_time,
                rate_func=linear
            )
        )
        animation_time = run_time
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        step = sequence[6]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            self.play(Circumscribe(self.objects["sine_wave_dots"], color=GREEN))
        # Wait for the remaining duration
        animation_time = 1.0  # For Circumscribe
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final wait
        self.wait(max(0.1, 2))

    def extract_sequence(self):
        """Simulate parsing the sequence from the provided JSON."""
        return [
            {
                "step": 1,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_00.mp3",
                "duration": 8.472,
                "signal_action": None
            },
            {
                "step": 2,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_01.mp3",
                "duration": 3.696,
                "signal_action": {"type": "Indicate", "target": "circle_axes", "color": "WHITE"}
            },
            {
                "step": 3,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_02.mp3",
                "duration": 9.048,
                "signal_action": {"type": "Indicate", "target": "sine_axes", "color": "WHITE"}
            },
            {
                "step": 4,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_03.mp3",
                "duration": 11.496,
                "signal_action": {"type": "Circumscribe", "target": "dot_label", "color": "YELLOW"}
            },
            {
                "step": 5,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_04.mp3",
                "duration": 11.424,
                "signal_action": {"type": "Indicate", "target": "projection_line", "color": "YELLOW"}
            },
            {
                "step": 6,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_05.mp3",
                "duration": 8.352,
                "signal_action": None
            },
            {
                "step": 7,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_06.mp3",
                "duration": 8.064,
                "signal_action": {"type": "Circumscribe", "target": "sine_wave_dots", "color": "GREEN"}
            }
        ]