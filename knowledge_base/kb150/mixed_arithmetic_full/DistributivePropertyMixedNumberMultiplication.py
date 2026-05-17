from manim import *

class DistributivePropertyMixedNumberMultiplication(Scene):
    """
    Complete mixed arithmetic 完整的四則混合運算: Visualizes applying the distributive property to calculate 39 and 7/8 multiplied by -4, showing 39 * (-4) + 7/8 * (-4).
    """
    def construct(self):
        # 1. Title and Initial Problem
        title = Text("Distributive Property with Mixed Numbers", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        problem_expr = MathTex(r"39\frac{7}{8} \times (-4)", font_size=60)
        self.play(Write(problem_expr))
        self.wait(1)

        # 2. Deconstruct Mixed Number into sum and apply parentheses
        # Target expression: (39 + 7/8) * (-4)
        decomposed_expr = MathTex(r"\left(39 + \frac{7}{8}\right) \times (-4)", font_size=60)
        
        # Move the problem expression up to make space for the next step
        self.play(problem_expr.animate.shift(UP * 1.5))
        
        # Transform the mixed number part into (integer + fraction) using TransformMatchingTex
        # This will match '39', '7/8', 'x (-4)' and add parentheses and '+'
        self.play(TransformMatchingTex(problem_expr, decomposed_expr))
        self.wait(1.5)

        # 3. Apply Distributive Property
        # Target expression for distribution: 39 * (-4) + 7/8 * (-4)
        distributed_expr = MathTex(r"39 \times (-4) + \frac{7}{8} \times (-4)", font_size=60)
        distributed_expr.next_to(decomposed_expr, DOWN, buff=1)

        # Identify the terms for distribution from decomposed_expr
        # Based on inspection: decomposed_expr.submobjects -> ['(', '39', '+', '\\frac{7}{8}', ')', '\\times', '(', '-', '4', ')']
        term1_obj = decomposed_expr[1] # 39
        term2_obj = decomposed_expr[3] # 7/8
        multiplier_obj = VGroup(decomposed_expr[6], decomposed_expr[7], decomposed_expr[8], decomposed_expr[9]) # (-4)

        # Show the distribution arrows
        arrow1 = Arrow(multiplier_obj.get_left(), term1_obj.get_right(), buff=0.1, color=YELLOW)
        arrow2 = Arrow(multiplier_obj.get_left(), term2_obj.get_right(), buff=0.1, color=YELLOW)

        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # Animate the distribution using TransformMatchingTex
        # TransformMatchingTex will handle the duplication of '(-4)' and insertion of 'x' and '+'
        self.play(
            TransformMatchingTex(decomposed_expr, distributed_expr),
            FadeOut(arrow1, arrow2)
        )
        self.wait(2)

        # Move the distributed expression to the center for clarity
        self.play(distributed_expr.animate.move_to(ORIGIN))
        self.wait(1)

        # 4. Compare with Option A
        option_A_label = Text("This matches Option A:", font_size=35).next_to(distributed_expr, DOWN, buff=1)
        option_A_expr = MathTex(r"39 \times (-4) + \frac{7}{8} \times (-4)", font_size=60, color=GREEN)
        option_A_expr.next_to(option_A_label, DOWN, buff=0.5)

        self.play(Write(option_A_label))
        # Use TransformMatchingTex to show it's the same expression, but with a color change
        self.play(TransformMatchingTex(distributed_expr.copy(), option_A_expr))
        self.wait(2)

        # Final highlight of the correct option
        final_box = SurroundingRectangle(option_A_expr, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)