from manim import *

class DistributivePropertyWithNegatives(Scene):
    """
    PEMDAS order of operations without bracket removal 四則運算算則 不含去括號: Visualizes the distributive property for $(-76) \times 115 - (-76) \times 15$ to simplify calculation.
    """
    def construct(self):
        # Title
        title = Text("运用分配律简化计算", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Display the original expression
        original_expression_str = "(-76) \\times 115 - (-76) \\times 15"
        original_expression = MathTex(original_expression_str)
        original_expression.move_to(ORIGIN)
        self.play(Write(original_expression))
        self.wait(1)

        # Step 2: Identify the common factor (-76)
        # Indices for "(-76)" in the MathTex string:
        # First "(-76)" is at index 0 to 4.
        # Second "(-76)" is at index 11 to 15.
        common_factor_1_part = original_expression[0][0:5]
        common_factor_2_part = original_expression[0][11:16]

        self.play(
            Indicate(common_factor_1_part, color=YELLOW),
            Indicate(common_factor_2_part, color=YELLOW)
        )
        self.wait(1)

        # Hint for distributive law
        dist_law_hint = Text("应用分配律 (Distributive Law)", font_size=30, color=BLUE)
        dist_law_hint.next_to(original_expression, UP, buff=0.7)
        self.play(Write(dist_law_hint))
        self.wait(1)

        # Step 3: Apply the distributive property
        transformed_expression_str = "(-76) \\times (115 - 15)"
        transformed_expression = MathTex(transformed_expression_str)
        transformed_expression.move_to(original_expression.get_center())

        self.play(
            Transform(original_expression, transformed_expression),
            FadeOut(dist_law_hint)
        )
        self.wait(1)

        # Step 4: Calculate inside the parentheses (115 - 15 = 100)
        # Indices for "(115 - 15)" in "(-76) \times (115 - 15)":
        # It starts at index 7 and ends at index 14 (exclusive 15).
        parentheses_content_part = transformed_expression[0][7:15]
        self.play(Indicate(parentheses_content_part, color=BLUE))
        self.wait(0.5)

        calculation_hint_1 = MathTex("115 - 15 = 100", color=YELLOW)
        calculation_hint_1.next_to(transformed_expression, RIGHT, buff=1)
        self.play(Write(calculation_hint_1))
        self.wait(1)

        # Transform (115 - 15) to 100
        intermediate_expression_str = "(-76) \\times 100"
        intermediate_expression = MathTex(intermediate_expression_str)
        intermediate_expression.move_to(transformed_expression.get_center())

        self.play(
            Transform(transformed_expression, intermediate_expression),
            FadeOut(calculation_hint_1)
        )
        self.wait(1)

        # Step 5: Final multiplication (-76 * 100 = -7600)
        self.play(Indicate(intermediate_expression, color=GREEN))
        self.wait(0.5)

        calculation_hint_2 = MathTex("(-76) \\times 100 = -7600", color=YELLOW)
        calculation_hint_2.next_to(intermediate_expression, RIGHT, buff=1)
        self.play(Write(calculation_hint_2))
        self.wait(1)

        # Transform to final result
        final_result_str = "-7600"
        final_result = MathTex(final_result_str)
        final_result.move_to(intermediate_expression.get_center())

        self.play(
            Transform(intermediate_expression, final_result),
            FadeOut(calculation_hint_2)
        )
        self.wait(1)

        # Final answer box
        final_box = SurroundingRectangle(final_result, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)