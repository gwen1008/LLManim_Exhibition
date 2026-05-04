# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 老師向學生們解釋「散度」和「旋度」在某些非空間問題中也有用處，學生們呈現不同的反應表情。



from manim import *
class RelevantInNonSpatialCircumstances(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            """
                $\\textbf{div}$ and $\\textbf{curl}$ are \\\\
                even useful in some \\\\
                non-spatial problems
            """,
            target_mode="hooray"
        )
        self.play_student_changes(
            "sassy", "confused", "hesitant"
        )
        self.wait(3)
