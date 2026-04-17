# Source: 3b1b/_2019/diffyq/part4/pi_creature_scenes.py
# Description: [3b1b translated] 展示教師與學生討論的場景，學生先提出可以用波函數求和解決問題，隨後強調其他方法不行。



from manim import *
class SolveForWavesNothingElse(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Sure, we can\\\\solve it for\\\\sums of waves...",
            target_mode="sassy",
            index=2,
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_student_changes("pondering", "pondering", "sassy")
        self.look_at(self.screen)
        self.wait(4)
        self.student_says(
            "But nothing else!",
            target_mode="angry",
        )
        self.play_student_changes(
            "concerned_musician",
            "concerned_musician",
            "angry",
        )
        self.wait(5)
