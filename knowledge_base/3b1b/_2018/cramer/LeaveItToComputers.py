# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示教師與學生場景中，透過動態視覺化逐步推導克拉瑪法則的過程，從線性系統到行列式公式的轉換。



from manim import *
class LeaveItToComputers(TeacherStudentsScene):
    def __init__(self, random_seed=1, **kwargs):
        super().__init__(**kwargs)
        self.random_seed = random_seed

    def construct(self):
        system = LinearSystem(height=3)
        system.next_to(self.pi_creatures, UP)
        system.generate_target()
        system.target.scale(0.5)
        system.target.to_corner(UL)

        cramer_groups = VGroup()
        for i in range(3):
            numer_matrix = get_cramer_matrix(
                system.matrix_mobject, system.output_vect_mob,
                index=i
            )
            color = YELLOW
            VGroup(*numer_matrix.mob_matrix[:, i]).set_color(color)
            VGroup(*numer_matrix.mob_matrix[:, i]).set_stroke(color, 1)
            numer = VGroup(
                get_det_text(numer_matrix, initial_scale_factor=3),
                numer_matrix
            )
            numer.to_corner(UP)
            denom_matrix_mobject = system.matrix_mobject.deepcopy()
            denom = VGroup(
                get_det_text(denom_matrix_mobject, initial_scale_factor=3),
                denom_matrix_mobject,
            )
            rhs = VGroup(numer, Line(LEFT, RIGHT).match_width(numer), denom)
            rhs.arrange(DOWN)
            rhs.set_height(2.25)
            rhs.move_to(self.hold_up_spot, DOWN)
            rhs.to_edge(RIGHT, buff=LARGE_BUFF)
            equals = MathTex("=").next_to(rhs, LEFT)
            variable = system.input_vect_mob.elements[i].copy()
            variable.next_to(equals, LEFT)
            cramer_group = VGroup(variable, equals, rhs)
            cramer_group.variable = variable
            cramer_group.equals = equals
            cramer_group.rhs = rhs
            cramer_groups.add(cramer_group)

        self.play(
            Write(system),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students("pondering", "thinking", "hooray")
        )
        self.wait(2)
        self.play(
            PiCreatureSays(
                self.teacher, "Let the computer \\\\ handle it",
                target_mode="shruggie",
            ),
            MoveToTarget(system, path_arc=90 * DEGREES),
            self.change_students(*["confused"] * 3)
        )
        self.wait(3)

        cg = cramer_groups[0]
        scale_factor = 1.5
        cg.scale(scale_factor, about_edge=DOWN)
        numer, line, denom = cg.rhs
        x_copy = system.input_vect_mob.elements[0].copy()
        self.play(
            RemovePiCreatureBubble(
                self.teacher, target_mode="raise_right_hand"),
            Create(line),
            ReplacementTransform(
                system.matrix_mobject.copy(),
                denom[1],
            ),
            Write(denom[0]),
            FadeIn(cg.equals),
            ReplacementTransform(x_copy, cg.variable),
        )
        denom_mover = denom.deepcopy()
        denom_mover.target = numer.deepcopy()
        column1 = VGroup(*denom_mover.target[1].mob_matrix[:, 0])
        column1.set_fill(opacity=0)
        column1.set_stroke(width=0)
        self.play(MoveToTarget(denom_mover))
        self.look_at(system)
        self.play(
            ReplacementTransform(
                system.output_vect_mob.elements.copy(),
                VGroup(*numer[1].mob_matrix[:, 0]),
                path_arc=90 * DEGREES
            ),
            self.teacher.animate.change("happy"),
        )
        self.remove(denom_mover)
        self.add(cg)
        self.play_all_student_changes("sassy")
        self.wait(2)
        self.play(
            cramer_groups[0].animate.scale(1 / scale_factor),
            cramer_groups[0].animate.next_to(cramer_groups[1], LEFT, MED_LARGE_BUFF),
            FadeIn(cramer_groups[1]),
            FadeOut(system),
            self.change_students(*3 * ["horrified"], look_at=UP),
        )
        self.wait()
        self.play(
            FadeIn(cramer_groups[2]),
            cramer_groups[:2].animate.next_to(cramer_groups[2], LEFT, MED_LARGE_BUFF),
            self.change_students(*3 * ["horrified"], look_at=UP),
        )
        self.wait()

        brace = Brace(cramer_groups, UP)
        rule_text = brace.get_text("``Cramer's rule''")

        self.play(
            GrowFromCenter(brace),
            Write(rule_text),
            self.change_students(
                "pondering", "erm", "maybe",
                look_at=brace,
            )
        )
        self.wait(3)
