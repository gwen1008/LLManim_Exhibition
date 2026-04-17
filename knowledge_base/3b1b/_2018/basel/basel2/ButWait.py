# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示一個教師與學生互動的場景，學生質疑教師關於無窮級數的承諾，教師回應說這非常接近。



from manim import *
class ButWait(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But wait!",
            target_mode = "angry",
            run_time = 1,
        )
        self.play_student_changes(
            "sassy", "angry", "sassy",
            added_anims = [self.teacher.change, "guilty"],
            run_time = 1
        )
        self.student_says(
            """
            You promised us \\\\
            $1+{1 \\over 4} + {1 \\over 9} + {1 \\over 16} + \\cdots$
            """,
            target_mode = "sassy",
        )
        self.wait(3)
        self.teacher_says("Yes, but that's \\\\ very close.")
        self.play_student_changes(*["plain"]*3)
        self.wait(2)
