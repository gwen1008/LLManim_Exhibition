# [VISUAL REASONING]
# Branch A selected: visual cancellation of 18/18 makes the shortcut intuitive.
# Title at top, single equation at center, hint at bottom.
# Strike marks via Cross on isolated MathTex pieces (numerator/denominator built
# as separate Mobjects via VGroup) so strikes always align with their targets.

from manim import *

class FractionMultiplicationCancellation(Scene):
    """
    分數乘除: 整數與分母相同時直接約分

    題目：計算 18 × (-37/18) 的值
    """
    def construct(self):
        title = Text("約分捷徑：18 × (-37/18)", color=WHITE, font_size=36).to_edge(UP, buff=0.5)

        # 用獨立 MathTex 組裝分數，避免 \dfrac 子索引不穩問題
        int_18 = MathTex(r"18", color=WHITE).scale(1.2)
        times_sign = MathTex(r"\times", color=WHITE).scale(1.2)
        # 簡單括號：用大括號字元；負號併入分數前
        left_paren = MathTex(r"(\, -", color=WHITE).scale(1.2)
        numerator_37 = MathTex(r"37", color=WHITE).scale(1.0)
        frac_bar = Line(LEFT * 0.35, RIGHT * 0.35, color=WHITE, stroke_width=2)
        denom_18 = MathTex(r"18", color=WHITE).scale(1.0)
        frac_group = VGroup(numerator_37, frac_bar, denom_18).arrange(DOWN, buff=0.08)
        right_paren = MathTex(r"\,)", color=WHITE).scale(1.2)
        eq_initial = VGroup(int_18, times_sign, left_paren, frac_group, right_paren).arrange(RIGHT, buff=0.12).move_to(ORIGIN)

        # Cross 自動圍繞目標 Mobject，永遠對齊
        strike_top = Cross(int_18, stroke_color=RED, stroke_width=6, scale_factor=0.7)
        strike_bottom = Cross(denom_18, stroke_color=RED, stroke_width=6, scale_factor=0.7)

        eq_cancelled = MathTex(r"1 \times (-37)", color=WHITE).scale(1.2).move_to(ORIGIN)
        eq_final = MathTex(r"-37", color=YELLOW, font_size=72).move_to(ORIGIN)
        hint = Text("整數等於分母 → 直接約分", color=GREY_B, font_size=28).move_to(ORIGIN + np.array([0, -2.3, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.wait(3.85)

        # Step 2
        anim_time_2 = 2.0
        self.play(Write(eq_initial), run_time=2.0)
        self.wait(5.03)

        # Step 3
        anim_time_3 = 2.0
        self.play(Indicate(eq_initial, color=YELLOW), run_time=1.0)
        self.play(Create(strike_top), Create(strike_bottom), run_time=1.0)
        self.wait(2.96)

        # Step 4
        anim_time_4 = 1.5
        self.play(
            FadeOut(strike_top), FadeOut(strike_bottom),
            ReplacementTransform(eq_initial, eq_cancelled),
            run_time=1.5
        )
        self.wait(2.7)

        # Step 5
        anim_time_5 = 2.5
        self.play(ReplacementTransform(eq_cancelled, eq_final), FadeIn(hint), run_time=1.5)
        self.play(Circumscribe(eq_final, color=YELLOW), run_time=1.0)
        self.wait(1.14)
