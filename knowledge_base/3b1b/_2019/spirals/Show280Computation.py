# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示歐拉函數 φ(710) 的計算過程，透過彩色括號和標籤逐步解釋每個因數的過濾步驟。



from manim import *
class Show280Computation(Scene):
    def construct(self):
        equation = MathTex(
            "\\phi(710) = ",
            "710",
            "\\left({1 \\over 2}\\right)",
            "\\left({4 \\over 5}\\right)",
            "\\left({70 \\over 71}\\right)",
            "=",
            "280",
        )
        equation.set_width(FRAME_WIDTH - 1)
        equation.move_to(UP)
        words = VGroup(
            Text("Filter out\nevens"),
            Text("Filter out\nmultiples of 5"),
            Text("Filter out\nmultiples of 71"),
        )
        vects = [DOWN, UP, DOWN]
        colors = [RED, BLUE, LIGHT_PINK]
        for part, word, vect, color in zip(equation[2:5], words, vects, colors):
            brace = Brace(part, vect)
            brace.stretch(0.8, 0)
            word.brace = brace
            word.next_to(brace, vect)
            part.set_color(color)
            word.set_color(color)
            word.set_stroke(BLACK, 5, background=True)
        equation.set_stroke(BLACK, 5, background=True)

        etf_label = Text("Euler's totient function")
        etf_label.to_corner(UL)
        arrow = Arrow(etf_label.get_bottom(), equation[0][0].get_top())
        equation[0][0].set_color(YELLOW)
        etf_label.set_color(YELLOW)

        rect = FullScreenFadeRectangle(fill_opacity=0.9)
        self.play(
            FadeIn(rect),
            FadeIn(equation, shift=DOWN),
            FadeIn(etf_label),
            GrowArrow(arrow),
        )
        self.wait()
        for word in words:
            self.play(
                FadeIn(word),
                GrowFromCenter(word.brace),
            )
            self.wait()
