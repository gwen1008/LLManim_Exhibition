from manim import *

class FractionSubtractionComparison(Scene):
    """
    Fraction addition subtraction 分數加減: Visualizes fraction subtraction and comparison, finding which fraction '乙' does not satisfy '甲 - 乙 > 0' when '甲 = -5/8'.
    """
    def construct(self):
        # [VISUAL REASONING]
        # 1. Pedagogical Goal: Demonstrate how 'A - B > 0' implies 'A > B' and apply this to negative fractions.
        # 2. Layout Strategy: Problem statement and derivation on the left, options and checks on the right.
        # 3. Anti-Overlap Check: Uses VGroup and .arrange() for structured placement.
        # 4. Animation Flow: Introduce problem, derive inequality, then check each option step-by-step.

        # --- 1. Title and Problem Introduction ---
        title = Text("分數減法與大小比較", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        known_alpha = MathTex(r"\text{甲} = -\frac{5}{8}", font_size=48)
        condition = MathTex(r"\text{甲} - \text{乙} > 0", font_size=48)

        problem_group = VGroup(known_alpha, condition).arrange(DOWN, buff=0.8).to_edge(LEFT).shift(UP*0.5)
        
        self.play(Write(known_alpha))
        self.wait(1)
        self.play(Write(condition))
        self.wait(1)

        # --- 2. Derivation of the Inequality ---
        derivation_text = Text("根據條件，如果 甲 - 乙 > 0，則", font_size=30).next_to(problem_group, DOWN, buff=0.8).align_to(problem_group, LEFT)
        self.play(Write(derivation_text))
        self.wait(0.5)

        derivation_eq = MathTex(r"\text{甲} > \text{乙}", font_size=48).next_to(derivation_text, DOWN, buff=0.3).align_to(derivation_text, LEFT)
        self.play(Write(derivation_eq))
        self.wait(1)

        substitution_text = Text("將 甲 的值代入，我們得到：", font_size=30).next_to(derivation_eq, DOWN, buff=0.8).align_to(derivation_eq, LEFT)
        self.play(Write(substitution_text))
        self.wait(0.5)

        final_condition = MathTex(r"\text{乙} < -\frac{5}{8}", font_size=48, color=YELLOW).next_to(substitution_text, DOWN, buff=0.3).align_to(substitution_text, LEFT)
        self.play(Write(final_condition))
        self.wait(1.5)

        self.play(
            VGroup(known_alpha, condition, derivation_text, derivation_eq, substitution_text).animate.set_opacity(0.3),
            final_condition.animate.shift(LEFT * 2).scale(1.2)
        )
        self.wait(0.5)

        # --- 3. Check Each Option ---
        options_label = Text("檢查各選項：", font_size=36).to_edge(UP).shift(RIGHT*3)
        self.play(FadeIn(options_label, shift=UP))
        self.wait(0.5)

        # Define options and their corresponding MathTex objects
        option_A_val = MathTex(r"(A) -1")
        option_B_val = MathTex(r"(B) -\frac{3}{4}")
        option_C_val = MathTex(r"(C) -\frac{1}{2}")
        option_D_val = MathTex(r"(D) -\frac{7}{8}")

        options_group = VGroup(option_A_val, option_B_val, option_C_val, option_D_val).arrange(DOWN, buff=0.6).next_to(options_label, DOWN, buff=0.5).to_edge(RIGHT)
        
        self.play(FadeIn(options_group, shift=RIGHT))
        self.wait(1)

        # Helper function to check an option
        def check_option(option_mob, original_fraction, converted_fraction, comparison_result, is_correct):
            self.play(option_mob.animate.set_color(YELLOW).scale(1.1))
            self.wait(0.5)

            conversion_eq = MathTex(f"{original_fraction} = {converted_fraction}", font_size=36).next_to(option_mob, LEFT, buff=1.0)
            self.play(Write(conversion_eq))
            self.wait(0.5)

            comparison_eq = MathTex(f"{converted_fraction} {comparison_result} -\\frac{{5}}{{8}}", font_size=36).next_to(conversion_eq, DOWN, buff=0.3).align_to(conversion_eq, LEFT)
            self.play(Write(comparison_eq))
            self.wait(0.5)

            result_text = Text("符合", color=GREEN, font_size=30) if is_correct else Text("不符合", color=RED, font_size=30)
            result_text.next_to(comparison_eq, RIGHT, buff=0.5)
            self.play(Write(result_text))
            self.wait(1.5)

            self.play(
                option_mob.animate.set_color(WHITE).scale(1/1.1),
                FadeOut(conversion_eq, comparison_eq, result_text)
            )
            self.wait(0.5)

        # Check Option A
        check_option(option_A_val, r"-1", r"-\frac{8}{8}", r"<", True)

        # Check Option B
        check_option(option_B_val, r"-\frac{3}{4}", r"-\frac{6}{8}", r"<", True)

        # Check Option C (The incorrect one)
        check_option(option_C_val, r"-\frac{1}{2}", r"-\frac{4}{8}", r">", False)
        
        # Highlight the incorrect option
        self.play(
            option_C_val.animate.set_color(RED).scale(1.2),
            final_condition.animate.set_opacity(0.3)
        )
        final_answer_box = SurroundingRectangle(option_C_val, color=RED, buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)

        # Check Option D
        check_option(option_D_val, r"-\frac{7}{8}", r"-\frac{7}{8}", r"<", True)

        self.wait(1)
        self.play(FadeOut(*self.mobjects)) # Clear all mobjects
        self.wait(0.5)

        final_conclusion = VGroup(
            Text("因此，乙數不可能是選項(C)的數值。", font_size=40),
            MathTex(r"(C) -\frac{1}{2}", font_size=48, color=RED)
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Write(final_conclusion))
        self.wait(3)