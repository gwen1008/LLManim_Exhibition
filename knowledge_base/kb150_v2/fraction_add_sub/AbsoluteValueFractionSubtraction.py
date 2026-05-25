# [VISUAL REASONING]
# Sequential ReplacementTransform morphing equations through 5 stages
# to demonstrate |a| - |b| where a = -3 2/5, b = 2 1/4, answer = 23/20.
from manim import *

class AbsoluteValueFractionSubtraction(Scene):
    """
    分數加減: 絕對值 → 帶分數化假分數 → 通分 → 分子加減

    題目：若 a = -3 2/5, b = 2 1/4, 求 |a| - |b| 的值
    """
    def construct(self):
        # Step 1
        title = Text("Absolute Value of Mixed Fractions", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5)
        self.wait(2.0)

        # Step 2 — Given: a = -3 2/5, b = 2 1/4, find |a| - |b|
        step_label1 = Text("Step 1: Given a = -3 2/5, b = 2 1/4", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq1 = MathTex(r"\left| -3\tfrac{2}{5} \right| - \left| 2\tfrac{1}{4} \right|", color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(step_label1), Write(eq1), run_time=2.0)
        self.wait(2.5)

        # Step 3 — Remove absolute values
        step_label2 = Text("Step 2: Remove Absolute Values", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq2 = MathTex(r"3\tfrac{2}{5} - 2\tfrac{1}{4}", color=WHITE).move_to(ORIGIN)
        explain1 = Text("|-3 2/5| = 3 2/5,  |2 1/4| = 2 1/4", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        self.play(Circumscribe(eq1, color=YELLOW), run_time=1.0)
        self.play(
            ReplacementTransform(step_label1, step_label2),
            ReplacementTransform(eq1, eq2),
            FadeIn(explain1),
            run_time=2.0
        )
        self.wait(2.0)

        # Step 4 — Convert mixed to improper fractions
        step_label3 = Text("Step 3: Convert to Improper Fractions", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq3 = MathTex(r"\tfrac{17}{5} - \tfrac{9}{4}", color=WHITE).move_to(ORIGIN)
        explain2 = Text("3 2/5 = (3*5+2)/5 = 17/5;  2 1/4 = (2*4+1)/4 = 9/4", color=WHITE, font_size=22).move_to(ORIGIN + np.array([0, -2.3, 0]))
        self.play(FadeOut(explain1), run_time=0.3)
        self.play(
            ReplacementTransform(step_label2, step_label3),
            ReplacementTransform(eq2, eq3),
            FadeIn(explain2),
            run_time=2.0
        )
        self.wait(2.0)

        # Step 5 — Common denominator (LCM = 20)
        step_label4 = Text("Step 4: Common Denominator (LCM = 20)", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq4 = MathTex(r"\tfrac{68}{20} - \tfrac{45}{20}", color=WHITE).move_to(ORIGIN)
        explain3 = Text("17/5 = 68/20,  9/4 = 45/20", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        self.play(FadeOut(explain2), run_time=0.3)
        self.play(
            ReplacementTransform(step_label3, step_label4),
            ReplacementTransform(eq3, eq4),
            FadeIn(explain3),
            run_time=2.0
        )
        self.wait(2.0)

        # Step 6 — Final answer
        step_label5 = Text("Step 5: Subtract Numerators", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq5 = MathTex(r"\tfrac{68 - 45}{20} = \tfrac{23}{20}", color=GREEN).move_to(ORIGIN)
        self.play(FadeOut(explain3), run_time=0.3)
        self.play(Indicate(eq4, color=GREEN), run_time=1.0)
        self.play(
            ReplacementTransform(step_label4, step_label5),
            ReplacementTransform(eq4, eq5),
            run_time=2.0
        )
        self.wait(2.5)
