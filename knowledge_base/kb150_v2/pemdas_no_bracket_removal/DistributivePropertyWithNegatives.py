# [VISUAL REASONING]
# Branch A: Stepwise distributive law morphing at ORIGIN.
# Single equation visible at a time, with step label above and explanation below.
# Each step uses TransformMatchingTex/ReplacementTransform for in-place morphing.

from manim import *

class DistributivePropertyWithNegatives(Scene):
    def construct(self):
        title = Text("分配律：提出共同因式", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        step_label = Text("步驟 1：原始算式", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))

        eq_step1 = MathTex(r"(-83) \times 124 - (-83) \times 24", color=WHITE).move_to(ORIGIN)
        eq_step2 = MathTex(r"(-83) \times (124 - 24)", color=WHITE).move_to(ORIGIN)
        eq_step3 = MathTex(r"(-83) \times 100", color=WHITE).move_to(ORIGIN)
        eq_final = MathTex(r"-8300", color=GREEN).move_to(ORIGIN)

        explain1 = Text("注意兩項都有共同因式 (-83)", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain2 = Text("括號內相減：124 - 24 = 100", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain3 = Text("相乘得到最終結果", color=WHITE, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(step_label), Write(eq_step1), run_time=2.0)
        self.wait(4.94)

        # Step 2
        anim_time_2 = 3.5
        self.play(Circumscribe(eq_step1, color=YELLOW), run_time=1.0)
        new_label2 = Text("步驟 2：提出共同因式", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        self.play(Transform(step_label, new_label2), run_time=0.5)
        self.play(
            TransformMatchingTex(eq_step1, eq_step2),
            FadeIn(explain1, shift=UP*0.2),
            run_time=2.0
        )
        self.wait(4.92)

        # Step 3
        anim_time_3 = 3.5
        self.play(FadeOut(explain1), run_time=0.3)
        self.play(Indicate(eq_step2, color=RED), run_time=1.0)
        new_label3 = Text("步驟 3：化簡括號", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        self.play(Transform(step_label, new_label3), run_time=0.5)
        self.play(
            TransformMatchingTex(eq_step2, eq_step3),
            FadeIn(explain2, shift=UP*0.2),
            run_time=2.0
        )
        self.wait(3.02)

        # Step 4
        anim_time_4 = 4.0
        self.play(FadeOut(explain2), run_time=0.3)
        self.play(Circumscribe(eq_step3, color=GREEN), run_time=1.2)
        new_label4 = Text("步驟 4：得到答案", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        self.play(Transform(step_label, new_label4), run_time=0.5)
        self.play(
            ReplacementTransform(eq_step3, eq_final),
            FadeIn(explain3, shift=UP*0.2),
            run_time=2.0
        )
        self.wait(2.72)
