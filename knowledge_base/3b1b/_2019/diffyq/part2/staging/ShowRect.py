# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示一個黃色矩形被創建並隨後淡出的動畫過程。



from manim import *
class ShowRect(Scene):
    def __init__(self, height=1, width=3, **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.width = width

    def construct(self):
        rect = Rectangle(
            height=self.height,
            width=self.width,
        )
        rect.set_color(YELLOW)
        self.play(Create(rect), FadeOut(rect))
