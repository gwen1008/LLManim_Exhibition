# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示老師與學生對話場景，學生表示更喜歡圖形方法，老師鼓勵他們鍛煉概念思維。



from manim import *
class NotBetterThanGraphs(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Um, yeah, I'll stick \\\\ with graphs thanks",
            target_mode="sassy",
        )
        self.play(
            self.teacher.animate.change("guilty"),
            self.change_students("sad", "sassy", "hesitant")
        )
        self.wait(2)
        self.play(
            FadeOut(self.students[1].bubble),
            self.teacher.animate.change("raise_right_hand")
        )
        self.play_all_student_changes(
            "confused", look_at=self.screen
        )
        self.wait(3)
        self.teacher_says(
            "You must flex those \\\\ conceptual muscles",
            added_anims=[self.change_students(
                *3 * ["thinking"],
                look_at=self.teacher.eyes
            )]
        )
        self.wait(3)
