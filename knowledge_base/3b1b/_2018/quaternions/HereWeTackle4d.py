# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示教師與學生場景中，標題動畫與角色表情變化，說明四元數在4D與3D中的應用主題切換。



from manim import *
class HereWeTackle4d(TeacherStudentsScene):
    def construct(self):
        titles = VGroup(
            TexText(
                "This video:\\\\",
                "Quaternions in 4d"
            ),
            TexText(
                "Next video:\\\\",
                "Quaternions acting on 3d"
            )
        )
        for title in titles:
            title.move_to(self.hold_up_spot, DOWN)
        titles[0].set_color(YELLOW)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(titles[0], shift=DOWN),
            self.change_students("confused", "horrified", "sad")
        )
        self.look_at(self.screen)
        self.wait()
        self.play_student_changes(
            "erm", "thinking", "pondering",
            look_at=self.screen
        )
        self.wait(3)
        self.play_student_changes(
            "pondering", "confused", "happy"
        )
        self.look_at(self.screen)
        self.wait(3)
        self.play(
            self.teacher.animate.change("hooray"),
            FadeIn(titles[1]),
            titles[0].animate.shift(2 * UP).set_rate_func(
                lambda t: squish_rate_func(smooth, 0.2, 1)(t)
            )
        )
        self.play_all_student_changes("hooray")
        self.play(self.teacher.animate.change("happy"))
        self.look_at(self.screen)
        self.wait(3)
        self.play_student_changes("pondering", "happy", "thinking")
        self.wait(4)
