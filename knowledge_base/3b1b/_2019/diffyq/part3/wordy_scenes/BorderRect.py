# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示一個白色邊框的全螢幕矩形，內部為透明。



from manim import *
class BorderRect(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        rect.set_stroke(WHITE, 3)
        rect.set_fill(opacity=0)
        self.add(rect)
