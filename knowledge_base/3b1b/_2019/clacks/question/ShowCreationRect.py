# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個矩形圍繞文字動態繪製，然後淡出的過程。



from manim import *
class ShowCreationRect(Scene):
    def construct(self):
        rect = SurroundingRectangle(MathTex("\\# Collisions: 3"))
        self.play(Create(rect))
        self.play(FadeOut(rect))
        self.wait()
