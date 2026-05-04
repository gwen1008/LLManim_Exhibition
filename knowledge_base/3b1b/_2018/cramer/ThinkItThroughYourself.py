# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 老師鼓勵學生思考，學生們轉為沉思的表情。



from manim import *
class ThinkItThroughYourself(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Try thinking \\\\ it through!",
            target_mode="hooray"
        )
        self.play_all_student_changes("pondering")
        self.wait(4)
