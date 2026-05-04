# Source: 3b1b/_2018/eop/chapter1/million_flips.py
# Description: [3b1b translated] 展示一個機率公式，其中特定符號被標記為紅色，最終結果被標記為黃色。



from manim import *
class PropHeadsWithinThousandth(Scene):
    def construct(self):
        prob = MathTex(
            "P(499{,}000 \\le", "\\# \\text{H}", "\\le 501{,}000)",
            "\\approx", "0.9545",
        )
        prob[1].set_color(RED)
        prob[-1].set_color(YELLOW)
        self.add(prob)
