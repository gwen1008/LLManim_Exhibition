# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示三名學生在課堂上同時露出驚恐表情，並看向左上方某個位置的場景。



from manim import *
class StudentsHorrifiedAtScene(TeacherStudentsScene):
    def construct(self):
        self.play_student_changes(
            *["horrified", "horrified", "horrified"],
            look_at = 2*UP + 3*LEFT
        )
        self.wait(4)
