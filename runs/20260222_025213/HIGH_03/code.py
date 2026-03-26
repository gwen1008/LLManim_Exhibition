from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on layout zones
        title_anchor = 3.5 * UP
        circle_center = 3 * LEFT
        graph_origin = 3 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Sine Wave from the Unit Circle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle and its axes
        circle = Circle(radius=2, color=BLUE, stroke_width=3)
        circle.move_to(circle_center)
        self.objects["circle"] = circle

        circle_axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY},
            tips=False
        )
        circle_axes.move_to(circle_center)
        self.objects["circle_axes"] = circle_axes

        # Moving point and radius line (initial position at angle 0)
        moving_point = Dot(radius=0.08, color=YELLOW)
        moving_point.move_to(circle_center + 2 * RIGHT)
        self.objects["moving_point"] = moving_point

        radius_line = Line(
            start=circle_center,
            end=circle_center + 2 * RIGHT,
            color=GREEN,
            stroke_width=2
        )
        self.objects["radius_line"] = radius_line

        # Graph axes and sine graph
        graph_axes = Axes(
            x_range=[0, 6.283, 1.571],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY},
            tips=False
        )
        graph_axes.move_to(graph_origin)
        self.objects["graph_axes"] = graph_axes

        # Full sine wave (static, for reference)
        sine_graph = ParametricFunction(
            lambda t: np.array([t * 0.6366, 2 * np.sin(t), 0]),
            t_range=[0, 2 * np.pi],
            color=RED,
            stroke_width=3
        )
        sine_graph.move_to(graph_origin)
        self.objects["sine_graph"] = sine_graph

        # Drawn sine (starts empty, will be drawn progressively)
        drawn_sine = ParametricFunction(
            lambda t: np.array([t * 0.6366, 2 * np.sin(t), 0]),
            t_range=[0, 0],
            color=RED,
            stroke_width=4
        )
        drawn_sine.move_to(graph_origin)
        self.objects["drawn_sine"] = drawn_sine

        # Graph point (initial at origin)
        graph_point = Dot(radius=0.08, color=YELLOW)
        graph_point.move_to(graph_origin)
        self.objects["graph_point"] = graph_point

        # Projection line (dashed, from circle point to graph point)
        projection_line = DashedLine(
            start=circle_center + 2 * RIGHT,
            end=graph_origin,
            color=WHITE,
            stroke_width=1.5,
            stroke_opacity=0.7,
            dash_length=0.1
        )
        self.objects["projection_line"] = projection_line

        # Parameter text
        parameter_text = MathTex("t = 0", color=BLUE, font_size=28)
        parameter_text.move_to(footer_anchor)
        self.objects["parameter_text"] = parameter_text

        # ValueTracker for synchronization
        t_tracker = ValueTracker(0)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["circle_axes"]))
        self.wait(0.1)

        # Step 2
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["circle"]))
        self.wait(0.1)

        # Step 3
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["graph_axes"], color=YELLOW))
        self.play(Create(self.objects["graph_axes"]))
        self.wait(0.1)

        # Step 4
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["moving_point"], color=YELLOW))
        self.play(
            Create(self.objects["moving_point"]),
            Create(self.objects["radius_line"])
        )
        self.wait(0.1)

        # Step 5
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["projection_line"], color=WHITE))
        self.play(
            Create(self.objects["graph_point"]),
            Create(self.objects["projection_line"])
        )
        self.wait(0.1)

        # Add updaters AFTER creating all objects
        moving_point.add_updater(lambda m: m.move_to(
            circle_center + 2 * np.array([np.cos(t_tracker.get_value()), np.sin(t_tracker.get_value()), 0])
        ))
        radius_line.add_updater(lambda l: l.become(
            Line(circle_center, moving_point.get_center(), color=GREEN, stroke_width=2)
        ))
        graph_point.add_updater(lambda d: d.move_to(
            graph_origin + np.array([t_tracker.get_value() * 0.6366, 2 * np.sin(t_tracker.get_value()), 0])
        ))
        projection_line.add_updater(lambda dl: dl.become(
            DashedLine(
                start=moving_point.get_center(),
                end=graph_point.get_center(),
                color=WHITE,
                stroke_width=1.5,
                stroke_opacity=0.7,
                dash_length=0.1
            )
        ))
        drawn_sine.add_updater(lambda ps: ps.become(
            ParametricFunction(
                lambda t: np.array([t * 0.6366, 2 * np.sin(t), 0]),
                t_range=[0, t_tracker.get_value()],
                color=RED,
                stroke_width=4
            ).move_to(graph_origin)
        ))
        parameter_text.add_updater(lambda mt: mt.become(
            MathTex(f"t = {t_tracker.get_value():.2f}", color=BLUE, font_size=28).move_to(footer_anchor)
        ))

        # Step 6
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Add the static sine graph for reference (faded)
        sine_graph_faded = self.objects["sine_graph"].copy().set_opacity(0.3)
        self.add(sine_graph_faded)
        # Add the title
        self.play(Create(self.objects["title"]))
        # Add the parameter text
        self.add(self.objects["parameter_text"])
        # Animate t from 0 to 2π
        self.play(
            t_tracker.animate.set_value(2 * np.pi),
            run_time=6,
            rate_func=linear
        )
        self.wait(0.1)

        # Step 7
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["drawn_sine"], color=YELLOW, run_time=1))
        self.wait(2)