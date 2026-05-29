from manim import *
import numpy as np


class GeneratedScene(ThreeDScene):
    def construct(self):
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0

        def lorenz(state, dt):
            x, y, z = state
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return state + np.array([dx, dy, dz]) * dt

        dt = 0.005
        n_steps = 6000
        points = np.zeros((n_steps, 3))
        points[0] = np.array([0.1, 0.0, 0.0])
        for i in range(1, n_steps):
            points[i] = lorenz(points[i - 1], dt)

        scale = 0.12
        shift = np.array([0, 0, -25 * scale])
        scaled = points * scale + shift

        axes = ThreeDAxes(
            x_range=[-30, 30, 10],
            y_range=[-30, 30, 10],
            z_range=[0, 50, 10],
            x_length=7,
            y_length=7,
            z_length=6,
        ).scale(scale).shift(shift)

        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.15)

        title = Text("Lorenz Attractor", font_size=36)
        params = MathTex(r"\sigma=10,\ \rho=28,\ \beta=8/3", font_size=28)
        title.to_corner(UL)
        params.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(title, params)

        self.play(Create(axes), run_time=1.5)

        chunk = 60
        colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PURPLE]
        prev = scaled[0]
        segments = VGroup()
        for i in range(1, n_steps, chunk):
            end = min(i + chunk, n_steps)
            pts = scaled[i - 1:end]
            color = colors[(i // chunk) % len(colors)]
            curve = VMobject(stroke_width=2).set_points_as_corners(
                [np.array(p) for p in pts]
            ).set_color(color)
            segments.add(curve)

        self.play(
            LaggedStart(
                *[Create(s, rate_func=linear) for s in segments],
                lag_ratio=0.02,
            ),
            run_time=10,
        )

        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(1)