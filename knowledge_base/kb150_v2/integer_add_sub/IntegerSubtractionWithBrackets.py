# [VISUAL REASONING]
# Single-anchor in-place transformation walking through bracket removal,
# double-negative simplification, regrouping, and final evaluation to 365.
from manim import *

class IntegerSubtractionWithBrackets(Scene):
    """
    整數加減: 括號去除法則 + 項重排優化（相反數相消）

    題目：計算 365 - [148 + (-365)] - 217 的值
    """
    def construct(self):
        title = Text("Evaluate: 365 - [148 + (-365)] - 217", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Original Expression", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq1 = MathTex("365 - [148 + (-365)] - 217", color=WHITE).move_to(ORIGIN)
        eq2 = MathTex("365 - 148 - (-365) - 217", color=WHITE).move_to(ORIGIN)
        eq3 = MathTex("365 - 148 + 365 - 217", color=WHITE).move_to(ORIGIN)
        eq4 = MathTex("(365 + 365) - 148 - 217", color=WHITE).move_to(ORIGIN)
        eq5 = MathTex("730 - 365", color=WHITE).move_to(ORIGIN)
        eq6 = MathTex("= 365", color=GREEN).move_to(ORIGIN)
        explain = Text("Remove brackets carefully: signs flip inside a subtracted bracket.",
                       color=GREY_A, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 2.5
        self.play(FadeIn(title), FadeIn(step_label), FadeIn(explain), run_time=0.5)
        self.play(Write(eq1), run_time=2.0)
        self.wait(8.8)

        # Step 2
        new_step = Text("Step 2: Remove Brackets", color=YELLOW, font_size=28).move_to(step_label.get_center())
        self.play(FadeOut(explain), Transform(step_label, new_step), run_time=0.5)
        anim_time_2 = 2.8
        self.play(Indicate(eq1, color=YELLOW), run_time=0.8)
        self.play(ReplacementTransform(eq1, eq2), run_time=2.0)
        self.wait(13.59)

        # Step 3
        new_step3 = Text("Step 3: Simplify Double Negative", color=YELLOW, font_size=28).move_to(step_label.get_center())
        self.play(Transform(step_label, new_step3), run_time=0.5)
        anim_time_3 = 2.0
        self.play(ReplacementTransform(eq2, eq3), run_time=2.0)
        self.wait(5.96)

        # Step 4
        new_step4 = Text("Step 4: Group Like Terms", color=YELLOW, font_size=28).move_to(step_label.get_center())
        self.play(Transform(step_label, new_step4), run_time=0.5)
        anim_time_4 = 2.8
        self.play(Circumscribe(eq3, color=GREEN), run_time=0.8)
        self.play(ReplacementTransform(eq3, eq4), run_time=2.0)
        self.wait(4.95)

        # Step 5
        new_step5 = Text("Step 5: Combine", color=YELLOW, font_size=28).move_to(step_label.get_center())
        self.play(Transform(step_label, new_step5), run_time=0.5)
        anim_time_5 = 2.5
        self.play(ReplacementTransform(eq4, eq5), run_time=2.0)
        self.wait(15.86)

        # Step 6
        new_step6 = Text("Step 6: Final Answer", color=YELLOW, font_size=28).move_to(step_label.get_center())
        self.play(Transform(step_label, new_step6), run_time=0.5)
        anim_time_6 = 2.8
        self.play(ReplacementTransform(eq5, eq6), run_time=2.0)
        self.play(Circumscribe(eq6, color=GREEN), run_time=0.8)
        self.wait(2.33)
