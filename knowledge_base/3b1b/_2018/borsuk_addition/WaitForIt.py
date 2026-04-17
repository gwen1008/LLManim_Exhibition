# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示文字 "Wait for it" 和動態寫入的省略號動畫。



from manim import *
class WaitForIt(Scene):
    def construct(self):
        words = MathTex(r"\text{Wait for it}", r"\dots", arg_separator="")
        words.scale(2)
        self.add(words[0])
        self.play(Write(words[1], run_time=3))
        self.wait()
