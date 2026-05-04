# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 在場景中央顯示帶有背景矩形的 "Cramer's Rule" 文字，並以書寫動畫呈現。



from manim import *
class WriteCramersRule(Scene):
    def construct(self):
        words = Text("``Cramer's Rule''")
        words.set_width(config.frame_width - LARGE_BUFF)
        words.add_background_rectangle()
        self.play(Write(words))
        self.wait()
