# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 顯示紅色文字 "(Real part of the)" 並以書寫動畫呈現。



from manim import *
class RealPartOfInsert(Scene):
    def construct(self):
        words = Text("(Real part of the)", color=RED)
        self.play(Write(words))
        self.wait(5)
