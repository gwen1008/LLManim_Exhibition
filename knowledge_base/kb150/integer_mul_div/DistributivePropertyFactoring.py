from manim import *

class DistributivePropertyFactoring(Scene):
    """
    Integer multiplication division 整數乘除: Visualizes factoring out a common integer (-13) using the distributive property for (-13)*24 - (-13)*(-76).
    """
    def construct(self):
        # 1. Initial Expression
        title = Text("Distributive Property: Factoring Common Factor", font_size=36).to_edge(UP)
        self.play(Write(title))

        initial_expression_str = "(-13) \\times 24 - (-13) \\times (-76)"
        initial_expression = MathTex(initial_expression_str, font_size=48)
        initial_expression.to_center().shift(UP * 1.5)
        self.play(Write(initial_expression))
        self.wait(1)

        # 2. Identify Common Factor
        common_factor_text = Text("Identify common factor:", font_size=30).next_to(initial_expression, DOWN, buff=0.8).align_to(initial_expression, LEFT)
        self.play(Write(common_factor_text))

        # Highlight (-13) in both terms
        # MathTex structure: ( -13 ) \times 24 - ( -13 ) \times ( -76 )
        # Indices:           0  1   2  3      4   5  6  7   8  9      10 11 12
        common_factor_1 = initial_expression[1]
        common_factor_2 = initial_expression[7]

        self.play(
            common_factor_1.animate.set_color(YELLOW),
            common_factor_2.animate.set_color(YELLOW),
            Indicate(common_factor_1),
            Indicate(common_factor_2)
        )
        self.wait(1)

        common_factor_value = MathTex("-13", color=YELLOW, font_size=36).next_to(common_factor_text, RIGHT)
        self.play(Write(common_factor_value))
        self.wait(1)

        # 3. Apply Distributive Property (Factor out -13)
        distributive_law_text = Text("Apply Distributive Property (reverse):", font_size=30).next_to(common_factor_text, DOWN, buff=0.8).align_to(common_factor_text, LEFT)
        self.play(
            FadeOut(common_factor_text, shift=UP),
            FadeOut(common_factor_value, shift=UP),
            FadeIn(distributive_law_text, shift=UP)
        )

        factored_expression_str = "(-13) \\times [ 24 - (-76) ]"
        factored_expression = MathTex(factored_expression_str, font_size=48)
        factored_expression.align_to(initial_expression, LEFT)
        factored_expression.next_to(distributive_law_text, DOWN, buff=0.8)

        # Transform initial expression to factored expression
        self.play(
            TransformMatchingTex(initial_expression, factored_expression),
            FadeOut(distributive_law_text)
        )
        self.wait(1.5)

        # 4. Simplify Inside Brackets
        simplify_brackets_text = Text("Simplify inside brackets:", font_size=30).next_to(factored_expression, DOWN, buff=0.8).align_to(factored_expression, LEFT)
        self.play(Write(simplify_brackets_text))

        # Highlight the bracketed part
        bracket_content = factored_expression[5:10] # [ 24 - (-76) ]
        self.play(Indicate(bracket_content, color=BLUE))
        self.wait(0.5)

        step1_bracket = MathTex("24 - (-76)", font_size=40).next_to(simplify_brackets_text, RIGHT, buff=0.5)
        self.play(Write(step1_bracket))
        self.wait(0.5)

        step2_bracket = MathTex("= 24 + 76", font_size=40).next_to(step1_bracket, RIGHT, buff=0.5)
        self.play(TransformMatchingTex(step1_bracket, step2_bracket))
        self.wait(0.5)

        step3_bracket = MathTex("= 100", font_size=40).next_to(step2_bracket, RIGHT, buff=0.5)
        self.play(TransformMatchingTex(step2_bracket, step3_bracket))
        self.wait(1)

        # Substitute 100 back into the expression
        new_factored_expression_str = "(-13) \\times 100"
        new_factored_expression = MathTex(new_factored_expression_str, font_size=48)
        new_factored_expression.align_to(factored_expression, LEFT)
        new_factored_expression.next_to(simplify_brackets_text, DOWN, buff=0.8)

        self.play(
            FadeOut(simplify_brackets_text, shift=UP),
            FadeOut(step3_bracket, shift=UP),
            TransformMatchingTex(factored_expression, new_factored_expression)
        )
        self.wait(1)

        # 5. Final Multiplication
        final_calculation_text = Text("Final calculation:", font_size=30).next_to(new_factored_expression, DOWN, buff=0.8).align_to(new_factored_expression, LEFT)
        self.play(Write(final_calculation_text))

        final_answer = MathTex("= -1300", font_size=48, color=GREEN).next_to(new_factored_expression, RIGHT, buff=0.5)
        self.play(Write(final_answer))
        self.wait(1.5)

        # Highlight the final answer
        final_answer_group = VGroup(new_factored_expression, final_answer)
        box = SurroundingRectangle(final_answer_group, color=GREEN, buff=0.2)
        self.play(Create(box))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(final_calculation_text),
            FadeOut(final_answer_group),
            FadeOut(box)
        )
        self.wait(0.5)