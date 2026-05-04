# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個數學標籤，說明高度壓縮因子等於 R/d 的公式。



from manim import *
class HeightSquishLabel(Scene):
    def construct(self):
        text = MathTex(
            "\\text{Height squish factor} =",
            "\\frac{R}{d}"
        )
        self.play(Write(text))
        self.wait()
