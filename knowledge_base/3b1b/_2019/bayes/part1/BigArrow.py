# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一個帶有弧度的箭頭從左下到右下的動態繪製過程。



from manim import *
class BigArrow(Scene):
    def construct(self):
        arrow = Arrow(
            start=3 * DOWN + 4 * LEFT,
            end=3 * RIGHT + DOWN,
            path_arc=50 * DEGREES,
        )

        self.play(Create(arrow))
        self.wait()
