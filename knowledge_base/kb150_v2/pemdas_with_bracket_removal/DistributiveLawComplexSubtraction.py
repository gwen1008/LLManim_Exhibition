# [VISUAL REASONING]
# Substitution n=2025 reveals symmetry; distributive law + cancellation yields -2.
# Single equation morphs in place at ORIGIN via ReplacementTransform.
from manim import *

class DistributiveLawComplexSubtraction(Scene):
    """
    四則運算（含去括號）: 代換法 + 分配律 = 用代換簡化相似項結構，再用分配律展開

    題目：計算 2025 × (-2026) - 2024 × (-2027) 的值
    """
    def construct(self):
        title = Text("Substitution + Distributive Law", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        eq_original = MathTex(r"2025 \times (-2026) - 2024 \times (-2027)", color=WHITE).move_to(ORIGIN)
        eq_substitute = MathTex(r"Let  n = 2025,\ \ n(-n-1) - (n-1)(-n-2)", color=YELLOW).scale(0.85).move_to(ORIGIN)
        eq_expand = MathTex(r"(-n^2 - n) - (-n^2 - 2n + n + 2)", color=WHITE).move_to(ORIGIN)
        eq_simplify = MathTex(r"-n^2 - n + n^2 + n - 2", color=WHITE).move_to(ORIGIN)
        eq_final = MathTex(r"= -2", color=GREEN).scale(1.4).move_to(ORIGIN)
        step_label = Text("Step 1: Observe the structure", color=BLUE, font_size=28).move_to(ORIGIN + np.array([0, 1.5, 0]))
        footer_note = Text("Large numbers near each other -> substitute and cancel", color=GREY, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 3.5
        self.play(Write(title), run_time=1.5)
        self.play(LaggedStart(Write(eq_original), FadeIn(step_label), FadeIn(footer_note), lag_ratio=0.2, run_time=2.0))
        self.wait(9.74)

        # Step 2
        new_step2 = Text("Step 2: Substitute n = 2025", color=BLUE, font_size=28).move_to(step_label.get_center())
        anim_time_2 = 3.0
        self.play(Circumscribe(eq_original, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(eq_original, eq_substitute), Transform(step_label, new_step2), run_time=2.0)
        self.wait(10.96)

        # Step 3
        new_step3 = Text("Step 3: Distribute", color=BLUE, font_size=28).move_to(step_label.get_center())
        anim_time_3 = 3.0
        self.play(Indicate(eq_substitute, color=RED), run_time=1.0)
        self.play(ReplacementTransform(eq_substitute, eq_expand), Transform(step_label, new_step3), run_time=2.0)
        self.wait(3.36)

        # Step 4
        new_step4 = Text("Step 4: Cancel terms", color=BLUE, font_size=28).move_to(step_label.get_center())
        anim_time_4 = 3.0
        self.play(Indicate(eq_expand, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(eq_expand, eq_simplify), Transform(step_label, new_step4), run_time=2.0)
        self.wait(6.43)

        # Step 5
        new_step5 = Text("Answer: -2", color=GREEN, font_size=28).move_to(step_label.get_center())
        anim_time_5 = 3.0
        self.play(FadeOut(footer_note), run_time=0.5)
        self.play(ReplacementTransform(eq_simplify, eq_final), Transform(step_label, new_step5), run_time=2.0)
        self.play(Circumscribe(eq_final, color=GREEN), run_time=1.0)
        self.wait(3.74)
