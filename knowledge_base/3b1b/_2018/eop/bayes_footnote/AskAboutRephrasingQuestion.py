# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 老師向學生提問，詢問如果重新表述問題會怎樣。



from manim import *
class AskAboutRephrasingQuestion(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "What if we rephrased \\\\ the question?",
            run_time = 1
        )
        self.wait(3)
