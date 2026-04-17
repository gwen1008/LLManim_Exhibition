# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示老師與學生場景中，一位學生提問關於改變信號長度的影響，老師和學生們做出相應反應的過程。



from manim import *
class AskAboutLongVsShort(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What happens if we \\\\ change the length of \\\\ the signal?",
            index = 2,
        )
        self.play(
            self.teacher.animate.change("happy"),
            self.change_students("pondering", "confused", "raise_right_hand")
        )
        self.wait(5)
