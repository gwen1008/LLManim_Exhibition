# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示老師告訴學生逆畢氏定理適用時，學生們歡呼的場景。



from manim import *
class YayIPTApplies(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Heyo!  The Inverse \\\\ Pythagorean Theorem \\\\ applies!",
            bubble_config = {"width" : 5},
            target_mode = "surprised"
        )
        self.play_student_changes(*3*["hooray"])
        self.wait(2)
