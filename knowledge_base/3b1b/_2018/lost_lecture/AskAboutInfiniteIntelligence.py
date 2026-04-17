# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示老師與學生對話的場景，學生對「無限智慧」感到困惑，老師則給予鼓勵並引導他們看向螢幕。



from manim import *
class AskAboutInfiniteIntelligence(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Infinite intelligence?",
            target_mode="confused"
        )
        self.play(
            self.change_students("horrified", "confused", "sad"),
            self.teacher.animate.change("happy"),
        )
        self.wait()
        self.teacher_says(
            "Stay focused, \\\\ go full screen, \\\\ and you'll be fine.",
            added_anims=[self.change_students(*["happy"] * 3)]
        )
        self.wait()
        self.look_at(self.screen)
        self.wait(5)
