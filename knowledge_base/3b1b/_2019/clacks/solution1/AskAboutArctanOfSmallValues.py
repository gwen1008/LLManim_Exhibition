# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示教師與學生場景中，從 arctan(x) ≈ x 推導出 x ≈ tan(x) 的數學公式變換過程。



from manim import *
class AskAboutArctanOfSmallValues(TeacherStudentsScene):
    def construct(self):
        self.add_title()

        equation1 = MathTex(
            "\\arctan", "(", "x", ")", "\\approx", "x"
        )
        equation1.set_color_by_tex("arctan", YELLOW)
        equation2 = MathTex(
            "x", "\\approx", "\\tan", "(", "x", ")",
        )
        equation2.set_color_by_tex("tan", BLUE)
        for mob in equation1, equation2:
            mob.move_to(self.hold_up_spot, DOWN)

        self.play(
            FadeIn(equation1, shift=DOWN),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(
                "erm", "sassy", "confused"
            )
        )
        self.look_at(3 * UL)
        self.play(equation1.animate.shift(UP))
        self.play(
            TransformFromCopy(
                VGroup(*[equation1[i] for i in (2, 4, 5)]),
                VGroup(*[equation2[i] for i in (0, 1, 4)]),
            )
        )
        self.play(
            TransformFromCopy(
                VGroup(*[equation1[i] for i in (0, 1, 3)]),
                VGroup(*[equation2[i] for i in (2, 3, 5)]),
            ),
            self.change_students(
                "confused", "erm", "sassy",
            ),
        )
        self.look_at(3 * UL)
        self.wait(3)

    def add_title(self):
        title = TexText("For small $x$")
        subtitle = TexText("(e.g. $x = 0.001$)")
        subtitle.scale(0.75)
        subtitle.next_to(title, DOWN)
        title.add(subtitle)
        title.move_to(self.hold_up_spot)
        title.to_edge(UP)
        self.add(title)
