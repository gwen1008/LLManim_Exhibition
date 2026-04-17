# Source: 3b1b/_2018/eop/chapter1/various_intro_visuals.py
# Description: [3b1b translated] 展示隨機點雲中所有點對形成的矩形，根據 y 軸相對位置以不同顏色（紅/藍）淡入，視覺化協方差概念。


from manim import *
import numpy as np
import itertools as it

class VisualCovariance(Scene):
    def construct(self):
        size = 4
        square = Square(side_length=size)
        n_points = 30
        cloud = VGroup(*[
            Dot((x + 0.8 * y) * RIGHT + y * UP).set_fill(WHITE, 1)
            for x, y in zip(
                np.random.normal(0, 1, n_points),
                np.random.normal(0, 1, n_points)
            )
        ])
        # ManimCE 沒有 add_foreground_mobject，直接加入場景
        self.add(cloud)

        x_axis = Vector(8 * RIGHT, color=WHITE).move_to(2.5 * DOWN)
        y_axis = Vector(5 * UP, color=WHITE).move_to(4 * LEFT)

        self.add(x_axis, y_axis)

        random_pairs = [(p1, p2) for (p1, p2) in it.combinations(cloud, 2)]
        np.random.shuffle(random_pairs)

        for (p1, p2) in random_pairs:
            c1, c2 = p1.get_center(), p2.get_center()
            x1, y1, x2, y2 = c1[0], c1[1], c2[0], c2[1]
            if x1 >= x2:
                continue
            if y2 > y1:
                # make a red rect
                color = RED
                opacity = 0.1
            elif y2 < y1:
                # make a blue rect
                color = BLUE
                opacity = 0.2
            else:
                continue  # y1 == y2 的情況跳過

            rect = Rectangle(width=x2 - x1, height=abs(y2 - y1))
            rect.set_fill(color=color, opacity=opacity)
            rect.set_stroke(width=0)
            rect.move_to((c1 + c2) / 2)

            self.play(FadeIn(rect), run_time=0.05)
