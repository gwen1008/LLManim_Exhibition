# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示老師與學生場景中，一位學生舉手詢問關於θ的問題，其他學生和老師做出相應反應。



from manim import *
class AskAboutTheta(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But what is $\\theta$?",
            target_mode="raise_left_hand",
        )
        self.play_student_changes(
            "confused", "sassy", "raise_left_hand",
            added_anims=[self.teacher.animate.change("happy")]
        )
        self.wait(3)
