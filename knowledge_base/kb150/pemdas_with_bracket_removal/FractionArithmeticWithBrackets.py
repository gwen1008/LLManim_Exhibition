from manim import *

class FractionArithmeticWithBrackets(Scene):
    """
    PEMDAS with bracket removal distributive 四則運算 含去括號: Visualizes the step-by-step calculation of a complex fraction arithmetic problem
    involving brackets, multiplication, division, and subtraction with negative numbers:
    1/2 * [2/3 - (-1/4) * 2] / 7/6, demonstrating order of operations.
    """
    def construct(self):
        # Original problem statement
        problem_text = MathTex(
            r"\frac{1}{2} \times \left[ \frac{2}{3} - \left(-\frac{1}{4}\right) \times 2 \right] \div \frac{7}{6}"
        ).to_edge(UP)
        self.play(Write(problem_text))
        self.wait(1)

        # Keep a mutable reference to the current state of the expression
        current_expression = problem_text.copy()
        self.add(current_expression)

        # Step 1: Calculate innermost multiplication: (-1/4) * 2
        step1_label = Text("Step 1: Calculate innermost multiplication", font_size=30).next_to(current_expression, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(step1_label))
        self.wait(0.5)

        # Highlight (-1/4) * 2 in the current expression
        # Indices for (-\frac{1}{4}) \times 2 are 5 to 10
        highlight_part1 = VGroup(*current_expression[5:11])
        rect1 = SurroundingRectangle(highlight_part1, color=YELLOW)
        self.play(Create(rect1))
        self.wait(1)

        calculation1 = MathTex(r"\left(-\frac{1}{4}\right) \times 2 = -\frac{1}{2}").next_to(step1_label, DOWN, buff=0.3).align_to(step1_label, LEFT)
        self.play(Write(calculation1))
        self.wait(1)

        # Replace the calculated part in the main expression
        new_expression1 = MathTex(
            r"\frac{1}{2} \times \left[ \frac{2}{3} - \left(-\frac{1}{2}\right) \right] \div \frac{7}{6}"
        ).move_to(current_expression)
        
        self.play(
            FadeOut(rect1),
            Transform(current_expression, new_expression1),
            FadeOut(calculation1),
            FadeOut(step1_label)
        )
        self.wait(1)

        # Step 2: Simplify subtraction in brackets: 2/3 - (-1/2)
        step2_label = Text("Step 2: Simplify subtraction in brackets", font_size=30).next_to(current_expression, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(step2_label))
        self.wait(0.5)

        # Highlight 2/3 - (-1/2) in the current expression
        # Indices for \frac{2}{3} - \left(-\frac{1}{2}\right) are 3 to 8
        highlight_part2 = VGroup(*current_expression[3:9])
        rect2 = SurroundingRectangle(highlight_part2, color=YELLOW)
        self.play(Create(rect2))
        self.wait(1)

        explanation2 = MathTex(r"\frac{2}{3} - \left(-\frac{1}{2}\right) = \frac{2}{3} + \frac{1}{2}").next_to(step2_label, DOWN, buff=0.3).align_to(step2_label, LEFT)
        self.play(Write(explanation2))
        self.wait(1)

        # Replace the calculated part in the main expression
        new_expression2 = MathTex(
            r"\frac{1}{2} \times \left[ \frac{2}{3} + \frac{1}{2} \right] \div \frac{7}{6}"
        ).move_to(current_expression)

        self.play(
            FadeOut(rect2),
            Transform(current_expression, new_expression2),
            FadeOut(explanation2),
            FadeOut(step2_label)
        )
        self.wait(1)

        # Step 3: Calculate addition in brackets: 2/3 + 1/2
        step3_label = Text("Step 3: Calculate addition in brackets (common denominator)", font_size=30).next_to(current_expression, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(step3_label))
        self.wait(0.5)

        # Highlight 2/3 + 1/2 in the current expression
        # Indices for \frac{2}{3} + \frac{1}{2} are 3 to 5
        highlight_part3 = VGroup(*current_expression[3:6])
        rect3 = SurroundingRectangle(highlight_part3, color=YELLOW)
        self.play(Create(rect3))
        self.wait(1)

        calculation3a = MathTex(r"\frac{2}{3} + \frac{1}{2} = \frac{4}{6} + \frac{3}{6}").next_to(step3_label, DOWN, buff=0.3).align_to(step3_label, LEFT)
        self.play(Write(calculation3a))
        self.wait(1)

        calculation3b = MathTex(r"= \frac{7}{6}").next_to(calculation3a, RIGHT, buff=0.3)
        self.play(Write(calculation3b))
        self.wait(1)

        # Replace the calculated part in the main expression (remove brackets)
        new_expression3 = MathTex(
            r"\frac{1}{2} \times \frac{7}{6} \div \frac{7}{6}"
        ).move_to(current_expression)

        self.play(
            FadeOut(rect3),
            Transform(current_expression, new_expression3),
            FadeOut(calculation3a),
            FadeOut(calculation3b),
            FadeOut(step3_label)
        )
        self.wait(1)

        # Step 4: Calculate remaining multiplication and division
        step4_label = Text("Step 4: Calculate remaining multiplication and division (left to right)", font_size=30).next_to(current_expression, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(step4_label))
        self.wait(0.5)

        # Highlight the entire expression
        rect4 = SurroundingRectangle(current_expression, color=YELLOW)
        self.play(Create(rect4))
        self.wait(1)

        explanation4 = MathTex(r"\frac{1}{2} \times \frac{7}{6} \div \frac{7}{6}").next_to(step4_label, DOWN, buff=0.3).align_to(step4_label, LEFT)
        explanation4_cont = MathTex(r"= \frac{1}{2} \times \left(\frac{7}{6} \div \frac{7}{6}\right)").next_to(explanation4, DOWN, buff=0.3).align_to(explanation4, LEFT)
        explanation4_cont2 = MathTex(r"= \frac{1}{2} \times 1").next_to(explanation4_cont, DOWN, buff=0.3).align_to(explanation4_cont, LEFT)
        explanation4_final = MathTex(r"= \frac{1}{2}").next_to(explanation4_cont2, DOWN, buff=0.3).align_to(explanation4_cont2, LEFT)

        self.play(Write(explanation4))
        self.wait(1)
        self.play(Write(explanation4_cont))
        self.wait(1)
        self.play(Write(explanation4_cont2))
        self.wait(1)
        self.play(Write(explanation4_final))
        self.wait(1)

        # Final answer
        final_answer_label = Text("Final Answer:", font_size=35).next_to(explanation4_final, DOWN, buff=0.7).to_edge(LEFT)
        final_answer_value = MathTex(r"\frac{1}{2}", color=GREEN).next_to(final_answer_label, RIGHT, buff=0.3)
        
        self.play(
            FadeOut(rect4),
            FadeOut(current_expression),
            FadeOut(step4_label),
            FadeOut(explanation4),
            FadeOut(explanation4_cont),
            FadeOut(explanation4_cont2),
            Transform(explanation4_final, final_answer_value),
            Write(final_answer_label)
        )
        self.wait(2)

        # Move final answer to center for emphasis
        final_answer_group = VGroup(final_answer_label, explanation4_final)
        self.play(final_answer_group.animate.center().shift(DOWN*0.5))
        self.wait(2)