# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 老師告訴學生「你的直覺知道貝氏定理」，學生們表現出困惑、感激和內疚的反應。



from manim import *
class YourGutKnowsBayesRule(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Your gut knows \\\\ Bayes' rule.",
            run_time = 1
        )
        self.play_student_changes("confused", "gracious", "guilty")
        self.wait(3)
