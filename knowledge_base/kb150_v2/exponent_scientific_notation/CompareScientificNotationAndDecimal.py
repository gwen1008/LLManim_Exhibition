# [VISUAL REASONING]
# Unify exponents to 10^-4 to compare coefficients directly: C(2.1) < B(8.2) < A(75).
# Vertical stack with color coding (A=BLUE, B=GREEN, C=YELLOW), then highlight final order.

from manim import *

class CompareScientificNotationAndDecimal(Scene):
    """
    指數與科學記號: 科學記號統一後比較大小

    題目：比較三數大小並由小到大排列：A = 7.5×10^-3, B = 8.2×10^-4, C = 0.00021
    """
    def construct(self):
        title = Text("Compare & Sort: Scientific Notation", color=WHITE, font_size=38)
        title.to_edge(UP, buff=0.5)

        row_A = MathTex(r"A = 7.5 \times 10^{-3}", color=BLUE).move_to(ORIGIN + np.array([0, 1.6, 0]))
        row_B = MathTex(r"B = 8.2 \times 10^{-4}", color=GREEN).next_to(row_A, DOWN, buff=0.4)
        row_C = MathTex(r"C = 0.00021", color=YELLOW).next_to(row_B, DOWN, buff=0.4)

        row_A_unified = MathTex(r"A = 75 \times 10^{-4}", color=BLUE).move_to(row_A)
        row_B_unified = MathTex(r"B = 8.2 \times 10^{-4}", color=GREEN).move_to(row_B)
        row_C_unified = MathTex(r"C = 2.1 \times 10^{-4}", color=YELLOW).move_to(row_C)

        final_order = MathTex(r"C < B < A", color=WHITE).move_to(ORIGIN + np.array([0, -1.3, 0]))
        highlight_box = SurroundingRectangle(final_order, color=RED)

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(4.02)

        # Step 2
        anim_time_2 = 2.5
        self.play(LaggedStart(Write(row_A), Write(row_B), Write(row_C), lag_ratio=0.4), run_time=2.5)
        self.wait(5.56)

        # Step 3
        self.play(Circumscribe(row_C, color=YELLOW), run_time=1.0)
        anim_time_3 = 1.0 + 2.0
        self.play(TransformMatchingTex(row_C, row_C_unified), run_time=2.0)
        self.wait(1.5)

        # Step 4
        self.play(Indicate(row_A, color=RED), run_time=1.0)
        anim_time_4 = 1.0 + 2.0
        self.play(TransformMatchingTex(row_A, row_A_unified), run_time=2.0)
        self.wait(1.5)

        # Step 5
        self.play(Write(final_order), run_time=1.0)
        self.play(Create(highlight_box), run_time=1.5)
        anim_time_5 = 1.0 + 1.5 + 1.0
        self.play(Circumscribe(final_order, color=RED), run_time=1.0)
        self.wait(1.5)
