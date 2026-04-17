# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個數學公式，內容是「寬度縮放因子等於 R 除以 d」。



from manim import *
class WidthScaleLabel(Scene):
    def construct(self):
        text = MathTex(
            "\\text{Width scale factor} =",
            "\\frac{R}{d}"
        )
        self.play(Write(text))
        self.wait()
