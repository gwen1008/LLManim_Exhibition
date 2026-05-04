# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個以藍色描邊的數學公式 "π = 6.283185..." 和下方文字 "...according to Euler." 組成的縮圖場景。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        pi, eq, num = formula = MathTex(
            "\\pi", "=", "6.283185\\dots"
        )
        formula.scale(2)
        pi.scale(1.5, about_edge=RIGHT)
        formula.set_stroke(BLUE, 1)
        formula.set_width(config.frame_width - 2)
        # formula.shift(0.5*RIGHT)
        self.add(formula)

        words = Tex("...according to Euler.")
        words.scale(1.5)
        words.next_to(formula, DOWN, buff=MED_LARGE_BUFF)
        self.add(words)
