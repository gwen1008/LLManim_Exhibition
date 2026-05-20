# [VISUAL REASONING]
# Branch A selected: Concrete factoring narrative with stepwise equation transforms.
# Title at top, equations centered, explanations at bottom, final answer highlighted.

from manim import *

class DistributivePropertyNegativeFactor(Scene):
    def construct(self):
        title = Text("Factoring a Negative Common Factor", color=WHITE, font_size=36).to_edge(UP, buff=0.5)
        eq0 = MathTex(r"73 \times (-28) - 27 \times 28", color=WHITE).move_to(ORIGIN)
        eq1 = MathTex(r"73 \times (-28) + 27 \times (-28)", color=WHITE).move_to(ORIGIN)
        eq2 = MathTex(r"(-28) \times (73 + 27)", color=WHITE).move_to(ORIGIN)
        eq3 = MathTex(r"(-28) \times 100", color=WHITE).move_to(ORIGIN)
        eq4 = MathTex(r"-2800", color=YELLOW).move_to(ORIGIN)
        explain1 = Text("Rewrite -27x28 as +27x(-28)", color=GREY_A, font_size=28).to_edge(DOWN, buff=0.8)
        explain2 = Text("Both terms share factor (-28)", color=GREY_A, font_size=28).to_edge(DOWN, buff=0.8)
        explain3 = Text("73 + 27 = 100", color=GREY_A, font_size=28).to_edge(DOWN, buff=0.8)

        # Step 1
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.0)
        self.play(Write(eq0), run_time=2.0)
        self.wait(7.39)

        # Step 2
        anim_time_2 = 3.0
        self.play(Circumscribe(eq0, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(eq0, eq1), FadeIn(explain1), run_time=2.0)
        self.wait(6.67)

        # Step 3
        anim_time_3 = 3.0
        self.play(FadeOut(explain1), run_time=0.3)
        self.play(Indicate(eq1, color=YELLOW), run_time=0.7)
        self.play(ReplacementTransform(eq1, eq2), FadeIn(explain2), run_time=2.0)
        self.wait(3.64)

        # Step 4
        anim_time_4 = 2.1
        self.play(FadeOut(explain2), run_time=0.3)
        self.play(ReplacementTransform(eq2, eq3), FadeIn(explain3), run_time=1.8)
        self.wait(4.02)

        # Step 5
        anim_time_5 = 3.3
        self.play(FadeOut(explain3), run_time=0.3)
        self.play(ReplacementTransform(eq3, eq4), run_time=1.5)
        answer_box = SurroundingRectangle(eq4, color=YELLOW, buff=0.2)
        self.play(Create(answer_box), run_time=0.5)
        self.play(Circumscribe(eq4, color=YELLOW), run_time=1.0)
        self.wait(2.94)
