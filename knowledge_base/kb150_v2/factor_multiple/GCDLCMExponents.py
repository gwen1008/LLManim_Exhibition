"""
[VISUAL REASONING]
- Title at top, equations centered, footer note at bottom.
- Show given GCD/LCM, then prime factorizations, then extract exponents and sum.
- Signal actions: Circumscribe factor_gcd, Indicate factor_lcm.
- Cleanup intermediate equations before showing final boxed result.
"""
from manim import *


class GCDLCMExponents(Scene):
    def construct(self):
        title = Text("Finding a + b via GCD and LCM", color=WHITE, font_size=38).to_edge(UP)
        stage_center = ORIGIN
        footer_pos = np.array([0, -3.0, 0])

        given_eq = MathTex(r"\gcd(P,Q)=225,\quad lcm(P,Q)=259875", color=WHITE).scale(0.8)
        given_eq.move_to(stage_center + np.array([0, 1.5, 0]))

        factor_gcd = MathTex(r"225 = 3^{2}\cdot 5^{2}", color=YELLOW).scale(0.9)
        factor_gcd.move_to(stage_center + np.array([0, 0.3, 0]))

        factor_lcm = MathTex(r"259875 = 3^{3}\cdot 5^{3}\cdot 7\cdot 11", color=TEAL).scale(0.9)
        factor_lcm.move_to(stage_center + np.array([0, -0.7, 0]))

        result = MathTex(r"a + b = 6", color=YELLOW).scale(1.2)
        result.move_to(stage_center + np.array([0, -0.5, 0]))
        result_box = SurroundingRectangle(result, color=RED)

        footer_note = Text("Verified: P=4725, Q=12375", color=GREY, font_size=24)
        footer_note.move_to(footer_pos + np.array([0, 0.3, 0]))

        # Step 1
        anim_time_1 = 1.5
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(footer_note), run_time=0.4)
        self.wait(5.68)

        # Step 2
        anim_time_2 = 2.0
        self.play(Write(given_eq), run_time=2.0)
        self.wait(6.8)

        # Step 3
        anim_time_3 = 2.0
        self.play(Write(factor_gcd), run_time=2.0)
        self.play(Circumscribe(factor_gcd, color=YELLOW), run_time=1.2)
        self.wait(3.85)

        # Step 4
        anim_time_4 = 2.5
        self.play(Write(factor_lcm), run_time=2.5)
        self.play(Indicate(factor_lcm, color=TEAL), run_time=1.0)
        self.wait(9.34)

        # Step 5
        self.play(FadeOut(given_eq), FadeOut(factor_gcd), FadeOut(factor_lcm), run_time=0.8)
        anim_time_5 = 2.0 + 0.8
        self.play(Write(result), run_time=2.0)
        self.play(Create(result_box), run_time=0.8)
        self.wait(1.5)
