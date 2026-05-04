# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示教師與學生場景中，三個微分方程範例從上方淡入的過程。



from manim import *
class ExampleTypicalODE(TeacherStudentsScene):
    def construct(self):
        examples = VGroup(
            MathTex(
                "{\\dot x}(t) = k{x}(t)",
                tex_to_color_map={
                    "{\\dot x}": BLUE,
                    "{x}": BLUE,
                },
            ),
            get_ode(),
            MathTex(
                "{\\partial T", "\\over", "\\partial t} = ",
                "{\\partial^2 T", "\\over", "\\partial x^2}", "+",
                "{\\partial^2 T", "\\over", "\\partial y^2}", "+",
                "{\\partial^2 T", "\\over", "\\partial z^2}",
                tex_to_color_map={
                    "T": RED,
                }
            ),
        )
        examples[1].get_parts_by_tex("theta").set_color(GREEN)
        examples.arrange(DOWN, buff=MED_LARGE_BUFF)
        examples.to_edge(UP)

        self.play(
            FadeIn(examples[0], shift=UP),
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play(
            FadeIn(examples[1], shift=UP),
            self.change_students(
                *3 * ["pondering"],
                look_at=examples,
            ),
        )
        self.play(
            FadeIn(examples[2], shift=UP)
        )
        self.wait(5)
