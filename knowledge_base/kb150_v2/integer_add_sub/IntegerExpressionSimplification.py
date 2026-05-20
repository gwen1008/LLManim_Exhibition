# [VISUAL REASONING]
# Pairing opposites visually to show cancellation to zero.
# Step 1: Show original expression with double negatives.
# Step 2: Transform to simplified form (resolve double negatives).
# Step 3: Show grouped expression highlighting inverse pairs.
# Step 4: Reveal each pair's sum (+1000 and -1000).
# Step 5: Final sum equals zero.

from manim import *


class IntegerExpressionSimplification(Scene):
    def construct(self):
        title = Text("Pairing Opposites to Reach Zero", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.5)

        expr_original = MathTex("(-3456) + 789 - (-4456) - 1789", color=WHITE)
        expr_original.move_to(ORIGIN + np.array([0, 1.5, 0]))

        expr_simplified = MathTex("-3456 + 789 + 4456 - 1789", color=WHITE)
        expr_simplified.move_to(ORIGIN + np.array([0, 1.5, 0]))

        expr_grouped = MathTex("(-3456 + 4456) + (789 - 1789)", color=WHITE)
        expr_grouped.move_to(ORIGIN + np.array([0, 0.3, 0]))

        pair1_label = MathTex("= 1000", color=GREEN)
        pair1_label.move_to(ORIGIN + np.array([-2.2, -1.0, 0]))

        pair2_label = MathTex("= -1000", color=ORANGE)
        pair2_label.move_to(ORIGIN + np.array([2.2, -1.0, 0]))

        final_sum = MathTex("1000 + (-1000) = 0", color=YELLOW)
        final_sum.move_to(ORIGIN + np.array([0, -2.0, 0]))

        self.add(title)

        # Step 1
        anim_time_1 = 2.0
        self.play(Write(expr_original), run_time=2.0)
        self.wait(12.64)

        # Step 2
        self.play(Circumscribe(expr_original, color=YELLOW))
        anim_time_2 = 2.0
        self.play(ReplacementTransform(expr_original, expr_simplified), run_time=2.0)
        self.wait(6.12)

        # Step 3
        anim_time_3 = 2.0
        self.play(Write(expr_grouped), run_time=2.0)
        self.wait(11.39)

        # Step 4
        self.play(Indicate(expr_grouped, color=GREEN))
        anim_time_4 = 3.0
        self.play(
            LaggedStart(
                Write(pair1_label),
                Write(pair2_label),
                lag_ratio=0.5,
            ),
            run_time=3.0,
        )
        self.wait(3.08)

        # Step 5
        anim_time_5 = 2.0
        self.play(Write(final_sum), run_time=2.0)
        self.play(Circumscribe(final_sum, color=YELLOW))
        self.wait(4.58)
