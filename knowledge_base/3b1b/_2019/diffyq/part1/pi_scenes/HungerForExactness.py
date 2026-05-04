# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 展示教師與學生討論微分方程的精確解，從近似解過渡到複雜的雅可比橢圓函數解，最後以神秘問號和重新定義收尾。



from manim import *
class HungerForExactness(TeacherStudentsScene):
    def construct(self):
        students = self.students
        you = students[2]
        teacher = self.teacher

        ode = get_ode()
        ode.to_corner(UL)
        left_part = ode[:5]
        friction_part = ode[5:11]
        self.add(ode)

        proposed_solution = MathTex(
            "\\theta_0\\cos((\\sqrt{g/L})t)e^{-\\mu t}"
        )
        proposed_solution.next_to(
            you.get_corner(UL), UP, buff=0.7
        )
        proposed_solution_rect = SurroundingRectangle(
            proposed_solution, buff=MED_SMALL_BUFF,
        )
        proposed_solution_rect.set_color(BLUE)
        proposed_solution_rect.round_corners()

        solution_p1 = MathTex(
            """
            \\theta(t) = 2\\text{am}\\left(
                \\frac{\\sqrt{2g + Lc_1} (t + c_2)}{2\\sqrt{L}},
                \\frac{4g}{2g + Lc_1}
            \\right)
            """,
        )
        solution_p1.to_corner(UL)
        solution_p2 = MathTex(
            "c_1, c_2 = \\text{Constants depending on initial conditions}"
        )
        solution_p2.set_color(GREY_B)
        solution_p2.scale(0.75)
        solution_p3 = MathTex(
            """
            \\text{am}(u, k) =
            \\int_0^u \\text{dn}(v, k)\\,dv
            """
        )
        solution_p3.name = Text(
            "(Jacobi amplitude function)"
        )
        solution_p4 = MathTex(
            """
            \\text{dn}(u, k) =
            \\sqrt{1 - k^2 \\sin^2(\\phi)}
            """
        )
        solution_p4.name = Text(
            "(Jacobi elliptic function)"
        )
        solution_p5 = Text("Where $\\phi$ satisfies")
        solution_p6 = MathTex(
            """
            u = \\int_0^\\phi \\frac{dt}{\\sqrt{1 - k^2 \\sin^2(t)}}
            """
        )

        solution = VGroup(
            solution_p1,
            solution_p2,
            solution_p3,
            solution_p4,
            solution_p5,
            solution_p6,
        )
        solution.arrange(DOWN)
        solution.scale(0.7)
        solution.to_corner(UL, buff=MED_SMALL_BUFF)
        solution.set_stroke(width=0, background=True)

        solution.remove(solution_p2)
        solution_p1.add(solution_p2)
        solution.remove(solution_p5)
        solution_p6.add(solution_p5)

        for part in [solution_p3, solution_p4]:
            part.name.scale(0.7 * 0.7)
            part.name.set_color(GREY_B)
            part.name.next_to(part, RIGHT)
            part.add(part.name)

        self.student_says(
            "Right, but like,\\\\"
            "what \\emph{is} $\\theta(t)$?",
            target_mode="sassy",
            added_anims=[teacher.animate.change("guilty")],
        )
        self.wait()
        self.play(
            FadeIn(proposed_solution, shift=DOWN),
            RemovePiCreatureBubble(
                you,
                target_mode="raise_left_hand",
                look_at=proposed_solution,
            ),
            teacher.animate.change("pondering"),
            students[0].animate.change("pondering"),
            students[1].animate.change("hesitant"),
        )
        self.play(Create(proposed_solution_rect))
        self.play(
            proposed_solution.animate.shift(3 * RIGHT),
            proposed_solution_rect.animate.shift(3 * RIGHT),
            you.animate.change("raise_right_hand", teacher.eyes),
        )
        self.wait(3)

        self.play(
            FadeOut(proposed_solution),
            FadeOut(proposed_solution_rect),
            ode.animate.move_to(self.hold_up_spot).shift(DOWN + LEFT),
            teacher.animate.change("raise_right_hand"),
            self.change_students(*3 * ["pondering"])
        )
        self.wait()
        ode.save_state()
        self.play(
            left_part.animate.move_to(friction_part.get_right()),
            left_part.animate.match_y(left_part),
            friction_part.animate.to_corner(DR),
            friction_part.animate.set_opacity(0.5),
        )
        self.wait()

        modes = ["erm", "sad", "sad", "horrified"]
        for part, mode in zip(solution, modes):
            self.play(
                FadeIn(part, shift=UP),
                self.change_students(
                    *3 * [mode],
                    look_at=part,
                )
            )
            self.wait()
        self.wait(3)
        self.play_student_changes("tired", "sad", "concerned_musician")
        self.wait(4)
        self.look_at(solution)
        self.wait(5)
        self.play(
            FadeOut(solution, shift=2 * LEFT),
            Restore(ode),
            self.change_students(
                "sick", "angry", "tired",
            )
        )
        self.wait(3)

        mystery = MathTex(
            "\\theta(t) = ???",
            tex_to_color_map={"\\theta": BLUE},
        )
        mystery.scale(2)
        mystery.to_edge(UP)
        mystery.set_stroke(width=0, background=True)
        mystery_boundary = AnimatedBoundary(
            mystery, stroke_width=1
        )

        self.play(
            FadeIn(mystery, shift=DOWN),
            self.teacher.animate.change("pondering")
        )
        self.add(mystery_boundary, mystery)
        self.play_all_student_changes("sad")
        self.look_at(mystery)
        self.wait(5)

        # Define
        self.student_says(
            "Let $\\text{P}(\\mu, g, L; t)$ be a\\\\"
            "function satisfying this ODE.",
            index=0,
            target_mode="speaking",
            added_anims=[
                FadeOut(mystery),
                FadeOut(mystery_boundary),
                ode.animate.to_corner(UR)
            ]
        )
        self.play_student_changes(
            "hooray", "sassy", "sassy",
            look_at=students[0].eyes.get_corner(UR),
        )
        self.wait(2)
