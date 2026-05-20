"""
[VISUAL REASONING]
Telescoping product visualized with colored diagonal strike-throughs on
adjacent canceling pairs (5,7,9,11), revealing the simplified 3/13.
"""
from manim import *


class TelescopingProductFractions(Scene):
    """
    分數乘除: 相鄰分子分母相消的連乘式化簡（望遠鏡型約分）

    題目：計算 (3/5) × (5/7) × (7/9) × (9/11) × (11/13) 的值
    """
    def construct(self):
        title = Text("Telescoping Product", color=WHITE, font_size=40).to_edge(UP, buff=0.6)

        # Build each fraction as VGroup(numerator, bar, denominator) so each digit is addressable.
        def make_frac(num_str: str, den_str: str, color=WHITE):
            num = MathTex(num_str, color=color)
            bar = Line(LEFT * 0.3, RIGHT * 0.3, color=color, stroke_width=2)
            den = MathTex(den_str, color=color)
            grp = VGroup(num, bar, den).arrange(DOWN, buff=0.08)
            grp.num = num
            grp.den = den
            return grp

        f1 = make_frac("3", "5")
        t1 = MathTex(r"\times")
        f2 = make_frac("5", "7")
        t2 = MathTex(r"\times")
        f3 = make_frac("7", "9")
        t3 = MathTex(r"\times")
        f4 = make_frac("9", "11")
        t4 = MathTex(r"\times")
        f5 = make_frac("11", "13")
        expr = VGroup(f1, t1, f2, t2, f3, t3, f4, t4, f5).arrange(RIGHT, buff=0.18).move_to(ORIGIN + np.array([0, 0.6, 0]))

        # 配對相消（分母 ↔ 下一個分數的分子）— Cross 自動對齊各 Mobject
        cancel_5 = VGroup(Cross(f1.den, stroke_color=YELLOW, stroke_width=5, scale_factor=0.9),
                          Cross(f2.num, stroke_color=YELLOW, stroke_width=5, scale_factor=0.9))
        cancel_7 = VGroup(Cross(f2.den, stroke_color=GREEN, stroke_width=5, scale_factor=0.9),
                          Cross(f3.num, stroke_color=GREEN, stroke_width=5, scale_factor=0.9))
        cancel_9 = VGroup(Cross(f3.den, stroke_color=ORANGE, stroke_width=5, scale_factor=0.9),
                          Cross(f4.num, stroke_color=ORANGE, stroke_width=5, scale_factor=0.9))
        cancel_11 = VGroup(Cross(f4.den, stroke_color=PINK, stroke_width=5, scale_factor=0.9),
                           Cross(f5.num, stroke_color=PINK, stroke_width=5, scale_factor=0.9))

        final_answer = MathTex(r"= \frac{3}{13}", color=YELLOW).move_to(ORIGIN + np.array([0, -1.7, 0]))
        answer_box = SurroundingRectangle(final_answer, color=YELLOW, buff=0.15)

        footer = Text(
            "Adjacent numerators and denominators cancel out",
            color=GREY_B,
            font_size=26,
        ).move_to(ORIGIN + np.array([0, -2.4, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(3.06)

        # Step 2
        anim_time_2 = 2.5
        self.play(Write(expr), run_time=2.5)
        self.wait(5.75)

        # Step 3
        self.play(Circumscribe(expr, color=YELLOW))
        anim_time_3 = 1.0 + 1.0 + 1.0 + 1.0 + 1.2
        self.play(Create(cancel_5), run_time=1.0)
        self.play(Create(cancel_7), run_time=1.0)
        self.play(Create(cancel_9), run_time=1.0)
        self.play(Create(cancel_11), run_time=1.0)
        self.wait(1.5)

        # Step 4
        anim_time_4 = 2.0
        self.play(Write(footer), run_time=2.0)
        self.play(Indicate(footer, color=WHITE))
        self.wait(4.44)

        # Step 5
        anim_time_5 = 1.5
        self.play(Write(final_answer), run_time=1.5)
        self.play(Create(answer_box))
        self.play(Circumscribe(final_answer, color=YELLOW))
        self.wait(1.99)
