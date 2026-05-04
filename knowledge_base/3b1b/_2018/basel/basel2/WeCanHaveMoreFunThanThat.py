# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示老師對學生說「我們可以更有趣！」並伴隨學生表情變化和老師手勢的場景。



from manim import *
class WeCanHaveMoreFunThanThat(TeacherStudentsScene):
    def construct(self):
        point = VectorizedPoint(config.frame_width * LEFT / 2 + config.frame_height * UP / 2)
        self.teacher_says(
            "We can have \\\\ more fun than that!",
            target_mode = "hooray"
        )
        self.play_student_changes(*3*["erm"], look_at = point)
        self.wait()
        self.play(
            FadeOut(self.teacher.bubble, shift=UP),
            self.teacher.animate.change("raise_right_hand", look_at=point),
            self.change_students(*3*["pondering"], look_at = point)
        )
        self.wait(3)
