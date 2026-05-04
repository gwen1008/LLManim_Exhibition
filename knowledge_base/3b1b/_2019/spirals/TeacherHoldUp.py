# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 老師舉起右手，學生們抬頭思考的場景。



from manim import *
class TeacherHoldUp(TeacherStudentsScene):
    def construct(self):
        self.play_all_student_changes(
            "pondering", look_at=2 * UP,
            added_anims=[
                self.teacher.animate.change("raise_right_hand")
            ]
        )
        self.wait(8)
