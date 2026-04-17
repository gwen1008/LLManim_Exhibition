# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示老師和學生們的對話場景，學生請求毛絨玩具，老師困惑回應。



from manim import *
class PlushMe(TeacherStudentsScene):
    def construct(self):
        self.student_says("Plushie me?")
        self.play_student_changes("happy", None, "happy")
        self.play(self.teacher.animate.change("confused"))
        self.wait()
        self.teacher_says("...why?", target_mode="maybe")
        self.wait(2)
