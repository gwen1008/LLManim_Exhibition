# [VISUAL REASONING]
# Pair grouping exposes the hidden constant difference -13,
# transforming a tedious 6-term computation into a simple 3×(-13) multiplication.

from manim import *

class GroupedIntegerSubtraction(Scene):
    def construct(self):
        title = Text("Alternating Sum by Pair Grouping", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        expr_full = MathTex("45 - 58 + 65 - 78 + 85 - 98", color=WHITE).move_to(ORIGIN + np.array([0, 0.8, 0]))
        brace1 = MathTex("\\underbrace{45 - 58}_{-13}", color=YELLOW).move_to(ORIGIN + np.array([-3.6, -0.3, 0]))
        brace2 = MathTex("\\underbrace{65 - 78}_{-13}", color=YELLOW).move_to(ORIGIN + np.array([0, -0.3, 0]))
        brace3 = MathTex("\\underbrace{85 - 98}_{-13}", color=YELLOW).move_to(ORIGIN + np.array([3.6, -0.3, 0]))
        simplified = MathTex("(-13) + (-13) + (-13)", color=WHITE).move_to(ORIGIN + np.array([0, 0.8, 0]))
        multiplied = MathTex("3 \\times (-13)", color=ORANGE).move_to(ORIGIN + np.array([0, 0.8, 0]))
        final_answer = MathTex("= -39", color=GREEN).move_to(ORIGIN + np.array([0, -1.0, 0]))
        footer_note = Text("Tip: Look for constant differences in alternating sums.", color=GREY, font_size=24).move_to(ORIGIN + np.array([0, -2.2, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(6.8)

        # Step 2
        anim_time_2 = 2.0
        self.play(Write(expr_full), run_time=2.0)
        self.wait(1.88)

        # Step 3
        self.play(Circumscribe(expr_full, color=YELLOW))
        anim_time_3 = 2.5 + 1.0
        self.play(Create(brace1), run_time=2.5)
        self.wait(1.5)

        # Step 4
        anim_time_4 = 2.0
        self.play(Create(brace2), run_time=2.0)
        self.wait(3.54)

        # Step 5
        anim_time_5 = 2.0
        self.play(Create(brace3), run_time=2.0)
        self.wait(1.64)

        # Step 6
        self.play(FadeOut(expr_full))
        anim_time_6 = 2.0 + 1.0
        self.play(Write(simplified), run_time=2.0)
        self.wait(1.5)

        # Step 7
        self.play(FadeOut(simplified), FadeOut(brace1), FadeOut(brace2), FadeOut(brace3))
        anim_time_7 = 2.0 + 1.0
        self.play(Write(multiplied), run_time=2.0)
        self.play(Indicate(multiplied, color=ORANGE))
        self.wait(1.5)

        # Step 8
        anim_time_8 = 2.0
        self.play(Write(final_answer), run_time=2.0)
        self.play(Circumscribe(final_answer, color=GREEN))
        self.wait(2.63)

        # Step 9
        anim_time_9 = 2.0
        self.play(Write(footer_note), run_time=2.0)
        self.wait(4.98)
