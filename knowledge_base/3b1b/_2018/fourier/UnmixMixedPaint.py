# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示四個彩色象限旋轉混合成一個泥色圓形，然後再分離恢復的動態過程。


from manim import *
import numpy as np
import itertools as it

class UnmixMixedPaint(Scene):
    def __init__(self, colors=[BLUE, RED, YELLOW, GREEN], **kwargs):
        super().__init__(**kwargs)
        self.colors = colors

    def construct(self):
        angles = np.arange(4) * np.pi / 2
        quadrants = VGroup(*[
            Square(side_length=2).scale(0.5).rotate(angle, about_point=ORIGIN).set_color(color)
            for color, angle in zip(self.colors, angles)
        ])
        quadrants.add(*it.chain(*[
            quadrants.copy().rotate(angle)
            for angle in np.linspace(0, 0.02 * TAU, 10)
        ]))
        quadrants.set_fill(opacity=0.5)

        mud_color = average_color(*self.colors)
        mud_circle = Circle(radius=2, stroke_width=0)
        mud_circle.set_fill(mud_color, 1)
        mud_circle.save_state()
        mud_circle.scale(0)

        def update_quadrant(quadrant, alpha):
            points = quadrant.get_anchors()
            dt = 0.03
            norms = np.apply_along_axis(np.linalg.norm, 1, points)

            points[:, 0] -= dt * points[:, 1] / np.clip(norms, 0.1, np.inf)
            points[:, 1] += dt * points[:, 0] / np.clip(norms, 0.1, np.inf)

            new_norms = np.apply_along_axis(np.linalg.norm, 1, points)
            new_norms = np.clip(new_norms, 0.001, np.inf)
            radius = np.max(norms)
            multiplier = norms / new_norms
            multiplier = multiplier.reshape((len(multiplier), 1))
            multiplier = np.repeat(multiplier, points.shape[1], axis=1)
            points *= multiplier
            quadrant.set_points_smoothly(points)

        self.add(quadrants)
        run_time = 30
        self.play(
            *[
                UpdateFromAlphaFunc(quadrant, update_quadrant)
                for quadrant in quadrants
            ] + [
                mud_circle.animate.restore(rate_func=linear)
            ],
            run_time=run_time
        )
