# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示老師與學生場景中，學生提問後老師表情變化的過程。



from manim import *
class WalkThroughOneMoreStep(TeacherStudentsScene):
    def construct(self):
        self.student_says("""
            Wait...can you walk \\\\
            through one more step?
        """)
        self.play(self.teacher.animate.change("happy"))
        self.wait(4)
