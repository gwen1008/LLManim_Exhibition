from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("三次多項式與等差數列根", font_size=40)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            MathTex(r"a \in \{-6,-4,-2,2,4,6\}", font_size=34),
            MathTex(r"f(x) = a(x-r_1)(x-r_2)(x-r_3)", font_size=34),
        ).arrange(DOWN, buff=0.35).next_to(title, DOWN, buff=0.4)
        self.play(Write(setup[0]))
        self.play(Write(setup[1]))
        self.wait(0.5)

        roots = MathTex(
            r"r_1=-7,\quad r_2=-7+a,\quad r_3=-7+2a",
            font_size=34,
        ).next_to(setup, DOWN, buff=0.4)
        self.play(Write(roots))
        self.wait(0.5)

        f0 = VGroup(
            MathTex(r"f(0)=a(7)(7-a)(7-2a)", font_size=36),
            MathTex(r"f(0)>0 \iff a(7-a)(7-2a)>0", font_size=36),
        ).arrange(DOWN, buff=0.35).next_to(roots, DOWN, buff=0.45)
        self.play(Write(f0[0]))
        self.play(Write(f0[1]))
        self.wait(0.8)

        self.play(
            FadeOut(setup), FadeOut(roots), FadeOut(f0[0]),
            f0[1].animate.next_to(title, DOWN, buff=0.4),
        )
        self.wait(0.3)

        data = [
            (-6, r"(-6)(13)(19)<0", False),
            (-4, r"(-4)(11)(15)<0", False),
            (-2, r"(-2)(9)(11)<0", False),
            (2,  r"(2)(5)(3)=30>0", True),
            (4,  r"(4)(3)(-1)=-12<0", False),
            (6,  r"(6)(1)(-5)=-30<0", False),
        ]

        rows = VGroup()
        for a, expr, ok in data:
            mark = r"\checkmark" if ok else r"\times"
            color = GREEN if ok else RED
            row = MathTex(
                rf"a={a}:\ {expr}\ {mark}",
                font_size=32,
            ).set_color(color)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(f0[1], DOWN, buff=0.5)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.5)

        box = SurroundingRectangle(rows[3], color=YELLOW, buff=0.12)
        self.play(Create(box))
        self.wait(0.5)

        ans = MathTex(r"\Rightarrow \text{只有 } a=2,\ \text{共 } 1 \text{ 個}", font_size=40, color=YELLOW)
        ans.next_to(rows, DOWN, buff=0.5)
        self.play(Write(ans))
        self.wait(2)