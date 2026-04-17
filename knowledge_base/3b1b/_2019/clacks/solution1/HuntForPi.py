# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示老師與學生場景中，學生說出「Hunt for π!」並與老師一起歡呼的動畫。



from manim import *
class HuntForPi(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Hunt for $\\pi$!",
            bubble_config={"direction": LEFT},
            target_mode="hooray"
        )
        self.play_all_student_changes(
            "hooray",
            added_anims=[self.teacher.animate.change("happy")]
        )
        self.wait()
