# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 一顆愛心符號從下方淡入，然後淡出消失。



from manim import *
class FadeInHeart(Scene):
    def construct(self):
        heart = SuitSymbol("hearts")

        self.play(FadeIn(heart, shift=DOWN))
        self.play(FadeOut(heart))
