# [VISUAL REASONING]
# Sequential ReplacementTransform of nested expression centered at origin,
# with step labels above and title at top. Final answer boxed in green.

from manim import *

class NestedParenthesesArithmetic(Scene):
    def construct(self):
        # Step 1
        title = Text("Order of Operations with Nested Brackets", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.5)
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(6.18)

        # Step 2
        eq0 = MathTex("30 - (-5) \\times [18 - (-2) \\times 4] \\div 10", color=WHITE).scale(0.9)
        eq0.move_to(ORIGIN)
        anim_time_2 = 2.0
        self.play(Write(eq0), run_time=2.0)
        self.wait(6.01)

        # Step 3
        step_label_1 = Text("Step 1: Innermost multiplication (-2) x 4", color=YELLOW, font_size=28)
        step_label_1.move_to(ORIGIN + np.array([0, 2.0, 0]))
        self.play(Circumscribe(eq0, color=YELLOW), run_time=1.5)
        anim_time_3 = 1.5 + 1.5
        self.play(Write(step_label_1), run_time=1.5)
        self.wait(1.5)

        # Step 4
        eq1 = MathTex("30 - (-5) \\times [18 - (-8)] \\div 10", color=WHITE).scale(0.9)
        eq1.move_to(ORIGIN)
        anim_time_4 = 2.0
        self.play(ReplacementTransform(eq0, eq1), run_time=2.0)
        self.wait(5.39)

        # Step 5
        step_label_2 = Text("Step 2: Resolve brackets  18 - (-8) = 26", color=YELLOW, font_size=28)
        step_label_2.move_to(ORIGIN + np.array([0, 2.0, 0]))
        eq2 = MathTex("30 - (-5) \\times 26 \\div 10", color=WHITE).scale(0.9)
        eq2.move_to(ORIGIN)
        anim_time_5 = 1.5
        self.play(ReplacementTransform(step_label_1, step_label_2), run_time=1.5)
        self.wait(8.67)

        # Step 6
        anim_time_6 = 2.0
        self.play(ReplacementTransform(eq1, eq2), run_time=2.0)
        self.wait(3.56)

        # Step 7
        step_label_3 = Text("Step 3: Multiplication and division left to right", color=YELLOW, font_size=28)
        step_label_3.move_to(ORIGIN + np.array([0, 2.0, 0]))
        eq3 = MathTex("30 - (-130) \\div 10", color=WHITE).scale(0.9)
        eq3.move_to(ORIGIN)
        anim_time_7 = 1.5 + 1.5
        self.play(ReplacementTransform(step_label_2, step_label_3), run_time=1.5)
        self.play(ReplacementTransform(eq2, eq3), run_time=1.5)
        self.wait(1.5)

        # Step 8
        eq4 = MathTex("30 - (-13)", color=WHITE).scale(0.9)
        eq4.move_to(ORIGIN)
        anim_time_8 = 2.0
        self.play(ReplacementTransform(eq3, eq4), run_time=2.0)
        self.wait(1.5)

        # Step 9
        step_label_4 = Text("Step 4: Final subtraction", color=YELLOW, font_size=28)
        step_label_4.move_to(ORIGIN + np.array([0, 2.0, 0]))
        eq5 = MathTex("= 43", color=GREEN).scale(0.9)
        eq5.move_to(ORIGIN)
        anim_time_9 = 1.5 + 1.5
        self.play(ReplacementTransform(step_label_3, step_label_4), run_time=1.5)
        self.play(ReplacementTransform(eq4, eq5), run_time=1.5)
        self.wait(1.5)

        # Step 10
        answer_box = SurroundingRectangle(eq5, color=GREEN, buff=0.2)
        self.play(Indicate(eq5, color=GREEN), run_time=1.0)
        anim_time_10 = 1.0 + 1.5
        self.play(Create(answer_box), run_time=1.5)
        self.wait(1.5)
