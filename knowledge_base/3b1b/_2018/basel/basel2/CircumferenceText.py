# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 在畫面上方左角顯示文字 "Circumference 16"。



from manim import *
class CircumferenceText(Scene):
    def __init__(self, n=16, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    def construct(self):
        words = Text(f"Circumference {self.n}")
        words.scale(1.25)
        words.to_corner(UP + LEFT)
        self.add(words)
