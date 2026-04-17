# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 老師對學生說「So be playful!」，學生們表現出思考、歡呼和快樂的反應。



from manim import *
class BePlayful(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "So be playful!",
            target_mode="hooray",
        )
        self.play_student_changes("thinking", "hooray", "happy")
        self.wait(3)
