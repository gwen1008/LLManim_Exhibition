# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示作者資訊的文字動畫，文字從上方淡入並停留在畫面中央。



from manim import *
class ByLine(Scene):
    def construct(self):
        text = MathTex(r"""
            Written and animated by \\
            \quad \\
            Sridhar Ramesh \\
            Grant Sanderson
        """).shift(2 * UP)
        self.play(FadeIn(text, shift=DOWN))
        self.wait()
