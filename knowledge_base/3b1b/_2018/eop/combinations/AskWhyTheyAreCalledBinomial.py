# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示教師與學生場景，解釋為何二項式係數被稱為「二項式」，包含帕斯卡三角形、二項式展開示例和文字標籤的動畫。



from manim import *
class AskWhyTheyAreCalledBinomial(TeacherStudentsScene):
    def construct(self):
        example_binomials = VGroup(*[
            MathTex(f"(x+y)^{{{d}}}")
            for d in range(2, 7)
        ])
        example_binomials.arrange(UP)
        example_binomials.next_to(
            self.teacher.get_corner(UP+LEFT), UP 
        )

        pascals = PascalsTriangle(n_rows = 6)
        pascals.set_height(3)
        pascals.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        pascals.set_color_by_gradient(BLUE, YELLOW)

        binomial_word = Text(
            "Bi", "nomials",
            arg_separator = "",
        )
        binomial_word.set_color_by_tex("Bi", YELLOW)
        binomial_word.set_color_by_tex("nomials", WHITE)
        binomial_word.next_to(example_binomials, LEFT, buff = 1.5)
        arrows = VGroup(*[
            Arrow(binomial_word.get_right(), binom.get_left())
            for binom in example_binomials
        ])
        arrows.set_color(BLUE)

        two_variables = Text("Two", "variables")
        two_variables.next_to(binomial_word, DOWN)
        two_variables.shift(SMALL_BUFF*LEFT)
        for tv, bw in zip(two_variables, binomial_word):
            tv.set_color(bw.get_color())

        self.student_says(
            "Why are they called \\\\ ``binomial coefficients''?"
        )
        self.play(LaggedStartMap(FadeIn, pascals))
        self.wait()
        self.play(
            FadeIn(example_binomials[0]),
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand",
        )
        moving_binom = example_binomials[0].copy()
        for binom in example_binomials[1:]:
            self.play(Transform(moving_binom, binom))
            self.add(binom)
        self.wait()

        #Name them
        self.play(
            Write(binomial_word),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.play_student_changes(*["pondering"]*3)
        self.play(Write(two_variables))
        self.wait(2)
