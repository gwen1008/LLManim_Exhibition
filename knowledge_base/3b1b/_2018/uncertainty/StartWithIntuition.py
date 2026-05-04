# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 老師對學生說「你已經有這個直覺」，學生們表現出思考、困惑和猶豫的反應。



from manim import *
class StartWithIntuition(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "You already \\\\ have this \\\\ intuition",
            bubble_config = {
                "height" : 3.5,
                "width" : 3,
            },
        )
        self.play_student_changes("pondering", "erm", "maybe")
        self.look_at(4*LEFT + 2*UP)
        self.wait(5)
