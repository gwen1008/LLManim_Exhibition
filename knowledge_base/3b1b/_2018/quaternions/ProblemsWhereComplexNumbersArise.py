# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示三個複雜數字意外有用的問題實例，並以動畫方式呈現標題和項目符號列表。



from manim import *
class ProblemsWhereComplexNumbersArise(Scene):
    def construct(self):
        text = "Problems where complex numbers are surprisingly useful"
        title = Text(*text.split(" "), color=BLUE)
        title.to_edge(UP)
        underline = Line(LEFT, RIGHT)
        underline.set_width(title.width + 0.5)
        underline.next_to(title, DOWN)

        problems = VGroup(
            MathTex(
                "\\text{Integer solutions to}\\\\ a^2 + b^2 = c^2",
                alignment=""
            ),
            MathTex(
                "\\text{Understanding}\\\\",
                "1 - \\frac{1}{3} + \\frac{1}{5} - \\frac{1}{7} + \\cdots" +
                "=\\frac{\\pi}{4}",
                alignment="",
            ),
            Text("Frequency analysis")
        )
        problems.arrange(
            DOWN, buff=LARGE_BUFF, aligned_edge=LEFT
        )
        for problem in problems:
            problems.add(Dot().next_to(problem[0], LEFT))
        problems.next_to(underline, DOWN, buff=MED_LARGE_BUFF)
        problems.to_edge(LEFT)
        v_dots = MathTex("\\vdots")
        v_dots.scale(2)
        v_dots.next_to(problems, DOWN, aligned_edge=LEFT)

        self.add(problems, v_dots)
        self.play(
            Create(underline),
            LaggedStart(*[FadeIn(word, shift=DOWN) for word in title], lag_ratio=0.5),
            run_time=3
        )
        self.wait()
