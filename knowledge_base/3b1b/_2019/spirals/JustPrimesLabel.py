# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 顯示 "Just the primes" 文字在左上角，然後淡出。



from manim import *
class JustPrimesLabel(Scene):
    def construct(self):
        text = Text("Just the primes")
        text.scale(2)
        text.to_corner(UL)
        self.play(Write(text))
        self.wait(3)
        self.play(FadeOut(text, shift=DOWN))
