from manim import *

class GroupedIntegerSubtraction(Scene):
    """
    Integer addition subtraction 整數加減: Visualizes simplifying 99 - 198 + 299 - 398 by grouping terms into (99 - 198) + (299 - 398).
    """
    def construct(self):
        # Title/Problem Statement
        problem_title = Text("Calculate: 99 - 198 + 299 - 398", font_size=40).to_edge(UP)
        self.play(Write(problem_title))
        self.wait(1)

        # Original Expression
        expr_0 = MathTex("99 - 198 + 299 - 398")
        expr_0.next_to(problem_title, DOWN, buff=1)
        self.play(Write(expr_0))
        self.wait(2)

        # Strategy Hint
        strategy_hint = Text("Strategy: Group terms to simplify", font_size=30, color=YELLOW)
        strategy_hint.next_to(expr_0, DOWN, buff=1.5).to_edge(LEFT)
        self.play(Write(strategy_hint))
        self.wait(2)

        # Grouping the expression
        expr_1 = MathTex("(99 - 198)", "+", "(299 - 398)")
        expr_1.move_to(expr_0.get_center()) # Start at the same position
        
        self.play(
            FadeOut(expr_0),
            FadeIn(expr_1)
        )
        self.wait(2)

        # Highlight first group and calculate
        first_group_box = SurroundingRectangle(expr_1[0], color=BLUE)
        self.play(Create(first_group_box))
        self.wait(1)

        calc1 = MathTex("99 - 198 = -99", color=BLUE)
        calc1.next_to(expr_1, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(calc1))
        self.wait(2.5)

        # Replace first group with its result
        expr_2 = MathTex("(-99)", "+", "(299 - 398)")
        expr_2.move_to(expr_1.get_center())
        
        self.play(
            FadeOut(first_group_box),
            TransformMatchingTex(expr_1, expr_2)
        )
        self.wait(1)

        # Highlight second group and calculate
        second_group_box = SurroundingRectangle(expr_2[2], color=RED)
        self.play(Create(second_group_box))
        self.wait(1)

        calc2 = MathTex("299 - 398 = -99", color=RED)
        calc2.next_to(calc1, DOWN, buff=0.5).align_to(calc1, LEFT)
        self.play(Write(calc2))
        self.wait(2.5)

        # Replace second group with its result
        expr_3 = MathTex("(-99)", "+", "(-99)")
        expr_3.move_to(expr_2.get_center())

        self.play(
            FadeOut(second_group_box),
            TransformMatchingTex(expr_2, expr_3)
        )
        self.wait(1)

        # Perform final addition
        final_result_eq = MathTex("= -198")
        final_result_eq.next_to(expr_3, RIGHT, buff=0.3)

        self.play(
            FadeOut(calc1, calc2, strategy_hint),
            expr_3.animate.move_to(ORIGIN).shift(UP*0.5)
        )
        self.wait(1)

        self.play(Write(final_result_eq))
        self.wait(2.5)

        # Final Answer Highlight
        final_answer_group = VGroup(expr_3, final_result_eq)
        final_box = SurroundingRectangle(final_answer_group, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(3)

        self.play(FadeOut(final_box, final_answer_group, problem_title))
        self.wait(1)