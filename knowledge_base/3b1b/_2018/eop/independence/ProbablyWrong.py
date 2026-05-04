# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 老師對學生說「可能錯了！」，三名學生同時表現出生氣的反應。



from manim import *
class ProbablyWrong(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Probably wrong!",
            run_time=1,
        )
        self.play_student_changes(
            *["angry"]*3,
            run_time=1
        )
        self.wait()
