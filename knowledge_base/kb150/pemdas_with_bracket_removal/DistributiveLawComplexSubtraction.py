from manim import *

class DistributiveLawComplexSubtraction(Scene):
    """
    PEMDAS with bracket removal distributive 四則運算 含去括號: Visualizes simplifying 1999 * (-2000) - 1998 * (-2001) using substitution and the distributive law.
    """
    def get_glow_rect(self, mobject, color="#3A86FF", buff=0.15):

        return RoundedRectangle(

            corner_radius=0.15,

            color=color,

            stroke_width=3,

            fill_color=color,

            fill_opacity=0.15

        ).surround(mobject, buff=buff)


    def construct(self):

        # 🌌 Set sleek deep-dark slate background

        self.camera.background_color = "#0B0F19"


        # 📐 Add modern thin background coordinate grid

        grid = NumberPlane(

            x_range=[-7, 7, 1], y_range=[-4, 4, 1],

            background_line_style={"stroke_color": "#1E293B", "stroke_opacity": 0.4, "stroke_width": 1}

        )

        self.add(grid)

        # Problem statement
        problem_statement = MathTex(
            "\\text{Compute: } 1999 \\times (-2000) - 1998 \\times (-2001)",
            font_size=36
        ).to_edge(UP)
        self.play(Write(problem_statement))
        self.wait(0.5)

        # Initial expression (split into substring parts so get_parts_by_tex works)
        eq0 = MathTex("1999", "\\times", "(-2000)", "-", "1998", "\\times", "(-2001)")
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
        # eq0 was split as: [0]="1999" [1]="\times" [2]="(-2000)" [3]="-" [4]="1998" [5]="\times" [6]="(-2001)"
        target_1998 = eq0[4]
        target_minus_2001 = eq0[6]

        self.play(
            Indicate(target_1998, color="#FFBE0B", scale_factor=1.2),
            Indicate(target_minus_2001, color="#FFBE0B", scale_factor=1.2),
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

        # Step 7: Identify and cancel opposing terms by direct transform
        # The "1999*(-2000)" and "-1999*(-2000)" cancel each other.
        # Rather than slicing the un-split MathTex, just transform into the simplified form.
        eq5_canceled = MathTex("0 - 2").move_to(eq5)
        self.play(Transform(eq5, eq5_canceled))
        self.wait(0.5)
        
        # Step 8: Final result
        eq6 = MathTex("-2")
        self.play(TransformMatchingTex(eq5, eq6))
        self.wait(2)

        final_answer_box = self.get_glow_rect(eq6, color="#06D6A0", buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)
        
        self.play(FadeOut(problem_statement), FadeOut(eq6), FadeOut(final_answer_box))
        self.wait(0.5)