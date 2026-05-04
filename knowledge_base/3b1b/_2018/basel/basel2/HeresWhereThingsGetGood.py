# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 老師對學生說「現在是精彩的部分！」，學生們表現出歡呼和高興的反應。



from manim import *
class HeresWhereThingsGetGood(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("Now for the \\\\ good part!")
        self.play_student_changes(*["hooray"]*3)
        self.play_student_changes(*["happy"]*3)
        self.wait()
