# Source: 3b1b/_2018/for_flammy.py
# Description: [3b1b translated] 展示積分符號的視覺化解釋，從環的面積逐步推導到球面面積公式的過程。



from manim import *
class IntegralSymbols(Scene):
    def construct(self):
        int_sign = MathTex("\\displaystyle \\int")
        int_sign.set_height(1.5)
        int_sign.move_to(5 * LEFT)

        circumference, times, thickness = ctt = TexText(
            "circumference", "$\\times$", "thickness"
        )
        circumference.set_color(MAROON_B)
        ctt.next_to(int_sign, RIGHT, buff=SMALL_BUFF)
        area_brace = Brace(ctt, DOWN)
        area_text = area_brace.get_text("Area of a ring")

        all_rings = TexText("All rings")
        all_rings.scale(0.5)
        all_rings.next_to(int_sign, DOWN, buff=SMALL_BUFF)
        all_rings.shift(SMALL_BUFF * LEFT)

        circum_formula = MathTex(
            "2\\pi", "R\\cos(\\theta)",
        )
        circum_formula[1].set_color(RED)
        circum_formula.move_to(circumference)
        circum_brace = Brace(circum_formula, UP)

        R_dtheta = MathTex("R \\, d\\theta")
        R_dtheta.move_to(thickness, LEFT)
        R_dtheta_brace = Brace(R_dtheta, UP)

        zero, pi_halves = bounds = MathTex("0", "\\pi / 2")
        bounds.scale(0.5)
        zero.move_to(all_rings)
        pi_halves.next_to(int_sign, UP, buff=SMALL_BUFF)
        pi_halves.shift(SMALL_BUFF * RIGHT)

        self.add(int_sign)
        self.play(
            GrowFromCenter(area_brace),
            FadeIn(area_text, shift=UP),
        )
        self.wait()
        self.play(FadeIn(circumference, shift=DOWN))
        self.play(
            FadeIn(thickness, shift=DOWN),
            Write(times)
        )
        self.play(Write(all_rings))
        self.wait()

        self.play(
            circumference.animate.next_to(circum_brace, UP, buff=MED_SMALL_BUFF),
            circumference.animate.shift(SMALL_BUFF * UR),
            GrowFromCenter(circum_brace),
        )
        self.play(FadeIn(circum_formula, shift=UP))
        self.wait()
        self.play(
            thickness.animate.next_to(circumference, RIGHT, buff=MED_SMALL_BUFF),
            GrowFromCenter(R_dtheta_brace),
            area_brace.animate.stretch(0.84, 0, about_edge=LEFT),
            MaintainPositionRelativeTo(area_text, area_brace),
        )
        self.play(FadeIn(R_dtheta, shift=UP))
        self.wait()
        self.play(ReplacementTransform(all_rings, bounds))
        self.wait()

        # RHS
        rhs = MathTex(
            "\\displaystyle =", "2\\pi R^2", "\\int_0^{\\pi / 2}",
            "\\cos(\\theta)", "d\\theta",
        )
        rhs.set_color_by_tex("cos", RED)
        rhs.next_to(R_dtheta, RIGHT)
        int_brace = Brace(rhs[2:], DOWN)
        q_marks = int_brace.get_text("???")
        one = MathTex("1")
        one.move_to(q_marks)

        self.play(FadeIn(rhs, shift=4 * LEFT))
        self.wait()
        self.play(Create(SurroundingRectangle(rhs[1])))
        self.play(FadeOut(SurroundingRectangle(rhs[1])))
        self.wait()
        self.play(Create(SurroundingRectangle(rhs[2:])))
        self.play(FadeOut(SurroundingRectangle(rhs[2:])))
        self.wait()
        self.play(
            GrowFromCenter(int_brace),
            LaggedStart(*[FadeIn(mark, shift=UP) for mark in q_marks])
        )
        self.wait()
        self.play(ReplacementTransform(q_marks, one))
        self.wait()
