from manim import *

class FractionExpressionSimplification(Scene):
    """
    Fraction addition subtraction 分數加減: Visualizes simplifying a complex fraction expression by removing parentheses and grouping like terms.
    """
    def construct(self):
        # Title
        title = Text("Simplifying Fraction Expressions", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Initial Expression
        initial_expr_text = MathTex(
            r"-\left(4 \frac{2}{7} - 3 \frac{5}{9}\right) + \left(2 \frac{4}{9} - 1 \frac{5}{7}\right)"
        ).scale(0.9)
        self.play(Write(initial_expr_text))
        self.wait(1)

        # Step 2: Remove Parentheses
        step1_label = Text("Step 1: Remove Parentheses", font_size=28, color=YELLOW).to_edge(LEFT).shift(UP*2)
        self.play(Write(step1_label))
        self.wait(0.5)

        # Animate removal of first parenthesis (negative sign changes signs)
        # Animate removal of second parenthesis (positive sign keeps signs)
        expr_after_parentheses = MathTex(
            r"-4 \frac{2}{7} + 3 \frac{5}{9} + 2 \frac{4}{9} - 1 \frac{5}{7}"
        ).scale(0.9).next_to(initial_expr_text, DOWN, buff=0.8).align_to(initial_expr_text, LEFT)

        # Highlight terms that change sign
        minus_sign_1 = initial_expr_text[0][0] # -
        paren_1_open = initial_expr_text[0][1] # (
        term_4_2_7 = initial_expr_text[0][2:6] # 4 2/7
        minus_sign_2 = initial_expr_text[0][6] # -
        term_3_5_9 = initial_expr_text[0][7:11] # 3 5/9
        paren_1_close = initial_expr_text[0][11] # )

        plus_sign_3 = initial_expr_text[0][12] # +
        paren_2_open = initial_expr_text[0][13] # (
        term_2_4_9 = initial_expr_text[0][14:18] # 2 4/9
        minus_sign_4 = initial_expr_text[0][18] # -
        term_1_5_7 = initial_expr_text[0][19:23] # 1 5/7
        paren_2_close = initial_expr_text[0][23] # )

        self.play(
            FadeOut(minus_sign_1, paren_1_open, paren_1_close),
            FadeOut(plus_sign_3, paren_2_open, paren_2_close),
            term_4_2_7.animate.shift(RIGHT * 0.5), # Adjust position slightly
            term_3_5_9.animate.shift(RIGHT * 0.5), # Adjust position slightly
            term_2_4_9.animate.shift(RIGHT * 0.5), # Adjust position slightly
            term_1_5_7.animate.shift(RIGHT * 0.5), # Adjust position slightly
            ReplacementTransform(initial_expr_text, expr_after_parentheses)
        )
        self.wait(1.5)

        # Step 3: Group Like Terms
        step2_label = Text("Step 2: Group Like Terms", font_size=28, color=YELLOW).next_to(step1_label, DOWN, buff=0.5).align_to(step1_label, LEFT)
        self.play(Write(step2_label))
        self.wait(0.5)

        grouped_expr = MathTex(
            r"\left(-4 \frac{2}{7} - 1 \frac{5}{7}\right) + \left(3 \frac{5}{9} + 2 \frac{4}{9}\right)"
        ).scale(0.9).next_to(expr_after_parentheses, DOWN, buff=0.8).align_to(expr_after_parentheses, LEFT)

        # Highlight terms to be grouped
        term_4_2_7_new = expr_after_parentheses[0][0:4] # -4 2/7
        term_1_5_7_new = expr_after_parentheses[0][11:15] # -1 5/7
        term_3_5_9_new = expr_after_parentheses[0][4:8] # +3 5/9
        term_2_4_9_new = expr_after_parentheses[0][8:11] # +2 4/9

        self.play(
            term_4_2_7_new.animate.set_color(BLUE),
            term_1_5_7_new.animate.set_color(BLUE),
            term_3_5_9_new.animate.set_color(GREEN),
            term_2_4_9_new.animate.set_color(GREEN),
            FadeOut(step1_label)
        )
        self.wait(1)

        self.play(
            ReplacementTransform(expr_after_parentheses, grouped_expr)
        )
        self.wait(1.5)

        # Step 4: Calculate Denominator 7 Terms
        step3_label = Text("Step 3: Calculate 7-denominator terms", font_size=28, color=YELLOW).next_to(step2_label, DOWN, buff=0.5).align_to(step2_label, LEFT)
        self.play(Write(step3_label))
        self.wait(0.5)

        calc_7_part_1 = MathTex(r"-4 \frac{2}{7} - 1 \frac{5}{7}").scale(0.8).next_to(grouped_expr, DOWN, buff=0.8).align_to(grouped_expr, LEFT)
        self.play(TransformFromCopy(grouped_expr[0][0:9], calc_7_part_1))
        self.wait(0.5)

        calc_7_part_2 = MathTex(r"-\left(\frac{30}{7} + \frac{12}{7}\right)").scale(0.8).next_to(calc_7_part_1, DOWN, buff=0.3).align_to(calc_7_part_1, LEFT)
        self.play(TransformMatchingTex(calc_7_part_1, calc_7_part_2))
        self.wait(0.5)

        calc_7_part_3 = MathTex(r"-\frac{42}{7}").scale(0.8).next_to(calc_7_part_2, DOWN, buff=0.3).align_to(calc_7_part_2, LEFT)
        self.play(TransformMatchingTex(calc_7_part_2, calc_7_part_3))
        self.wait(0.5)

        result_7 = MathTex(r"=-6").scale(0.8).next_to(calc_7_part_3, RIGHT, buff=0.3)
        self.play(Write(result_7))
        self.wait(1)

        # Step 5: Calculate Denominator 9 Terms
        step4_label = Text("Step 4: Calculate 9-denominator terms", font_size=28, color=YELLOW).next_to(step3_label, DOWN, buff=0.5).align_to(step3_label, LEFT)
        self.play(Write(step4_label), FadeOut(step2_label))
        self.wait(0.5)

        calc_9_part_1 = MathTex(r"3 \frac{5}{9} + 2 \frac{4}{9}").scale(0.8).next_to(result_7, DOWN, buff=0.8).align_to(calc_7_part_1, LEFT)
        self.play(TransformFromCopy(grouped_expr[0][10:19], calc_9_part_1))
        self.wait(0.5)

        calc_9_part_2 = MathTex(r"\frac{32}{9} + \frac{22}{9}").scale(0.8).next_to(calc_9_part_1, DOWN, buff=0.3).align_to(calc_9_part_1, LEFT)
        self.play(TransformMatchingTex(calc_9_part_1, calc_9_part_2))
        self.wait(0.5)

        calc_9_part_3 = MathTex(r"\frac{54}{9}").scale(0.8).next_to(calc_9_part_2, DOWN, buff=0.3).align_to(calc_9_part_2, LEFT)
        self.play(TransformMatchingTex(calc_9_part_2, calc_9_part_3))
        self.wait(0.5)

        result_9 = MathTex(r"=6").scale(0.8).next_to(calc_9_part_3, RIGHT, buff=0.3)
        self.play(Write(result_9))
        self.wait(1)

        # Step 6: Final Addition
        step5_label = Text("Step 5: Final Addition", font_size=28, color=YELLOW).next_to(step4_label, DOWN, buff=0.5).align_to(step4_label, LEFT)
        self.play(Write(step5_label), FadeOut(step3_label))
        self.wait(0.5)

        final_sum_expr = MathTex(r"-6 + 6").scale(0.9).next_to(result_9, DOWN, buff=0.8).align_to(calc_7_part_1, LEFT)
        self.play(
            TransformFromCopy(result_7, final_sum_expr[0][0:2]),
            TransformFromCopy(result_9, final_sum_expr[0][2:4])
        )
        self.wait(1)

        final_answer = MathTex(r"=0").scale(1.2).next_to(final_sum_expr, RIGHT, buff=0.5)
        self.play(Write(final_answer))
        self.wait(2)

        # Clean up
        self.play(
            FadeOut(title, step4_label, step5_label),
            FadeOut(initial_expr_text, grouped_expr, calc_7_part_1, calc_7_part_2, calc_7_part_3, result_7),
            FadeOut(calc_9_part_1, calc_9_part_2, calc_9_part_3, result_9, final_sum_expr),
            final_answer.animate.move_to(ORIGIN).set_color(GREEN)
        )
        self.wait(1)