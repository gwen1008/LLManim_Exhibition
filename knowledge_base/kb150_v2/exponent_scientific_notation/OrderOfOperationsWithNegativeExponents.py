# [VISUAL REASONING]
# Sequential ReplacementTransform on a centered equation to demonstrate PEMDAS
# with negative powers. Title fixed at top, step label upper-middle, equation
# at origin, explanation at bottom. Each step morphs the equation in place.

from manim import *


class OrderOfOperationsWithNegativeExponents(Scene):
    """
    指數與科學記號: 負數冪次運算遵循指數優先規則

    題目：計算 (-3)^3 ÷ 9 - (-2)^4 × 3 的值
    """
    def construct(self):
        # Step 1
        title = Text("Order of Operations with Negative Powers", color=WHITE, font_size=34)
        title.to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Original Expression", color=YELLOW, font_size=28)
        step_label.move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq0 = MathTex("(-3)^3 \\div 9 - (-2)^4 \\times 3", color=WHITE).move_to(ORIGIN)
        explain = Text("Powers first, then × and ÷, then + and -", color=BLUE, font_size=24)
        explain.move_to(ORIGIN + np.array([0, -2.2, 0]))

        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(6.58)

        # Step 2
        anim_time_2 = 2.0
        self.play(
            LaggedStart(
                Write(step_label),
                Write(eq0),
                FadeIn(explain),
                lag_ratio=0.2,
            ),
            run_time=2.0,
        )
        self.wait(4.69)

        # Step 3
        step_label_2 = Text("Step 2: Evaluate Powers", color=YELLOW, font_size=28)
        step_label_2.move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq1 = MathTex("-27 \\div 9 - 16 \\times 3", color=WHITE).move_to(ORIGIN)
        self.play(Indicate(eq0, color=YELLOW), run_time=0.8)
        anim_time_3 = 2.0
        self.play(
            ReplacementTransform(eq0, eq1),
            ReplacementTransform(step_label, step_label_2),
            run_time=2.0,
        )
        self.wait(6.8)

        # Step 4
        step_label_3 = Text("Step 3: Multiply and Divide", color=YELLOW, font_size=28)
        step_label_3.move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq2 = MathTex("-3 - 48", color=WHITE).move_to(ORIGIN)
        self.play(Indicate(eq1, color=ORANGE), run_time=0.8)
        anim_time_4 = 2.0
        self.play(
            ReplacementTransform(eq1, eq2),
            ReplacementTransform(step_label_2, step_label_3),
            run_time=2.0,
        )
        self.wait(7.08)

        # Step 5
        step_label_4 = Text("Step 4: Subtract", color=YELLOW, font_size=28)
        step_label_4.move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq3 = MathTex("-51", color=GREEN).move_to(ORIGIN)
        self.play(Circumscribe(eq2, color=GREEN), run_time=0.8)
        anim_time_5 = 2.0
        self.play(
            ReplacementTransform(eq2, eq3),
            ReplacementTransform(step_label_3, step_label_4),
            FadeOut(explain),
            run_time=2.0,
        )
        self.wait(3.7)
