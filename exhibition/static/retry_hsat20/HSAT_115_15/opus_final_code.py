from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("等差數列與共線問題", font_size=40)
        self.play(Write(title))
        title.to_edge(UP)
        self.wait(0.5)

        problem = VGroup(
            VGroup(
                MathTex(r"a, b, c"), Text("成等差,", font_size=28), MathTex(r"a<b<c")
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                MathTex(r"(a,\log 3a),\ (b,\log 4b),\ (c,\log 6c)"),
                Text("共線", font_size=28),
            ).arrange(RIGHT, buff=0.2),
            MathTex(r"\frac{b}{a} = ?"),
        ).arrange(DOWN, buff=0.4).scale(0.8).next_to(title, DOWN, buff=0.5)
        for p in problem:
            self.play(FadeIn(p, shift=UP * 0.2))
        self.wait(1)

        self.play(problem.animate.scale(0.7).to_edge(LEFT).shift(DOWN * 0.5))

        steps = VGroup(
            VGroup(Text("等差:", font_size=24), MathTex(r"2b = a+c")).arrange(RIGHT, buff=0.2),
            Text("共線且 b 為中點:", font_size=24),
            MathTex(r"2\log(4b) = \log(3a) + \log(6c)"),
            MathTex(r"(4b)^2 = 18ac \ \Rightarrow\ 16b^2 = 18ac"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.65)
        steps.to_edge(RIGHT).shift(UP * 1.5)

        for s in steps:
            self.play(Write(s))
            self.wait(0.5)

        self.wait(0.5)
        self.play(FadeOut(steps))

        solve = VGroup(
            MathTex(r"16\left(\tfrac{a+c}{2}\right)^2 = 18ac"),
            MathTex(r"4(a+c)^2 = 18ac"),
            MathTex(r"2a^2 - 5ac + 2c^2 = 0"),
            MathTex(r"2t^2 - 5t + 2 = 0,\ \ t=\tfrac{a}{c}"),
            VGroup(MathTex(r"t = 2"), Text("或", font_size=24), MathTex(r"t = \tfrac{1}{2}")).arrange(RIGHT, buff=0.2),
            MathTex(r"a<c \Rightarrow \tfrac{a}{c}=\tfrac{1}{2},\ c=2a"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).scale(0.6)
        solve.to_edge(RIGHT).shift(UP * 1.2)

        for s in solve:
            self.play(Write(s))
            self.wait(0.3)
        self.wait(0.5)

        final = MathTex(
            r"b=\frac{a+c}{2}=\frac{3a}{2}\ \Rightarrow\ \frac{b}{a}=\frac{3}{2}",
            font_size=44,
            color=YELLOW,
        )
        box = SurroundingRectangle(final, color=YELLOW, buff=0.3)
        group = VGroup(final, box).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(solve), Write(final))
        self.play(Create(box))
        self.wait(2)