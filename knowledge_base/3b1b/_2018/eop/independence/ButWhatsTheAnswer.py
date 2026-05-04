# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示老師與學生場景中，學生提問後老師陷入思考的互動過程。



from manim import *
class ButWhatsTheAnswer(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But what's the \\\\ actual answer?",
            target_mode = "confused"
        )
        self.play_student_changes(*["confused"]*3)
        self.wait()
        self.play(self.teacher.animate.change("pondering"))
        self.wait(3)
