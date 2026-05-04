# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 老師與學生場景中，兩個學生分別提出關於「確定性」和「波」的問題。



from manim import *
class AskAboutUncertainty(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What does this have \\\\ to do with ``certainty''",
            bubble_config = {"direction" : LEFT},
            student_index = 2
        )
        self.play(self.students[0].animate.change("confused").say(
            "What even are \\\\ these waves?",
            target_mode = "confused"
        ))
        self.wait(2)
