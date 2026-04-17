# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一個白色矩形從原始高度垂直壓縮到幾乎消失，同時填充不透明度變為完全不透明的動畫過程。



from manim import *
class YCoordZero(Scene):
    def construct(self):
        rect = Rectangle(height=4, width=8)
        rect.set_stroke(width=0)
        rect.set_fill(WHITE, 0.5)
        rect.save_state()
        self.play(
            rect.animate.stretch(0.01, 1).set_fill(opacity=1)
        )
        self.wait()
