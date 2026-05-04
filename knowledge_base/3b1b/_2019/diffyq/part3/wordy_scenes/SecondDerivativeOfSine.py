# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示二階導數公式的數學方程式，其中變數 x 以綠色標示。



from manim import *
class SecondDerivativeOfSine(Scene):
    def construct(self):
        equation = MathTex(
            "{d^2 \\over d{x}^2}",
            "\\cos\\left({x}\\right) =",
            "-\\cos\\left({x}\\right)",
            tex_to_color_map={
                "{x}": GREEN,
            }
        )

        self.add(equation)
