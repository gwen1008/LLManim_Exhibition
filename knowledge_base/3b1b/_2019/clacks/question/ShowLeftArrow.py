# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個紅色箭頭從左側生長出來，然後淡出消失的過程。



from manim import *
class ShowLeftArrow(Scene):
    def construct(self):
        arrow = Vector(2 * LEFT, color=RED)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrow))
