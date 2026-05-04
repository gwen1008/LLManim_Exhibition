# Source: 3b1b/_2019/diffyq/part4/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師和學生們的互動場景，學生困惑地提問，老師露出愧疚表情並回應。



from manim import *
class YouSaidThisWasEasier(TeacherStudentsScene):
    def construct(self):
        self.play_all_student_changes(
            "confused", look_at=self.screen,
        )
        self.student_says(
            "I'm sorry, you said\\\\this was easier?",
            target_mode="sassy"
        )
        self.play(self.teacher.animate.change("guilty"))
        self.wait(3)
        self.teacher_says(
            "Bear with\\\\me",
            bubble_config={"height": 3, "width": 3},
        )
        self.look_at(self.screen)
        self.wait(3)
