# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示四個滿足阿波羅尼奧斯圓定理的圓，從中心向外動態繪製，並在上方顯示對應的數學公式。


from manim import *
import numpy as np
import itertools as it

class ShowApollonianCircles(Scene):
    def construct(self):
        radii = [1.0, 2.0, 3.0]
        curvatures = [1.0 / r for r in radii]
        k4 = sum(curvatures) - 2 * np.sqrt(
            sum([
                k1 * k2
                for k1, k2 in it.combinations(curvatures, 2)
            ])
        )
        radii.append(1.0 / k4)
        centers = [
            ORIGIN, 3 * RIGHT, 4 * UP,
            4 * UP + 3 * RIGHT,
        ]
        circles = VGroup(*[
            Circle(radius=r).shift(c)
            for r, c in zip(radii, centers)
        ])

        circles.set_height(FRAME_HEIGHT - 3)
        circles.center().to_edge(DOWN)
        # circles.set_fill(opacity=1)
        circles.submobjects.reverse()
        circles.set_stroke(width=5)
        circles.set_color_by_gradient(BLUE, YELLOW)

        equation = MathTex(r"""
            \left(
            {1 \over r_1} + {1 \over r_2} +
            {1 \over r_3} + {1 \over r_4}
            \right)^2 = 
            2\left(
            {1 \over r_1^2} + {1 \over r_2^2} +
            {1 \over r_3^2} + {1 \over r_4^2}
            \right)
        """)
        # equation.scale(1.5)
        equation.next_to(circles, UP)

        self.add(equation)
        self.play(LaggedStart(
            *[Create(circle) for circle in circles],
            lag_ratio=0.3
        ))
        self.wait()
