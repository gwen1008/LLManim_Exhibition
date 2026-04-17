# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 老師對學生說「這些只是技術細節」，學生們開心地反應，老師移除對話框並舉起右手，然後看向螢幕。



from manim import *
class JustTechnicalities(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "These are just \\\\ technicalities"
        )
        self.play_all_student_changes("happy")
        # 移除老師的對話框並改變老師的姿勢
        self.play(
            FadeOut(self.teacher.bubble),
            self.teacher.animate.change("raise_right_hand")
        )
        self.look_at(self.screen)
        self.wait(4)
