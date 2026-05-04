# Source: 3b1b/_2019/diffyq/part4/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師與學生課堂互動的場景，學生提出質疑後老師引導大家思考。



from manim import *
class WhyWouldYouCare(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Who cares!",
            target_mode="sassy",
            student_index=2,
            added_anims=[self.teacher.animate.change("guilty")]
        )
        self.wait()
        self.play(
            FadeOut(self.students[2].bubble),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(
                "pondering", "erm", "thinking",
                look_at=self.screen
            )
        )
        self.look_at(self.screen)
        self.wait(5)
