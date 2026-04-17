# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示老師對學生說話，並在第二次說話時讓學生們的表情變為開心的場景。



from manim import *
class MoreToCover(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Much more to say...",
            target_mode="hooray",
            run_time=1,
        )
        self.wait()
        self.teacher_says(
            "SO MUCH!",
            target_mode="surprised",
            added_anims=[self.change_students(*3*["happy"])],
            run_time=0.5
        )
        self.wait(2)
