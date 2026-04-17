# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示老師與學生互動的場景，學生提出疑問，老師以微笑回應。



from manim import *
class HowDoesThisSolveProblems(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Is this...useful?",
            target_mode="confused"
        )
        self.play_student_changes("maybe", "confused", "sassy")
        self.play(self.teacher.animate.change("happy"))
        self.wait(3)
