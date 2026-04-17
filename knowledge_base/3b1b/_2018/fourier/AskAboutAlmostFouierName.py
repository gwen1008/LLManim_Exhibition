# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 老師與學生對話場景，學生提問「幾乎傅立葉變換？」，老師回答幾分鐘後會講到真正的傅立葉變換。



from manim import *
class AskAboutAlmostFouierName(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "``Almost'' Fourier transform?",
            target_mode = "sassy"
        )
        self.play_student_changes("confused", "sassy", "confused")
        self.wait()
        self.teacher_says(
            "We'll get to the real \\\\ one in a few minutes",
            added_anims = [self.change_students(*["plain"]*3)]
        )
        self.wait(2)
