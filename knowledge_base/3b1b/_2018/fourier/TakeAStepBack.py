# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 老師與學生場景中，學生提出疑問，老師露出微笑。



from manim import *
class TakeAStepBack(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Hang on, go over \\\\ that again?",
            target_mode = "confused"
        )
        self.play_student_changes(*["confused"]*3)
        self.play(self.teacher.animate.change("happy"))
        self.wait(3)
