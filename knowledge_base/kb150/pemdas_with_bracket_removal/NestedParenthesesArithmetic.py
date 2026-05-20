from manim import *

class NestedParenthesesArithmetic(Scene):
    """
    PEMDAS with bracket removal distributive 四則運算 含去括號: Visualizes the step-by-step calculation of 24 - (-3) * [ 12 - (-4) * 3 ] / 6, emphasizing order of operations and nested parentheses.
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

        # Initial expression
        problem_tex = MathTex("24 - (-3) \\times [ 12 - (-4) \\times 3 ] \\div 6")
        problem_tex.move_to(UP * 2)
        self.play(Write(problem_tex))
        self.wait(1)

        current_expr = problem_tex

        # Step 1: Calculate (-4) * 3 = -12 (innermost multiplication)
        # Highlight (-4) \times 3
        # Indices for "(-4) \times 3" in the initial expression
        step1_highlight_target = current_expr[0][13:19] 
        highlight_rect_1 = self.get_glow_rect(step1_highlight_target, color="#FFBE0B")
        self.play(Create(highlight_rect_1))
        
        step1_calc = MathTex("(-4) \\times 3 = -12").next_to(current_expr, DOWN, buff=1)
        self.play(Write(step1_calc))
        self.wait(1)

        # Replace the calculated part with its result
        new_expr_1 = MathTex("24 - (-3) \\times [ 12 - (-12) ] \\div 6")
        new_expr_1.move_to(current_expr.get_center())
        
        self.play(
            TransformMatchingTex(current_expr, new_expr_1),
            FadeOut(step1_calc),
            FadeOut(highlight_rect_1)
        )
        current_expr = new_expr_1
        self.wait(1)

        # Step 2: Calculate 12 - (-12) = 24 (middle bracket subtraction)
        # Highlight 12 - (-12)
        # Indices for "12 - (-12)" in new_expr_1
        step2_highlight_target = current_expr[0][8:16] 
        highlight_rect_2 = self.get_glow_rect(step2_highlight_target, color="#FFBE0B")
        self.play(Create(highlight_rect_2))

        step2_calc = MathTex("12 - (-12) = 12 + 12 = 24").next_to(current_expr, DOWN, buff=1)
        self.play(Write(step2_calc))
        self.wait(1)

        # Replace the calculated part with its result
        new_expr_2 = MathTex("24 - (-3) \\times 24 \\div 6")
        new_expr_2.move_to(current_expr.get_center())
        
        self.play(
            TransformMatchingTex(current_expr, new_expr_2),
            FadeOut(step2_calc),
            FadeOut(highlight_rect_2)
        )
        current_expr = new_expr_2
        self.wait(1)

        # Step 3: Calculate (-3) * 24 = -72 (multiplication from left to right)
        # Highlight (-3) \times 24
        # Indices for "(-3) \times 24" in new_expr_2
        step3_highlight_target = current_expr[0][2:9] 
        highlight_rect_3 = self.get_glow_rect(step3_highlight_target, color="#FFBE0B")
        self.play(Create(highlight_rect_3))

        step3_calc = MathTex("(-3) \\times 24 = -72").next_to(current_expr, DOWN, buff=1)
        self.play(Write(step3_calc))
        self.wait(1)

        # Replace the calculated part with its result
        new_expr_3 = MathTex("24 - (-72) \\div 6")
        new_expr_3.move_to(current_expr.get_center())
        
        self.play(
            TransformMatchingTex(current_expr, new_expr_3),
            FadeOut(step3_calc),
            FadeOut(highlight_rect_3)
        )
        current_expr = new_expr_3
        self.wait(1)

        # Step 4: Calculate -72 / 6 = -12 (division from left to right)
        # Highlight (-72) \div 6
        # Indices for "(-72) \div 6" in new_expr_3
        step4_highlight_target = current_expr[0][2:9] 
        highlight_rect_4 = self.get_glow_rect(step4_highlight_target, color="#FFBE0B")
        self.play(Create(highlight_rect_4))

        step4_calc = MathTex("-72 \\div 6 = -12").next_to(current_expr, DOWN, buff=1)
        self.play(Write(step4_calc))
        self.wait(1)

        # Replace the calculated part with its result
        new_expr_4 = MathTex("24 - (-12)")
        new_expr_4.move_to(current_expr.get_center())
        
        self.play(
            TransformMatchingTex(current_expr, new_expr_4),
            FadeOut(step4_calc),
            FadeOut(highlight_rect_4)
        )
        current_expr = new_expr_4
        self.wait(1)

        # Step 5: Calculate 24 - (-12) = 36 (final subtraction)
        # Highlight the entire remaining expression
        step5_highlight_target = current_expr 
        highlight_rect_5 = self.get_glow_rect(step5_highlight_target, color="#FFBE0B")
        self.play(Create(highlight_rect_5))

        step5_calc = MathTex("24 - (-12) = 24 + 12 = 36").next_to(current_expr, DOWN, buff=1)
        self.play(Write(step5_calc))
        self.wait(1)

        # Replace the expression with the final answer
        final_answer_tex = MathTex("36")
        final_answer_tex.move_to(current_expr.get_center())
        
        self.play(
            TransformMatchingTex(current_expr, final_answer_tex),
            FadeOut(step5_calc),
            FadeOut(highlight_rect_5)
        )
        current_expr = final_answer_tex 
        self.wait(0.5)

        # Final highlight of the answer
        final_box = self.get_glow_rect(current_expr, color="#06D6A0", buff=0.2)
        self.play(Create(final_box), current_expr.animate.scale(1.2))
        self.wait(2)