from manim import *

class OrderOfOperationsComplexArithmetic(Scene):
    """
    PEMDAS order of operations without bracket removal 四則運算算則 不含去括號: Visualizes the step-by-step calculation of (-48) / (-6) * (-2) - (13 - 25) * 3, emphasizing order of operations.
    """
    def construct(self):
        # Initial expression to be calculated
        expr0_str = "(-48) \\div (-6) \\times (-2) - (13 - 25) \\times 3"
        expr0 = MathTex(expr0_str).scale(0.9).to_edge(UP + LEFT)
        self.play(Write(expr0))
        self.wait(1)

        # Step 1: Calculate (-48) \div (-6)
        # MathTex tokenization: `(-48)` is tokens 0,1,2; `\div` is token 3; `(-6)` is tokens 4,5,6.
        # So, `(-48) \div (-6)` corresponds to `expr0[0:7]`.
        highlight_part1 = expr0[0:7]
        rect1 = SurroundingRectangle(highlight_part1, color=BLUE)
        self.play(Create(rect1))
        self.wait(0.5)

        calc_text1 = MathTex("(-48) \\div (-6) = 8").next_to(expr0, DOWN, buff=0.8).align_to(expr0, LEFT)
        self.play(Write(calc_text1))
        self.wait(1)

        # Replace the calculated part with its result in the main expression
        expr1_str = "8 \\times (-2) - (13 - 25) \\times 3"
        expr1 = MathTex(expr1_str).scale(0.9).move_to(expr0.get_center())
        self.play(
            TransformMatchingTex(expr0, expr1, transform_mobject=rect1),
            FadeOut(calc_text1)
        )
        self.wait(1)

        # Step 2: Calculate 8 \times (-2)
        # expr1 tokens: `8` is 0; `\times` is 1; `(-2)` is 2,3,4.
        # So, `8 \times (-2)` corresponds to `expr1[0:5]`.
        highlight_part2 = expr1[0:5]
        rect2 = SurroundingRectangle(highlight_part2, color=BLUE)
        self.play(Create(rect2))
        self.wait(0.5)

        calc_text2 = MathTex("8 \\times (-2) = -16").next_to(expr1, DOWN, buff=0.8).align_to(expr1, LEFT)
        self.play(Write(calc_text2))
        self.wait(1)

        # Replace the calculated part
        expr2_str = "-16 - (13 - 25) \\times 3"
        expr2 = MathTex(expr2_str).scale(0.9).move_to(expr1.get_center())
        self.play(
            TransformMatchingTex(expr1, expr2, transform_mobject=rect2),
            FadeOut(calc_text2)
        )
        self.wait(1)

        # Step 3: Calculate (13 - 25)
        # expr2 tokens: `(` is 2; `13` is 3; `-` is 4; `25` is 5; `)` is 6.
        # So, `(13 - 25)` corresponds to `expr2[2:7]`.
        highlight_part3 = expr2[2:7]
        rect3 = SurroundingRectangle(highlight_part3, color=BLUE)
        self.play(Create(rect3))
        self.wait(0.5)

        calc_text3 = MathTex("13 - 25 = -12").next_to(expr2, DOWN, buff=0.8).align_to(expr2, LEFT)
        self.play(Write(calc_text3))
        self.wait(1)

        # Replace the calculated part
        expr3_str = "-16 - (-12) \\times 3"
        expr3 = MathTex(expr3_str).scale(0.9).move_to(expr2.get_center())
        self.play(
            TransformMatchingTex(expr2, expr3, transform_mobject=rect3),
            FadeOut(calc_text3)
        )
        self.wait(1)

        # Step 4: Calculate (-12) \times 3
        # expr3 tokens: `(` is 2; `-12` is 3; `)` is 4; `\times` is 5; `3` is 6.
        # So, `(-12) \times 3` corresponds to `expr3[2:7]`.
        highlight_part4 = expr3[2:7]
        rect4 = SurroundingRectangle(highlight_part4, color=BLUE)
        self.play(Create(rect4))
        self.wait(0.5)

        calc_text4 = MathTex("(-12) \\times 3 = -36").next_to(expr3, DOWN, buff=0.8).align_to(expr3, LEFT)
        self.play(Write(calc_text4))
        self.wait(1)

        # Replace the calculated part
        expr4_str = "-16 - (-36)"
        expr4 = MathTex(expr4_str).scale(0.9).move_to(expr3.get_center())
        self.play(
            TransformMatchingTex(expr3, expr4, transform_mobject=rect4),
            FadeOut(calc_text4)
        )
        self.wait(1)

        # Step 5: Calculate -16 - (-36)
        # Highlight the entire expression for the final step
        highlight_part5 = expr4
        rect5 = SurroundingRectangle(highlight_part5, color=BLUE)
        self.play(Create(rect5))
        self.wait(0.5)

        # Show the full calculation for the final step
        expr4_expanded_str = "-16 - (-36) = -16 + 36 = 20"
        expr4_expanded = MathTex(expr4_expanded_str).scale(0.9).move_to(expr4.get_center())
        self.play(
            TransformMatchingTex(expr4, expr4_expanded, transform_mobject=rect5)
        )
        self.wait(1)

        # Highlight the final answer
        final_answer_part = expr4_expanded[-1] # The '20' token
        final_rect = SurroundingRectangle(final_answer_part, color=GREEN, buff=0.2)
        self.play(Create(final_rect))
        self.wait(2)