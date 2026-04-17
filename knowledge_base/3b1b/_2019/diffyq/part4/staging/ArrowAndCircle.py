# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一個紅色箭頭從右上角指向左下角，然後在其旁邊出現一個紅色圓圈，最後圓圈淡出。



from manim import *
class ArrowAndCircle(Scene):
    def construct(self):
        circle = Circle(color=RED)
        circle.set_stroke(width=4)
        circle.set_height(0.25)

        arrow = Arrow(start=ORIGIN, end=DL, color=RED, buff=0)
        arrow.set_color(RED)
        arrow.next_to(circle, UR)
        self.play(Create(arrow))
        self.play(Create(circle))
        self.play(FadeOut(circle))
        self.wait()
