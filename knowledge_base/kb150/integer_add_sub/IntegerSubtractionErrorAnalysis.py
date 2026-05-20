from manim import *

class IntegerSubtractionErrorAnalysis(Scene):
    """
    Integer addition subtraction 整數加減: Visualizes an error analysis problem for integer subtraction, specifically the rule for extracting a negative sign.
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
        title = Text("Error Analysis: Integer Add/Subtract", font_size=36).to_edge(UP)
        self.play(Write(title))

        problem_intro = Text("A student computes:", font_size=28).next_to(title, DOWN, buff=0.5).align_to(LEFT, LEFT)
        original_expression = MathTex("-45 - (-23) + (-12)", font_size=48)
        original_expression.next_to(problem_intro, DOWN, buff=0.3).align_to(problem_intro, LEFT)

        self.play(Write(problem_intro), Write(original_expression))
        self.wait(1)

        # Student's Steps
        step1_label = Text("Step 1:", font_size=28).next_to(original_expression, DOWN, buff=0.8).align_to(original_expression, LEFT)
        step1_eq = MathTex("\\text{expr} = -45 + 23 - 12", font_size=48).next_to(step1_label, RIGHT, buff=0.2)

        step2_label = Text("Step 2:", font_size=28).next_to(step1_label, DOWN, buff=0.8).align_to(step1_label, LEFT)
        step2_eq = MathTex("\\text{expr} = -(45 + 23) - 12", font_size=48).next_to(step2_label, RIGHT, buff=0.2)

        step3_label = Text("Step 3:", font_size=28).next_to(step2_label, DOWN, buff=0.8).align_to(step2_label, LEFT)
        step3_eq = MathTex("\\text{expr} = -68 - 12", font_size=48).next_to(step3_label, RIGHT, buff=0.2)

        step4_label = Text("Step 4:", font_size=28).next_to(step3_label, DOWN, buff=0.8).align_to(step3_label, LEFT)
        step4_eq = MathTex("\\text{expr} = -80", font_size=48).next_to(step4_label, RIGHT, buff=0.2)

        student_steps_group = VGroup(
            VGroup(step1_label, step1_eq),
            VGroup(step2_label, step2_eq),
            VGroup(step3_label, step3_eq),
            VGroup(step4_label, step4_eq)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(RIGHT*0.5) # Adjust position to make space for explanations

        self.play(FadeOut(problem_intro, original_expression))
        self.play(Write(student_steps_group[0]))
        self.wait(0.5)

        # Analysis of Step 1
        explanation_title = Text("Analyze Step 1:", font_size=28, color="#FFBE0B").to_corner(UR)
        exp1_part1 = MathTex("-(-23) = +23", font_size=40).next_to(explanation_title, DOWN, buff=0.5).align_to(explanation_title, LEFT)
        exp1_part2 = MathTex("+( -12) = -12", font_size=40).next_to(exp1_part1, DOWN, buff=0.3).align_to(exp1_part1, LEFT)
        exp1_conclusion = Text("Step 1 is correct.", font_size=28, color="#06D6A0").next_to(exp1_part2, DOWN, buff=0.5).align_to(exp1_part2, LEFT)

        self.play(Write(explanation_title))
        self.play(
            Indicate(original_expression[0][3:7], color="#3A86FF"), # -(-23)
            Indicate(step1_eq[0][4:7], color="#3A86FF") # +23
        )
        self.play(Write(exp1_part1))
        self.wait(0.5)
        self.play(
            Indicate(original_expression[0][7:11], color="#3A86FF"), # +(-12)
            Indicate(step1_eq[0][7:10], color="#3A86FF") # -12
        )
        self.play(Write(exp1_part2))
        self.play(Write(exp1_conclusion))
        self.wait(1.5)

        # Analysis of Step 2
        self.play(FadeOut(explanation_title, exp1_part1, exp1_part2, exp1_conclusion))
        self.play(Write(student_steps_group[1]))
        self.wait(0.5)

        explanation_title_2 = Text("Analyze Step 2:", font_size=28, color="#FFBE0B").to_corner(UR)
        self.play(Write(explanation_title_2))

        # Highlight the transformation in question
        rect_step1_part = self.get_glow_rect(step1_eq[0][2:7], color="#FF006E") # -45 + 23
        rect_step2_part = self.get_glow_rect(step2_eq[0][2:9], color="#FF006E") # -(45 + 23)
        self.play(Create(rect_step1_part))
        self.play(Transform(rect_step1_part, rect_step2_part))
        self.wait(1)

        # Show the incorrect extraction
        incorrect_extraction = MathTex("-45 + 23 \\neq -(45 + 23)", font_size=40, color="#FF006E")
        incorrect_extraction.next_to(explanation_title_2, DOWN, buff=0.5).align_to(explanation_title_2, LEFT)
        self.play(Write(incorrect_extraction))
        self.wait(1)

        # Demonstrate why it's incorrect
        expand_incorrect = MathTex("-(45 + 23) = -45 - 23", font_size=40).next_to(incorrect_extraction, DOWN, buff=0.3).align_to(incorrect_extraction, LEFT)
        self.play(Write(expand_incorrect))
        self.wait(1)

        # Show the correct extraction
        correct_extraction_label = Text("Correct sign extraction:", font_size=28).next_to(expand_incorrect, DOWN, buff=0.5).align_to(expand_incorrect, LEFT)
        correct_extraction_eq = MathTex("-45 + 23 = -(45 - 23)", font_size=40, color="#06D6A0").next_to(correct_extraction_label, DOWN, buff=0.3).align_to(correct_extraction_label, LEFT)
        
        self.play(Write(correct_extraction_label))
        self.play(Write(correct_extraction_eq))
        self.wait(1)

        expand_correct = MathTex("-(45 - 23) = -45 + 23", font_size=40).next_to(correct_extraction_eq, DOWN, buff=0.3).align_to(correct_extraction_eq, LEFT)
        self.play(Write(expand_correct))
        self.wait(1.5)

        # Conclude the error
        error_conclusion = Text("Therefore, the error occurs at Step 2.", font_size=26, color="#FF006E").next_to(expand_correct, DOWN, buff=0.8).align_to(expand_correct, LEFT)
        self.play(Write(error_conclusion))
        self.play(Indicate(step2_label, color="#FF006E"), Indicate(step2_eq, color="#FF006E"))
        self.wait(2)

        # Show the correct calculation path
        self.play(
            FadeOut(explanation_title_2, incorrect_extraction, expand_incorrect,
                    correct_extraction_label, correct_extraction_eq, expand_correct,
                    error_conclusion, rect_step1_part)
        )
        self.play(
            student_steps_group[0].animate.shift(LEFT*2),
            student_steps_group[1].animate.shift(LEFT*2),
            student_steps_group[2].animate.shift(LEFT*2),
            student_steps_group[3].animate.shift(LEFT*2),
            title.animate.shift(LEFT*2)
        )

        correct_path_title = Text("Correct calculation:", font_size=28, color="#06D6A0").to_corner(UR)
        self.play(Write(correct_path_title))

        correct_step1 = MathTex("\\text{expr} = -45 + 23 - 12", font_size=48).next_to(correct_path_title, DOWN, buff=0.5).align_to(correct_path_title, LEFT)
        correct_step2 = MathTex("= (-45 + 23) - 12", font_size=48).next_to(correct_step1, DOWN, buff=0.3).align_to(correct_step1, LEFT)
        correct_step3 = MathTex("= -22 - 12", font_size=48).next_to(correct_step2, DOWN, buff=0.3).align_to(correct_step2, LEFT)
        correct_step4 = MathTex("= -34", font_size=48).next_to(correct_step3, DOWN, buff=0.3).align_to(correct_step3, LEFT)

        self.play(Write(correct_step1))
        self.wait(0.5)
        self.play(Write(correct_step2))
        self.wait(0.5)
        self.play(Write(correct_step3))
        self.wait(0.5)
        self.play(Write(correct_step4))
        self.wait(2)

        final_answer_box = self.get_glow_rect(correct_step4, color="#06D6A0", buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)