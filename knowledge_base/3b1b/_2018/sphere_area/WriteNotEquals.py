# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個不等於符號被書寫出來的動畫。



from manim import *
class WriteNotEquals(Scene):
    def construct(self):
        symbol = MathTex("\\ne")
        symbol.scale(2)
        symbol.set_background_stroke(width=0)
        self.play(Write(symbol))
        self.wait()
