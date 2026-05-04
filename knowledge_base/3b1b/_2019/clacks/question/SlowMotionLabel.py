# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示「Slow motion replay」文字從上方向下寫入的動畫效果。



from manim import *
class SlowMotionLabel(Scene):
    def construct(self):
        words = Text("Slow motion replay")
        words.scale(2).to_edge(UP)
        self.play(Write(words))
        self.wait()
