from manim import *

class IntegerSignDeduction(Scene):
    """
    Integer multiplication division 整數乘除: Visualizes deducing integer sign relationships from given multiplication/division inequalities.
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

        # Title and Problem Statement
        title = Text("Integer Sign Deduction Problem", font_size=40).to_edge(UP)
        self.play(Write(title))

        problem_intro = Text("Given a, b, c are non-zero integers.", font_size=30)
        condition1_math = MathTex("a \\times b < 0")
        condition2_math = MathTex("b \\div c > 0")
        question_text = Text("Which statement is definitely true?", font_size=30)

        # Arrange problem statement elements
        problem_group = VGroup(problem_intro, condition1_math, condition2_math, question_text).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        problem_group.to_edge(LEFT).shift(UP*0.5)

        self.play(FadeIn(problem_intro, shift=UP))
        self.play(Write(condition1_math))
        self.play(Write(condition2_math))
        self.play(Write(question_text))
        self.wait(1)

        # --- Step 1: Analyze a * b < 0 ---
        step1_title = Text("Step 1: Analyze ", font_size=32, color="#3A86FF")
        step1_eq = condition1_math.copy()
        step1_analysis_group = VGroup(step1_title, step1_eq).arrange(RIGHT, buff=0.1)
        step1_analysis_group.next_to(problem_group, RIGHT, buff=1).align_to(problem_intro, UP)

        self.play(
            TransformFromCopy(condition1_math, step1_eq),
            Write(step1_title)
        )
        self.wait(0.5)

        explanation1_short = MathTex("\\Rightarrow \\text{a, b are opposite signs}", font_size=32)
        explanation1_short.next_to(step1_analysis_group, DOWN, buff=0.5).align_to(step1_analysis_group, LEFT)
        
        self.play(Write(explanation1_short))
        self.wait(1)

        # Example cases for a, b
        case1_a = MathTex("a > 0", color="#06D6A0")
        case1_b = MathTex("b < 0", color="#FF006E")
        case1_group = VGroup(case1_a, case1_b).arrange(RIGHT, buff=0.5)

        case2_a = MathTex("a < 0", color="#FF006E")
        case2_b = MathTex("b > 0", color="#06D6A0")
        case2_group = VGroup(case2_a, case2_b).arrange(RIGHT, buff=0.5)
        
        example_cases_ab = VGroup(case1_group, case2_group).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        example_cases_ab.next_to(explanation1_short, DOWN, buff=0.3).align_to(explanation1_short, LEFT)

        self.play(FadeIn(example_cases_ab, shift=UP))
        self.wait(1)

        # --- Step 2: Analyze b / c > 0 ---
        self.play(
            FadeOut(example_cases_ab),
            step1_analysis_group.animate.shift(UP*1.5),
            explanation1_short.animate.shift(UP*1.5)
        )

        step2_title = Text("Step 2: Analyze ", font_size=32, color="#3A86FF")
        step2_eq = condition2_math.copy()
        step2_analysis_group = VGroup(step2_title, step2_eq).arrange(RIGHT, buff=0.1)
        step2_analysis_group.next_to(step1_analysis_group, DOWN, buff=0.5).align_to(step1_analysis_group, LEFT)

        self.play(
            TransformFromCopy(condition2_math, step2_eq),
            Write(step2_title)
        )
        self.wait(0.5)

        explanation2_short = MathTex("\\Rightarrow \\text{b, c are same sign}", font_size=32)
        explanation2_short.next_to(step2_analysis_group, DOWN, buff=0.5).align_to(step2_analysis_group, LEFT)
        self.play(Write(explanation2_short))
        self.wait(1)

        # Example cases for b, c
        case3_b = MathTex("b > 0", color="#06D6A0")
        case3_c = MathTex("c > 0", color="#06D6A0")
        case3_group = VGroup(case3_b, case3_c).arrange(RIGHT, buff=0.5)

        case4_b = MathTex("b < 0", color="#FF006E")
        case4_c = MathTex("c < 0", color="#FF006E")
        case4_group = VGroup(case4_b, case4_c).arrange(RIGHT, buff=0.5)
        
        example_cases_bc = VGroup(case3_group, case4_group).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        example_cases_bc.next_to(explanation2_short, DOWN, buff=0.3).align_to(explanation2_short, LEFT)

        self.play(FadeIn(example_cases_bc, shift=UP))
        self.wait(1)

        # --- Step 3: Deduce a vs c relationship ---
        self.play(
            FadeOut(example_cases_bc),
            step1_analysis_group.animate.shift(UP*1.5),
            explanation1_short.animate.shift(UP*1.5),
            step2_analysis_group.animate.shift(UP*1.5),
            explanation2_short.animate.shift(UP*1.5)
        )
        
        deduction_title = Text("Step 3: Deduce a vs c relationship", font_size=32, color="#3A86FF")
        deduction_title.next_to(step2_analysis_group, DOWN, buff=0.5).align_to(step1_analysis_group, LEFT)
        self.play(Write(deduction_title))

        # Bring back key findings
        summary_ab = explanation1_short.copy()
        summary_bc = explanation2_short.copy()
        summary_group = VGroup(summary_ab, summary_bc).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_group.next_to(deduction_title, DOWN, buff=0.5).align_to(deduction_title, LEFT)
        
        self.play(
            TransformFromCopy(explanation1_short, summary_ab),
            TransformFromCopy(explanation2_short, summary_bc)
        )
        self.wait(0.5)

        arrow_ab_bc = Arrow(summary_ab.get_bottom(), summary_bc.get_top(), buff=0.1, color="#FFBE0B")
        self.play(Create(arrow_ab_bc))

        deduction_ac = Text("Since 'a' and 'b' are opposite, and 'b' and 'c' are same,", font_size=28)
        deduction_ac_cont = Text("then 'a' and 'c' must be opposite signs.", font_size=28)
        deduction_text_group = VGroup(deduction_ac, deduction_ac_cont).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        deduction_text_group.next_to(summary_group, DOWN, buff=0.5).align_to(summary_group, LEFT)
        
        self.play(Write(deduction_text_group))
        self.wait(1)

        final_conclusion_math = MathTex("\\Rightarrow a, c \\text{ are opposite signs}", font_size=36, color="#06D6A0")
        final_conclusion_math.next_to(deduction_text_group, DOWN, buff=0.5).align_to(deduction_text_group, LEFT)
        self.play(Write(final_conclusion_math))
        self.wait(1)

        # --- Step 4: Final Answer ---
        self.play(
            FadeOut(summary_group, arrow_ab_bc, deduction_text_group),
            deduction_title.animate.shift(UP*2.5),
            final_conclusion_math.animate.shift(UP*2.5)
        )

        final_step_title = Text("Step 4: Conclusion", font_size=32, color="#3A86FF")
        final_step_title.next_to(deduction_title, DOWN, buff=0.5).align_to(deduction_title, LEFT)
        self.play(Write(final_step_title))

        final_statement = Text("If 'a' and 'c' have opposite signs, then:", font_size=28)
        final_statement.next_to(final_step_title, DOWN, buff=0.5).align_to(final_step_title, LEFT)
        self.play(Write(final_statement))

        result_mult = MathTex("a \\times c < 0", font_size=36)
        result_div = MathTex("a \\div c < 0", font_size=36, color="#FFBE0B")
        
        final_results_group = VGroup(result_mult, result_div).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        final_results_group.next_to(final_statement, DOWN, buff=0.3).align_to(final_statement, LEFT)
        
        self.play(Write(result_mult))
        self.play(Write(result_div))
        self.wait(1)

        # Highlight the answer
        final_answer_box = self.get_glow_rect(result_div, color="#06D6A0", buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)