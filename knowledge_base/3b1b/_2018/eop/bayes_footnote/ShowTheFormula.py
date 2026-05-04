# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示貝葉斯公式在教師與學生場景中的逐步推導過程，從條件機率定義到數值計算結果。



from manim import *
class ShowTheFormula(TeacherStudentsScene):
    def __init__(self, seconds_to_blink=3, **kwargs):
        super().__init__(seconds_to_blink=seconds_to_blink, **kwargs)
    
    def construct(self):
        scale_factor = 0.7
        sick = "\\text{sick}"
        positive = "\\text{positive}"
        formula = MathTex(
            "P(", sick, "\\,|\\,", positive, ")", "=",
            "{\\quad P(", sick, "\\text{ and }", positive, ") \\quad",
            "\\over",
            "P(", positive, ")}", "=",
            "{1/1{,}000", "\\over", "1/1{,}000", "+", "(999/1{,}000)(0.01)}"
        )
        formula.scale(scale_factor)
        formula.next_to(self.pi_creatures, UP, buff=LARGE_BUFF)
        formula.shift_onto_screen(buff=MED_LARGE_BUFF)
        
        equals_group = formula.get_parts_by_tex("=")
        equals_indices = [
            formula.index_of_part(equals)
            for equals in equals_group
        ]

        lhs = VGroup(*formula[:equals_indices[0]])
        initial_formula = VGroup(*formula[:equals_indices[1]])
        initial_formula.save_state()
        initial_formula.shift(3*RIGHT)

        over = formula.get_part_by_tex("\\over")
        num_start_index = equals_indices[0] + 1
        num_end_index = formula.index_of_part(over)
        numerator = VGroup(
            *formula[num_start_index:num_end_index]
        )
        numerator_rect = SurroundingRectangle(numerator)

        alt_numerator = MathTex(
            "P(", sick, ")", "P(", positive, "\\,|\\,", sick, ")"
        )
        alt_numerator.scale(scale_factor)
        alt_numerator.move_to(numerator)

        number_fraction = VGroup(*formula[equals_indices[-1]:])

        rhs = MathTex("\\approx 0.09")
        rhs.scale(scale_factor)
        rhs.move_to(equals_group[-1], LEFT)
        rhs.set_color(YELLOW)

        for mob in [formula, alt_numerator]:
            mob.set_color_by_tex(sick, SICKLY_GREEN)
            mob.set_color_by_tex(positive, YELLOW)

        # Ask question
        self.student_says("What does the \\\\ formula look like here?")
        self.play(self.teacher.animate.change("happy"))
        self.wait()
        self.play(
            Write(lhs),
            RemovePiCreatureBubble(
                self.students[1], target_mode="pondering",
            ),
            self.teacher.animate.change("raise_right_hand"),
            self.students[0].animate.change("pondering"),
            self.students[2].animate.change("pondering"),
        )
        self.wait()

        # Show initial formula
        lhs_copy = lhs.copy()
        self.play(
            LaggedStartMap(
                FadeIn, initial_formula, 
                lag_ratio=0.7
            ),
            Animation(lhs_copy, remover=True),
        )
        self.wait(2)
        self.play(Create(numerator_rect))
        self.play(FadeOut(numerator_rect))
        self.wait()
        self.play(Transform(numerator, alt_numerator))
        initial_formula.add(*numerator)
        formula.add(*numerator)
        self.wait(3)

        # Show number_fraction
        self.play(
            initial_formula.animate.move_to(initial_formula.saved_state),
            FadeIn(VGroup(*number_fraction[:3]))
        )
        self.wait(2)
        self.play(LaggedStartMap(
            FadeIn, VGroup(*number_fraction[3:]),
            run_time=3,
            lag_ratio=0.7
        ))
        self.wait(2)

        # Show rhs
        self.play(formula.animate.shift(UP))
        self.play(Write(rhs))
        self.play_student_changes(*["happy"]*3)
        self.look_at(rhs)
        self.wait(2)
