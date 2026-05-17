from manim import *

class MixedArithmeticOrderOfOperations(Scene):
    """
    PEMDAS order of operations without bracket removal 四則運算算則 不含去括號: Visualizes the step-by-step solution of 38 - 48 ÷ (-6 - 2) × 3, following order of operations.
    """
    def construct(self):
        # Title
        title = Text("Order of Operations: 38 - 48 ÷ (-6 - 2) × 3", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Initial expression as a VGroup of MathTex parts
        # This allows for flexible replacement of sub-expressions.
        expr_parts = [
            MathTex("38 - 48 \\div (", font_size=48),
            MathTex("-6 - 2", font_size=48),
            MathTex(") \\times 3", font_size=48)
        ]
        current_expr_vgroup = VGroup(*expr_parts).arrange(RIGHT, buff=0.1)
        current_expr_vgroup.to_edge(LEFT).shift(UP * 0.5)
        self.play(Write(current_expr_vgroup))
        self.wait(1)

        # Step 1: Parentheses (-6 - 2)
        step_label_1 = Text("Step 1: Parentheses", font_size=30, color=BLUE).next_to(current_expr_vgroup, DOWN, buff=0.8).align_to(current_expr_vgroup, LEFT)
        self.play(Write(step_label_1))

        # Highlight the part to be calculated
        highlight_target_1 = current_expr_vgroup[1] # "-6 - 2"
        highlight_rect_1 = SurroundingRectangle(highlight_target_1, color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect_1))
        self.wait(1)

        # Show calculation on the right
        calc_text_1 = MathTex("-6 - 2 = -8", font_size=40).next_to(current_expr_vgroup, RIGHT, buff=1.5).align_to(current_expr_vgroup, UP)
        self.play(Write(calc_text_1))
        self.wait(1.5)

        # Replace the calculated part
        replacement_1 = MathTex("-8", font_size=48)
        self.play(
            Transform(highlight_target_1, replacement_1), # Transform the old part to the new result
            FadeOut(highlight_rect_1),
            FadeOut(calc_text_1),
            FadeOut(step_label_1)
        )
        # Update the VGroup: replace old mobject with new one
        current_expr_vgroup[1] = replacement_1
        self.play(current_expr_vgroup.animate.arrange(RIGHT, buff=0.1)) # Re-arrange to adjust spacing
        self.wait(1.5)

        # Step 2: Division (48 ÷ -8) - Left to right for multiplication/division
        step_label_2 = Text("Step 2: Division (Left to Right)", font_size=30, color=BLUE).next_to(current_expr_vgroup, DOWN, buff=0.8).align_to(current_expr_vgroup, LEFT)
        self.play(Write(step_label_2))

        # current_expr_vgroup is now: [0] "38 - 48 \div (", [1] "-8", [2] ") \times 3"
        # We need to highlight "48 \div (-8)"
        # This involves parts of current_expr_vgroup[0], current_expr_vgroup[1], current_expr_vgroup[2]
        # Let's create a temporary VGroup for highlighting
        highlight_target_2_parts = VGroup(
            current_expr_vgroup[0][5:], # "48 \div (" (from '4')
            current_expr_vgroup[1],     # "-8"
            current_expr_vgroup[2][0]   # ")"
        )
        highlight_rect_2 = SurroundingRectangle(highlight_target_2_parts, color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect_2))
        self.wait(1)

        calc_text_2 = MathTex("48 \\div (-8) = -6", font_size=40).next_to(current_expr_vgroup, RIGHT, buff=1.5).align_to(current_expr_vgroup, UP)
        self.play(Write(calc_text_2))
        self.wait(1.5)

        # Fade out the parts being replaced
        self.play(
            FadeOut(highlight_target_2_parts),
            FadeOut(highlight_rect_2),
            FadeOut(calc_text_2),
            FadeOut(step_label_2)
        )
        
        # Create the new VGroup structure
        # The parts are: [0] "38 - ", [1] "-6", [2] " \times 3"
        replacement_2 = MathTex("-6", font_size=48)
        new_expr_parts_2 = [
            current_expr_vgroup[0][:5], # "38 - " (before '4')
            replacement_2,
            current_expr_vgroup[2][1:] # " \times 3" (after ')')
        ]
        next_expr_vgroup = VGroup(*new_expr_parts_2).arrange(RIGHT, buff=0.1)
        next_expr_vgroup.align_to(current_expr_vgroup, LEFT).align_to(current_expr_vgroup, UP)

        self.play(
            Transform(current_expr_vgroup, next_expr_vgroup) # Transform the old VGroup to the new VGroup
        )
        current_expr_vgroup = next_expr_vgroup # Update the reference
        self.wait(1.5)

        # Step 3: Multiplication (-6 * 3)
        step_label_3 = Text("Step 3: Multiplication (Left to Right)", font_size=30, color=BLUE).next_to(current_expr_vgroup, DOWN, buff=0.8).align_to(current_expr_vgroup, LEFT)
        self.play(Write(step_label_3))

        # current_expr_vgroup is now: [0] "38 - ", [1] "-6", [2] " \times 3"
        # Highlight "-6 \times 3"
        highlight_target_3 = VGroup(current_expr_vgroup[1], current_expr_vgroup[2])
        highlight_rect_3 = SurroundingRectangle(highlight_target_3, color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect_3))
        self.wait(1)

        calc_text_3 = MathTex("-6 \\times 3 = -18", font_size=40).next_to(current_expr_vgroup, RIGHT, buff=1.5).align_to(current_expr_vgroup, UP)
        self.play(Write(calc_text_3))
        self.wait(1.5)

        # Fade out the parts being replaced
        self.play(
            FadeOut(highlight_target_3),
            FadeOut(highlight_rect_3),
            FadeOut(calc_text_3),
            FadeOut(step_label_3)
        )

        # Create the new VGroup structure
        # The parts are: [0] "38 - ", [1] "(-18)"
        replacement_3 = MathTex("(-18)", font_size=48) # Add parentheses for clarity of negative number
        new_expr_parts_3 = [
            current_expr_vgroup[0], # "38 - "
            replacement_3
        ]
        next_expr_vgroup = VGroup(*new_expr_parts_3).arrange(RIGHT, buff=0.1)
        next_expr_vgroup.align_to(current_expr_vgroup, LEFT).align_to(current_expr_vgroup, UP)

        self.play(
            Transform(current_expr_vgroup, next_expr_vgroup)
        )
        current_expr_vgroup = next_expr_vgroup
        self.wait(1.5)

        # Step 4: Subtraction (38 - (-18))
        step_label_4 = Text("Step 4: Subtraction", font_size=30, color=BLUE).next_to(current_expr_vgroup, DOWN, buff=0.8).align_to(current_expr_vgroup, LEFT)
        self.play(Write(step_label_4))

        # Highlight the entire expression
        highlight_rect_4 = SurroundingRectangle(current_expr_vgroup, color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect_4))
        self.wait(1)

        calc_text_4 = MathTex("38 - (-18) = 38 + 18 = 56", font_size=40).next_to(current_expr_vgroup, RIGHT, buff=1.5).align_to(current_expr_vgroup, UP)
        self.play(Write(calc_text_4))
        self.wait(1.5)

        # Transform to final answer
        final_answer_mobject = MathTex("56", font_size=64, color=GREEN)
        final_answer_mobject.move_to(current_expr_vgroup.get_center())

        self.play(
            Transform(current_expr_vgroup, final_answer_mobject),
            FadeOut(highlight_rect_4),
            FadeOut(calc_text_4),
            FadeOut(step_label_4)
        )
        self.wait(2)

        # Final emphasis
        final_box = SurroundingRectangle(final_answer_mobject, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)