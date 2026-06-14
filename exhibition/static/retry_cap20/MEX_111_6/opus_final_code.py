from manim import *


class GeneratedScene(Scene):
    def construct(self):
        formula = MathTex(r"\sqrt{2022}").scale(1.2)
        subtitle = Text("介於哪兩數之間?", font_size=32)
        title = VGroup(formula, subtitle).arrange(RIGHT, buff=0.3)
        title.to_edge(UP)
        self.play(Write(formula), FadeIn(subtitle))
        self.wait(0.5)

        options = VGroup(
            Text("(A) 25, 30", font_size=28),
            Text("(B) 30, 35", font_size=28),
            Text("(C) 35, 40", font_size=28),
            Text("(D) 40, 45", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        options.to_edge(LEFT).shift(DOWN * 0.3)
        self.play(LaggedStartMap(FadeIn, options, lag_ratio=0.2))
        self.wait(0.5)

        idea = Text("關鍵：找平方接近 2022 的整數", font_size=24)
        idea.to_corner(UR).shift(DOWN * 1.2 + LEFT * 0.3)
        self.play(FadeIn(idea, shift=UP))
        self.wait(0.3)

        calc = VGroup(
            MathTex(r"40^2 = 1600"),
            MathTex(r"44^2 = 1936"),
            MathTex(r"45^2 = 2025"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.8)
        calc.next_to(idea, DOWN, buff=0.5).align_to(idea, LEFT)

        for c in calc:
            self.play(Write(c))
            self.wait(0.3)

        highlight = SurroundingRectangle(calc[2], color=YELLOW)
        compare = MathTex(r"1936 < 2022 < 2025").scale(0.8)
        compare.next_to(calc, DOWN, buff=0.5).align_to(calc, LEFT)
        self.play(Create(highlight), Write(compare))
        self.wait(0.5)

        conclude = MathTex(r"44 < \sqrt{2022} < 45 \approx 44.97").scale(0.85)
        conclude.next_to(compare, DOWN, buff=0.5).align_to(compare, LEFT)
        self.play(TransformFromCopy(compare, conclude))
        self.wait(0.5)

        ans_box = SurroundingRectangle(options[3], color=GREEN, buff=0.15)
        self.play(
            Create(ans_box),
            options[3].animate.set_color(GREEN),
        )
        self.play(
            *[options[i].animate.set_opacity(0.4) for i in range(3)]
        )
        self.wait(0.5)

        answer = Text("答案：(D) 40, 45", color=GREEN, font_size=32)
        answer.to_edge(DOWN)
        self.play(FadeIn(answer, shift=UP))
        self.wait(2)