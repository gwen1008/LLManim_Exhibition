# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示老師與學生在課堂上的互動，學生提問後老師回應，學生們的表情從挑釁轉為內疚再陷入思考。



from manim import *
class ComplainAboutNotKnowingTheStats(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Are people expected\\\\to know that?",
            index=2
        )
        self.play_student_changes(
            "sassy", "sassy",
        )
        self.play(self.teacher.animate.change("hesitant"))
        self.look_at(self.screen)
        self.wait(3)
        self.teacher_says(
            "No, but did you\\\\think to estimate it?",
            bubble_config={"width": 4.5, "height": 3.5},
        )
        self.play_all_student_changes("guilty")
        self.wait(2)
        self.play_all_student_changes("pondering")
        self.wait(3)
