# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 老師舉起右手，學生們呈現思考的姿態，並看向原點。



from manim import *
class TeacherHoldingUp(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.animate.change("raise_right_hand")
        )
        self.play_all_student_changes("pondering")
        self.look_at(ORIGIN)
        self.wait(5)
