# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示一個週期公式和旁邊的問號，兩者都經過縮放並相鄰排列。



from manim import *
class PeriodFormula(Scene):
    def construct(self):
        formula = get_period_formula()
        formula.scale(2)
        q_mark = MathTex("?")
        q_mark.scale(3)
        q_mark.next_to(formula, RIGHT)
        self.add(formula, q_mark)
