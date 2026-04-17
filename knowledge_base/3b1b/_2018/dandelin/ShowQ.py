# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個帶有黑色描邊的字母 "Q" 從下方淡入並放大顯示的過程。



from manim import *
class ShowQ(Scene):
    def construct(self):
        mob = MathTex("Q")
        mob.scale(2)
        # 複製一份作為黑色描邊背景
        stroke_mob = mob.copy().set_stroke(color=BLACK, width=5)
        mob.add_to_back(stroke_mob)
        # 從下方淡入
        self.play(FadeIn(mob, shift=DOWN))
        self.wait()
