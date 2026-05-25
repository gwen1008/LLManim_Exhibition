from manim import *

class MixedFractionMultiplicationCancellation(Scene):
    """
    Fraction multiplication division 分數乘除: Visualizes the step-by-step calculation of (-5 1/7) * 1 1/11 * (-1 2/9) * 7/36 using mixed-to-improper fraction conversion, commutative property, and cancellation.
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

        def create_fraction(num_tex, den_tex, font_size=48):
            num = MathTex(num_tex, font_size=font_size)
            den = MathTex(den_tex, font_size=font_size)
            width = max(num.width, den.width) + 0.2
            bar = Line(LEFT * width / 2, RIGHT * width / 2, stroke_width=2)
            num.next_to(bar, UP, buff=0.1)
            den.next_to(bar, DOWN, buff=0.1)
            return VGroup(num, bar, den)

        # Initial problem statement
        problem_text = Text("Calculate the value of:", font_size=36).to_edge(UP)
        initial_expr_parts = [
            MathTex(r"\left(-5\frac{1}{7}\right)"),
            MathTex(r"\times"),
            MathTex(r"\left(1\frac{1}{11}\right)"),
            MathTex(r"\times"),
            MathTex(r"\left(-1\frac{2}{9}\right)"),
            MathTex(r"\times"),
            MathTex(r"\left(\frac{7}{36}\right)")
        ]
        initial_expr = VGroup(*initial_expr_parts).arrange(RIGHT, buff=0.2).next_to(problem_text, DOWN, buff=0.5)
        
        self.play(Write(problem_text))
        self.play(Write(initial_expr))
        self.wait(1)

        # Step 1: Convert mixed numbers to improper fractions
        step1_label = Text("Step 1: Convert mixed numbers to improper fractions", font_size=30).to_edge(LEFT).shift(UP*2)
        self.play(Write(step1_label))
        self.wait(0.5)

        # Conversion 1: -5 1/7 = -36/7
        improper1 = MathTex(r"-\frac{36}{7}", font_size=48).move_to(initial_expr_parts[0])
        self.play(Transform(initial_expr_parts[0], improper1))
        self.wait(0.5)

        # Conversion 2: 1 1/11 = 12/11
        improper2 = MathTex(r"\frac{12}{11}", font_size=48).move_to(initial_expr_parts[2])
        self.play(Transform(initial_expr_parts[2], improper2))
        self.wait(0.5)

        # Conversion 3: -1 2/9 = -11/9
        improper3 = MathTex(r"-\frac{11}{9}", font_size=48).move_to(initial_expr_parts[4])
        self.play(Transform(initial_expr_parts[4], improper3))
        self.wait(0.5)

        # Update the full expression after conversions and shift up
        current_expr_converted = VGroup(*initial_expr_parts)
        self.play(
            current_expr_converted.animate.shift(UP * 1.5),
            FadeOut(step1_label)
        )
        self.wait(1)

        # Step 2: Rearrange terms using commutative property
        step2_label = Text("Step 2: Rearrange terms for easier cancellation", font_size=30).to_edge(LEFT).shift(UP*1)
        self.play(Write(step2_label))
        self.wait(0.5)

        # Highlight terms to be grouped
        self.play(Indicate(initial_expr_parts[0], color="#FFBE0B"), Indicate(initial_expr_parts[6], color="#FFBE0B")) # (-36/7) and (7/36)
        self.play(Indicate(initial_expr_parts[2], color="#3A86FF"), Indicate(initial_expr_parts[4], color="#3A86FF")) # (12/11) and (-11/9)
        self.wait(1)

        # Create the rearranged expression
        rearranged_expr_part1 = MathTex(r"\left(-\frac{36}{7} \times \frac{7}{36}\right)", font_size=48)
        rearranged_expr_part2 = MathTex(r"\left(\frac{12}{11} \times \left(-\frac{11}{9}\right)\right)", font_size=48)
        
        rearranged_expr = VGroup(rearranged_expr_part1, MathTex(r"\times", font_size=48), rearranged_expr_part2).arrange(RIGHT, buff=0.5)
        rearranged_expr.next_to(current_expr_converted, DOWN, buff=0.8)

        # Animate rearrangement by fading out old and fading in new
        self.play(
            FadeOut(current_expr_converted),
            FadeIn(rearranged_expr),
            FadeOut(step2_label)
        )
        self.wait(1)

        # Step 3: Perform cancellation in the first group
        step3_label = Text("Step 3: Cancel terms in the first group", font_size=30).to_edge(LEFT).shift(UP*0.5)
        self.play(Write(step3_label))
        self.wait(0.5)

        # Isolate the first group for cancellation (remove parentheses for clearer lines)
        frac1 = create_fraction("36", "7", font_size=48)
        frac2 = create_fraction("7", "36", font_size=48)
        first_group_for_cancel = VGroup(
            MathTex("-", font_size=48),
            frac1,
            MathTex(r"\times", font_size=48),
            frac2
        ).arrange(RIGHT, buff=0.2).move_to(rearranged_expr_part1)
        self.play(Transform(rearranged_expr_part1, first_group_for_cancel))
        self.wait(0.5)

        # Cancellation lines for 36
        line_36_1 = Line(frac1[0].get_corner(UL), frac1[0].get_corner(DR), stroke_width=3, color="#FF006E") # 36 in first fraction
        line_36_2 = Line(frac2[2].get_corner(UL), frac2[2].get_corner(DR), stroke_width=3, color="#FF006E") # 36 in second fraction
        self.play(Create(line_36_1), Create(line_36_2))
        self.wait(0.5)
        
        # Cancellation lines for 7
        line_7_1 = Line(frac1[2].get_corner(UL), frac1[2].get_corner(DR), stroke_width=3, color="#FF006E") # 7 in first fraction
        line_7_2 = Line(frac2[0].get_corner(UL), frac2[0].get_corner(DR), stroke_width=3, color="#FF006E") # 7 in second fraction
        self.play(Create(line_7_1), Create(line_7_2))
        self.wait(0.5)

        # Show result of first group
        result_group1 = MathTex(r"-1", font_size=48).move_to(first_group_for_cancel)
        self.play(
            FadeOut(line_36_1, line_36_2, line_7_1, line_7_2),
            Transform(first_group_for_cancel, result_group1),
            FadeOut(step3_label)
        )
        self.wait(1)

        # Step 4: Perform cancellation in the second group
        step4_label = Text("Step 4: Cancel terms in the second group", font_size=30).to_edge(LEFT).shift(UP*0.5)
        self.play(Write(step4_label))
        self.wait(0.5)

        # Isolate the second group for cancellation
        frac3 = create_fraction("12", "11", font_size=48)
        frac4 = create_fraction("11", "9", font_size=48)
        second_group_for_cancel = VGroup(
            frac3,
            MathTex(r"\times", font_size=48),
            MathTex(r"\left(-", font_size=48),
            frac4,
            MathTex(r"\right)", font_size=48)
        ).arrange(RIGHT, buff=0.15).move_to(rearranged_expr_part2)
        self.play(Transform(rearranged_expr_part2, second_group_for_cancel))
        self.wait(0.5)

        # Cancellation lines for 11
        line_11_1 = Line(frac3[2].get_corner(UL), frac3[2].get_corner(DR), stroke_width=3, color="#FF006E") # 11 in first fraction
        line_11_2 = Line(frac4[0].get_corner(UL), frac4[0].get_corner(DR), stroke_width=3, color="#FF006E") # 11 in second fraction
        self.play(Create(line_11_1), Create(line_11_2))
        self.wait(0.5)

        # Cancellation lines for 12 and 9 (by 3)
        line_12 = Line(frac3[0].get_corner(UL), frac3[0].get_corner(DR), stroke_width=3, color="#FF006E") # 12
        new_4 = MathTex("4", font_size=36, color="#06D6A0").next_to(frac3[0], UP, buff=0.1)
        line_9 = Line(frac4[2].get_corner(UL), frac4[2].get_corner(DR), stroke_width=3, color="#FF006E") # 9
        new_3 = MathTex("3", font_size=36, color="#06D6A0").next_to(frac4[2], DOWN, buff=0.1)
        
        self.play(Create(line_12), Write(new_4))
        self.play(Create(line_9), Write(new_3))
        self.wait(0.5)

        # Show result of second group
        result_group2 = MathTex(r"-\frac{4}{3}", font_size=48).move_to(second_group_for_cancel)
        self.play(
            FadeOut(line_11_1, line_11_2, line_12, line_9, new_4, new_3),
            Transform(second_group_for_cancel, result_group2),
            FadeOut(step4_label)
        )
        self.wait(1)

        # Step 5: Final multiplication
        step5_label = Text("Step 5: Multiply the results", font_size=30).to_edge(LEFT).shift(UP*0.5)
        self.play(Write(step5_label))
        self.wait(0.5)

        # The rearranged_expr now contains result_group1, the original times sign, and result_group2
        final_multiplication_expr = VGroup(first_group_for_cancel, rearranged_expr[1], second_group_for_cancel).arrange(RIGHT, buff=0.5)
        final_multiplication_expr.next_to(rearranged_expr, DOWN, buff=0.8)
        
        # Shift up the previous line and arrange the final multiplication
        self.play(
            rearranged_expr.animate.shift(UP * 1.5),
            Transform(VGroup(first_group_for_cancel, rearranged_expr[1], second_group_for_cancel), final_multiplication_expr)
        )
        self.wait(1)

        final_result = MathTex(r"\frac{4}{3}", font_size=60, color="#06D6A0").next_to(final_multiplication_expr, DOWN, buff=0.8)
        self.play(Write(final_result))
        self.wait(1)

        final_answer_box = self.get_glow_rect(final_result, color="#06D6A0", buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)
        
        self.play(FadeOut(*self.mobjects))
        self.wait(1)