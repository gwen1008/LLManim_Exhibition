# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示使用克拉瑪法則計算行列式時，分子分母中對應項目的顏色標記過程。



from manim import *
class CramersXEvaluation(Scene):
    def construct(self):
        # 使用 MathTex 替代 OldTex
        frac = MathTex("{(4)(1) - (-1)(2) \\over (2)(1) - (-1)(0)}")[0]
        # 使用 set_color 替代 highlight
        VGroup(frac[1], frac[12]).set_color(MAROON_B)
        VGroup(frac[4], frac[8], frac[9]).set_color(RED)
        VGroup(frac[16], frac[27]).set_color(GREEN)
        VGroup(frac[19], frac[23], frac[24]).set_color(RED)

        # 建立群組並排列
        group = VGroup(
            MathTex("="), frac,
            MathTex("= \\frac{6}{2}"), MathTex("=3")
        )
        group.arrange(RIGHT)
        # 添加背景矩形
        group.add_to_back(BackgroundRectangle(group))

        self.add(group)
        self.wait(1)
