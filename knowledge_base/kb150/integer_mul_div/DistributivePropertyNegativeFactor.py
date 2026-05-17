from manim import *

class DistributivePropertyNegativeFactor(Scene):
    """
    Integer multiplication division 整數乘除: Visualizes the calculation of 54 * (-39) - 46 * 39 using the distributive property with a negative common factor.
    """
    def construct(self):
        # Title of the scene
        title = Text("Calculation: $54 \\times (-39) - 46 \\times 39$", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Display the initial expression
        expr1 = MathTex("54", "\\times", "(-39)", "-", "46", "\\times", "39")
        expr1.move_to(ORIGIN)
        self.play(Write(expr1))
        self.wait(1)

        # Explanation for rewriting subtraction
        explanation1 = Text("Rewrite subtraction as addition with a negative factor.", font_size=28).next_to(expr1, DOWN, buff=0.8)
        self.play(Write(explanation1))
        self.play(
            Indicate(expr1[3], color=YELLOW), # Highlight '-'
            Indicate(expr1[6], color=YELLOW)  # Highlight '39'
        )
        self.wait(1)

        # Step 2: Transform - 46 * 39 to + 46 * (-39)
        # The parts are carefully defined for TransformMatchingTex to match correctly.
        expr2 = MathTex("54", "\\times", "(-39)", "+", "46", "\\times", "(-39)")
        expr2.move_to(expr1) # Keep the expression centered

        self.play(
            TransformMatchingTex(expr1, expr2),
            FadeOut(explanation1)
        )
        self.wait(1)

        # Explanation for factoring out the common term
        explanation2 = Text("Factor out the common term (-39).", font_size=28).next_to(expr2, DOWN, buff=0.8)
        self.play(Write(explanation2))
        self.play(
            Indicate(expr2[2], color=YELLOW), # Highlight first (-39)
            Indicate(expr2[6], color=YELLOW)  # Highlight second (-39)
        )
        self.wait(1)

        # Step 3: Apply Distributive Property: (-39) * (54 + 46)
        expr3 = MathTex("(-39)", "\\times", "(", "54", "+", "46", ")")
        expr3.move_to(expr2)

        self.play(
            TransformMatchingTex(expr2, expr3),
            FadeOut(explanation2)
        )
        self.wait(1)

        # Explanation for calculating the sum in parentheses
        explanation3 = Text("Calculate the sum inside the parentheses.", font_size=28).next_to(expr3, DOWN, buff=0.8)
        self.play(Write(explanation3))
        self.play(
            Indicate(VGroup(expr3[3], expr3[4], expr3[5]), color=YELLOW) # Highlight 54 + 46
        )
        self.wait(1)

        # Step 4: Simplify the parentheses: (-39) * 100
        expr4 = MathTex("(-39)", "\\times", "100")
        expr4.move_to(expr3)

        self.play(
            TransformMatchingTex(expr3, expr4),
            FadeOut(explanation3)
        )
        self.wait(1)

        # Explanation for the final multiplication
        explanation4 = Text("Perform the final multiplication.", font_size=28).next_to(expr4, DOWN, buff=0.8)
        self.play(Write(explanation4))
        self.wait(1)

        # Step 5: Final answer -3900
        final_answer = MathTex("-3900")
        final_answer.move_to(expr4)

        self.play(
            TransformMatchingTex(expr4, final_answer),
            FadeOut(explanation4)
        )
        self.wait(1)

        # Highlight the final answer
        final_rect = SurroundingRectangle(final_answer, color=GREEN, buff=0.2)
        self.play(Create(final_rect))
        self.wait(2)