# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示傅立葉級數公式的數學表達式，並用顏色標記變數 n 和 t。



from manim import *
class FourierSeriesFormula(Scene):
    def construct(self):
        formula = MathTex(
            "c_{n} = \\int_0^1 e^{-2\\pi i {n} {t}}f({t}){dt}",
            tex_to_color_map={
                "{n}": YELLOW,
                "{t}": PINK,
            }
        )

        self.play(Write(formula))
        self.wait()
