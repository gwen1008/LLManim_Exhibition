# Source: 3b1b/_2018/for_flammy.py
# Description: [3b1b translated] 展示老師與學生場景中，學生提問並引發師生表情變化的互動過程。



from manim import *
class ShamelessPlug(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But why $4\\pi R^2$?",
            target_mode="maybe"
        )
        self.play_student_changes(
            "erm", "maybe", "happy",
            added_anims=[self.teacher.change, "happy"]
        )
        self.wait(3)
