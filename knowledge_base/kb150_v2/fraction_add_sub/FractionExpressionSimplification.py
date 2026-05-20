# [VISUAL REASONING]
# Single-anchor in-place transformation with color-coded denominator grouping.
# Each step uses ReplacementTransform to update the central equation while
# the step label above tracks progress. Signal actions (Indicate/Circumscribe)
# emphasize each transition before the equation morphs.

from manim import *

class FractionExpressionSimplification(Scene):
    def construct(self):
        # Step 1
        title = Text("Grouping Mixed Numbers by Denominator", color=WHITE, font_size=34).to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Original Expression", color=YELLOW, font_size=26).move_to(ORIGIN + np.array([0, 1.7, 0]))
        eq_original = MathTex(r"-\left(5\tfrac{3}{11} - 2\tfrac{5}{8}\right) + \left(5\tfrac{3}{8} - 2\tfrac{8}{11}\right)", color=WHITE).scale(0.85).move_to(ORIGIN)

        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(step_label), Write(eq_original), run_time=2.0)
        self.wait(3.86)

        # Step 2
        new_label_2 = Text("Step 2: Remove Parentheses", color=YELLOW, font_size=26).move_to(ORIGIN + np.array([0, 1.7, 0]))
        eq_expanded = MathTex(r"-5\tfrac{3}{11} + 2\tfrac{5}{8} + 5\tfrac{3}{8} - 2\tfrac{8}{11}", color=WHITE).scale(0.85).move_to(ORIGIN)
        explain = Text("Remove parentheses, flipping signs inside the negated group.", color=GREY_B, font_size=24).move_to(ORIGIN + np.array([0, -2.3, 0]))

        anim_time_2 = 3.0
        self.play(Indicate(eq_original, color=RED), run_time=1.0)
        self.play(
            ReplacementTransform(step_label, new_label_2),
            ReplacementTransform(eq_original, eq_expanded),
            FadeIn(explain),
            run_time=2.0
        )
        self.wait(5.54)

        # Step 3
        new_label_3 = Text("Step 3: Group by Denominator", color=YELLOW, font_size=26).move_to(ORIGIN + np.array([0, 1.7, 0]))
        eq_grouped = MathTex(r"\left(2\tfrac{5}{8} + 5\tfrac{3}{8}\right) + \left(-5\tfrac{3}{11} - 2\tfrac{8}{11}\right)", color=WHITE).scale(0.85).move_to(ORIGIN)

        anim_time_3 = 3.5
        self.play(FadeOut(explain), Circumscribe(eq_expanded, color=ORANGE), run_time=1.3)
        self.play(
            ReplacementTransform(step_label if step_label in self.mobjects else new_label_2, new_label_3),
            ReplacementTransform(eq_expanded, eq_grouped),
            run_time=2.2
        )
        self.wait(3.72)

        # Step 4
        new_label_4 = Text("Step 4: Compute Each Group", color=YELLOW, font_size=26).move_to(ORIGIN + np.array([0, 1.7, 0]))
        eq_computed = MathTex(r"8 \; + \; (-8)", color=WHITE).move_to(ORIGIN)

        anim_time_4 = 3.0
        self.play(Indicate(eq_grouped, color=YELLOW), run_time=1.0)
        self.play(
            ReplacementTransform(new_label_3, new_label_4),
            ReplacementTransform(eq_grouped, eq_computed),
            run_time=2.0
        )
        self.wait(2.78)

        # Step 5
        new_label_5 = Text("Step 5: Final Answer", color=YELLOW, font_size=26).move_to(ORIGIN + np.array([0, 1.7, 0]))
        eq_final = MathTex(r"= 0", color=GREEN).move_to(ORIGIN)

        anim_time_5 = 3.5
        self.play(Circumscribe(eq_computed, color=GREEN), run_time=1.0)
        self.play(
            ReplacementTransform(new_label_4, new_label_5),
            ReplacementTransform(eq_computed, eq_final),
            run_time=1.5
        )
        final_box = SurroundingRectangle(eq_final, color=GREEN, buff=0.25)
        self.play(Create(final_box), run_time=1.0)
        self.wait(3.19)
