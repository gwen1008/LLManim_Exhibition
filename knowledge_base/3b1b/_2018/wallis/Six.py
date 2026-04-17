# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示一個帶有背景矩形的數字 "6" 被放大並置於場景中央。



from manim import *
class Six(Scene):
    def construct(self):
        six = MathTex("6")
        six.add_background_rectangle(opacity=1)
        six.background_rectangle.stretch(1.5, 0)
        six.set_height(7)
        self.add(six)
