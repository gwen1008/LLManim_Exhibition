from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Text("單擺運動：時間圖 與 相位空間", font="PingFang TC").scale(0.6).to_edge(UP)
        self.add(title)

        omega = 2.0
        theta0 = PI / 4
        T_max = 8.0

        # Left axes: theta vs t
        left_axes = Axes(
            x_range=[0, T_max, 2],
            y_range=[-1.0, 1.0, 0.5],
            x_length=5.5,
            y_length=4.5,
            axis_config={"include_tip": True, "stroke_width": 2},
        ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        left_labels = left_axes.get_axis_labels(x_label="t", y_label=r"\theta")
        left_title = Text("θ - t 圖", font="PingFang TC").scale(0.4).next_to(left_axes, UP, buff=0.15)

        # Right axes: phase space
        right_axes = Axes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-2.5, 2.5, 1],
            x_length=5.0,
            y_length=4.5,
            axis_config={"include_tip": True, "stroke_width": 2},
        ).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        right_labels = right_axes.get_axis_labels(x_label=r"\theta", y_label=r"\dot\theta")
        right_title = Text("相位空間", font="PingFang TC").scale(0.4).next_to(right_axes, UP, buff=0.15)

        self.play(
            Create(left_axes), Create(right_axes),
            FadeIn(left_labels), FadeIn(right_labels),
            FadeIn(left_title), FadeIn(right_title),
        )

        # Ghost ellipse on phase space
        ellipse_pts = [
            right_axes.c2p(theta0 * np.cos(omega * s), -theta0 * omega * np.sin(omega * s))
            for s in np.linspace(0, 2 * PI / omega, 200)
        ]
        ghost = VMobject(stroke_color=GREY, stroke_opacity=0.4, stroke_width=2)
        ghost.set_points_smoothly(ellipse_pts)
        self.play(Create(ghost), run_time=1.2)

        t_tracker = ValueTracker(0.0)

        left_curve = always_redraw(lambda: left_axes.plot(
            lambda t: theta0 * np.cos(omega * t),
            x_range=[0, max(1e-3, t_tracker.get_value())],
            color=BLUE,
            stroke_width=3,
        ))

        right_trace = VMobject(stroke_color=YELLOW, stroke_width=3)
        right_trace.set_points_as_corners([
            right_axes.c2p(theta0, 0), right_axes.c2p(theta0, 0)
        ])

        def update_trace(m):
            t = t_tracker.get_value()
            ts = np.linspace(0, t, max(2, int(t * 40) + 2))
            pts = [right_axes.c2p(theta0 * np.cos(omega * s),
                                  -theta0 * omega * np.sin(omega * s)) for s in ts]
            m.set_points_as_corners(pts)
        right_trace.add_updater(update_trace)

        left_dot = always_redraw(lambda: Dot(
            left_axes.c2p(t_tracker.get_value(), theta0 * np.cos(omega * t_tracker.get_value())),
            color=RED, radius=0.08,
        ))
        right_dot = always_redraw(lambda: Dot(
            right_axes.c2p(
                theta0 * np.cos(omega * t_tracker.get_value()),
                -theta0 * omega * np.sin(omega * t_tracker.get_value()),
            ),
            color=RED, radius=0.08,
        ))

        eq_left = MathTex(r"\theta(t)=\theta_0\cos(\omega t)").scale(0.55).next_to(left_axes, DOWN, buff=0.2)
        eq_right = MathTex(r"\theta^2+(\dot\theta/\omega)^2=\theta_0^2").scale(0.55).next_to(right_axes, DOWN, buff=0.2)

        self.add(left_curve, right_trace, left_dot, right_dot)
        self.play(FadeIn(eq_left), FadeIn(eq_right))

        self.play(t_tracker.animate.set_value(T_max), run_time=8, rate_func=linear)
        self.wait(0.5)
        right_trace.clear_updaters()