# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示老師詢問學生是否在暫停思考，學生從內疚轉為思考的動畫場景。



from manim import *
class AreYouPausingAndPondering(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Are you pausing \\\\ and pondering?",
            target_mode="sassy",
            added_anims=[self.change_students(*3 * ["guilty"])]
        )
        self.wait()
        self.play_all_student_changes(
            "thinking",
            added_anims=[
                RemovePiCreatureBubble(self.teacher, target_mode="raise_right_hand")
            ],
            look_at=self.screen
        )
        self.wait(6)
