from manim import *

class ScientificNotationSubtraction(Scene):
    """
    Exponent scientific notation 指數與科學記號: Visualizes subtracting 2.1e6 from 4.5e7 by unifying exponents to 10^7, resulting in 4.29e7.
    """
    def construct(self):
        # Title and initial problem statement
        title = Text("Scientific Notation Subtraction", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        problem_text = MathTex(
            "4.5 \\times 10^7",
            "-",
            "2.1 \\times 10^6"
        ).scale(1.2).next_to(title, DOWN, buff=1)
        self.play(Write(problem_text))
        self.wait(1)

        # Highlight the different exponents
        exp7 = problem_text[0][5:7] # 10^7
        exp6 = problem_text[2][5:7] # 10^6

        diff_exponents_label = Text("Exponents are different!", font_size=30, color=YELLOW).next_to(problem_text, DOWN, buff=0.5)
        self.play(
            Indicate(exp7, scale_factor=1.2),
            Indicate(exp6, scale_factor=1.2),
            Write(diff_exponents_label)
        )
        self.wait(1.5)

        self.play(FadeOut(diff_exponents_label))

        # Explanation for unifying exponents
        explanation1 = Text("To subtract, exponents must be the same.", font_size=30).next_to(problem_text, DOWN, buff=0.5)
        explanation2 = Text("Convert the smaller exponent to the larger one.", font_size=30).next_to(explanation1, DOWN)
        self.play(Write(explanation1))
        self.play(Write(explanation2))
        self.wait(1.5)

        self.play(FadeOut(explanation1), FadeOut(explanation2))

        # Focus on the term to be converted
        term_to_convert = problem_text[2].copy().next_to(problem_text, DOWN, buff=1.0)
        self.play(
            TransformMatchingTex(problem_text[2], term_to_convert),
            problem_text[0].animate.set_opacity(0.3),
            problem_text[1].animate.set_opacity(0.3)
        )
        self.wait(0.5)

        conversion_arrow = Arrow(term_to_convert.get_bottom(), DOWN * 2 + LEFT * 2, buff=0.2)
        conversion_text = Text("Convert:", font_size=30).next_to(term_to_convert, LEFT, buff=0.5)
        self.play(Write(conversion_text))

        # Step-by-step conversion of 2.1 x 10^6 to 0.21 x 10^7
        original_num = MathTex("2.1 \\times 10^6").scale(1.1).next_to(conversion_text, RIGHT, buff=0.5)
        self.play(Write(original_num))
        self.wait(0.5)

        decimal_point = original_num[0][1] # The '.' in 2.1
        arrow_left = Arrow(decimal_point.get_center(), decimal_point.get_center() + LEFT * 0.5, buff=0.05, color=YELLOW)
        shift_decimal_text = Text("Shift decimal left by 1", font_size=25, color=YELLOW).next_to(arrow_left, UP, buff=0.1)
        self.play(GrowArrow(arrow_left), Write(shift_decimal_text))
        self.wait(1)

        new_coeff = MathTex("0.21").scale(1.1).move_to(original_num[0][0:3], aligned_edge=LEFT)
        new_exponent = MathTex("10^7").scale(1.1).move_to(original_num[0][4:], aligned_edge=LEFT)
        
        self.play(
            Transform(original_num[0][0:3], new_coeff),
            FadeOut(arrow_left),
            FadeOut(shift_decimal_text)
        )
        self.wait(0.5)

        increase_exp_text = Text("Increase exponent by 1", font_size=25, color=GREEN).next_to(original_num[0][4:], UP, buff=0.1)
        self.play(
            Transform(original_num[0][4:], new_exponent),
            Write(increase_exp_text)
        )
        self.wait(1.5)

        converted_term = VGroup(new_coeff, MathTex("\\times").scale(1.1), new_exponent).arrange(RIGHT, buff=0.1).move_to(original_num)
        self.play(
            FadeOut(original_num),
            FadeOut(increase_exp_text),
            Transform(term_to_convert, converted_term),
            FadeOut(conversion_text)
        )
        self.wait(1)

        # Replace the original term with the converted one
        self.play(
            TransformMatchingTex(problem_text[2], converted_term.copy().move_to(problem_text[2])),
            FadeOut(term_to_convert), # Remove the temporary converted term
            problem_text[0].animate.set_opacity(1),
            problem_text[1].animate.set_opacity(1)
        )
        problem_text[2].become(converted_term) # Update problem_text[2] to the new mobject
        self.wait(1)

        # Rewrite the problem with unified exponents
        unified_problem = MathTex(
            "4.5 \\times 10^7 - 0.21 \\times 10^7"
        ).scale(1.2).move_to(problem_text)
        self.play(TransformMatchingTex(problem_text, unified_problem))
        self.wait(1)

        # Factor out the common exponent
        factored_problem = MathTex(
            "(4.5 - 0.21)",
            "\\times 10^7"
        ).scale(1.2).move_to(unified_problem)
        self.play(TransformMatchingTex(unified_problem, factored_problem))
        self.wait(1.5)

        # Perform the subtraction
        subtraction_hint = MathTex("4.5 - 0.21 = 4.29", color=YELLOW).next_to(factored_problem, DOWN, buff=0.5)
        self.play(Write(subtraction_hint))
        self.wait(1.5)

        result = MathTex(
            "4.29",
            "\\times 10^7"
        ).scale(1.2).move_to(factored_problem)
        self.play(
            TransformMatchingTex(factored_problem, result),
            FadeOut(subtraction_hint)
        )
        self.wait(1.5)

        # Final answer breakdown (a and n)
        final_a = MathTex("a = 4.29", color=BLUE).next_to(result, DOWN, buff=0.8).align_to(result, LEFT)
        final_n = MathTex("n = 7", color=GREEN).next_to(final_a, RIGHT, buff=1.0)

        self.play(Write(final_a))
        self.play(Write(final_n))
        self.wait(2)

        # Highlight final answer
        final_answer_group = VGroup(result, final_a, final_n)
        final_box = SurroundingRectangle(final_answer_group, color=WHITE, buff=0.5)
        self.play(Create(final_box))
        self.wait(2)