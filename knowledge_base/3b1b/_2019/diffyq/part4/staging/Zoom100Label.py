# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示文字 "100x Zoom" 從中心點放大出現的動畫。



from manim import *
class Zoom100Label(Scene):
    def construct(self):
        text = Text("100x Zoom")
        text.scale(2)
        self.play(GrowFromCenter(text))
        self.wait()
