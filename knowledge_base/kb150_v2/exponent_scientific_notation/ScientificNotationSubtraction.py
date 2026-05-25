# [VISUAL REASONING]
# Translating Director's blueprint: morph a single central equation through four
# stages to teach addition in scientific notation, with synchronized step labels
# and explanations. Uses ReplacementTransform per implementation hints.

from manim import *

class ScientificNotationSubtraction(Scene):
    """
    指數與科學記號: 統一指數後提公因數加減

    題目：計算 (5.4×10^6) + (9×10^4) 並化為科學記號
    """
    def construct(self):
        title = Text("Adding Numbers in Scientific Notation", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Original Expression", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        step_label2 = Text("Step 2: Unify the Exponents", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        step_label3 = Text("Step 3: Factor Out 10^6", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        step_label4 = Text("Step 4: Add and Simplify", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))

        eq_stage1 = MathTex(r"(5.4 \times 10^{6}) + (9 \times 10^{4})", color=WHITE).move_to(ORIGIN)
        eq_stage2 = MathTex(r"(5.4 \times 10^{6}) + (0.09 \times 10^{6})", color=WHITE).move_to(ORIGIN)
        eq_stage3 = MathTex(r"(5.4 + 0.09) \times 10^{6}", color=WHITE).move_to(ORIGIN)
        eq_stage4 = MathTex(r"5.49 \times 10^{6}", color=GREEN).move_to(ORIGIN)

        explain1 = Text("Convert 9 x 10^4 = 0.09 x 10^6 to match exponents", color=BLUE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain2 = Text("Factor out the common 10^6", color=BLUE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain3 = Text("Add the coefficients: 5.4 + 0.09 = 5.49", color=BLUE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 3.0
        self.play(Write(title), Write(step_label), run_time=1.0)
        self.play(Write(eq_stage1), run_time=2.0)
        self.wait(6.62)

        # Step 2
        anim_time_2 = 3.5
        self.play(Circumscribe(eq_stage1, color=YELLOW), run_time=1.0)
        self.play(
            ReplacementTransform(eq_stage1, eq_stage2),
            ReplacementTransform(step_label, step_label2),
            FadeIn(explain1),
            run_time=2.0,
        )
        self.wait(4.03)

        # Step 3
        anim_time_3 = 3.5
        self.play(Indicate(eq_stage2, color=RED), run_time=1.0)
        self.play(
            ReplacementTransform(eq_stage2, eq_stage3),
            ReplacementTransform(step_label2, step_label3),
            FadeOut(explain1),
            FadeIn(explain2),
            run_time=2.0,
        )
        self.wait(2.76)

        # Step 4
        anim_time_4 = 3.5
        self.play(Circumscribe(eq_stage3, color=GREEN), run_time=1.0)
        self.play(
            ReplacementTransform(eq_stage3, eq_stage4),
            ReplacementTransform(step_label3, step_label4),
            FadeOut(explain2),
            FadeIn(explain3),
            run_time=2.0,
        )
        self.wait(8.16)

        # Step 5
        anim_time_5 = 2.5
        self.play(FadeOut(explain3), FadeOut(step_label4), run_time=0.5)
        self.play(Indicate(eq_stage4), run_time=1.0)
        self.play(Circumscribe(eq_stage4, color=GREEN), run_time=1.0)
        self.wait(2.18)
