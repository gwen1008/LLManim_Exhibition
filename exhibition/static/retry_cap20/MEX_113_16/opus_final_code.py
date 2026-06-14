from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("全球平均氣溫預估", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Problem statement
        info1_text = Text("趨勢：每十年上升", font_size=28)
        info1_math = MathTex(r"0.08^\circ C", font_size=32)
        info1 = VGroup(info1_text, info1_math).arrange(RIGHT, buff=0.2)
        info2_text = Text("2020 年氣溫 =", font_size=28)
        info2_math = MathTex(r"14.88^\circ C", font_size=32)
        info2 = VGroup(info2_text, info2_math).arrange(RIGHT, buff=0.2)
        info1.next_to(title, DOWN, buff=0.5)
        info2.next_to(info1, DOWN, buff=0.3)
        self.play(FadeIn(info1, shift=UP))
        self.play(FadeIn(info2, shift=UP))
        self.wait(1)

        # Convert per-decade to per-year
        step1_label = Text("每年上升幅度：", font_size=28, color=YELLOW)
        step1 = MathTex(r"\frac{0.08}{10} = 0.008^\circ C", font_size=36)
        step1_label.next_to(info2, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        step1.next_to(step1_label, RIGHT, buff=0.3)
        self.play(Write(step1_label))
        self.play(Write(step1))
        self.wait(1)

        # Build the formula
        step2_label = Text("第 x 年後的氣溫：", font_size=28, color=YELLOW)
        step2_label.next_to(step1_label, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.play(Write(step2_label))

        formula = MathTex(
            r"T", r"=", r"14.88", r"+", r"0.008", r"\cdot", r"x",
            font_size=40,
        )
        formula.next_to(step2_label, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # Highlight components
        base_box = SurroundingRectangle(formula[2], color=GREEN, buff=0.1)
        rate_box = SurroundingRectangle(formula[4], color=RED, buff=0.1)
        self.play(Create(base_box))
        self.wait(0.5)
        self.play(Create(rate_box))
        self.wait(1)

        # Final answer
        result = MathTex(r"14.88 + 0.008x", font_size=48, color=GOLD)
        result.next_to(formula, DOWN, buff=0.8)
        ans_label = Text("答案：(B)", font_size=36, color=GOLD)
        ans_label.next_to(result, DOWN, buff=0.3)
        self.play(
            FadeOut(base_box),
            FadeOut(rate_box),
            TransformFromCopy(formula, result),
        )
        self.play(Write(ans_label))
        self.wait(2)