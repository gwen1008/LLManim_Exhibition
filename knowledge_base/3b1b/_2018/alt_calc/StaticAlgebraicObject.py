# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個無限連分式從中心生長出來，然後縮小變灰，最後標題替換為多項式方程。



from manim import *
class StaticAlgebraicObject(Scene):
    def construct(self):
        frac = get_phi_continued_fraction(40)
        frac.set_width(FRAME_WIDTH - 1)
        # frac.shift(2 * DOWN)
        frac.to_edge(DOWN)
        frac.set_stroke(WHITE, width=0.5)

        title = MathTex(
            "\\infty \\ne \\lim",
            tex_to_color_map={"\\ne": RED}
        )
        title.scale(1.5)
        title.to_edge(UP)

        polynomial = MathTex("x^2 - x - 1 = 0")
        polynomial.move_to(title)

        self.add(title)
        self.play(LaggedStartMap(
            GrowFromCenter, frac,
            lag_ratio=0.1,
            run_time=3
        ))
        self.wait()
        factor = 1.1
        self.play(frac.animate.scale(factor), run_time=0.5)
        self.play(
            frac.animate.scale(1 / factor).set_color(GREY_B),
            run_time=0.5, rate_func=lambda t: t**5,
        )
        self.wait()
        self.play(
            FadeOut(title),
            FadeIn(polynomial)
        )
        self.wait(2)
