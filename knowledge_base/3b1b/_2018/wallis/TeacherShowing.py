# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 老師在課堂上展示螢幕內容，學生們專注觀看並思考。



from manim import *
class TeacherShowing(TeacherStudentsScene):
    def construct(self):
        screen = self.screen
        screen.set_height(4)
        screen.next_to(self.students, UP, MED_LARGE_BUFF, RIGHT)
        self.play(
            Create(screen),
            self.teacher.animate.change("raise_right_hand", screen),
            self.change_students(
                *["pondering"] * 3,
                look_at=screen
            )
        )
        self.wait(5)
