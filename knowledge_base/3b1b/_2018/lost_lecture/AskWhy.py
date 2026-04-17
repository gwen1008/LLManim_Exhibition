# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 老師和學生場景中，一位學生提出疑問，老師和學生們做出相應的表情和動作反應。



from manim import *
class AskWhy(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Um...why?",
            target_mode="confused",
            student_index=2,
            bubble_direction=LEFT,
        )
        self.play(
            self.teacher.animate.change("happy"),
            self.change_students("raise_left_hand", "sassy", "confused")
        )
        self.wait(5)
