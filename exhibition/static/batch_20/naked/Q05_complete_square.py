from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("L'Hôpital 法則求極限", include_underline=True)
        self.play(Write(title))
        self.wait(0.5)

        problem = MathTex(
            r"\lim_{x \to 0} \frac{\sin x - x}{x^3}"
        ).scale(1.2)
        problem.next_to(title, DOWN, buff=0.6)
        self.play(Write(problem))
        self.wait(1)

        # Step 0: check indeterminate form
        check0 = MathTex(
            r"\frac{\sin 0 - 0}{0^3} = \frac{0}{0}",
            r"\;\Rightarrow\; \text{不定型}"
        )
        check0.set_color_by_tex("0}{0", YELLOW)
        check0.next_to(problem, DOWN, buff=0.5)
        self.play(Write(check0))
        self.wait(1.5)

        self.play(
            FadeOut(check0),
            problem.animate.scale(0.75).next_to(title, DOWN, buff=0.3),
        )

        def make_step(label_text, expr_tex, check_tex, color):
            label = Tex(label_text).scale(0.8).set_color(color)
            expr = MathTex(*expr_tex).scale(1.0)
            check = MathTex(check_tex).scale(0.9).set_color(YELLOW)
            group = VGroup(label, expr, check).arrange(DOWN, buff=0.35)
            return group, label, expr, check

        # Step 1: first derivative
        s1, l1, e1, c1 = make_step(
            "第一次微分（分子分母同時微分）",
            [r"\frac{(\sin x - x)'}{(x^3)'}", r"=", r"\frac{\cos x - 1}{3x^2}"],
            r"\frac{\cos 0 - 1}{3\cdot 0^2} = \frac{0}{0}\;\Rightarrow\;\text{仍為不定型}",
            BLUE,
        )
        s1.next_to(problem, DOWN, buff=0.5)
        self.play(Write(l1))
        self.play(Write(e1))
        self.wait(0.8)
        self.play(Write(c1))
        self.wait(1.5)

        self.play(s1.animate.scale(0.7).to_edge(LEFT).shift(UP * 1.5))

        # Step 2: second derivative
        s2, l2, e2, c2 = make_step(
            "第二次微分",
            [r"\frac{(\cos x - 1)'}{(3x^2)'}", r"=", r"\frac{-\sin x}{6x}"],
            r"\frac{-\sin 0}{6\cdot 0} = \frac{0}{0}\;\Rightarrow\;\text{仍為不定型}",
            GREEN,
        )
        s2.move_to(ORIGIN).shift(DOWN * 0.3)
        self.play(Write(l2))
        self.play(Write(e2))
        self.wait(0.8)
        self.play(Write(c2))
        self.wait(1.5)

        self.play(s2.animate.scale(0.7).to_edge(LEFT).shift(DOWN * 0.5))

        # Step 3: third derivative
        s3, l3, e3, c3 = make_step(
            "第三次微分",
            [r"\frac{(-\sin x)'}{(6x)'}", r"=", r"\frac{-\cos x}{6}"],
            r"\frac{-\cos 0}{6} = \frac{-1}{6}\;\Rightarrow\;\text{可直接代入！}",
            ORANGE,
        )
        s3.move_to(RIGHT * 2.5)
        self.play(Write(l3))
        self.play(Write(e3))
        self.wait(0.8)
        self.play(Write(c3))
        self.wait(1.5)

        # Final answer box
        answer = MathTex(
            r"\lim_{x \to 0} \frac{\sin x - x}{x^3} = -\frac{1}{6}"
        ).scale(1.1)
        answer.next_to(s3, DOWN, buff=0.6).shift(RIGHT * 0)
        box = SurroundingRectangle(answer, color=RED, buff=0.25)
        self.play(Write(answer))
        self.play(Create(box))
        self.wait(2)