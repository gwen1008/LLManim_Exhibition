from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("財神廟抽發財金 期望值", font="PingFang SC", color=YELLOW).scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            Text("抽兩次籤，每次「吉」、「祥」機率皆為 1/3", font="PingFang SC").scale(0.5),
            Text("兩次都「吉」→ 180 元", font="PingFang SC").scale(0.5),
            Text("兩次都「祥」→ 90 元", font="PingFang SC").scale(0.5),
            Text("其餘情況 → 無獎金", font="PingFang SC").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        setup.next_to(title, DOWN, buff=0.5)
        for line in setup:
            self.play(FadeIn(line, shift=RIGHT * 0.3))
            self.wait(0.2)
        self.wait(0.5)

        self.play(setup.animate.scale(0.85).to_edge(LEFT, buff=0.5))

        # Probabilities (use Text for Chinese, MathTex for math)
        def prob_row(label_text):
            lbl = Text(label_text, font="PingFang SC").scale(0.5)
            eq = MathTex(r"= \frac{1}{3}\times\frac{1}{3} = \frac{1}{9}").scale(0.6)
            row = VGroup(lbl, eq).arrange(RIGHT, buff=0.2)
            return row

        p_ji = prob_row("P(吉,吉)")
        p_xiang = prob_row("P(祥,祥)")
        probs = VGroup(p_ji, p_xiang).arrange(DOWN, buff=0.5)
        probs.to_edge(RIGHT, buff=0.7).shift(UP * 1.2)

        self.play(Write(p_ji))
        self.wait(0.4)
        self.play(Write(p_xiang))
        self.wait(0.6)

        # Expectation
        exp_label = VGroup(
            MathTex(r"E = \sum").scale(0.7),
            Text("(獎金) × (機率)", font="PingFang SC").scale(0.5),
        ).arrange(RIGHT, buff=0.2)
        exp_label.next_to(probs, DOWN, buff=0.8)
        self.play(Write(exp_label))
        self.wait(0.4)

        exp1 = MathTex(
            r"E = 180\times\frac{1}{9} + 90\times\frac{1}{9}"
        ).scale(0.75)
        exp1.next_to(exp_label, DOWN, buff=0.5)
        self.play(Write(exp1))
        self.wait(0.5)

        exp2 = MathTex(r"E = 20 + 10").scale(0.8)
        exp2.next_to(exp1, DOWN, buff=0.5)
        self.play(Write(exp2))
        self.wait(0.4)

        result = MathTex(r"E = 30", color=YELLOW).scale(1.0)
        result.next_to(exp2, DOWN, buff=0.5)
        box = SurroundingRectangle(result, color=YELLOW, buff=0.2)
        self.play(Write(result))
        self.play(Create(box))
        self.wait(0.5)

        final = Text("期望值為 30 元", font="PingFang SC", color=GREEN).scale(0.7)
        final.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(final, shift=UP * 0.3))
        self.wait(2)