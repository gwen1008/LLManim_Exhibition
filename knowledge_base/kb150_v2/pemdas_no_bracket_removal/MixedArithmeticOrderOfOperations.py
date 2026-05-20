# [VISUAL REASONING]
# Branch A: Sequential in-place ReplacementTransform through PEMDAS steps.
# Central equation morphs: 25-36÷(-5-4)×2 → 25-36÷(-9)×2 → 25-(-4)×2 → 25-(-8) → 33
# Step labels above equation update each step. Circumscribe/Indicate highlights before each morph.

from manim import *

class MixedArithmeticOrderOfOperations(Scene):
    def construct(self):
        title = Text("Order of Operations", color=YELLOW, font_size=40).to_edge(UP, buff=0.5)
        step_label_1 = Text("Step 1: Evaluate inside parentheses", color=WHITE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        step_label_2 = Text("Step 2: Division before multiplication", color=WHITE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        step_label_3 = Text("Step 3: Multiplication", color=WHITE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        step_label_4 = Text("Step 4: Subtraction", color=WHITE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))

        eq0 = MathTex("25 - 36 \\div (-5 - 4) \\times 2", color=WHITE).move_to(ORIGIN)
        eq1 = MathTex("25 - 36 \\div (-9) \\times 2", color=WHITE).move_to(ORIGIN)
        eq2 = MathTex("25 - (-4) \\times 2", color=WHITE).move_to(ORIGIN)
        eq3 = MathTex("25 - (-8)", color=WHITE).move_to(ORIGIN)
        eq4 = MathTex("33", color=GREEN).move_to(ORIGIN)

        # Step 1
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.0)
        self.play(Write(eq0), run_time=2.0)
        self.wait(13.27)

        # Step 2
        anim_time_2 = 3.5
        self.play(Circumscribe(eq0, color=YELLOW), run_time=1.0)
        self.play(FadeIn(step_label_1, shift=DOWN*0.2), run_time=0.5)
        self.play(ReplacementTransform(eq0, eq1), run_time=2.0)
        self.wait(4.78)

        # Step 3
        anim_time_3 = 3.5
        self.play(Circumscribe(eq1, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(step_label_1, step_label_2), run_time=0.5)
        self.play(ReplacementTransform(eq1, eq2), run_time=2.0)
        self.wait(6.67)

        # Step 4
        anim_time_4 = 3.5
        self.play(Indicate(eq2, color=RED), run_time=1.0)
        self.play(ReplacementTransform(step_label_2, step_label_3), run_time=0.5)
        self.play(ReplacementTransform(eq2, eq3), run_time=2.0)
        self.wait(2.04)

        # Step 5
        anim_time_5 = 4.5
        self.play(Indicate(eq3, color=GREEN), run_time=1.0)
        self.play(ReplacementTransform(step_label_3, step_label_4), run_time=0.5)
        self.play(ReplacementTransform(eq3, eq4), run_time=2.0)
        answer_box = SurroundingRectangle(eq4, color=GREEN, buff=0.3)
        self.play(Create(answer_box), run_time=1.0)
        self.wait(2.91)
