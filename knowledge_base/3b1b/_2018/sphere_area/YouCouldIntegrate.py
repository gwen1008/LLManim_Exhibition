# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示老師與學生對話的場景，學生提問「積分？」，老師回應「我們會更接近阿基米德的方法」，學生們露出困惑表情。



from manim import *
class YouCouldIntegrate(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Integrate?",
            student_index=2,
            bubble_config={"direction": LEFT},
        )
        self.play(self.teacher.animate.change("hesitant"))
        self.wait()
        self.teacher_says(
            "We'll be a bit \\\\ more Archimedean",
            target_mode="speaking"
        )
        self.play_all_student_changes("confused")
        self.wait()
