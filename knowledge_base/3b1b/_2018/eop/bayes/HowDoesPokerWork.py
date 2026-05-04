# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示老師與學生場景中，一位學生提出關於撲克牌規則的困惑問題，其他學生也表現出困惑表情。



from manim import *
class HowDoesPokerWork(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Wait, how does \\\\ poker work again?",
            target_mode = "confused",
            run_time = 1
        )
        self.play(self.students[0].animate.change("confused"),
                  self.students[1].animate.change("confused"),
                  self.students[2].animate.change("confused"))
        self.wait(2)
