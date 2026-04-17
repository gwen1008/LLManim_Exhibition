# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示一個文字群組，包含說明文字和一個黃色的不等式，並將其置於畫面底部。



from manim import *
class ABCNotBCA(Scene):
    def construct(self):
        words = Text("If order mattered:")
        equation = MathTex(r"(A, B, C) \ne (B, C, A)")
        equation.set_color(YELLOW)
        equation.next_to(words, DOWN)
        group = VGroup(words, equation)
        group.set_width(config.frame_width - 1)
        group.to_edge(DOWN)
        self.add(words, equation)
