# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 展示老師在黑板上寫出單擺的運動方程，學生質疑推導過程，老師心虛的互動場景。



from manim import *
class ProveTeacherWrong(TeacherStudentsScene):
    def construct(self):
        tex_config = {
            "tex_to_color_map": {
                "{\\theta}": BLUE,
                "{\\dot\\theta}": YELLOW,
                "{\\ddot\\theta}": RED,
            }
        }
        func = MathTex(
            "{\\theta}(t)", "=",
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)",
            **tex_config,
        )
        d_func = MathTex(
            "{\\dot\\theta}(t)", "=",
            "-\\left(\\sqrt{g / L}\\right)",
            "\\theta_0", "\\sin(\\sqrt{g / L} \\cdot t)",
            **tex_config,
        )
        dd_func = MathTex(
            "{\\ddot\\theta}(t)", "=",
            "-\\left(g / L\\right)",
            "\\theta_0", "\\cos(\\sqrt{g / L} \\cdot t)",
            **tex_config,
        )
        # ode = MathTex(
        #     "\\ddot {\\theta}({t})", "=",
        #     "-\\mu \\dot {\\theta}({t})",
        #     "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        #     **tex_config,
        # )
        ode = get_ode()  # 假設 get_ode() 返回一個 MathTex 對象
        arrows = [MathTex("\\Downarrow") for x in range(2)]

        VGroup(func, d_func, dd_func, ode, *arrows).scale(0.7)

        teacher = self.teacher
        you = self.students[2]

        self.student_thinks(ode)
        you.add_updater(lambda m: m.look_at(func))
        self.teacher_holds_up(func)
        self.wait()

        group = VGroup(arrows[0], d_func, arrows[1], dd_func)
        group.arrange(DOWN)
        group.move_to(func, DOWN)

        arrow = Arrow(
            group.get_corner(UL),
            ode.get_top(),
            path_arc=PI / 2,
        )
        q_marks = VGroup(*[
            MathTex("?").scale(1.5).next_to(
                arrow.point_from_proportion(a),
                UP
            )
            for a in np.linspace(0.2, 0.8, 5)
        ])
        cycle_animation(VFadeInThenOut(
            q_marks,
            lag_ratio=0.2,
            run_time=4,
            rate_func=squish_rate_func(smooth, 0, 0.5)
        ))

        self.play(
            func.animate.next_to(group, UP),
            LaggedStartMap(
                FadeIn, group,
                lambda m: (m, UP)
            ),
            teacher.animate.change("guilty"),
            you.animate.change("sassy"),
        )

        rect = SurroundingRectangle(
            VGroup(group, func)
        )
        dashed_rect = DashedVMobject(rect, num_dashes=75)
        animated_rect = AnimatedBoundary(dashed_rect, cycle_rate=1)

        self.wait()
        self.add(animated_rect, q_marks)
        self.play(
            Create(arrow),
            # FadeIn(q_mark, shift=DOWN),
            self.change_students("confused", "confused")
        )
        self.wait(4)
        self.play_student_changes(
            *3 * ["pondering"],
            self.teacher.animate.change("maybe")
        )
        self.wait(8)
