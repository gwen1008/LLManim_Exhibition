# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示老師和學生在課堂上互動的場景，其中一位學生說「Cool!」並帶動全班氣氛。



from manim import *
class ThatsKindOfInteresting(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Cool!", target_mode="hooray",
            student_index=2,
            added_anims=[self.teacher.animate.change("happy")]
        )
        self.play(
            self.students[0].animate.change("happy"),
            self.students[1].animate.change("happy"),
            self.students[2].animate.change("happy")
        )
        self.wait(2)
