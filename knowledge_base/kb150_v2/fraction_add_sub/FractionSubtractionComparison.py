# [VISUAL REASONING]
# Number line zoomed around -0.4 to show -2/5 > -3/7
# Demonstrates that a - b < 0 when a = -3/7, b = -2/5, so option D fails the condition
from manim import *


class FractionSubtractionComparison(Scene):
    """
    分數加減: 利用 x - y > 0 ⇒ x > y 來建立分數不等式比較條件

    題目：若 a = -3/7, 求下列哪個 b 值不滿足 a - b > 0：(A) -1/2 (B) -4/5 (C) -7/10 (D) -2/5
    """
    def construct(self):
        title = Text("Identifying the Failing Option", color=WHITE, font_size=36)
        title.move_to(ORIGIN + np.array([0, 3.2, 0]))

        rule = MathTex(r"a - b > 0 \;\Longleftrightarrow\; a > b", color=YELLOW).scale(0.9)
        rule.move_to(ORIGIN + np.array([0, 2.2, 0]))

        number_line = NumberLine(
            x_range=[-0.6, -0.3, 0.05],
            length=10,
            include_numbers=False,
            color=GREY,
        )
        number_line.move_to(ORIGIN + np.array([0, 0.3, 0]))

        dot_b = Dot(point=number_line.n2p(-3/7), color=BLUE, radius=0.12)
        dot_a = Dot(point=number_line.n2p(-2/5), color=RED, radius=0.12)

        label_b = MathTex(r"-\tfrac{3}{7}", color=BLUE).scale(0.9).next_to(dot_b, DOWN, buff=0.3)
        label_a = MathTex(r"-\tfrac{2}{5}", color=RED).scale(0.9).next_to(dot_a, UP, buff=0.3)

        compare_eq = MathTex(r"-\tfrac{2}{5} > -\tfrac{3}{7}", color=GREEN).scale(0.9)
        compare_eq.move_to(ORIGIN + np.array([0, -1.3, 0]))

        conclusion = MathTex(r"a - b = -\tfrac{3}{7} - (-\tfrac{2}{5}) < 0", color=WHITE).scale(0.9)
        conclusion.move_to(ORIGIN + np.array([0, -2.2, 0]))

        final_answer = MathTex(r"\Rightarrow Answer: (D) \; -\tfrac{2}{5}", color=YELLOW).scale(0.9)
        final_answer.move_to(ORIGIN + np.array([0, -2.2, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(4.83)

        # Step 2
        anim_time_2 = 1.8 + 1.0
        self.play(Write(rule), run_time=1.8)
        self.play(Circumscribe(rule, color=YELLOW), run_time=1.0)
        self.wait(1.5)

        # Step 3
        anim_time_3 = 2.5 + 1.0
        self.play(Create(number_line), run_time=2.5)
        self.play(
            LaggedStart(
                FadeIn(dot_b), FadeIn(label_b),
                FadeIn(dot_a), FadeIn(label_a),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.wait(1.5)

        # Step 4
        anim_time_4 = 2.0 + 1.0
        self.play(Write(compare_eq), run_time=2.0)
        self.play(Indicate(dot_a, color=RED), run_time=1.0)
        self.wait(1.5)

        # Step 5
        anim_time_5 = 2.0 + 1.0 + 1.2
        self.play(Write(conclusion), run_time=2.0)
        self.play(Circumscribe(conclusion, color=GREEN), run_time=1.0)
        self.play(ReplacementTransform(conclusion, final_answer), run_time=1.2)
        self.wait(1.5)
