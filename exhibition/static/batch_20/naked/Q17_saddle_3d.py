from manim import *
import numpy as np


class GeneratedScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=5,
        )

        saddle = Surface(
            lambda u, v: axes.c2p(u, v, u**2 - v**2),
            u_range=[-2.2, 2.2],
            v_range=[-2.2, 2.2],
            resolution=(32, 32),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        x_curve = ParametricFunction(
            lambda t: axes.c2p(t, 0, t**2),
            t_range=[-2.2, 2.2],
            color=YELLOW,
        )
        y_curve = ParametricFunction(
            lambda t: axes.c2p(0, t, -t**2),
            t_range=[-2.2, 2.2],
            color=RED,
        )

        saddle_point = Dot3D(axes.c2p(0, 0, 0), color=WHITE, radius=0.1)

        title = Text("Saddle Surface: z = x² − y²", font_size=32)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        x_label = Text("x 方向：向上彎 (z = x²)", font_size=24, color=YELLOW).to_corner(UR)
        y_label = Text("y 方向：向下彎 (z = −y²)", font_size=24, color=RED).next_to(x_label, DOWN, aligned_edge=RIGHT)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)
        self.play(Create(axes))
        self.play(Create(saddle), run_time=3)

        self.add_fixed_in_frame_mobjects(x_label)
        self.play(Create(x_curve), run_time=2)
        self.wait(0.5)

        self.add_fixed_in_frame_mobjects(y_label)
        self.play(Create(y_curve), run_time=2)
        self.wait(0.5)

        self.play(FadeIn(saddle_point, scale=2))

        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(1)