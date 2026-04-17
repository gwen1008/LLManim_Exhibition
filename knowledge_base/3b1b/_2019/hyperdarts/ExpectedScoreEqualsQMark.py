# Source: 3b1b/_2019/hyperdarts.py
# Description: [3b1b translated] 展示一個數學期望值等於問號的方程式，並從下方淡入其別名說明文字。



from manim import *
class ExpectedScoreEqualsQMark(Scene):
    def construct(self):
        equation = MathTex(
            "\\textbf{E}[Score] = ???",
            tex_to_color_map={
                "???": YELLOW,
            }
        )
        aka = Text("a.k.a. Long-term average")
        aka.next_to(equation, DOWN)

        self.play(Write(equation))
        self.wait(2)
        self.play(FadeIn(aka, shift=UP))
        self.wait()
