from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"y = -2x - 6", font_size=56, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        question = Text("通過下列哪一個點？", font_size=32)
        question.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(question))
        self.wait(0.5)

        options = VGroup(
            MathTex(r"(A)\ (-4,\ 1)", font_size=36),
            MathTex(r"(B)\ (-4,\ 2)", font_size=36),
            MathTex(r"(C)\ (-4,\ -1)", font_size=36),
            MathTex(r"(D)\ (-4,\ -2)", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        options.next_to(question, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(LaggedStart(*[FadeIn(o) for o in options], lag_ratio=0.3))
        self.wait(0.5)

        # 計算過程，放在右側
        calc = VGroup(
            Text("代入 x = -4", font_size=30),
            MathTex(r"y = -2(-4) - 6", font_size=40),
            MathTex(r"y = 8 - 6", font_size=40),
            MathTex(r"y = 2", font_size=44, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        calc.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.3)

        box = SurroundingRectangle(calc, color=BLUE, buff=0.3)
        self.play(Create(box))
        for line in calc:
            self.play(Write(line), run_time=0.8)
        self.wait(0.5)

        # 標出答案 B
        answer_box = SurroundingRectangle(options[1], color=GREEN, buff=0.15)
        self.play(
            options[1].animate.set_color(GREEN),
            Create(answer_box),
        )
        self.play(Indicate(options[1], color=GREEN, scale_factor=1.2))
        self.wait(0.5)

        conclusion = MathTex(r"(-4,\ 2)", font_size=48, color=GREEN)
        conclusion.next_to(calc, DOWN, buff=0.5)
        result = Text("即點 (-4, 2)，選 (B)", font_size=30, color=GREEN)
        result.next_to(calc, DOWN, buff=0.5)
        self.play(Write(result))
        self.wait(2)