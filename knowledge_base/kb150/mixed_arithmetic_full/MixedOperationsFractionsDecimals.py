from manim import *

class MixedOperationsFractionsDecimals(Scene):
    """
    Complete mixed arithmetic 完整的四則混合運算: Visualizes the step-by-step solution of a complex arithmetic expression: -3.2 ÷ [(1/4 - 1) × 8/3 + 1/2].
    """
    def construct(self):
        # Title
        title = Text("四則混合運算 (Mixed Operations)", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Initial Expression
        # Using a list of strings for MathTex allows easier indexing for highlighting and replacement
        expr_parts_0 = [
            r"-3.2", r"\div", r"[", r"(", r"\frac{1}{4}", r"-", r"1", r")",
            r"\times", r"\frac{8}{3}", r"+", r"\frac{1}{2}", r"]"
        ]
        current_expr = MathTex(*expr_parts_0).next_to(title, DOWN, buff=0.7)
        self.play(Write(current_expr))
        self.wait(1)

        # --- Step 1: Calculate (1/4 - 1) ---
        step_label_1 = Text("Step 1: Calculate inner parenthesis", font_size=28, color=BLUE).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(step_label_1))

        # Highlight (1/4 - 1)
        highlight_group_1 = VGroup(current_expr[3], current_expr[4], current_expr[5], current_expr[6], current_expr[7])
        rect1 = SurroundingRectangle(highlight_group_1, color=YELLOW)
        self.play(Create(rect1))
        self.wait(0.5)

        # Show calculation
        step1_calc = MathTex(r"\frac{1}{4} - 1 = \frac{1}{4} - \frac{4}{4} = -\frac{3}{4}").next_to(step_label_1, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(step1_calc))
        self.wait(1)

        # Update main expression
        expr_parts_1 = [
            r"-3.2", r"\div", r"[", r"-\frac{3}{4}", r"\times", r"\frac{8}{3}", r"+", r"\frac{1}{2}", r"]"
        ]
        next_expr_1 = MathTex(*expr_parts_1).move_to(current_expr.get_center())
        self.play(ReplacementTransform(current_expr, next_expr_1), FadeOut(rect1))
        current_expr = next_expr_1
        self.wait(1)

        # --- Step 2: Calculate -3/4 * 8/3 ---
        step_label_2 = Text("Step 2: Calculate multiplication in brackets", font_size=28, color=BLUE).next_to(step_label_1, DOWN, buff=1.0, aligned_edge=LEFT)
        self.play(Write(step_label_2), FadeOut(step_label_1))

        # Highlight -3/4 * 8/3
        highlight_group_2 = VGroup(current_expr[3], current_expr[4], current_expr[5])
        rect2 = SurroundingRectangle(highlight_group_2, color=YELLOW)
        self.play(Create(rect2))
        self.wait(0.5)

        # Show calculation
        step2_calc = MathTex(r"-\frac{3}{4} \times \frac{8}{3} = -\frac{3 \times 8}{4 \times 3} = -\frac{24}{12} = -2").next_to(step_label_2, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(step2_calc))
        self.wait(1)

        # Update main expression
        expr_parts_2 = [
            r"-3.2", r"\div", r"[", r"-2", r"+", r"\frac{1}{2}", r"]"
        ]
        next_expr_2 = MathTex(*expr_parts_2).move_to(current_expr.get_center())
        self.play(ReplacementTransform(current_expr, next_expr_2), FadeOut(rect2), FadeOut(step1_calc))
        current_expr = next_expr_2
        self.wait(1)

        # --- Step 3: Calculate -2 + 1/2 ---
        step_label_3 = Text("Step 3: Calculate addition in brackets", font_size=28, color=BLUE).next_to(step_label_2, DOWN, buff=1.0, aligned_edge=LEFT)
        self.play(Write(step_label_3), FadeOut(step_label_2))

        # Highlight -2 + 1/2
        highlight_group_3 = VGroup(current_expr[3], current_expr[4], current_expr[5])
        rect3 = SurroundingRectangle(highlight_group_3, color=YELLOW)
        self.play(Create(rect3))
        self.wait(0.5)

        # Show calculation
        step3_calc = MathTex(r"-2 + \frac{1}{2} = -\frac{4}{2} + \frac{1}{2} = -\frac{3}{2}").next_to(step_label_3, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(step3_calc))
        self.wait(1)

        # Update main expression
        expr_parts_3 = [
            r"-3.2", r"\div", r"\left(-\frac{3}{2}\right)"
        ]
        next_expr_3 = MathTex(*expr_parts_3).move_to(current_expr.get_center())
        self.play(ReplacementTransform(current_expr, next_expr_3), FadeOut(rect3), FadeOut(step2_calc))
        current_expr = next_expr_3
        self.wait(1)

        # --- Step 4: Convert -3.2 to fraction ---
        step_label_4 = Text("Step 4: Convert decimal to fraction", font_size=28, color=BLUE).next_to(step_label_3, DOWN, buff=1.0, aligned_edge=LEFT)
        self.play(Write(step_label_4), FadeOut(step_label_3))

        # Highlight -3.2
        highlight_group_4 = current_expr[0]
        rect4 = SurroundingRectangle(highlight_group_4, color=YELLOW)
        self.play(Create(rect4))
        self.wait(0.5)

        # Show calculation
        step4_calc = MathTex(r"-3.2 = -\frac{32}{10} = -\frac{16}{5}").next_to(step_label_4, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(step4_calc))
        self.wait(1)

        # Update main expression
        expr_parts_4 = [
            r"-\frac{16}{5}", r"\div", r"\left(-\frac{3}{2}\right)"
        ]
        next_expr_4 = MathTex(*expr_parts_4).move_to(current_expr.get_center())
        self.play(ReplacementTransform(current_expr, next_expr_4), FadeOut(rect4), FadeOut(step3_calc))
        current_expr = next_expr_4
        self.wait(1)

        # --- Step 5: Final Division ---
        step_label_5 = Text("Step 5: Perform final division", font_size=28, color=BLUE).next_to(step_label_4, DOWN, buff=1.0, aligned_edge=LEFT)
        self.play(Write(step_label_5), FadeOut(step_label_4))

        # Highlight entire expression
        highlight_group_5 = VGroup(current_expr[0], current_expr[1], current_expr[2])
        rect5 = SurroundingRectangle(highlight_group_5, color=YELLOW)
        self.play(Create(rect5))
        self.wait(0.5)

        # Show calculation
        step5_calc = MathTex(
            r"-\frac{16}{5} \div \left(-\frac{3}{2}\right) = -\frac{16}{5} \times \left(-\frac{2}{3}\right) = \frac{32}{15}"
        ).next_to(step_label_5, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(step5_calc))
        self.wait(1.5)

        # Final Answer
        final_answer = MathTex(r"\frac{32}{15}", color=GREEN, font_size=60).move_to(current_expr.get_center())
        self.play(ReplacementTransform(current_expr, final_answer), FadeOut(rect5))
        # Fade out all step labels and calculations
        self.play(FadeOut(VGroup(step_label_5, step4_calc, step5_calc))) 
        
        final_box = SurroundingRectangle(final_answer, color=GREEN, buff=0.2)
        final_text = Text("Final Answer", color=GREEN, font_size=30).next_to(final_answer, DOWN, buff=0.5)
        self.play(Create(final_box), Write(final_text))
        self.wait(2)