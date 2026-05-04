# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示使用克萊姆法則計算行列式時，分子分母中不同項目的顏色標記過程。



from manim import *
class CramersYEvaluation(Scene):
    def construct(self):
        # 使用 MathTex 替代 OldTex
        frac = MathTex("{(2)(2) - (4)(0) \\over (2)(1) - (-1)(0)}")[0]
        # 對分子分母中的特定項進行顏色標記
        VGroup(frac[1], frac[11], frac[15], frac[26]).set_color(GREEN)
        VGroup(frac[4], frac[8]).set_color(MAROON_B)
        VGroup(frac[18], frac[22], frac[23]).set_color(RED)

        # 將等號和分式排列成一行
        group = VGroup(
            MathTex("="), frac,
            MathTex("= \\frac{4}{2}"), MathTex("=2")
        )
        group.arrange(RIGHT)

        self.add(group)
        self.wait(1)
