# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一個程式設計師的SVG圖像從下方淡入並停留在畫面左下角的過程。



from manim import *
class ShowProgrammer(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        programmer = SVGMobject(file_name="programmer")
        programmer.set_stroke(width=0)
        programmer.set_fill(GREY, opacity=1)
        programmer.set_sheen(1, UL)
        programmer.set_height(3)

        programmer.to_corner(DL)
        self.play(FadeIn(programmer, shift=DOWN))
        self.wait()
