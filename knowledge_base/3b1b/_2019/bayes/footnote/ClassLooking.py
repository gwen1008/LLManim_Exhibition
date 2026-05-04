# Source: 3b1b/_2019/bayes/footnote.py
# Description: [3b1b translated] 展示老師和學生在課堂上互動的場景，包含表情變化和視線移動。



from manim import *
class ClassLooking(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.animate.change("pondering"),
            self.change_students(
                "pondering", "confused", "sassy",
                look_at=self.screen,
            ),
        )
        self.wait(5)
        self.play(
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play(
            self.change_students(
                "thinking", "pondering", "pondering",
                look_at=self.hold_up_spot + 2 * UP,
            )
        )
        self.wait(3)
