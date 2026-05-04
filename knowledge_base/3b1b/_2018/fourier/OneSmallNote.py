# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示老師對學生說「只是一個小註解...」的場景，學生們做出不同反應表情。



from manim import *
class OneSmallNote(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Just one \\\\ small note...",
        )
        self.play_student_changes("erm", "happy", "sassy")
        self.wait(2)
