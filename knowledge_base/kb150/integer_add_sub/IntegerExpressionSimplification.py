from manim import *

class IntegerExpressionSimplification(Scene):
    """
    Integer addition subtraction 整數加減: Visualizes simplifying the integer expression (-1234) + 567 - (-2234) - 1567 to 0 by grouping terms.
    """
    def construct(self):
        # Initial setup
        title = Text("Integer Expression Simplification", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Original expression
        initial_expr_str = "(-1234) + 567 - (-2234) - 1567"
        expr = MathTex(initial_expr_str).move_to(ORIGIN)
        self.play(Write(expr))
        self.wait(1)

        # Step 1: Simplify -(-2234) to +2234
        step1_title = Text("Step 1: Simplify -(-2234) to +2234", font_size=30).to_edge(UP)
        self.play(Transform(title, step1_title))
        self.wait(0.5)

        # Highlight the part to be changed: "- (-2234)"
        # MathTex("(-1234) + 567 - (-2234) - 1567")
        # Indices: [0]:(-1234), [1]:+, [2]:567, [3]:-, [4]:(-2234), [5]:-, [6]:1567
        neg_neg_term = VGroup(expr.submobjects[3], expr.submobjects[4])
        self.play(Indicate(neg_neg_term, scale_factor=1.2, color=YELLOW))
        self.wait(1)

        # New expression after simplification
        expr_step1_str = "-1234 + 567 + 2234 - 1567"
        expr_step1 = MathTex(expr_step1_str).move_to(ORIGIN)
        self.play(Transform(expr, expr_step1))
        self.wait(1.5)

        # Step 2: Rearrange and group terms
        step2_title = Text("Step 2: Rearrange and group terms", font_size=30).to_edge(UP)
        self.play(Transform(title, step2_title))
        self.wait(0.5)

        # Highlight terms to be grouped
        # MathTex("-1234 + 567 + 2234 - 1567")
        # Indices: [0]:-1234, [1]:+, [2]:567, [3]:+, [4]:2234, [5]:-, [6]:1567
        
        # Group (-1234 + 2234)
        group1_terms = VGroup(expr.submobjects[0], expr.submobjects[3], expr.submobjects[4])
        self.play(Indicate(group1_terms, color=YELLOW))
        self.wait(0.5)
        
        # Group (567 - 1567)
        group2_terms = VGroup(expr.submobjects[2], expr.submobjects[5], expr.submobjects[6])
        self.play(Indicate(group2_terms, color=BLUE))
        self.wait(1)

        # New expression after grouping
        expr_step2_str = "(-1234 + 2234) + (567 - 1567)"
        expr_step2 = MathTex(expr_step2_str).move_to(ORIGIN)
        self.play(Transform(expr, expr_step2))
        self.wait(1.5)

        # Step 3: Calculate the first group (-1234 + 2234)
        step3_title = Text("Step 3: Calculate the first group", font_size=30).to_edge(UP)
        self.play(Transform(title, step3_title))
        self.wait(0.5)

        # Highlight the first group
        # MathTex("(", "-1234", "+", "2234", ")", "+", "(", "567", "-", "1567", ")")
        # Indices: [0]:(, [1]:-1234, [2]:+, [3]:2234, [4]:)
        first_group = VGroup(expr.submobjects[0], expr.submobjects[1], expr.submobjects[2], expr.submobjects[3], expr.submobjects[4])
        self.play(Indicate(first_group, color=YELLOW))
        self.wait(0.5)

        calc1 = MathTex("-1234 + 2234 = 1000", color=YELLOW).next_to(expr, DOWN, buff=0.7)
        self.play(Write(calc1))
        self.wait(1.5)

        # Substitute the result back into the main expression
        expr_step3_str = "1000 + (567 - 1567)"
        expr_step3 = MathTex(expr_step3_str).move_to(ORIGIN)
        self.play(Transform(expr, expr_step3), FadeOut(calc1))
        self.wait(1.5)

        # Step 4: Calculate the second group (567 - 1567)
        step4_title = Text("Step 4: Calculate the second group", font_size=30).to_edge(UP)
        self.play(Transform(title, step4_title))
        self.wait(0.5)

        # Highlight the second group
        # MathTex("1000", "+", "(", "567", "-", "1567", ")")
        # Indices: [2]:(, [3]:567, [4]:-, [5]:1567, [6]:)
        second_group = VGroup(expr.submobjects[2], expr.submobjects[3], expr.submobjects[4], expr.submobjects[5], expr.submobjects[6])
        self.play(Indicate(second_group, color=BLUE))
        self.wait(0.5)

        calc2 = MathTex("567 - 1567 = -1000", color=BLUE).next_to(expr, DOWN, buff=0.7)
        self.play(Write(calc2))
        self.wait(1.5)

        # Substitute the result back into the main expression
        expr_step4_str = "1000 + (-1000)"
        expr_step4 = MathTex(expr_step4_str).move_to(ORIGIN)
        self.play(Transform(expr, expr_step4), FadeOut(calc2))
        self.wait(1.5)

        # Step 5: Calculate the final sum
        step5_title = Text("Step 5: Calculate the final sum", font_size=30).to_edge(UP)
        self.play(Transform(title, step5_title))
        self.wait(0.5)

        # Highlight the final sum
        self.play(Indicate(expr, color=GREEN))
        self.wait(0.5)

        calc3 = MathTex("1000 + (-1000) = 0", color=GREEN).next_to(expr, DOWN, buff=0.7)
        self.play(Write(calc3))
        self.wait(1.5)

        # Final result
        final_answer_str = "0"
        final_answer = MathTex(final_answer_str).move_to(ORIGIN)
        self.play(Transform(expr, final_answer), FadeOut(calc3))
        self.wait(0.5)

        # Surround the final answer
        final_box = SurroundingRectangle(expr, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(title, expr, final_box))
        self.wait(0.5)