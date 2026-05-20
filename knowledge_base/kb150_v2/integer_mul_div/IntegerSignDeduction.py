# [VISUAL REASONING]
# Number line anchors abstract sign reasoning to spatial intuition.
# Title at top, number line centered, conclusion at bottom.
# Red for negative side (n), green for positive side (p).

from manim import *


class IntegerSignDeduction(Scene):
    def construct(self):
        title = Text("Determining Signs of n and p", color=WHITE, font_size=38).move_to(ORIGIN + np.array([0, 3.0, 0]))
        num_line = NumberLine(x_range=[-5, 5, 1], length=10, include_numbers=False, color=GREY).move_to(ORIGIN)
        zero_label = MathTex("0", color=WHITE).move_to(ORIGIN + np.array([0, -0.5, 0]))
        neg_region = Text("Negative", color=RED, font_size=28).move_to(ORIGIN + np.array([-3.0, 0.8, 0]))
        pos_region = Text("Positive", color=GREEN, font_size=28).move_to(ORIGIN + np.array([3.0, 0.8, 0]))
        n_dot = Dot(point=[-3.0, 0, 0], color=RED, radius=0.12)
        n_label = MathTex("n", color=RED).next_to(n_dot, DOWN, buff=0.3)
        p_dot = Dot(point=[3.0, 0, 0], color=GREEN, radius=0.12)
        p_label = MathTex("p", color=GREEN).next_to(p_dot, DOWN, buff=0.3)
        conclusion_n = MathTex("n < 0", color=RED).move_to(ORIGIN + np.array([-2.0, -2.3, 0]))
        conclusion_p = MathTex("p > 0", color=GREEN).move_to(ORIGIN + np.array([2.0, -2.3, 0]))
        and_sym = MathTex(r"and", color=WHITE).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(3.34)

        # Step 2
        anim_time_2 = 2.5
        self.play(Create(num_line), run_time=2.0)
        self.play(LaggedStart(FadeIn(zero_label), FadeIn(neg_region), FadeIn(pos_region), lag_ratio=0.2), run_time=0.5)
        self.wait(6.3)

        # Step 3
        anim_time_3 = 2.0
        self.play(Indicate(neg_region, color=RED), run_time=0.8)
        self.play(Create(n_dot), Write(n_label), run_time=1.2)
        self.wait(3.35)

        # Step 4
        anim_time_4 = 2.0
        self.play(Indicate(pos_region, color=GREEN), run_time=0.8)
        self.play(Create(p_dot), Write(p_label), run_time=1.2)
        self.wait(2.6)

        # Step 5
        anim_time_5 = 3.0
        self.play(Write(conclusion_n), Write(and_sym), Write(conclusion_p), run_time=2.0)
        self.play(Circumscribe(conclusion_n, color=YELLOW), run_time=1.0)
        self.wait(1.32)
