from manim import *

class AbsoluteValueFractionSubtraction(Scene):
    """
    Fraction addition subtraction 分數加減: Visualizes the step-by-step calculation of |a| - |b| for mixed fractions
    a = -3 1/5 and b = 1 3/4, involving absolute values, mixed to improper fraction conversion,
    finding common denominators, and fraction subtraction.
    """
    def construct(self):
        # Initial problem statement
        a_val = MathTex(r"a = -3 \frac{1}{5}")
        b_val = MathTex(r"b = 1 \frac{3}{4}")
        problem_vars = VGroup(a_val, b_val).arrange(RIGHT, buff=1).to_edge(UP)
        self.play(Write(problem_vars))
        self.wait(0.5)

        initial_question = MathTex(r"\text{求 } |a| - |b| \text{ 的值}")
        initial_question.next_to(problem_vars, DOWN, buff=0.5)
        self.play(Write(initial_question))
        self.wait(1)

        # Main calculation line, starts by replacing the question
        current_expression = MathTex(r"|a| - |b|")
        current_expression.move_to(initial_question.get_center())
        self.add(current_expression) 
        self.play(FadeOut(initial_question, problem_vars))
        self.wait(0.5)

        # Step 1: Calculate absolute values
        step1_title = Text("步驟 1: 計算絕對值", font_size=30).to_edge(UL).shift(RIGHT*0.5)
        abs_a_calc = MathTex(r"|a| = \left|-3 \frac{1}{5}\right| = 3 \frac{1}{5}")
        abs_b_calc = MathTex(r"|b| = \left|1 \frac{3}{4}\right| = 1 \frac{3}{4}")
        abs_group = VGroup(abs_a_calc, abs_b_calc).arrange(DOWN, buff=0.3).next_to(step1_title, DOWN, buff=0.5).align_to(step1_title, LEFT)
        
        self.play(Write(step1_title), Write(abs_group))
        self.wait(1)

        # Transform current_expression to its first calculated form
        next_expression = MathTex(r"|a| - |b| = 3 \frac{1}{5} - 1 \frac{3}{4}")
        next_expression.move_to(current_expression.get_center()) 
        self.play(TransformMatchingTex(current_expression, next_expression))
        current_expression = next_expression
        self.wait(1.5)

        # Fade out step 1 details to make space for the next step
        self.play(FadeOut(step1_title, abs_group))
        self.wait(0.5)

        # Step 2: Convert mixed numbers to improper fractions
        step2_title = Text("步驟 2: 帶分數化為假分數", font_size=30).to_edge(UL).shift(RIGHT*0.5)
        conversion1 = MathTex(r"3 \frac{1}{5} = \frac{3 \times 5 + 1}{5} = \frac{16}{5}")
        conversion2 = MathTex(r"1 \frac{3}{4} = \frac{1 \times 4 + 3}{4} = \frac{7}{4}")
        conversion_group = VGroup(conversion1, conversion2).arrange(DOWN, buff=0.3).next_to(step2_title, DOWN, buff=0.5).align_to(step2_title, LEFT)
        
        self.play(Write(step2_title), Write(conversion_group))
        self.wait(1)

        # Transform current_expression to its second calculated form
        next_expression = MathTex(r"3 \frac{1}{5} - 1 \frac{3}{4} = \frac{16}{5} - \frac{7}{4}")
        next_expression.move_to(current_expression.get_center())
        self.play(TransformMatchingTex(current_expression, next_expression))
        current_expression = next_expression
        self.wait(1.5)

        # Fade out step 2 details
        self.play(FadeOut(step2_title, conversion_group))
        self.wait(0.5)

        # Step 3: Find common denominator (LCM) and convert
        step3_title = Text("步驟 3: 通分 (最小公倍數為 20)", font_size=30).to_edge(UL).shift(RIGHT*0.5)
        lcm_hint = MathTex(r"\text{LCM}(5, 4) = 20").next_to(step3_title, DOWN, buff=0.3).align_to(step3_title, LEFT)
        common_denom1 = MathTex(r"\frac{16}{5} = \frac{16 \times 4}{5 \times 4} = \frac{64}{20}")
        common_denom2 = MathTex(r"\frac{7}{4} = \frac{7 \times 5}{4 \times 5} = \frac{35}{20}")
        common_denom_group = VGroup(common_denom1, common_denom2).arrange(DOWN, buff=0.3).next_to(lcm_hint, DOWN, buff=0.5).align_to(step3_title, LEFT)
        
        self.play(Write(step3_title), Write(lcm_hint), Write(common_denom_group))
        self.wait(1)

        # Transform current_expression to its third calculated form
        next_expression = MathTex(r"\frac{16}{5} - \frac{7}{4} = \frac{64}{20} - \frac{35}{20}")
        next_expression.move_to(current_expression.get_center())
        self.play(TransformMatchingTex(current_expression, next_expression))
        current_expression = next_expression
        self.wait(1.5)

        # Fade out step 3 details
        self.play(FadeOut(step3_title, lcm_hint, common_denom_group))
        self.wait(0.5)

        # Step 4: Perform subtraction
        step4_title = Text("步驟 4: 分子相減", font_size=30).to_edge(UL).shift(RIGHT*0.5)
        subtraction_expr = MathTex(r"\frac{64}{20} - \frac{35}{20} = \frac{64 - 35}{20} = \frac{29}{20}")
        
        self.play(Write(step4_title))
        self.wait(0.5)

        # Transform current_expression to the final result
        next_expression = subtraction_expr
        next_expression.move_to(current_expression.get_center())
        self.play(TransformMatchingTex(current_expression, next_expression))
        current_expression = next_expression
        self.wait(2)

        # Final Answer
        final_answer_text = Text("最終答案:", font_size=36).next_to(current_expression, DOWN, buff=1).align_to(current_expression, LEFT)
        final_answer_value = MathTex(r"\frac{29}{20}", font_size=48, color=YELLOW).next_to(final_answer_text, RIGHT, buff=0.5)
        
        self.play(FadeOut(step4_title)) # Fade out last step title
        self.play(Write(final_answer_text), Write(final_answer_value))
        final_box = SurroundingRectangle(final_answer_value, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(3)