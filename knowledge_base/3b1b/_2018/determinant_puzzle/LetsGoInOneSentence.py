# Source: 3b1b/_2018/determinant_puzzle.py
# Description: [3b1b translated] 老師對學生說一句話，學生歡呼，然後老師改口說三句話，學生露出不以為然的表情。



from manim import *
class LetsGoInOneSentence(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Here we go, \\\\", "one sentence!"
        )
        self.play_all_student_changes("hooray")
        self.teacher_says(
            "Or three...", "",
            target_mode="guilty"
        )
        self.play_all_student_changes("sassy")
        self.wait(4)
