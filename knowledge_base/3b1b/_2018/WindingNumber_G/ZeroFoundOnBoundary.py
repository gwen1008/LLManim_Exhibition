# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個箭頭從上方向左下角生長，同時文字「Found zero on boundary!」出現，並在箭頭起點處先有一個閃光效果。



from manim import *
class ZeroFoundOnBoundary(Scene):
    def construct(self):
        arrow = Vector(DOWN+LEFT, color=WHITE)
        words = Text("Found zero on boundary!")
        words.next_to(arrow.get_start(), UP)
        words.shift(1.5*RIGHT)

        point = Dot(radius=0.001, color=WHITE)  # 用極小的點模擬 VectorizedPoint
        point.next_to(arrow, DOWN+LEFT)

        self.play(Flash(point))
        self.play(
            GrowArrow(arrow),
            Write(words),
        )
        self.wait()
