# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 老師對學生說「你只需要無限智慧」，學生們露出驚恐表情並看向螢幕。



from manim import *
class IKnowThisIsTricky(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "All you need is \\\\ infinite intelligence",
            bubble_config={
                "width": 4,
                "height": 3,
            },
            added_anims=[
                self.change_students(
                    *3 * ["horrified"],
                    look_at=self.screen
                )
            ]
        )
        self.look_at(self.screen)
        self.wait(3)
