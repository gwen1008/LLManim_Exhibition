from manim import *

class OrderOfOperationsWithNegativeExponents(Scene):
    """
    Exponent scientific notation 指數與科學記號: Visualizes the calculation of (-2)^4 / (-4) - (-3)^2 * 2, demonstrating order of operations and negative exponent rules.
    """
    def construct(self):
        # Original problem statement
        problem_title = Text("Calculate:", font_size=40)
        original_expression_str = "(-2)^4 \\div (-4) - (-3)^2 \\times 2"
        original_expression_math = MathTex(original_expression_str, font_size=48)
        
        problem_statement_group = VGroup(problem_title, original_expression_math).arrange(RIGHT, buff=0.2)
        problem_statement_group.to_edge(UP)
        
        self.play(Write(problem_statement_group))
        self.wait(0.5)

        # The expression that will be updated step-by-step
        current_expression_display = original_expression_math.copy()
        current_expression_display.next_to(problem_statement_group, DOWN, buff=1)
        self.play(TransformFromCopy(original_expression_math, current_expression_display))
        self.wait(0.5)

        # --- Step 1: Calculate Exponents ---
        step1_title = Text("Step 1: Calculate Exponents", font_size=36, color=BLUE)
        step1_title.next_to(current_expression_display, DOWN, buff=1).to_edge(LEFT)
        self.play(Write(step1_title))
        self.wait(0.5)

        # Calculate (-2)^4
        term1_calc = MathTex("(-2)^4", "=", "16", font_size=40)
        term1_calc.next_to(step1_title, DOWN, buff=0.5).align_to(step1_title, LEFT)

        highlight_term1 = current_expression_display.get_parts_by_tex("(-2)^4")
        self.play(Indicate(highlight_term1, scale_factor=1.2))
        self.play(Write(term1_calc))
        self.wait(0.8)

        explanation1 = Text("Even power of a negative number is positive.", font_size=28, color=YELLOW)
        explanation1.next_to(term1_calc, DOWN, buff=0.3).align_to(term1_calc, LEFT)
        self.play(Write(explanation1))
        self.wait(1.2)
        self.play(FadeOut(explanation1))

        # Substitute 16 back into the expression
        new_expression_str_after_step1 = "16 \\div (-4) - (-3)^2 \\times 2"
        new_expression_after_step1 = MathTex(new_expression_str_after_step1, font_size=48).move_to(current_expression_display.get_center())

        self.play(
            TransformMatchingTex(current_expression_display, new_expression_after_step1),
            FadeOut(term1_calc)
        )
        current_expression_display = new_expression_after_step1
        self.wait(0.8)

        # Calculate (-3)^2
        term2_calc = MathTex("(-3)^2", "=", "9", font_size=40)
        term2_calc.next_to(step1_title, DOWN, buff=0.5).align_to(step1_title, LEFT) # Reuse position

        highlight_term2 = current_expression_display.get_parts_by_tex("(-3)^2")
        self.play(Indicate(highlight_term2, scale_factor=1.2))
        self.play(Write(term2_calc))
        self.wait(0.8)

        explanation2 = Text("Even power of a negative number is positive.", font_size=28, color=YELLOW)
        explanation2.next_to(term2_calc, DOWN, buff=0.3).align_to(term2_calc, LEFT)
        self.play(Write(explanation2))
        self.wait(1.2)
        self.play(FadeOut(explanation2))

        # Substitute 9 back
        new_expression_str_after_step2 = "16 \\div (-4) - 9 \\times 2"
        new_expression_after_step2 = MathTex(new_expression_str_after_step2, font_size=48).move_to(current_expression_display.get_center())

        self.play(
            TransformMatchingTex(current_expression_display, new_expression_after_step2),
            FadeOut(term2_calc),
            FadeOut(step1_title) # Fade out step title as we move to next operation type
        )
        current_expression_display = new_expression_after_step2
        self.wait(0.8)

        # --- Step 2: Perform Multiplication and Division (Left to Right) ---
        step3_title = Text("Step 2: Perform Multiplication and Division (Left to Right)", font_size=36, color=BLUE)
        step3_title.next_to(current_expression_display, DOWN, buff=1).to_edge(LEFT)
        self.play(Write(step3_title))
        self.wait(0.5)

        # Calculate 16 / (-4)
        div_calc = MathTex("16 \\div (-4)", "=", "-4", font_size=40)
        div_calc.next_to(step3_title, DOWN, buff=0.5).align_to(step3_title, LEFT)

        highlight_div = current_expression_display.get_parts_by_tex("16 \\div (-4)")
        self.play(Indicate(highlight_div, scale_factor=1.2))
        self.play(Write(div_calc))
        self.wait(0.8)

        # Substitute -4 back
        new_expression_str_after_step3 = "-4 - 9 \\times 2"
        new_expression_after_step3 = MathTex(new_expression_str_after_step3, font_size=48).move_to(current_expression_display.get_center())

        self.play(
            TransformMatchingTex(current_expression_display, new_expression_after_step3),
            FadeOut(div_calc)
        )
        current_expression_display = new_expression_after_step3
        self.wait(0.8)

        # Calculate 9 * 2
        mult_calc = MathTex("9 \\times 2", "=", "18", font_size=40)
        mult_calc.next_to(step3_title, DOWN, buff=0.5).align_to(step3_title, LEFT) # Reuse position

        highlight_mult = current_expression_display.get_parts_by_tex("9 \\times 2")
        self.play(Indicate(highlight_mult, scale_factor=1.2))
        self.play(Write(mult_calc))
        self.wait(0.8)

        # Substitute 18 back
        new_expression_str_after_step4 = "-4 - 18"
        new_expression_after_step4 = MathTex(new_expression_str_after_step4, font_size=48).move_to(current_expression_display.get_center())

        self.play(
            TransformMatchingTex(current_expression_display, new_expression_after_step4),
            FadeOut(mult_calc),
            FadeOut(step3_title) # Fade out step title
        )
        current_expression_display = new_expression_after_step4
        self.wait(0.8)

        # --- Step 3: Perform Addition and Subtraction ---
        step5_title = Text("Step 3: Perform Addition and Subtraction", font_size=36, color=BLUE)
        step5_title.next_to(current_expression_display, DOWN, buff=1).to_edge(LEFT)
        self.play(Write(step5_title))
        self.wait(0.5)

        # Calculate -4 - 18
        final_calc = MathTex("-4 - 18", "=", "-22", font_size=40)
        final_calc.next_to(step5_title, DOWN, buff=0.5).align_to(step5_title, LEFT)

        self.play(Indicate(current_expression_display, scale_factor=1.1))
        self.play(Write(final_calc))
        self.wait(0.8)

        # --- Final Answer ---
        final_answer_text = Text("Final Answer:", font_size=40)
        final_answer_value = MathTex("-22", font_size=60, color=GREEN)
        final_answer_group = VGroup(final_answer_text, final_answer_value).arrange(RIGHT, buff=0.5)
        final_answer_group.next_to(final_calc, DOWN, buff=1).align_to(final_calc, LEFT)

        self.play(
            FadeOut(current_expression_display),
            FadeOut(final_calc),
            FadeOut(step5_title)
        )
        self.play(Write(final_answer_group))
        self.play(Create(SurroundingRectangle(final_answer_value, color=GREEN, buff=0.2)))
        self.wait(2)