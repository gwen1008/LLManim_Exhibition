# [VISUAL REASONING]
# Problem: virus diameter 6×10^-8 m × 5×10^9 viruses → total length
# Show original setup → multiply coefficients → add exponents → simplify → final answer 3.0×10² m

from manim import *

class ScientificNotationBacterialLength(Scene):
    """
    指數與科學記號: 單位換算 + 科學記號分離數字與指數相乘

    題目：某病毒直徑約 6×10^-8 公尺，若 5×10^9 個首尾相連緊密排成一直線，求總長度，請以科學記號 a×10^n 表示
    """
    def construct(self):
        # Step 1 — Problem statement
        title = Text("Virus diameter × count", color=WHITE, font_size=36).to_edge(UP, buff=0.6)
        problem = Text("6×10⁻⁸ m diameter, 5×10⁹ viruses → total length?", color=WHITE, font_size=24).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(problem), run_time=1.0)
        self.wait(2.0)

        # Step 2 — Setup equation
        eq1 = MathTex(r"(6 \times 10^{-8}) \times (5 \times 10^{9})", color=WHITE).move_to(ORIGIN).scale(1.1)
        self.play(Write(eq1), run_time=1.5)
        self.play(Circumscribe(eq1, color=YELLOW))
        self.wait(1.5)

        # Step 3 — Group coefficients and powers
        eq2 = MathTex(r"(6 \times 5) \times (10^{-8} \times 10^{9})", color=YELLOW).move_to(ORIGIN).scale(1.1)
        explain1 = Text("Group coefficients and powers of 10", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        self.play(ReplacementTransform(eq1, eq2), FadeIn(explain1), run_time=1.8)
        self.wait(2.0)

        # Step 4 — Multiply coefficients, add exponents
        eq3 = MathTex(r"30 \times 10^{1}", color=WHITE).move_to(ORIGIN).scale(1.2)
        explain2 = Text("6 × 5 = 30,   10⁻⁸ × 10⁹ = 10¹", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        self.play(FadeOut(explain1), run_time=0.3)
        self.play(ReplacementTransform(eq2, eq3), FadeIn(explain2), run_time=1.8)
        self.wait(2.0)

        # Step 5 — Normalize to scientific notation (coefficient 1 <= a < 10)
        eq4 = MathTex(r"3.0 \times 10^{2}\, \text{m}", color=GREEN).move_to(ORIGIN).scale(1.2)
        explain3 = Text("Normalize: 30 = 3.0 × 10,  so 30 × 10¹ = 3.0 × 10²", color=WHITE, font_size=22).move_to(ORIGIN + np.array([0, -2.3, 0]))
        self.play(FadeOut(explain2), run_time=0.3)
        self.play(Indicate(eq3, color=GREEN))
        self.play(ReplacementTransform(eq3, eq4), FadeIn(explain3), run_time=2.0)
        self.play(Circumscribe(eq4, color=GREEN))
        self.wait(3.0)
