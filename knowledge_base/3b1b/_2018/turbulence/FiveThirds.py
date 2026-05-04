# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示老師向學生講解湍流基本常數5/3，並將數字放大展示的教學場景。



from manim import *
class FiveThirds(TeacherStudentsScene):
    def construct(self):
        words = MathTex(
            "5/3", "\\text{is a sort of fundamental}\\\\ \\text{constant of turbulence}"
        )
        self.teacher_says(words)
        self.play_student_changes("pondering", "maybe", "erm")
        self.play(
            FadeOut(self.teacher.bubble),
            FadeOut(words[1]),
            self.teacher.change, "raise_right_hand",
            words[0].animate.scale(1.5),
            words[0].animate.move_to(self.hold_up_spot)
        )
        self.play_student_changes("thinking", "pondering", "hooray")
        self.wait(3)
