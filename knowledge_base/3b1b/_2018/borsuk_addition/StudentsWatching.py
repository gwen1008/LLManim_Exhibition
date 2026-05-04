# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示老師舉起右手，學生們看向螢幕思考的場景。



from manim import *
class StudentsWatching(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.animate.change("raise_right_hand"),
            *[
                student.animate.change("thinking", self.screen)
                for student in self.students
            ],
            VFadeIn(self.pi_creatures, run_time=2)
        )
        self.wait(5)
