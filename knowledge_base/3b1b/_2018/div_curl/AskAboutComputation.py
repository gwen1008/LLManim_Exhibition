# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示教師與學生討論如何計算散度和旋度的對話場景，包含學生提問、教師回應及學生思考的動畫過程。



from manim import *
class AskAboutComputation(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Sure, but how do you \\\\" +
            "\\emph{compute} $\\textbf{div}$ and $\\textbf{curl}$?",
            target_mode="sassy",
        )
        self.play_student_changes(
            "confused", "sassy", "angry",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.wait()
        self.teacher_says(
            "Are you familiar \\\\" +
            "with my work \\\\" +
            "at Khan Academy?",
            target_mode="speaking",
            bubble_config={"width": 4, "height": 3}
        )
        self.play_student_changes(
            * 3 * ["pondering"],
            look_at=self.screen
        )
        self.wait(5)
