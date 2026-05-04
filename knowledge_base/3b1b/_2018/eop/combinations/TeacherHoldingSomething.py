# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 老師舉起右手，學生們抬頭思考的場景。



from manim import *
class TeacherHoldingSomething(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = 2*UP+2*RIGHT
        )
        self.wait(6)
