# Source: 3b1b/_2019/bayes/footnote.py
# Description: [3b1b translated] 展示老師與學生場景中，一系列數學公式依序出現並與對話框互動的過程。



from manim import *
class LandscapeOfTools(TeacherStudentsScene):
    def construct(self):
        group = self.get_formulas()
        bayes = group[0].copy()

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(
                *3 * ["confused"],
                look_at=group,
            ),
            FadeIn(bayes, shift=DOWN),
        )
        self.remove(bayes)
        self.play(
            ShowSubmobjectsOneByOne(group, remover=True),
            run_time=5
        )
        self.add(bayes)
        self.wait(2)

        bubble = self.students[0].get_bubble()
        self.add(bubble, bayes)
        self.play(
            bayes.animate.move_to(bubble.get_bubble_center()),
            DrawBorderThenFill(bubble),
            self.teacher.animate.change("happy"),
            self.change_students(
                "pondering", "erm", "erm",
                look_at=bubble,
            )
        )
        self.play_all_student_changes(
            "thinking", look_at=bayes,
        )
        self.wait()
        self.play(
            FadeOut(bayes),
            bubble.animate.set_fill(BLACK, 0.2),
            bubble.animate.set_stroke(WHITE, 1),
            self.change_students(
                "pleading", "guilty", "guilty",
            ),
            self.teacher.animate.change("hesitant")
        )
        self.wait(2)

    def get_formulas(self):
        group = VGroup(
            get_bayes_formula(),
            MathTex(
                "P(X = k) = {\\lambda^k \\over k!}", "e^{-\\lambda}",
                tex_to_color_map={
                    "k": YELLOW,
                    "\\lambda": GREEN,
                }
            ),
            MathTex(
                "{1 \\over \\sigma\\sqrt{2\\pi}}",
                "e^{\\frac{1}{2}\\left({(x - \\mu) \\over \\sigma}\\right)^2}",
                tex_to_color_map={
                    "\\sigma": GREEN,
                    "\\mu": BLUE,
                }
            ),
            MathTex(
                "P(X = k) =", "\\left({n \\over k}\\right)", "p^k(1-p)^{n-k}",
                tex_to_color_map={
                    "\\over": BLACK,
                    "p": WHITE,
                    "k": YELLOW,
                    "n": BLUE,
                    "k": GREEN
                }
            ),
            MathTex(
                "E[X + Y] = E[x] + E[y]"
            ),
            MathTex(
                "\\text{Var}(X + Y) = \\text{Var}(x) + \\text{Var}(y) + 2\\text{Cov}(X, Y)"
            ),
            MathTex(
                "H = \\sum_{i} -p_i \\log", "(p_i)",
                tex_to_color_map={
                    "p_i": YELLOW,
                }
            ),
            MathTex(
                "{n \\choose k}",
                "{B(k + \\alpha, n -k + \\beta) \\over B(\\alpha, \\beta)}",
                tex_to_color_map={
                    "\\alpha": BLUE,
                    "\\beta": YELLOW,
                }
            ),
            MathTex(
                "P(d) = \\log_{10}\\left(1 + {1 \\over d}\\right)",
                tex_to_color_map={"d": BLUE},
            ),
            MathTex(
                "\\text{Cov}(X, Y) = \\sum_{i, j} p({x}_i, {y}_j)({x}_i - \\mu_{x})({y}_j - \\mu_{y})",
                tex_to_color_map={
                    "{x}": BLUE,
                    "{y}": RED,
                }
            ),
        )

        group.move_to(self.hold_up_spot, DOWN)
        group.shift_onto_screen()
        return group
