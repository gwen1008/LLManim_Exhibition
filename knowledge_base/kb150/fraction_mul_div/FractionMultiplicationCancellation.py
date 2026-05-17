from manim import *

class FractionMultiplicationCancellation(Scene):
    """
    Fraction multiplication division 分數乘除: Visualizes the calculation of 2023 * (-2024/2023) by demonstrating direct cancellation of common factors.
    """
    def construct(self):
        # Title of the scene
        title = Text("Fraction Multiplication with Cancellation", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Display the initial problem statement and equation
        problem_statement = Text("Calculate: ", font_size=36)
        
        # Using VGroup to arrange the MathTex parts of the equation
        eq_initial_parts = VGroup(
            MathTex("2023", font_size=48),
            MathTex("\\times", font_size=48),
            MathTex("\\left(", font_size=48),
            MathTex("-", font_size=48),
            MathTex("\\frac{2024}{2023}", font_size=48),
            MathTex("\\right)", font_size=48)
        ).arrange(RIGHT, buff=0.1)

        # Group the problem statement and the equation for overall positioning
        initial_problem_group = VGroup(problem_statement, eq_initial_parts).arrange(RIGHT, buff=0.2).next_to(title, DOWN, buff=1)
        
        self.play(Write(initial_problem_group))
        self.wait(1)

        # Identify the common factors for cancellation
        integer_2023 = eq_initial_parts[0]
        denominator_2023 = eq_initial_parts[4][1] # Accessing the denominator part of the fraction

        # Highlight the common factors with surrounding rectangles
        rect_int = SurroundingRectangle(integer_2023, color=YELLOW, buff=0.1)
        rect_den = SurroundingRectangle(denominator_2023, color=YELLOW, buff=0.1)
        self.play(Create(rect_int), Create(rect_den))
        self.wait(1)

        # Add an explanation for the cancellation step
        cancellation_hint = Text(
            "Identify and cancel common factors (2023).",
            font_size=30,
            color=BLUE
        ).next_to(initial_problem_group, DOWN, buff=1)
        self.play(Write(cancellation_hint))
        self.wait(1)

        # Visually cross out the common factors
        cross_int = Cross(integer_2023, stroke_width=5, color=RED)
        cross_den = Cross(denominator_2023, stroke_width=5, color=RED)
        self.play(
            Create(cross_int),
            Create(cross_den),
            FadeOut(rect_int),
            FadeOut(rect_den)
        )
        self.wait(1)

        # Step 2: Show the simplified expression and the final result
        # Create the final result equation
        final_result_eq = MathTex("=", "-2024", font_size=48).move_to(initial_problem_group) # Position it where the initial problem was
        
        # Animate fading out the initial problem, crosses, and hint, then writing the final result
        self.play(
            FadeOut(initial_problem_group), # Fade out the entire initial problem group
            FadeOut(cross_int),
            FadeOut(cross_den),
            FadeOut(cancellation_hint),
            Write(final_result_eq)
        )
        self.wait(1)

        # Final answer statement and context
        final_answer_text = Text(
            "The exact result of the calculation is -2024.",
            font_size=30,
            color=GREEN
        ).next_to(final_result_eq, DOWN, buff=1)
        
        closest_integer_text = Text(
            "Therefore, the closest integer is -2024.",
            font_size=30,
            color=GREEN
        ).next_to(final_answer_text, DOWN, buff=0.5)

        self.play(Write(final_answer_text))
        self.wait(1)
        self.play(Write(closest_integer_text))
        self.wait(2)