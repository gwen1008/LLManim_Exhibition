# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 老師與學生討論證明方法，老師舉起「複分析」字卡，學生們露出困惑表情。



from manim import *
class TalkAboutProof(TeacherStudentsScene):
    def construct(self):
        teacher = self.teacher
        students = self.students

        # Ask question
        self.student_says(
            "So how'd he\\\\prove it?",
            index=0,
        )
        bubble = students[0].bubble
        students[0].bubble = None
        self.play(
            teacher.animate.change("hesitant"),
            students[1].animate.change("happy"),
            students[2].animate.change("happy"),
        )
        self.wait()
        self.teacher_says(
            "...er...it's a\\\\bit complicated",
            target_mode="guilty",
        )
        self.play_all_student_changes(
            "tired",
            look_at=teacher.bubble,
            lag_ratio=0.1,
        )
        self.play(
            FadeOut(bubble),
            FadeOut(bubble.content),
        )
        self.wait(3)

        # Bring up complex analysis
        ca = Text("Complex Analysis")
        ca.move_to(self.hold_up_spot, DOWN)

        self.play(
            teacher.animate.change("raise_right_hand"),
            FadeIn(ca, shift=DOWN),
            FadeOut(teacher.bubble),
            FadeOut(teacher.bubble.content),
            self.change_students(*["pondering"] * 3),
        )
        self.wait()
        self.play(
            ca.animate.scale(2),
            ca.animate.center(),
            ca.animate.to_edge(UP),
            teacher.animate.change("happy"),
        )
        self.play(ca[1].animate.set_color(GREEN))
        self.wait(2)
        self.play(ca[0].animate.set_color(YELLOW))
        self.wait(2)
        self.play_all_student_changes(
            "confused", look_at=ca,
        )
        self.wait(4)
