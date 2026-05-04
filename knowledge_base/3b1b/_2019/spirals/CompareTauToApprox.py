# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示兩個數學等式（2π 和 710/113）及其近似值，並將近似值的前八位數字標記為紅色。



from manim import *
class CompareTauToApprox(Scene):
    def construct(self):
        eqs = VGroup(
            MathTex("2\\pi", "=", "{:.10}\\dots".format(TAU)),
            MathTex("\\frac{710}{113}", "=", "{:.10}\\dots".format(710 / 113)),
        )
        eqs.arrange(DOWN, buff=LARGE_BUFF)
        eqs[1].shift((eqs[0][2].get_left()[0] - eqs[1][2].get_left()[0]) * RIGHT)

        eqs.generate_target()
        for eq in eqs.target:
            eq[2][:8].set_color(RED)
            eq.set_stroke(BLACK, 8, background=True)

        self.play(LaggedStart(
            FadeIn(eqs[0], shift=DOWN),
            FadeIn(eqs[1], shift=UP),
        ))
        self.play(MoveToTarget(eqs))
        self.wait()
