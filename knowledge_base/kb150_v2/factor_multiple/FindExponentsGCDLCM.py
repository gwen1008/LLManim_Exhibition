# [VISUAL REASONING]
# Vertical stack of M, N, GCD, LCM equations aligned by '=' for prime-by-prime
# comparison. Min/max rule shown below, answers x=2, y=2, z=1 revealed sequentially
# with Indicate highlights driving the derivation.

from manim import *

class FindExponentsGCDLCM(Scene):
    """
    因數與倍數: 利用 GCD(最小指數) 與 LCM(最大指數) 反推質因數分解中的未知指數

    題目：已知 M = 2^x × 3^3 × 7^z, N = 2^4 × 3^y × 7^2, GCD(M,N) = 2^2 × 3^2 × 7, LCM(M,N) = 2^4 × 3^3 × 7^2，求 x, y, z 的值
    """
    def construct(self):
        title = Text("Finding x, y, z from GCD and LCM", color=WHITE, font_size=34)
        title.move_to(ORIGIN + np.array([0, 3.2, 0]))

        eq_M = MathTex("M = 2^{x} \\cdot 3^{3} \\cdot 7^{z}", color=WHITE)
        eq_M.move_to(ORIGIN + np.array([0, 2.0, 0]))

        eq_N = MathTex("N = 2^{4} \\cdot 3^{y} \\cdot 7^{2}", color=WHITE)
        eq_N.move_to(ORIGIN + np.array([0, 1.0, 0]))

        eq_GCD = MathTex("\\gcd(M,N) = 2^{2} \\cdot 3^{2} \\cdot 7^{1}", color=YELLOW)
        eq_GCD.move_to(ORIGIN + np.array([0, 0.0, 0]))

        eq_LCM = MathTex("\\operatorname{lcm}(M,N) = 2^{4} \\cdot 3^{3} \\cdot 7^{2}", color=BLUE)
        eq_LCM.move_to(ORIGIN + np.array([0, -1.0, 0]))

        rule_label = MathTex("\\gcd:\\min(a,b)\\quad \\operatorname{lcm}:\\max(a,b)", color=GREEN)
        rule_label.move_to(ORIGIN + np.array([0, -2.0, 0]))

        ans_x = MathTex("x = 2", color=ORANGE).move_to(ORIGIN + np.array([-3.5, -2.3, 0]))
        ans_y = MathTex("y = 2", color=ORANGE).move_to(ORIGIN + np.array([0, -2.3, 0]))
        ans_z = MathTex("z = 1", color=ORANGE).move_to(ORIGIN + np.array([3.5, -2.3, 0]))

        # Step 1
        anim_time_1 = 1.5 + 2.4
        self.play(Write(title), run_time=1.5)
        self.play(LaggedStart(
            Write(eq_M), Write(eq_N), Write(eq_GCD), Write(eq_LCM),
            lag_ratio=0.2, run_time=2.4
        ))
        self.wait(1.5)

        # Step 2
        anim_time_2 = 2.0 + 1.2
        self.play(Write(rule_label), run_time=2.0)
        self.play(Circumscribe(rule_label, color=GREEN), run_time=1.2)
        self.wait(1.5)

        # Step 3
        self.play(FadeOut(rule_label), run_time=0.4)
        anim_time_3 = 0.4 + 1.2 + 1.8
        self.play(Indicate(eq_GCD, color=YELLOW), run_time=1.2)
        self.play(Write(ans_x), run_time=1.8)
        self.wait(1.5)

        # Step 4
        anim_time_4 = 1.2 + 1.8
        self.play(Indicate(eq_N, color=YELLOW), run_time=1.2)
        self.play(Write(ans_y), run_time=1.8)
        self.wait(1.5)

        # Step 5
        anim_time_5 = 1.2 + 1.8
        self.play(Indicate(eq_M, color=YELLOW), run_time=1.2)
        self.play(Write(ans_z), run_time=1.8)
        self.wait(1.5)
