# [VISUAL REASONING]
# Centered single-equation morph using ReplacementTransform.
# Color-coded cancellation pairs (3-3, 5-5, 13-26).
# Step labels above, explanations below, title fixed at top.

from manim import *

class MixedFractionMultiplicationCancellation(Scene):
    def construct(self):
        # Step 1
        title = Text("Multiplying Fractions with Cancellation", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Write the expression", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr_initial = MathTex(r"\left(-\frac{13}{3}\right) \cdot \frac{3}{2} \cdot \left(-\frac{7}{5}\right) \cdot \frac{5}{26}", color=WHITE).move_to(ORIGIN + np.array([0, 0.5, 0]))

        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(step_label), Write(expr_initial), run_time=1.5)
        self.wait(7.32)

        # Step 2
        step_label_2 = Text("Step 2: Handle the signs", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr_signs = MathTex(r"+\,\frac{13}{3} \cdot \frac{3}{2} \cdot \frac{7}{5} \cdot \frac{5}{26}", color=WHITE).move_to(ORIGIN + np.array([0, 0.5, 0]))
        explain_signs = Text("Two negatives multiply to a positive", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.2, 0]))

        anim_time_2 = 3.5
        self.play(Circumscribe(expr_initial, color=RED), run_time=1.5)
        self.play(
            ReplacementTransform(step_label, step_label_2),
            ReplacementTransform(expr_initial, expr_signs),
            FadeIn(explain_signs),
            run_time=2.0
        )
        self.wait(6.38)

        # Step 3
        step_label_3 = Text("Step 3: Rearrange into pairs", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr_paired = MathTex(r"\frac{3}{3} \cdot \frac{5}{5} \cdot \frac{13}{26} \cdot \frac{7}{2}", color=WHITE).move_to(ORIGIN + np.array([0, 0.5, 0]))
        explain_pair = Text("Rearrange: pair 3-3, 5-5, 13-26", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.2, 0]))

        anim_time_3 = 3.5
        self.play(FadeOut(explain_signs), run_time=0.3)
        self.play(Indicate(expr_signs, color=BLUE), run_time=1.2)
        self.play(
            ReplacementTransform(step_label_2, step_label_3),
            ReplacementTransform(expr_signs, expr_paired),
            FadeIn(explain_pair),
            run_time=2.0
        )
        self.wait(5.69)

        # Step 4
        step_label_4 = Text("Step 4: Cancel each pair", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr_cancelled = MathTex(r"1 \cdot 1 \cdot \frac{1}{2} \cdot \frac{7}{2}", color=WHITE).move_to(ORIGIN + np.array([0, 0.5, 0]))
        explain_cancel = Text("Cancel matching pairs", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.2, 0]))

        anim_time_4 = 3.5
        self.play(FadeOut(explain_pair), run_time=0.3)
        self.play(Circumscribe(expr_paired, color=ORANGE), run_time=1.2)
        self.play(
            ReplacementTransform(step_label_3, step_label_4),
            ReplacementTransform(expr_paired, expr_cancelled),
            FadeIn(explain_cancel),
            run_time=2.0
        )
        self.wait(5.66)

        # Step 5
        step_label_5 = Text("Step 5: Final answer", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr_final = MathTex(r"= \frac{7}{4}", color=GREEN).move_to(ORIGIN + np.array([0, 0.5, 0]))
        explain_final = Text("Multiply remaining: 7/4", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, -2.2, 0]))

        anim_time_5 = 3.5
        self.play(FadeOut(explain_cancel), run_time=0.3)
        self.play(Indicate(expr_cancelled, color=GREEN), run_time=1.2)
        self.play(
            ReplacementTransform(step_label_4, step_label_5),
            ReplacementTransform(expr_cancelled, expr_final),
            FadeIn(explain_final),
            run_time=2.0
        )
        self.wait(5.4)
