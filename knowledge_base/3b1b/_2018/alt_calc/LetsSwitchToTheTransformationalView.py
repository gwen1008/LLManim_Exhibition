# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 老師對學生說「丟掉圖形！」，學生們呈現不同的反應表情。



from manim import *
class LetsSwitchToTheTransformationalView(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Lose the \\\\ graphs!",
            target_mode="hooray"
        )
        self.play_student_changes("hooray", "erm", "surprised")
        self.wait(5)
