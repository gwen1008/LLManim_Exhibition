# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示三維空間中圓柱體上的圓圈隨著時間拉伸並扭曲成環面的動態過程，同時帶有流動線條效果。


from manim import *
import numpy as np
import random

class VortedStretching(ThreeDScene):
    def __init__(self, n_circles=200, **kwargs):
        super().__init__(**kwargs)
        self.n_circles = n_circles

    def construct(self):
        axes = ThreeDAxes()
        axes.set_stroke(width=1)
        self.add(axes)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-145 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        short_circles = self.get_cylinder_circles(2, 0.5, 0.5)
        tall_circles = short_circles.copy().scale(0.125)
        tall_circles.stretch(16 * 4, 2)
        torus_circles = tall_circles.copy()
        for circle in torus_circles:
            circle.shift(RIGHT)
            z = circle.get_center()[2]
            circle.shift(z * IN)
            angle = PI * z / 2
            circle.rotate(angle, axis=DOWN, about_point=ORIGIN)

        circles = short_circles.copy()
        flow_lines = self.get_flow_lines(circles)

        self.add(circles, flow_lines)
        self.play(LaggedStartMap(Create, circles))
        self.wait(5)
        self.play(Transform(circles, tall_circles, run_time=3))
        self.wait(10)
        self.play(Transform(
            circles, torus_circles,
            run_time=3
        ))
        self.wait(10)

    def get_cylinder_circles(self, radius, radius_var, max_z):
        return VGroup(*[
            ParametricFunction(
                lambda t: np.array([
                    np.cos(TAU * t) * r,
                    np.sin(TAU * t) * r,
                    z
                ]),
                t_range=[0, 1],
                **self.get_circle_kwargs()
            )
            for z in sorted(max_z * np.random.random(self.n_circles))
            for r in [radius + radius_var * random.random()]
        ]).center()

    def get_torus_circles(self, out_r, in_r, in_r_var):
        result = VGroup()
        for u in sorted(np.random.random(self.n_circles)):
            r = in_r + in_r_var * random.random()
            circle = ParametricFunction(
                lambda t: r * np.array([
                    np.cos(TAU * t),
                    np.sin(TAU * t),
                    0,
                ]),
                t_range=[0, 1],
                **self.get_circle_kwargs()
            )
            circle.shift(out_r * RIGHT)
            circle.rotate(
                TAU * u - PI,
                about_point=ORIGIN,
                axis=DOWN,
            )
            result.add(circle)
        return result

    def get_flow_lines(self, circle_group):
        window = 0.3

        def update_circle(circle, dt):
            circle.total_time += dt
            diameter = np.linalg.norm(
                circle.template.point_from_proportion(0) -
                circle.template.point_from_proportion(0.5)
            )
            modulus = np.sqrt(diameter) + 0.1
            alpha = (circle.total_time % modulus) / modulus
            start = max(interpolate(-window, 1, alpha), 0)
            end = min(interpolate(0, 1 + window, alpha), 1)
            circle.become(circle.template)
            circle.pointwise_become_partial(circle.template, start, end)

        result = VGroup()
        for template in circle_group:
            circle = template.copy()
            circle.set_stroke(
                color=interpolate_color(BLUE_A, BLUE_E, random.random()),
                width=1,
            )
            circle.template = template
            circle.total_time = 4 * random.random()
            circle.add_updater(update_circle)
            result.add(circle)
        return result

    def get_circle_kwargs(self):
        return {
            "stroke_color": BLACK,
            "stroke_width": 0,
        }
