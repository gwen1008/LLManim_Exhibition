# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示教師與學生場景中，一條蜿蜒的虛線路徑從螢幕外繪製到螢幕上，隨後螢幕縮小並移動到角落，伴隨著文字和箭頭的動畫。



from manim import *
class ShowWritingTrajectory(TeacherStudentsScene):
    def construct(self):
        self.add_screen()
        self.show_meandering_path()
        self.show_previous_video()

    def add_screen(self):
        self.screen.scale(1.4, about_edge=UL)
        self.add(self.screen)

    def show_meandering_path(self):
        solid_path = VMobject().set_points_as_corners([
            3 * UP + 2 * RIGHT,
            2 * UP + 4 * RIGHT,
            3.5 * UP + 3.5 * RIGHT,
            2 * UP + 3 * RIGHT,
            3 * UP + 7 * RIGHT,
            3 * UP + 5 * RIGHT,
            UP + 6 * RIGHT,
            2 * RIGHT,
            2 * UP + 2 * RIGHT,
            self.screen.get_right()
        ])
        step = 1.0 / 80
        dashed_path = VGroup(*[
            VMobject().pointwise_become_partial(
                solid_path, x, x + step / 2
            )
            for x in np.arange(0, 1 + step, step)
        ])
        arrow = Arrow(
            solid_path.get_points()[-2],
            solid_path.get_points()[-1],
            buff=0
        )
        dashed_path.add(arrow.tip)
        dashed_path.set_color_by_gradient(BLUE, YELLOW)

        self.play(
            Create(
                dashed_path,
                rate_func=bezier([0, 0, 1, 1]),
                run_time=5,
            ),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(*["sassy"] * 3)
        )
        self.play(
            LaggedStartMap(
                ApplyMethod, dashed_path,
                lambda m: (m.scale, 0),
                remover=True
            ),
            self.teacher.animate.change("tease"),
            self.change_students(
                *["pondering"] * 3,
                look_at=self.screen
            )
        )

    def show_previous_video(self):
        screen = self.screen

        arrow = Arrow(start=RIGHT, end=LEFT, color=WHITE)
        arrow.next_to(screen, RIGHT)
        prev_words = Text("Previous video")
        prev_words.next_to(arrow, RIGHT)

        screen.generate_target()
        screen.target.set_height(3.75)
        screen.target.to_corner(UR)
        complex_words = Text("Complex derivatives")
        complex_words.next_to(
            screen.target, LEFT,
            buff=2 * SMALL_BUFF + arrow.get_length()
        )

        self.play(
            GrowArrow(arrow),
            Write(prev_words)
        )
        self.wait(3)
        self.play(
            arrow.animate.flip().next_to(screen.target, LEFT, SMALL_BUFF),
            MoveToTarget(screen),
            FadeOut(prev_words),
            Write(complex_words),
            self.teacher.animate.change("raise_right_hand").rotate(30 * DEGREES)
        )
        self.play_student_changes("erm", "sassy", "confused")
        self.look_at(screen)
        self.wait(2)
        self.play_student_changes("pondering", "confused", "sassy")
        self.wait(2)

        bubble = self.teacher.get_bubble(
            bubble_type=SpeechBubble,
            height=3, width=5
        )
        complex_words.generate_target()
        complex_words.target.move_to(bubble.get_bubble_center())
        # self.play(
        #     FadeOut(screen),
        #     FadeOut(arrow),
        #     Create(bubble),
        #     self.teacher.animate.change("hooray"),
        #     MoveToTarget(complex_words),
        # )

        s0 = self.students[0]
        s0.target_center = s0.get_center()

        def update_s0(s0, dt):
            s0.target_center += dt * LEFT * 0.5
            s0.move_to(s0.target_center)

        self.add(s0.add_updater(update_s0))
        self.play_student_changes("tired", "horrified", "sad")
        self.play(s0.animate.look(LEFT))
        self.wait(4)
