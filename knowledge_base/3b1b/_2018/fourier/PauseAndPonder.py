# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 老師對學生說「暫停並思考！」，學生們轉為思考狀態。



from manim import *
class PauseAndPonder(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Pause and \\\\ ponder!",
            target_mode = "hooray"
        )
        self.play_student_changes(*["thinking"]*3)
        self.wait(4)
