# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示一個包含紅色數學公式的文本，並以寫入動畫呈現。



from manim import *
class ISquaredRule(Scene):
    def construct(self):
        tex = MathTex(r"\text{Use}", r"i^2 = -1")
        tex[1].set_color(RED)
        tex.scale(2)
        self.play(Write(tex))
        self.wait()
