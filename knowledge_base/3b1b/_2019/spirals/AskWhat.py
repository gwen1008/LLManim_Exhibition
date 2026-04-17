# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個教師與學生場景，其中一名學生困惑地提問，教師和其他學生表現出相應的反應。



from manim import *
class AskWhat(TeacherStudentsScene):
    def construct(self):
        screen = self.screen
        self.student_says(
            "I'm sorry,\\\\what?!?",
            target_mode="angry",
            look_at=screen,
            index=2,
            added_anims=[
                self.teacher.animate.change("happy", screen),
                self.students[0].animate.change("confused", screen),
                self.students[1].animate.change("confused", screen),
            ]
        )
        self.wait(3)
