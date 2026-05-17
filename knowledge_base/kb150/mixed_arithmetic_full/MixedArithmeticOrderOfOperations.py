from manim import *

class MixedArithmeticOrderOfOperations(Scene):
    """
    Complete mixed arithmetic 完整的四則混合運算: Visualizes the step-by-step solution of a mixed arithmetic expression with powers and fractions: (-1/2)^3 / (1/4 - 1/3) * (-2)^2.
    """
    def construct(self):
        # Title and initial problem statement
        title = Text("Mixed Arithmetic Operations", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        problem_statement = MathTex(
            r"\left(-\frac{1}{2}\right)^3 \div \left(\frac{1}{4} - \frac{1}{3}\right) \times (-2)^2",
            font_size=54
        ).next_to(title, DOWN, buff=0.8)
        self.play(Write(problem_statement))
        self.wait(1)

        current_expression = problem_statement # This object will be transformed throughout the steps

        # Step 1: Calculate powers - (-1/2)^3
        step_label_1 = Text("Step 1: Calculate powers", font_size=36).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_1))
        self.wait(0.5)

        # Highlight (-1/2)^3 using its MathTex parts
        highlight_1 = SurroundingRectangle(current_expression[0][0:4], color=YELLOW, buff=0.1)
        self.play(Create(highlight_1))
        self.wait(0.5)

        calc_1 = MathTex(r"\left(-\frac{1}{2}\right)^3 = -\frac{1}{8}", font_size=48).next_to(current_expression, DOWN, buff=1)
        self.play(Write(calc_1))
        self.wait(1)

        # Create the new expression after this step
        updated_expr_1 = MathTex(
            r"-\frac{1}{8} \div \left(\frac{1}{4} - \frac{1}{3}\right) \times (-2)^2",
            font_size=54
        ).move_to(current_expression) # Position it where the old one was

        self.play(
            Transform(current_expression, updated_expr_1), # Transform the old expression to the new one
            FadeOut(highlight_1),
            FadeOut(calc_1),
            FadeOut(step_label_1)
        )
        current_expression = updated_expr_1 # Update reference
        self.wait(0.5)

        # Step 2: Calculate powers - (-2)^2
        step_label_2 = Text("Step 2: Calculate powers", font_size=36).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_2))
        self.wait(0.5)

        # Highlight (-2)^2
        highlight_2 = SurroundingRectangle(current_expression[0][8:12], color=YELLOW, buff=0.1)
        self.play(Create(highlight_2))
        self.wait(0.5)

        calc_2 = MathTex(r"(-2)^2 = 4", font_size=48).next_to(current_expression, DOWN, buff=1)
        self.play(Write(calc_2))
        self.wait(1)

        updated_expr_2 = MathTex(
            r"-\frac{1}{8} \div \left(\frac{1}{4} - \frac{1}{3}\right) \times 4",
            font_size=54
        ).move_to(current_expression)

        self.play(
            Transform(current_expression, updated_expr_2),
            FadeOut(highlight_2),
            FadeOut(calc_2),
            FadeOut(step_label_2)
        )
        current_expression = updated_expr_2
        self.wait(0.5)

        # Step 3: Calculate parentheses - (1/4 - 1/3)
        step_label_3 = Text("Step 3: Calculate parentheses", font_size=36).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_3))
        self.wait(0.5)

        # Highlight (1/4 - 1/3)
        highlight_3 = SurroundingRectangle(current_expression[0][2:7], color=YELLOW, buff=0.1)
        self.play(Create(highlight_3))
        self.wait(0.5)

        calc_3 = MathTex(
            r"\frac{1}{4} - \frac{1}{3} = \frac{3}{12} - \frac{4}{12} = -\frac{1}{12}",
            font_size=48
        ).next_to(current_expression, DOWN, buff=1)
        self.play(Write(calc_3))
        self.wait(2)

        updated_expr_3 = MathTex(
            r"-\frac{1}{8} \div \left(-\frac{1}{12}\right) \times 4",
            font_size=54
        ).move_to(current_expression)

        self.play(
            Transform(current_expression, updated_expr_3),
            FadeOut(highlight_3),
            FadeOut(calc_3),
            FadeOut(step_label_3)
        )
        current_expression = updated_expr_3
        self.wait(0.5)

        # Step 4: Calculate division (left to right) - (-1/8) / (-1/12)
        step_label_4 = Text("Step 4: Division (left to right)", font_size=36).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_4))
        self.wait(0.5)

        # Highlight -1/8 / (-1/12)
        highlight_4 = SurroundingRectangle(current_expression[0][0:5], color=YELLOW, buff=0.1)
        self.play(Create(highlight_4))
        self.wait(0.5)

        calc_4 = MathTex(
            r"-\frac{1}{8} \div \left(-\frac{1}{12}\right) = -\frac{1}{8} \times (-12) = \frac{12}{8} = \frac{3}{2}",
            font_size=48
        ).next_to(current_expression, DOWN, buff=1)
        self.play(Write(calc_4))
        self.wait(2)

        updated_expr_4 = MathTex(
            r"\frac{3}{2} \times 4",
            font_size=54
        ).move_to(current_expression)

        self.play(
            Transform(current_expression, updated_expr_4),
            FadeOut(highlight_4),
            FadeOut(calc_4),
            FadeOut(step_label_4)
        )
        current_expression = updated_expr_4
        self.wait(0.5)

        # Step 5: Calculate multiplication - (3/2) * 4
        step_label_5 = Text("Step 5: Multiplication", font_size=36).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_5))
        self.wait(0.5)

        # Highlight the entire remaining expression
        highlight_5 = SurroundingRectangle(current_expression, color=YELLOW, buff=0.1)
        self.play(Create(highlight_5))
        self.wait(0.5)

        calc_5 = MathTex(
            r"\frac{3}{2} \times 4 = 6",
            font_size=48
        ).next_to(current_expression, DOWN, buff=1)
        self.play(Write(calc_5))
        self.wait(1)

        final_answer = MathTex(r"6", font_size=72, color=GREEN).move_to(current_expression)
        self.play(
            Transform(current_expression, final_answer),
            FadeOut(highlight_5),
            FadeOut(calc_5),
            FadeOut(step_label_5)
        )
        self.wait(2)

        # Final cleanup
        self.play(FadeOut(title), FadeOut(current_expression))
        self.wait(1)