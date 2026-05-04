# Source: 3b1b/_2019/diffyq/part3/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師對學生說「如果只是！」的場景，老師表情生氣，學生們困惑地看向螢幕。



from manim import *
class IfOnly(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "If only!",
            target_mode="angry"
        )
        self.play_all_student_changes(
            "confused",
            look_at=self.screen
        )
        self.wait(3)
