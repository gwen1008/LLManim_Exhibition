from manim import *

class TelescopingProductFractions(Scene):
    """
    Fraction multiplication division 分數乘除: Visualizes the telescoping product (1 - 1/2) * (1 - 1/3) * ... * (1 - 1/10) demonstrating cancellation.
    """
    def construct(self):
        # Title and Problem Statement
        title = Text("Telescoping Product of Fractions", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        problem_statement_tex = "(1 - \\frac{1}{2}) \\times (1 - \\frac{1}{3}) \\times (1 - \\frac{1}{4}) \\times \\dots \\times (1 - \\frac{1}{10})"
        problem_statement = MathTex(problem_statement_tex).scale(0.8).next_to(title, DOWN, buff=0.5)
        self.play(Write(problem_statement))
        self.wait(1.5)

        # Step 1: Simplify each term
        step1_label = Text("Step 1: Simplify each term", font_size=30).to_corner(UL).shift(RIGHT*0.5)
        self.play(Write(step1_label))
        self.wait(0.5)

        eq1 = MathTex("1 - \\frac{1}{2} = \\frac{1}{2}")
        eq2 = MathTex("1 - \\frac{1}{3} = \\frac{2}{3}")
        eq3 = MathTex("1 - \\frac{1}{4} = \\frac{3}{4}")
        dots_eq = MathTex("\\dots")
        eq_last = MathTex("1 - \\frac{1}{10} = \\frac{9}{10}")

        equations_group = VGroup(eq1, eq2, eq3, dots_eq, eq_last).arrange(DOWN, buff=0.4).next_to(step1_label, DOWN, buff=0.5).align_to(step1_label, LEFT)
        
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(0.5)
        self.play(Write(eq3))
        self.wait(0.5)
        self.play(Write(dots_eq))
        self.wait(0.5)
        self.play(Write(eq_last))
        self.wait(1)

        self.play(FadeOut(equations_group, shift=LEFT), FadeOut(step1_label, shift=LEFT))
        self.wait(0.5)

        # Step 2: Form the product expression
        step2_label = Text("Step 2: Form the product", font_size=30).to_corner(UL).shift(RIGHT*0.5)
        self.play(Write(step2_label))
        self.wait(0.5)

        # Construct the product expression for cancellation
        # Each fraction is a MathTex object, and the times symbols are separate.
        # MathTex("\\frac{", "1", "}{", "2", "}") -> [1] is num, [3] is den
        
        frac_1_2 = MathTex("\\frac{", "1", "}{", "2", "}")
        times1 = MathTex("\\times")
        frac_2_3 = MathTex("\\frac{", "2", "}{", "3", "}")
        times2 = MathTex("\\times")
        frac_3_4 = MathTex("\\frac{", "3", "}{", "4", "}")
        times3 = MathTex("\\times")
        frac_4_5 = MathTex("\\frac{", "4", "}{", "5", "}") # Added for more visible cancellation
        times4 = MathTex("\\times")
        dots = MathTex("\\dots")
        times5 = MathTex("\\times")
        frac_9_10 = MathTex("\\frac{", "9", "}{", "10", "}")

        product_mobjects = VGroup(
            frac_1_2, times1, frac_2_3, times2, frac_3_4, times3, frac_4_5, times4, dots, times5, frac_9_10
        ).arrange(RIGHT, buff=0.2).scale(0.8).move_to(ORIGIN)

        # Transform the original problem statement into the product form
        self.play(Transform(problem_statement, product_mobjects))
        self.wait(1.5)
        
        self.play(FadeOut(step2_label, shift=LEFT))
        self.wait(0.5)

        # Step 3: Visualize cancellation
        step3_label = Text("Step 3: Cancel common terms", font_size=30).to_corner(UL).shift(RIGHT*0.5)
        self.play(Write(step3_label))
        self.wait(0.5)

        # Cancellation animations
        # Cancel '2' (den of 1/2) and '2' (num of 2/3)
        self.play(
            FadeOut(frac_1_2[3]), # Denominator '2'
            FadeOut(frac_2_3[1]), # Numerator '2'
            run_time=0.7
        )
        self.wait(0.3)

        # Cancel '3' (den of 2/3) and '3' (num of 3/4)
        self.play(
            FadeOut(frac_2_3[3]), # Denominator '3'
            FadeOut(frac_3_4[1]), # Numerator '3'
            run_time=0.7
        )
        self.wait(0.3)

        # Cancel '4' (den of 3/4) and '4' (num of 4/5)
        self.play(
            FadeOut(frac_3_4[3]), # Denominator '4'
            FadeOut(frac_4_5[1]), # Numerator '4'
            run_time=0.7
        )
        self.wait(0.3)

        # Indicate the pattern and fade out intermediate terms
        pattern_text = Text("...and so on, all intermediate terms cancel out.", font_size=28, color=YELLOW).next_to(product_mobjects, DOWN, buff=0.7)
        self.play(Write(pattern_text))
        self.wait(1.5)

        # Fade out remaining intermediate terms and symbols
        # This leaves frac_1_2[1] (the '1') and frac_9_10[3] (the '10') along with their empty \frac and / parts
        self.play(
            FadeOut(frac_4_5[0]), FadeOut(frac_4_5[2]), FadeOut(frac_4_5[3]), # The \frac, /, 5 parts of 4/5
            FadeOut(times1), FadeOut(times2), FadeOut(times3), FadeOut(times4), FadeOut(times5),
            FadeOut(dots),
            FadeOut(frac_9_10[0]), FadeOut(frac_9_10[1]), FadeOut(frac_9_10[2]), # The \frac, 9, / parts of 9/10
            FadeOut(pattern_text),
            run_time=1.5
        )
        self.wait(0.3)

        # At this point, only frac_1_2[1] (the '1') and frac_9_10[3] (the '10') are conceptually remaining.
        # The surrounding \frac and / from frac_1_2 are also still on screen but empty.
        
        # Create the final fraction 1/10
        final_fraction_result = MathTex("\\frac{1}{10}").scale(0.8)
        
        # Position it where the '1' and '10' are, and then move it to the center
        # Get the current position of the '1' and '10'
        current_1_pos = frac_1_2[1].get_center()
        current_10_pos = frac_9_10[3].get_center()
        
        # Calculate the center point for the new fraction
        target_center_for_new_frac = (current_1_pos + current_10_pos) / 2
        final_fraction_result.move_to(target_center_for_new_frac)

        # Fade out the old '1' and '10' (and their empty fraction structure) and write the new fraction
        self.play(
            FadeOut(frac_1_2[0]), FadeOut(frac_1_2[1]), FadeOut(frac_1_2[2]), # Fade out the empty \frac, '1', and '/' from 1/2
            FadeOut(frac_9_10[0]), FadeOut(frac_9_10[3]), FadeOut(frac_9_10[2]), # Fade out the empty \frac, '10', and '/' from 9/10
            Write(final_fraction_result)
        )
        self.wait(0.7)

        # Add the equals sign and center the final result
        equals_sign = MathTex("=").scale(0.8).next_to(final_fraction_result, LEFT, buff=0.2)
        self.play(Write(equals_sign))
        self.wait(0.7)

        final_answer_group = VGroup(equals_sign, final_fraction_result).move_to(ORIGIN)
        # Transform the problem_statement (which is currently the product_mobjects) into the final answer.
        # This will clean up any remaining invisible parts of product_mobjects.
        self.play(Transform(problem_statement, final_answer_group)) 
        self.wait(1.5)

        final_answer_box = SurroundingRectangle(final_answer_group, color=YELLOW, buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)
        self.play(FadeOut(step3_label)) # Fade out the last step label
        self.wait(1)