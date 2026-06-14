from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("等差 × 等比：求公比", font_size=42)
        self.play(Write(title))
        self.wait(0.5)

        # Given conditions
        f_def = MathTex(r"f(x) = a^{x},\quad a>0").scale(0.9)
        f_def.next_to(title, DOWN, buff=0.5)
        self.play(Write(f_def))
        self.wait(0.5)

        ap = MathTex(
            r"c_1,\ c_2,\ c_3\ \text{公差}=\tfrac{10}{3}"
        ).scale(0.8)
        gp = MathTex(
            r"f(c_1),\ f(c_2),\ f(c_3)\ \text{公比}=4"
        ).scale(0.8)
        conds = VGroup(ap, gp).arrange(DOWN, buff=0.4)
        conds.next_to(f_def, DOWN, buff=0.5)
        self.play(FadeIn(ap, shift=RIGHT))
        self.play(FadeIn(gp, shift=RIGHT))
        self.wait(0.6)

        # Key relation
        step1 = MathTex(
            r"\frac{f(c_2)}{f(c_1)} = a^{\,c_2-c_1} = a^{10/3} = 4"
        ).scale(0.85)
        step1.next_to(conds, DOWN, buff=0.6)
        self.play(Write(step1))
        self.wait(0.6)

        box = SurroundingRectangle(step1, color=YELLOW)
        self.play(Create(box))
        self.wait(0.5)

        # Solve for a
        step2 = MathTex(r"a^{10} = 4^{3} = 64").scale(0.85)
        step3 = MathTex(r"a = 64^{1/10} = 2^{3/5}").scale(0.85)
        sols = VGroup(step2, step3).arrange(DOWN, buff=0.35)
        sols.next_to(step1, DOWN, buff=0.55)

        self.play(FadeOut(box))
        self.play(
            VGroup(title, f_def, conds, step1).animate.scale(0.8).to_edge(UP),
        )
        sols.next_to(step1, DOWN, buff=0.55)
        self.play(Write(step2))
        self.wait(0.3)
        self.play(Write(step3))
        self.wait(0.6)

        # Target ratio
        target = MathTex(
            r"f(10),\ f(8),\ f(6)\ \text{的公比}"
        ).scale(0.8)
        ratio = MathTex(
            r"r = \frac{f(8)}{f(10)} = a^{8-10} = a^{-2}"
        ).scale(0.85)
        final = MathTex(
            r"= \left(2^{3/5}\right)^{-2} = 2^{-6/5}"
        ).scale(0.9).set_color(YELLOW)

        grp = VGroup(target, ratio, final).arrange(DOWN, buff=0.4)
        grp.next_to(sols, DOWN, buff=0.5)

        self.play(FadeIn(target, shift=UP))
        self.play(Write(ratio))
        self.wait(0.4)
        self.play(Write(final))

        ans_box = SurroundingRectangle(final, color=YELLOW, buff=0.2)
        self.play(Create(ans_box))
        self.wait(2)