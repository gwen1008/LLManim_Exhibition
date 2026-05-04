# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示老師對學生說「如果你需要熱身」的場景，老師說話時學生們思考地看向螢幕。



from manim import *
class IfYouNeedAWarmUp(TeacherStudentsScene):
    def construct(self):
        screen = self.screen
        screen.set_height(4)
        screen.to_corner(UL)
        self.add(screen)

        self.teacher_says(
            "If you need \\\\ a warm up",
            bubble_config={"width": 3.5, "height": 3},
        )
        self.play_all_student_changes(
            "pondering", look_at=screen,
        )
        self.wait(3)
        self.play(self.teacher.bubble.animate.fade(1), self.teacher.animate.change("plain"))
        self.wait(3)
