from manim import *

class CompareScientificNotationAndDecimal(Scene):
    """
    Exponent scientific notation 指數與科學記號: Visualizes comparing three numbers (3.4e-5, 4.3e-6, 0.000035) by converting all to scientific notation.
    """
    def construct(self):
        # 1. Title and Problem Statement
        title = Text("比較甲、乙、丙三數的大小關係", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Original numbers
        initial_a = MathTex(r"\text{甲 } = 3.4 \times 10^{-5}")
        initial_b = MathTex(r"\text{乙 } = 4.3 \times 10^{-6}")
        initial_c = MathTex(r"\text{丙 } = 0.000035")
        
        problem_group = VGroup(initial_a, initial_b, initial_c).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=1)
        
        self.play(Write(problem_group))
        self.wait(1)

        # 2. Strategy Introduction
        strategy_text = Text("策略：將所有數字轉換為科學記號", font_size=36, color=YELLOW).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(strategy_text))
        self.wait(1)

        # 3. Convert 丙 to scientific notation
        # Create separate label and value for 丙 to animate
        c_label_temp = MathTex(r"\text{丙 } = ").move_to(initial_c.get_left()).shift(RIGHT * 0.5)
        c_val_original_temp = MathTex(r"0.000035").next_to(c_label_temp, RIGHT, buff=0.1)
        
        # Replace initial_c with its components for animation
        self.play(
            FadeOut(initial_c),
            FadeIn(c_label_temp),
            FadeIn(c_val_original_temp)
        )
        self.wait(0.5)

        # Initial decimal point position (after the first 0)
        initial_dp_pos = c_val_original_temp[0][1].get_right() # Position after the first '0'
        decimal_point = Dot(initial_dp_pos, radius=0.05, color=RED)
        self.play(FadeIn(decimal_point))
        self.wait(0.5)

        # Target scientific notation value for 丙
        c_val_converted_target = MathTex(r"3.5 \times 10^{-5}").move_to(c_val_original_temp.get_center())
        target_dp_pos = c_val_converted_target[0][1].get_right() # Position after '3' in '3.5'
        
        arrow = Arrow(initial_dp_pos, target_dp_pos, buff=0, color=BLUE)
        arrow_text = Text("移動 5 位", font_size=25, color=BLUE).next_to(arrow, UP, buff=0.1)
        
        self.play(Create(arrow), Write(arrow_text))
        self.play(decimal_point.animate.move_to(target_dp_pos), run_time=2)
        self.play(FadeOut(arrow), FadeOut(arrow_text), FadeOut(decimal_point))
        
        self.play(Transform(c_val_original_temp, c_val_converted_target))
        self.wait(1)

        # 4. Display all numbers in standard scientific notation for comparison
        self.play(FadeOut(strategy_text))
        
        # Create new MathTex objects for comparison, aligned
        final_a_comp = MathTex(r"\text{甲 } = 3.4 \times 10^{-5}")
        final_b_comp = MathTex(r"\text{乙 } = 4.3 \times 10^{-6}")
        final_c_comp = MathTex(r"\text{丙 } = 3.5 \times 10^{-5}") # A fresh MathTex for consistency
        
        # Group the currently displayed objects for transformation
        current_display_group = VGroup(initial_a, initial_b, c_label_temp, c_val_original_temp)
        
        # Transform the current display into the final comparison group, moving to ORIGIN
        self.play(
            Transform(initial_a, final_a_comp),
            Transform(initial_b, final_b_comp),
            Transform(VGroup(c_label_temp, c_val_original_temp), final_c_comp), # Transform the VGroup of 丙 into the new MathTex
            current_display_group.animate.move_to(ORIGIN)
        )
        
        # Update the references to the new objects for subsequent steps
        initial_a = final_a_comp
        initial_b = final_b_comp
        initial_c = final_c_comp # This is now the MathTex for 丙
        comparison_group = VGroup(initial_a, initial_b, initial_c) # Re-create comparison_group with updated references
        
        self.wait(1)

        # 5. Comparison Step 1 (Exponents)
        compare_exp_text = Text("步驟1: 比較指數", font_size=36, color=YELLOW).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(compare_exp_text))
        self.wait(0.5)

        # Highlight exponents
        exp_a = initial_a[0][9:] # -5
        exp_b = initial_b[0][9:] # -6
        exp_c = initial_c[0][9:] # -5
        
        self.play(
            Indicate(exp_a, color=BLUE),
            Indicate(exp_b, color=BLUE),
            Indicate(exp_c, color=BLUE)
        )
        self.wait(1)

        exp_comparison = MathTex(r"-5 > -6").next_to(comparison_group, RIGHT, buff=1)
        self.play(Write(exp_comparison))
        self.wait(1)

        conclusion_exp = Text("因此，甲和丙 > 乙", font_size=30).next_to(exp_comparison, DOWN, buff=0.5)
        self.play(Write(conclusion_exp))
        self.wait(1)

        # Dim 乙 to indicate it's smaller
        self.play(initial_b.animate.set_opacity(0.3))
        self.wait(0.5)

        self.play(FadeOut(exp_comparison), FadeOut(conclusion_exp))
        self.wait(0.5)

        # 6. Comparison Step 2 (Coefficients for 甲 and 丙)
        compare_coeff_text = Text("步驟2: 比較甲和丙的係數", font_size=36, color=YELLOW).to_edge(LEFT).shift(UP*1.5)
        self.play(Transform(compare_exp_text, compare_coeff_text)) # Transform previous text
        self.wait(0.5)

        # Highlight coefficients of 甲 and 丙
        coeff_a = initial_a[0][3:6] # 3.4
        coeff_c = initial_c[0][3:6] # 3.5

        self.play(
            Indicate(coeff_a, color=GREEN),
            Indicate(coeff_c, color=GREEN)
        )
        self.wait(1)

        coeff_comparison = MathTex(r"3.5 > 3.4").next_to(comparison_group, RIGHT, buff=1)
        self.play(Write(coeff_comparison))
        self.wait(1)

        conclusion_coeff = Text("因此，丙 > 甲", font_size=30).next_to(coeff_comparison, DOWN, buff=0.5)
        self.play(Write(conclusion_coeff))
        self.wait(1)

        self.play(FadeOut(coeff_comparison), FadeOut(conclusion_coeff))
        self.wait(0.5)

        # 7. Final Ordering
        self.play(FadeOut(compare_exp_text)) # Fade out the transformed text
        self.play(initial_b.animate.set_opacity(1)) # Restore opacity of 乙
        
        final_ordering_text = Text("綜合比較結果：", font_size=36, color=YELLOW).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(final_ordering_text))
        self.wait(0.5)

        final_result = MathTex(r"\text{丙 } > \text{甲 } > \text{乙}", font_size=50, color=GREEN).next_to(comparison_group, DOWN, buff=1)
        self.play(Write(final_result))
        self.wait(2)

        final_box = SurroundingRectangle(final_result, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)

        self.play(FadeOut(VGroup(title, comparison_group, final_ordering_text, final_result, final_box)))
        self.wait(1)