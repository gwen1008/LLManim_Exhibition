# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一個紅色半透明矩形從右側縮放至完整寬度的動畫過程。



from manim import *
class XCoordNegative(Scene):
    def construct(self):
        rect = Rectangle(height=4, width=4)
        rect.set_stroke(width=0)
        rect.set_fill(RED, 0.5)
        rect.save_state()
        rect.stretch(0, 0, about_edge=RIGHT)
        self.play(Restore(rect))
        self.wait()
