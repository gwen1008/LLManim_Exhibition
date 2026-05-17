from manim import *

class DistributiveLawComplexSubtraction(Scene):
    """
    PEMDAS with bracket removal distributive 四則運算 含去括號: Visualizes simplifying 1999 * (-2000) - 1998 * (-2001) using substitution and the distributive law.
    """
    def construct(self):
        # Problem statement
        problem_statement = MathTex(
            "\\text{計算: } 1999 \\times (-2000) - 1998 \\times (-2001)",
            font_size=36
        ).to_edge(UP)
        self.play(Write(problem_statement))
        self.wait(0.5)

        # Initial expression (centered)
        eq0 = MathTex("1999 \\times (-2000) - 1998 \\times (-2001)")
        self.play(Write(eq0))
        self.wait(1)

        # Step 1: Introduce substitutions
        sub_hint1 = MathTex("1998", "=", "(1999 - 1)").next_to(eq0, UP, buff=1.0).shift(LEFT*3)
        sub_hint2 = MathTex("-2001", "=", "(-2000 - 1)").next_to(sub_hint1, DOWN, buff=0.5)
        
        self.play(
            FadeIn(sub_hint1[0], shift=LEFT),
            FadeIn(sub_hint1[1]),
            FadeIn(sub_hint1[2], shift=RIGHT),
            FadeIn(sub_hint2[0], shift=LEFT),
            FadeIn(sub_hint2[1]),
            FadeIn(sub_hint2[2], shift=RIGHT)
        )
        self.wait(1.5)

        # Highlight terms to be substituted in the original equation
        target_1998 = eq0.get_parts_by_tex("1998")
        target_minus_2001 = eq0.get_parts_by_tex("(-2001)")
        
        self.play(
            Indicate(target_1998, color=YELLOW),
            Indicate(target_minus_2001, color=YELLOW)
        )
        self.wait(0.5)

        # Step 2: Apply substitution
        eq1 = MathTex("1999 \\times (-2000) - [ (1999 - 1) \\times (-2000 - 1) ]")
        
        self.play(
            TransformMatchingTex(eq0, eq1),
            FadeOut(VGroup(sub_hint1, sub_hint2))
        )
        self.wait(1.5)

        # Step 3: Expand the bracketed multiplication using distributive law
        eq2 = MathTex("1999 \\times (-2000) - [ 1999 \\times (-2000) - 1999 \\times 1 - 1 \\times (-2000) + 1 \\times 1 ]")
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(2)

        # Step 4: Simplify terms inside the brackets
        eq3 = MathTex("1999 \\times (-2000) - [ 1999 \\times (-2000) - 1999 + 2000 + 1 ]")
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)

        # Step 5: Combine constant terms inside the brackets (-1999 + 2000 + 1 = 2)
        eq4 = MathTex("1999 \\times (-2000) - [ 1999 \\times (-2000) + 2 ]")
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(1.5)

        # Step 6: Remove the outer brackets by distributing the negative sign
        eq5 = MathTex("1999 \\times (-2000) - 1999 \\times (-2000) - 2")
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(1.5)

        # Step 7: Identify and cancel opposing terms
        term_pos = eq5.get_parts_by_tex("1999 \\times (-2000)")[0]
        term_neg = eq5.get_parts_by_tex("- 1999 \\times (-2000)")[0]

        self.play(
            term_pos.animate.set_color(GREEN),
            term_neg.animate.set_color(RED)
        )
        self.wait(0.5)
        
        self.play(
            FadeOut(term_pos, shift=UP*0.5),
            FadeOut(term_neg, shift=DOWN*0.5)
        )
        self.wait(0.5)
        
        # Step 8: Final result
        eq6 = MathTex("-2")
        self.play(TransformMatchingTex(eq5, eq6))
        self.wait(2)

        final_answer_box = SurroundingRectangle(eq6, color=GREEN, buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)
        
        self.play(FadeOut(problem_statement), FadeOut(eq6), FadeOut(final_answer_box))
        self.wait(0.5)