from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        # Left: unit circle
        circle_center = LEFT * 4
        radius = 1.5
        axes_left = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": False, "stroke_width": 2},
        ).move_to(circle_center)
        circle = Circle(radius=radius, color=BLUE).move_to(circle_center)

        # Right: sin curve axes
        right_center = RIGHT * 2.5
        axes_right = Axes(
            x_range=[0, TAU, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=4,
            tips=False,
            axis_config={"stroke_width": 2},
        ).move_to(right_center)
        x_label = axes_right.get_x_axis_label(MathTex("\\theta"))
        y_label = axes_right.get_y_axis_label(MathTex("\\sin\\theta"))

        title = Text("單位圓與正弦函數", font_size=32).to_edge(UP)

        self.play(Write(title))
        self.play(Create(axes_left), Create(circle), Create(axes_right), Write(x_label), Write(y_label))

        theta = ValueTracker(0)

        dot = always_redraw(
            lambda: Dot(
                circle_center + radius * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                color=YELLOW,
            )
        )
        radius_line = always_redraw(
            lambda: Line(
                circle_center,
                circle_center + radius * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                color=YELLOW,
            )
        )
        v_line = always_redraw(
            lambda: DashedLine(
                circle_center + radius * np.array([np.cos(theta.get_value()), 0, 0]),
                circle_center + radius * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                color=GREEN,
            )
        )
        h_proj = always_redraw(
            lambda: DashedLine(
                circle_center + radius * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
                axes_right.c2p(theta.get_value(), np.sin(theta.get_value())),
                color=RED,
                stroke_opacity=0.5,
            )
        )

        sin_graph = always_redraw(
            lambda: axes_right.plot(
                lambda x: np.sin(x),
                x_range=[0, max(0.001, theta.get_value())],
                color=RED,
            )
        )
        moving_dot = always_redraw(
            lambda: Dot(
                axes_right.c2p(theta.get_value(), np.sin(theta.get_value())),
                color=RED,
            )
        )

        theta_label = always_redraw(
            lambda: MathTex(f"\\theta = {theta.get_value():.2f}", font_size=28).next_to(
                axes_left, DOWN
            )
        )
        sin_label = always_redraw(
            lambda: MathTex(
                f"\\sin\\theta = {np.sin(theta.get_value()):.2f}", font_size=28
            ).next_to(axes_right, DOWN)
        )

        self.add(radius_line, dot, v_line, h_proj, sin_graph, moving_dot, theta_label, sin_label)
        self.play(theta.animate.set_value(TAU), run_time=8, rate_func=linear)
        self.wait(1)