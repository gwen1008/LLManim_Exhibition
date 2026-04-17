# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個黃色矩形以粗邊框繪製出來，然後淡出消失的過程。



from manim import *
class SurroundingRectangleSnippet(Scene):
    def construct(self):
        rect = Rectangle()
        rect.set_color(YELLOW)
        rect.set_stroke(width=5)
        self.play(Create(rect))
        self.play(FadeOut(rect))
