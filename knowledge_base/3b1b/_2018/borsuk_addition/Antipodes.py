# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 在畫面中央以深栗色顯示「Antipodes」文字，並以書寫動畫呈現。



from manim import *
class Antipodes(Scene):
    def construct(self):
        word = Text("``Antipodes''", color=MAROON_B)
        word.set_width(config.frame_width - 1)
        self.play(Write(word))
        self.wait()
