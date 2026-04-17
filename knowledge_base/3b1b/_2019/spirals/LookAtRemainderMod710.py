# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個數學等式 n = 710k + r，並用箭頭和標籤分別突出顯示 n 和 r 的含義。



from manim import *
class LookAtRemainderMod710(Scene):
    def construct(self):
        t2c = {
            "n": YELLOW,
            "r": GREEN
        }
        equation = MathTex(
            "n", "=", "710", "k", "+", "r",
            tex_to_color_map=t2c,
        )
        equation.scale(1.5)

        n_arrow = Arrow(start=DOWN, end=UP).next_to(equation.get_part_by_tex("n"), DOWN)
        r_arrow = Arrow(start=DOWN, end=UP).next_to(equation.get_part_by_tex("r"), DOWN)
        n_arrow.set_color(t2c["n"])
        r_arrow.set_color(t2c["r"])

        n_label = TexText("Some\\\\number")
        r_label = TexText("Remainder")
        VGroup(n_label, r_label).scale(1.5)
        n_label.next_to(n_arrow, DOWN)
        n_label.set_color(n_arrow.get_color())
        r_label.next_to(r_arrow, DOWN)
        r_label.set_color(r_arrow.get_color())

        self.add(equation)
        self.play(
            FadeIn(n_label, shift=UP),
            Create(n_arrow),
        )
        self.wait()
        self.play(
            FadeIn(r_label, shift=DOWN),
            Create(r_arrow),
        )
        self.wait()
