# [VISUAL REASONING]
# Linear PEMDAS reduction with in-place ReplacementTransform.
# Single equation visible at a time, step label above, subtitle below.

from manim import *

class OrderOfOperationsComplexArithmetic(Scene):
    def construct(self):
        # Step 1
        title = Text("Order of Operations", color=YELLOW, font_size=40).move_to(ORIGIN + np.array([0, 3.2, 0]))
        expr0 = MathTex(r"(-72) \div (-8) \times (-3) - (17 - 30) \times 2", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        anim_time_1 = 2.5
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(expr0), run_time=1.0)
        self.wait(9.45)

        # Step 2
        step_label = Text("Step 1: Division (left to right)", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr1 = MathTex(r"9 \times (-3) - (17 - 30) \times 2", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        anim_time_2 = 3.3
        self.play(Circumscribe(expr0, color=YELLOW), run_time=1.0)
        self.play(Write(step_label), run_time=0.8)
        self.play(ReplacementTransform(expr0, expr1), run_time=1.5)
        self.wait(4.69)

        # Step 3
        step_label2 = Text("Step 2: Multiplication", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr2 = MathTex(r"-27 - (17 - 30) \times 2", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        anim_time_3 = 3.6
        self.play(Indicate(expr1, color=RED), run_time=1.0)
        self.play(ReplacementTransform(step_label, step_label2), run_time=0.8)
        self.play(ReplacementTransform(expr1, expr2), run_time=1.8)
        self.wait(2.23)

        # Step 4
        step_label3 = Text("Step 3: Inside Parentheses", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr3 = MathTex(r"-27 - (-13) \times 2", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        anim_time_4 = 3.6
        self.play(Circumscribe(expr2, color=YELLOW), run_time=1.0)
        self.play(ReplacementTransform(step_label2, step_label3), run_time=0.8)
        self.play(ReplacementTransform(expr2, expr3), run_time=1.8)
        self.wait(2.54)

        # Step 5
        step_label4 = Text("Step 4: Multiply by 2", color=TEAL, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr4 = MathTex(r"-27 - (-26)", color=WHITE).move_to(ORIGIN + np.array([0, 0.3, 0]))
        anim_time_5 = 3.6
        self.play(Indicate(expr3, color=RED), run_time=1.0)
        self.play(ReplacementTransform(step_label3, step_label4), run_time=0.8)
        self.play(ReplacementTransform(expr3, expr4), run_time=1.8)
        self.wait(1.87)

        # Step 6
        step_label5 = Text("Step 5: Final Subtraction", color=GREEN, font_size=28).move_to(ORIGIN + np.array([0, 2.0, 0]))
        expr5 = MathTex(r"-27 + 26 = -1", color=GREEN).move_to(ORIGIN + np.array([0, 0.3, 0]))
        anim_time_6 = 4.6
        self.play(Circumscribe(expr4, color=GREEN), run_time=1.0)
        self.play(ReplacementTransform(step_label4, step_label5), run_time=0.8)
        self.play(ReplacementTransform(expr4, expr5), run_time=2.0)
        answer_box = SurroundingRectangle(expr5, color=GREEN, buff=0.2)
        self.play(Create(answer_box), run_time=0.8)
        self.wait(4.71)
