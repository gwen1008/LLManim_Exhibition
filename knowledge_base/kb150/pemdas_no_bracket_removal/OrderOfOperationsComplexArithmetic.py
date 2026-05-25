from manim import *

class OrderOfOperationsComplexArithmetic(Scene):
    """
    PEMDAS order of operations without bracket removal 四則運算算則 不含去括號: Visualizes the step-by-step calculation of (-48) / (-6) * (-2) - (13 - 25) * 3, emphasizing order of operations.
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

        # Initial expression to be calculated
        expr0 = MathTex("(-48)", r" \div ", "(-6)", r" \times ", "(-2)", " - ", "(", "13", " - ", "25", ")", r" \times ", "3").scale(0.9).to_edge(UP + LEFT)
        self.play(Write(expr0))
        self.wait(1)

        # Step 1: Calculate (-48) \div (-6)
        highlight_part1 = expr0[0:3]
        rect1 = self.get_glow_rect(highlight_part1, color="#3A86FF")
        self.play(Create(rect1))
        self.wait(0.5)

        calc_text1 = MathTex("(-48) \\div (-6) = 8").next_to(expr0, DOWN, buff=0.8).align_to(expr0, LEFT)
        self.play(Write(calc_text1))
        self.wait(1)

        # Replace the calculated part with its result in the main expression
        expr1 = MathTex("8", r" \times ", "(-2)", " - ", "(", "13", " - ", "25", ")", r" \times ", "3").scale(0.9).move_to(expr0.get_center())
        self.play(
            TransformMatchingTex(expr0, expr1),
            FadeOut(calc_text1),
            FadeOut(rect1)
        )
        self.wait(1)

        # Step 2: Calculate 8 \times (-2)
        highlight_part2 = expr1[0:3]
        rect2 = self.get_glow_rect(highlight_part2, color="#3A86FF")
        self.play(Create(rect2))
        self.wait(0.5)

        calc_text2 = MathTex("8 \\times (-2) = -16").next_to(expr1, DOWN, buff=0.8).align_to(expr1, LEFT)
        self.play(Write(calc_text2))
        self.wait(1)

        # Replace the calculated part
        expr2 = MathTex("-16", " - ", "(", "13", " - ", "25", ")", r" \times ", "3").scale(0.9).move_to(expr1.get_center())
        self.play(
            TransformMatchingTex(expr1, expr2),
            FadeOut(calc_text2),
            FadeOut(rect2)
        )
        self.wait(1)

        # Step 3: Calculate (13 - 25)
        highlight_part3 = expr2[2:7]
        rect3 = self.get_glow_rect(highlight_part3, color="#3A86FF")
        self.play(Create(rect3))
        self.wait(0.5)

        calc_text3 = MathTex("13 - 25 = -12").next_to(expr2, DOWN, buff=0.8).align_to(expr2, LEFT)
        self.play(Write(calc_text3))
        self.wait(1)

        # Replace the calculated part
        expr3 = MathTex("-16", " - ", "(-12)", r" \times ", "3").scale(0.9).move_to(expr2.get_center())
        self.play(
            TransformMatchingTex(expr2, expr3),
            FadeOut(calc_text3),
            FadeOut(rect3)
        )
        self.wait(1)

        # Step 4: Calculate (-12) \times 3
        highlight_part4 = expr3[2:5]
        rect4 = self.get_glow_rect(highlight_part4, color="#3A86FF")
        self.play(Create(rect4))
        self.wait(0.5)

        calc_text4 = MathTex("(-12) \\times 3 = -36").next_to(expr3, DOWN, buff=0.8).align_to(expr3, LEFT)
        self.play(Write(calc_text4))
        self.wait(1)

        # Replace the calculated part
        expr4 = MathTex("-16", " - ", "(-36)").scale(0.9).move_to(expr3.get_center())
        self.play(
            TransformMatchingTex(expr3, expr4),
            FadeOut(calc_text4),
            FadeOut(rect4)
        )
        self.wait(1)

        # Step 5: Calculate -16 - (-36)
        # Highlight the entire expression for the final step
        highlight_part5 = expr4
        rect5 = self.get_glow_rect(highlight_part5, color="#3A86FF")
        self.play(Create(rect5))
        self.wait(0.5)

        # Show the full calculation for the final step
        expr4_expanded = MathTex("-16", " - ", "(-36)", " = ", "-16", " + ", "36", " = ", "20").scale(0.9).move_to(expr4.get_center())
        self.play(
            TransformMatchingTex(expr4, expr4_expanded),
            FadeOut(rect5)
        )
        self.wait(1)

        # Highlight the final answer
        final_answer_part = expr4_expanded[-1] # The '20' token
        final_rect = self.get_glow_rect(final_answer_part, color="#06D6A0", buff=0.2)
        self.play(Create(final_rect))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        self.wait(1)