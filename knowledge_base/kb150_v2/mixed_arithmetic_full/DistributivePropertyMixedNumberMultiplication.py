# [VISUAL REASONING]
# Title at top, step label above equation, equations transformed at ORIGIN,
# explanation at bottom. Uses distributive law to show 49 5/6 × (-6) = -299.

from manim import *

class DistributivePropertyMixedNumberMultiplication(Scene):
    def construct(self):
        title = Text("Compute 49 5/6 × (-6)", color=WHITE, font_size=40).to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Split the mixed number", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.6, 0]))
        eq_initial = MathTex(r"49\tfrac{5}{6} \times (-6)", color=WHITE).move_to(ORIGIN)
        eq_split = MathTex(r"= \left(49 + \tfrac{5}{6}\right) \times (-6)", color=WHITE).move_to(ORIGIN)
        eq_distribute = MathTex(r"= 49 \times (-6) + \tfrac{5}{6} \times (-6)", color=WHITE).scale(0.9).move_to(ORIGIN)
        eq_compute = MathTex(r"= -294 + (-5)", color=WHITE).move_to(ORIGIN)
        eq_final = MathTex(r"= -299", color=GREEN).move_to(ORIGIN)
        explain = Text("Distribute -6 to both parts.", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(4.52)

        # Step 2
        anim_time_2 = 2.5
        self.play(Write(eq_initial), run_time=1.5)
        self.play(FadeIn(step_label), FadeIn(explain), run_time=1.0)
        self.wait(4.53)

        # Step 3
        anim_time_3 = 3.0
        self.play(Circumscribe(eq_initial, color=YELLOW), run_time=1.0)
        self.play(TransformMatchingTex(eq_initial, eq_split), run_time=2.0)
        self.wait(2.47)

        # Step 4
        new_step = Text("Step 2: Apply distributive law", color=YELLOW, font_size=28).move_to(step_label.get_center())
        anim_time_4 = 2.5
        self.play(Transform(step_label, new_step), run_time=0.5)
        self.play(TransformMatchingTex(eq_split, eq_distribute), run_time=2.0)
        self.wait(3.42)

        # Step 5
        anim_time_5 = 3.0
        self.play(Indicate(eq_distribute, color=RED), run_time=1.0)
        self.play(TransformMatchingTex(eq_distribute, eq_compute), run_time=2.0)
        self.wait(5.76)

        # Step 6
        anim_time_6 = 2.5
        self.play(FadeOut(explain), run_time=0.5)
        self.play(TransformMatchingTex(eq_compute, eq_final), run_time=2.0)
        self.wait(2.27)
