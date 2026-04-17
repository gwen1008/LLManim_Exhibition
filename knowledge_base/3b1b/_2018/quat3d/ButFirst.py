# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 老師對學生說「但首先！」然後所有學生轉為開心，老師移除對話框並舉起右手，學生和老師都看向螢幕。



from manim import *
class ButFirst(TeacherStudentsScene):
    def construct(self):
        for student in self.students:
            student.change("surprised")

        self.teacher_says("But first!")
        self.play_all_student_changes("happy")
        self.play(Uncreate(
            self.teacher.bubble,
            target_mode="raise_right_hand"
        ))
        self.play_student_changes(
            *["pondering"] * 3,
            look_at=self.screen,
        )
        self.play(self.teacher.animate.look_at(self.screen))
        self.wait(4)
