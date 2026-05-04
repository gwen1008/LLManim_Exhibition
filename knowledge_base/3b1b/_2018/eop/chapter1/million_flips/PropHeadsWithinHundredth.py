# Source: 3b1b/_2018/eop/chapter1/million_flips.py
# Description: [3b1b translated] 展示一個機率公式，其中特定部分以紅色和黃色高亮顯示。



from manim import *
class PropHeadsWithinHundredth(Scene):
    def construct(self):
        prob = MathTex(
            "P(490{,}000 \\le", "\\# \\text{H}", "\\le 510{,}000)",
            "\\approx", "0.99999999\\dots",
        )
        prob[1].set_color(RED)
        prob[-1].set_color(YELLOW)
        self.add(prob)
