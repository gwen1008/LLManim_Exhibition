# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示教室場景中學生抱怨空間擁擠，老師回應並引導學生思考的對話過程。



from manim import *
class FeelsALittleCramped(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Kind of cramped,\\\\ isn't it?",
            target_mode="sassy"
        )
        self.wait()
        self.teacher_says(
            "Sure, but think \\\\ locally"
        )
        self.play_all_student_changes("pondering", look_at=self.screen)
        self.wait(3)
