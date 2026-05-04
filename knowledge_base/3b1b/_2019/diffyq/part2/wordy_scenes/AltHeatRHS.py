# Source: 3b1b/_2019/diffyq/part2/wordy_scenes.py
# Description: [3b1b translated] 展示一個包含顏色標記的熱方程右側公式。



from manim import *
class AltHeatRHS(Scene):
    def construct(self):
        formula = MathTex(
            r"{\alpha \over 2}", r"\Big(",
            r"T({x} - 1, {t}) + T({x} + 1, {t})",
            r"\Big)",
            tex_to_color_map={
                "{x}": GREEN,
                "{t}": YELLOW,
            }
        )
        self.add(formula)
