# [VISUAL REASONING]
# Single equation anchor at center, morphed step-by-step following PEMDAS.
# Title at top, step label upper, explanation at bottom.

from manim import *

class MixedArithmeticOrderOfOperations(Scene):
    def construct(self):
        title = Text("Order of Operations", color=YELLOW, font_size=40).move_to(ORIGIN + np.array([0, 3.0, 0]))
        step_label = Text("Step 1: Evaluate the powers", color=ORANGE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq0 = MathTex(r"\left(-\tfrac{1}{3}\right)^2 \div \left(\tfrac{1}{6}-\tfrac{1}{4}\right) \times (-3)^2", color=WHITE).scale(0.9).move_to(ORIGIN)
        eq1 = MathTex(r"\tfrac{1}{9} \div \left(\tfrac{1}{6}-\tfrac{1}{4}\right) \times 9", color=WHITE).scale(0.9).move_to(ORIGIN)
        eq2 = MathTex(r"\tfrac{1}{9} \div \left(-\tfrac{1}{12}\right) \times 9", color=WHITE).scale(0.9).move_to(ORIGIN)
        eq3 = MathTex(r"\tfrac{1}{9} \times (-12) \times 9", color=WHITE).scale(0.9).move_to(ORIGIN)
        eq4 = MathTex(r"-12", color=GREEN).scale(1.2).move_to(ORIGIN)
        explain1 = Text("(-1/3)^2 = 1/9   and   (-3)^2 = 9", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain2 = Text("Common denominator 12: 2/12 - 3/12 = -1/12", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain3 = Text("Dividing by -1/12 = Multiplying by -12", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        explain4 = Text("(1/9) * (-12) * 9 = -12", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.5)
        self.play(Write(eq0), run_time=1.5)
        self.wait(2.11)

        # Step 2
        anim_time_2 = 4.5
        self.play(Circumscribe(eq0, color=YELLOW), run_time=1.0)
        self.play(Write(step_label), run_time=1.0)
        self.play(FadeIn(explain1), run_time=0.8)
        self.play(ReplacementTransform(eq0, eq1), run_time=1.7)
        self.wait(3.58)

        # Step 3
        new_step2 = Text("Step 2: Simplify the bracket", color=ORANGE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        anim_time_3 = 3.8
        self.play(FadeOut(explain1), run_time=0.4)
        self.play(Indicate(eq1, color=RED), run_time=0.8)
        self.play(ReplacementTransform(step_label, new_step2), run_time=0.8)
        self.play(FadeIn(explain2), run_time=0.6)
        self.play(ReplacementTransform(eq1, eq2), run_time=1.2)
        step_label = new_step2
        self.wait(1.5)

        # Step 4
        new_step3 = Text("Step 3: Convert division", color=ORANGE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        anim_time_4 = 3.8
        self.play(FadeOut(explain2), run_time=0.4)
        self.play(Indicate(eq2, color=BLUE), run_time=0.8)
        self.play(ReplacementTransform(step_label, new_step3), run_time=0.8)
        self.play(FadeIn(explain3), run_time=0.6)
        self.play(ReplacementTransform(eq2, eq3), run_time=1.2)
        step_label = new_step3
        self.wait(1.5)

        # Step 5
        new_step4 = Text("Step 4: Final multiplication", color=ORANGE, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        anim_time_5 = 4.3
        self.play(FadeOut(explain3), run_time=0.4)
        self.play(Circumscribe(eq3, color=GREEN), run_time=1.0)
        self.play(ReplacementTransform(step_label, new_step4), run_time=0.8)
        self.play(FadeIn(explain4), run_time=0.6)
        self.play(ReplacementTransform(eq3, eq4), run_time=1.5)
        self.wait(1.5)
