'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship sin(θ) = y-coordinate on the unit circle and how it generates the sine wave.
# 2. Layout Strategy: Dual-view layout with High-Low Split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and graph (right)
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check: Left column centered at (-4,0), right column at (4,0). Use VGroups to manage each side.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_a_Manim_anima_443438dafe/step_XX.mp3"
# 5. Animation Flow: Build circle system, then graph system, then connect them with a bridge line, finally animate rotation.
'''

from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        circle_center = np.array([-4, 0, 0])
        graph_origin = np.array([4, 0, 0])
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Sine Function: From Circle to Wave", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle Axes
        circle_axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True}
        )
        circle_axes.move_to(circle_center)
        self.objects["circle_axes"] = circle_axes

        # Unit Circle
        unit_circle = Circle(radius=2, color=BLUE, stroke_width=3)
        unit_circle.move_to(circle_center)
        self.objects["unit_circle"] = unit_circle

        # Circle Dot (initial position at (1,0) relative to circle center)
        circle_dot = Dot(radius=0.08, color=YELLOW)
        circle_dot.move_to(circle_center + np.array([2, 0, 0]))
        self.objects["circle_dot"] = circle_dot

        # Radius Line
        radius_line = Line(
            start=circle_center,
            end=circle_center + np.array([2, 0, 0]),
            color=GREEN,
            stroke_width=2
        )
        self.objects["radius_line"] = radius_line

        # Theta Label
        theta_label = MathTex(r"\theta", color=WHITE, font_size=30)
        theta_label.next_to(circle_center, UP+RIGHT, buff=0.1)
        self.objects["theta_label"] = theta_label

        # Sin Label Line (vertical dashed line)
        sin_label_line = DashedLine(
            start=circle_center + np.array([2, 0, 0]),
            end=circle_center + np.array([2, 0.1, 0]),
            color=RED,
            stroke_width=2
        )
        self.objects["sin_label_line"] = sin_label_line

        # Sin Label
        sin_label = MathTex(r"\sin(\theta)", color=RED, font_size=30)
        sin_label.next_to(circle_center + np.array([2, 0, 0]), RIGHT, buff=0.1)
        self.objects["sin_label"] = sin_label

        # Graph Axes
        graph_axes = Axes(
            x_range=[0, 6.283, 1.57],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "numbers_to_exclude": []
            },
            x_axis_config={
                "numbers_with_elongated_ticks": [0, 3.14, 6.28],
                "numbers_to_include": [0, 1.57, 3.14, 4.71, 6.28]
            }
        )
        graph_axes.move_to(graph_origin)
        self.objects["graph_axes"] = graph_axes

        # Sine Curve (ParametricFunction)
        # Scale factor: x-length 5 corresponds to 2π, so scale = 5/(2π) ≈ 0.796
        scale_x = 5 / (2 * PI)
        sine_curve = ParametricFunction(
            lambda t: np.array([
                graph_origin[0] + t * scale_x,
                graph_origin[1] + 2 * np.sin(t),
                0
            ]),
            t_range=[0, 2 * PI],
            color=BLUE,
            stroke_width=3
        )
        self.objects["sine_curve"] = sine_curve

        # Graph Dot
        graph_dot = Dot(radius=0.08, color=YELLOW)
        graph_dot.move_to(graph_origin)
        self.objects["graph_dot"] = graph_dot

        # Bridge Line (horizontal dashed line)
        bridge_line = DashedLine(
            start=circle_center + np.array([2, 0, 0]),
            end=graph_origin,
            color=PURPLE,
            stroke_width=2,
            dash_length=0.1
        )
        self.objects["bridge_line"] = bridge_line

        # Explanation Text
        explanation_text = Text(
            "The y-coordinate of the point on the unit circle is sin(θ).",
            color=WHITE,
            font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        audio_step1 = "media/audio/Create_a_Manim_anima_443438dafe/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        self.play(Create(self.objects["circle_axes"]), run_time=2.0)
        remaining_1 = max(0.1, 9.696 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_a_Manim_anima_443438dafe/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["unit_circle"]), run_time=2.0)
        remaining_2 = max(0.1, 6.144 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_a_Manim_anima_443438dafe/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["circle_dot"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["circle_dot"]), run_time=1.0)
        self.play(Create(self.objects["radius_line"]), run_time=1.0)
        self.play(Create(self.objects["sin_label_line"]), run_time=1.0)
        self.play(Write(self.objects["theta_label"]), Write(self.objects["sin_label"]), run_time=1.5)
        remaining_3 = max(0.1, 10.944 - 1 - 1.0 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_a_Manim_anima_443438dafe/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Create(self.objects["graph_axes"]), run_time=2.0)
        remaining_4 = max(0.1, 10.848 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_a_Manim_anima_443438dafe/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Create(self.objects["sine_curve"]), run_time=2.0)
        remaining_5 = max(0.1, 9.6 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_a_Manim_anima_443438dafe/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Create(self.objects["bridge_line"]), run_time=1.5)
        self.play(Create(self.objects["graph_dot"]), run_time=1.0)
        self.play(Write(self.objects["explanation_text"]), run_time=1.5)
        remaining_6 = max(0.1, 12.312 - 1.5 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7: Setup dynamic updaters and animate rotation
        audio_step7 = "media/audio/Create_a_Manim_anima_443438dafe/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # Create ValueTracker for theta
        theta_tracker = ValueTracker(0)
        self.objects["theta_tracker"] = theta_tracker

        # Define updater functions
        circle_center = np.array([-4, 0, 0])
        graph_origin = np.array([4, 0, 0])
        scale_x = 5 / (2 * PI)

        # Circle dot updater
        circle_dot_updater = always_redraw(lambda: self.objects["circle_dot"].move_to(
            circle_center + 2 * np.array([np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value()), 0])
        ))

        # Radius line updater
        radius_line_updater = always_redraw(lambda: self.objects["radius_line"].put_start_and_end_on(
            circle_center,
            circle_center + 2 * np.array([np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value()), 0])
        ))

        # Sin label line (vertical line from dot to x-axis)
        sin_label_line_updater = always_redraw(lambda: self.objects["sin_label_line"].put_start_and_end_on(
            circle_center + 2 * np.array([np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value()), 0]),
            circle_center + np.array([2 * np.cos(theta_tracker.get_value()), 0, 0])
        ))

        # Theta label position (near the arc)
        theta_label_updater = always_redraw(lambda: self.objects["theta_label"].move_to(
            circle_center + 0.5 * np.array([np.cos(theta_tracker.get_value()/2), np.sin(theta_tracker.get_value()/2), 0])
        ))

        # Sin label position (to the right of the vertical line)
        sin_label_updater = always_redraw(lambda: self.objects["sin_label"].next_to(
            circle_center + np.array([2 * np.cos(theta_tracker.get_value()), 0, 0]),
            RIGHT, buff=0.1
        ))

        # Graph dot updater
        graph_dot_updater = always_redraw(lambda: self.objects["graph_dot"].move_to(
            graph_origin + np.array([
                theta_tracker.get_value() * scale_x,
                2 * np.sin(theta_tracker.get_value()),
                0
            ])
        ))

        # Bridge line updater (horizontal line connecting y-values)
        bridge_line_updater = always_redraw(lambda: self.objects["bridge_line"].put_start_and_end_on(
            circle_center + 2 * np.array([np.cos(theta_tracker.get_value()), np.sin(theta_tracker.get_value()), 0]),
            graph_origin + np.array([
                theta_tracker.get_value() * scale_x,
                2 * np.sin(theta_tracker.get_value()),
                0
            ])
        ))

        # Add updaters to the scene (by adding the always_redraw mobjects)
        self.add(
            circle_dot_updater,
            radius_line_updater,
            sin_label_line_updater,
            theta_label_updater,
            sin_label_updater,
            graph_dot_updater,
            bridge_line_updater
        )

        # Animate theta from 0 to 2π
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=12.048,
            rate_func=linear
        )
        self.wait(max(0.1, 1))