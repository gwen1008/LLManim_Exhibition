# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個教師與學生場景，其中一名學生舉手提出「但為什麼？」的問題，教師表現出內疚的表情。



from manim import *
class ButWhy(TeacherStudentsScene):
    def __init__(
        self,
        student_mode="raise_right_hand",
        question="But why?",
        teacher_mode="guilty",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.student_mode = student_mode
        self.question = question
        self.teacher_mode = teacher_mode

    def construct(self):
        for student in self.students:
            student.change("pondering", self.screen)
        self.student_says(
            "But why?",
            index=2,
            target_mode=self.student_mode,
            bubble_config={"direction": LEFT},
        )
        self.play(
            self.teacher.animate.change(self.teacher_mode, self.students[2])
        )
        self.wait(5)
