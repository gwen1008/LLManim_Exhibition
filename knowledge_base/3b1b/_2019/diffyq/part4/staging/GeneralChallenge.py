# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一個數學挑戰場景，包含標題和傅立葉級數公式的排版與顏色標記。



from manim import *
class GeneralChallenge(Scene):
    def construct(self):
        title = Text("More ambitious challenge")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_color(BLUE)
        line = Line()
        line.match_width(title)
        line.next_to(title, DOWN, SMALL_BUFF)
        self.add(title, line)

        light_pink = interpolate_color(PINK, WHITE, 0.25)
        tex_config = {
            "tex_to_color_map": {
                "{t}": light_pink,
                "{dt}": light_pink,
                # "{0}": YELLOW,
                "{n}": YELLOW,
            }
        }
        words1 = Text(
            "In some texts, for a function $f$ on the input range $[0, 1]$,\\\\",
            "its Fourier series is presented like this:",
            alignment="",
        )
        formula1 = MathTex(
            "f(t) = {a_{0} \\over 2} + "
            "\\sum_{n = 1}^{\\infty} \\big("
            "a_{n} \\cos\\left({n} \\cdot 2\\pi {t}\\right) + "
            "b_{n} \\sin\\left({n} \\cdot 2\\pi {t}\\right) \\big)",
            **tex_config
        )
        formula1[0][6].set_color(YELLOW)
        words2 = Text("where")
        formula2 = MathTex(
            "a_{n} = 2\\int_0^1 f({t})\\cos\\left({n} \\cdot 2\\pi {t}\\right) {dt}\\\\"
            # "\\text{ and }"
            "b_{n} = 2\\int_0^1 f({t})\\sin\\left({n} \\cdot 2\\pi {t}\\right) {dt}",
            **tex_config
        )
        words3 = Text("How is this the same as what we just did?")

        prompt = VGroup(words1, formula1, words2, formula2, words3)
        prompt.arrange(DOWN, buff=MED_LARGE_BUFF)
        words2.align_to(words1, LEFT)
        words3.align_to(words1, LEFT)
        prompt.set_height(6)
        prompt.next_to(line, DOWN)

        self.add(prompt)
        self.wait()
