# [VISUAL REASONING]
# Branch A: Sequential morphing of the expression through ReplacementTransform.
# Title at top, step label upper-mid, equation centered, explanation footer.
# Each step updates label, transforms equation, and swaps explanation text.

from manim import *


class FractionArithmeticWithBrackets(Scene):
    """
    四則運算（含去括號）: 帶括號分數運算 = 按運算順序計算最內層乘除、括號內加減、最後乘除

    題目：計算 1/3 × [3/4 - (-1/6) × 3] ÷ 5/4 的值
    """
    def construct(self):
        title = Text("Order of Operations with Fractions", color=WHITE, font_size=36)
        title.move_to(ORIGIN + np.array([0, 3.0, 0]))

        step_label_1 = Text("Step 1: Original Expression", color=YELLOW, font_size=28).move_to(np.array([0, 1.6, 0]))
        step_label_2 = Text("Step 2: Compute innermost (-1/6) x 3", color=YELLOW, font_size=28).move_to(np.array([0, 1.6, 0]))
        step_label_3 = Text("Step 3: Resolve the bracket", color=YELLOW, font_size=28).move_to(np.array([0, 1.6, 0]))
        step_label_4 = Text("Step 4: Multiply and divide left to right", color=YELLOW, font_size=28).move_to(np.array([0, 1.6, 0]))
        step_label_5 = Text("Final Answer", color=GREEN, font_size=32).move_to(np.array([0, 1.6, 0]))

        eq1 = MathTex(r"\frac{1}{3} \times \left[ \frac{3}{4} - \left(-\frac{1}{6}\right) \times 3 \right] \div \frac{5}{4}", color=WHITE).move_to(ORIGIN)
        eq2 = MathTex(r"\frac{1}{3} \times \left[ \frac{3}{4} - \left(-\frac{1}{2}\right) \right] \div \frac{5}{4}", color=WHITE).move_to(ORIGIN)
        eq3 = MathTex(r"\frac{1}{3} \times \frac{5}{4} \div \frac{5}{4}", color=WHITE).move_to(ORIGIN)
        eq4 = MathTex(r"\frac{1}{3} \times \frac{5}{4} \times \frac{4}{5}", color=WHITE).move_to(ORIGIN)
        eq5 = MathTex(r"\frac{1}{3}", color=GREEN).move_to(ORIGIN)

        explain1 = Text("Identify innermost operation inside the bracket.", color=WHITE, font_size=24).move_to(np.array([0, -2.3, 0]))
        explain2 = Text("(-1/6) x 3 = -1/2", color=WHITE, font_size=24).move_to(np.array([0, -2.3, 0]))
        explain3 = Text("3/4 - (-1/2) = 3/4 + 1/2 = 5/4", color=WHITE, font_size=24).move_to(np.array([0, -2.3, 0]))
        explain4 = Text("Dividing by 5/4 equals multiplying by 4/5.", color=WHITE, font_size=24).move_to(np.array([0, -2.3, 0]))
        explain5 = Text("5/4 and 4/5 cancel, leaving 1/3.", color=GREEN, font_size=24).move_to(np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 3.5
        self.play(
            LaggedStart(
                Write(title),
                FadeIn(step_label_1, shift=DOWN * 0.2),
                Write(eq1),
                FadeIn(explain1, shift=UP * 0.2),
                lag_ratio=0.4,
            ),
            run_time=anim_time_1,
        )
        self.wait(6.02)

        # Step 2
        self.play(Circumscribe(eq1, color=YELLOW), run_time=1.2)
        self.play(FadeOut(explain1), run_time=0.3)
        anim_time_2 = 2.0
        self.play(
            ReplacementTransform(eq1, eq2),
            ReplacementTransform(step_label_1, step_label_2),
            FadeIn(explain2, shift=UP * 0.2),
            run_time=anim_time_2,
        )
        self.wait(6.1)

        # Step 3
        self.play(Indicate(eq2, color=RED), run_time=1.2)
        self.play(FadeOut(explain2), run_time=0.3)
        anim_time_3 = 2.0
        self.play(
            ReplacementTransform(eq2, eq3),
            ReplacementTransform(step_label_2, step_label_3),
            FadeIn(explain3, shift=UP * 0.2),
            run_time=anim_time_3,
        )
        self.wait(4.42)

        # Step 4
        self.play(FadeOut(explain3), run_time=0.3)
        anim_time_4 = 2.0
        self.play(
            ReplacementTransform(eq3, eq4),
            ReplacementTransform(step_label_3, step_label_4),
            FadeIn(explain4, shift=UP * 0.2),
            run_time=anim_time_4,
        )
        self.wait(6.77)

        # Step 5
        self.play(FadeOut(explain4), run_time=0.3)
        anim_time_5 = 2.0
        self.play(
            ReplacementTransform(eq4, eq5),
            ReplacementTransform(step_label_4, step_label_5),
            FadeIn(explain5, shift=UP * 0.2),
            run_time=anim_time_5,
        )
        self.play(Circumscribe(eq5, color=GREEN), run_time=1.5)
        self.wait(2.84)
