# [VISUAL REASONING]
# Inside-out simplification via ReplacementTransform on a single anchored equation.
# Title at top, step label above equation, hint at bottom. Signal actions highlight
# the active sub-expression before each morph. Traditional Chinese subtitles via
# self.set_subtitle. All objects within screen bounds.

from manim import *

class MixedOperationsFractionsDecimals(Scene):
    def construct(self):
        title = Text("Nested Brackets: Inside-Out Simplification", color=WHITE, font_size=34).move_to(ORIGIN + np.array([0, 3.0, 0]))
        eq0 = MathTex(r"-4.5 \div \left[\left(\tfrac{1}{5}-1\right)\times \tfrac{5}{4}+\tfrac{3}{4}\right]", color=WHITE).scale(0.95).move_to(np.array([0, 0.3, 0]))
        eq1 = MathTex(r"-4.5 \div \left[\left(-\tfrac{4}{5}\right)\times \tfrac{5}{4}+\tfrac{3}{4}\right]", color=WHITE).scale(0.95).move_to(np.array([0, 0.3, 0]))
        eq2 = MathTex(r"-4.5 \div \left[-1 + \tfrac{3}{4}\right]", color=WHITE).move_to(np.array([0, 0.3, 0]))
        eq3 = MathTex(r"-4.5 \div \left(-\tfrac{1}{4}\right)", color=WHITE).move_to(np.array([0, 0.3, 0]))
        eq4 = MathTex(r"= 18", color=YELLOW).scale(1.4).move_to(np.array([0, 0.3, 0]))
        label0 = Text("Step 1: Innermost parentheses", color=TEAL, font_size=28).move_to(np.array([0, 1.6, 0]))
        label1 = Text("Step 2: Multiply (-4/5) x (5/4)", color=TEAL, font_size=28).move_to(np.array([0, 1.6, 0]))
        label2 = Text("Step 3: Add inside the bracket", color=TEAL, font_size=28).move_to(np.array([0, 1.6, 0]))
        label3 = Text("Step 4: Final division", color=TEAL, font_size=28).move_to(np.array([0, 1.6, 0]))
        hint = Text("Rule: simplify brackets from the innermost layer outward.", color=GREY_B, font_size=24).move_to(np.array([0, -2.2, 0]))

        # Step 1
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.5)
        self.play(Write(eq0), FadeIn(hint), run_time=1.5)
        self.wait(7.29)

        # Step 2
        anim_time_2 = 2.7
        self.play(Circumscribe(eq0, color=YELLOW), run_time=1.0)
        self.play(Write(label0), run_time=0.8)
        self.play(ReplacementTransform(eq0, eq1), run_time=0.9)
        self.wait(5.67)

        # Step 3
        anim_time_3 = 3.2
        self.play(FadeOut(label0), run_time=0.4)
        self.play(Indicate(eq1, color=RED), run_time=0.8)
        self.play(Write(label1), run_time=0.8)
        self.play(ReplacementTransform(eq1, eq2), run_time=1.2)
        self.wait(6.83)

        # Step 4
        anim_time_4 = 3.2
        self.play(FadeOut(label1), run_time=0.4)
        self.play(Circumscribe(eq2, color=YELLOW), run_time=0.8)
        self.play(Write(label2), run_time=0.8)
        self.play(ReplacementTransform(eq2, eq3), run_time=1.2)
        self.wait(5.15)

        # Step 5
        anim_time_5 = 3.2
        self.play(FadeOut(label2), run_time=0.4)
        self.play(Indicate(eq3, color=GREEN), run_time=0.8)
        self.play(Write(label3), run_time=0.8)
        self.play(ReplacementTransform(eq3, eq4), run_time=1.2)
        self.wait(4.04)
