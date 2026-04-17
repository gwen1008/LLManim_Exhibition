# Source: 3b1b/_2019/clacks/solution2/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師與學生之間的互動場景，學生質疑類比的相關性，老師做出回應並引導學生思考。



from manim import *
class ComplainAboutRelevanceOfAnalogy(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Why would \\\\ you care",
            target_mode="maybe"
        )
        self.play_student_changes(
            "angry", "sassy", "maybe",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.wait(2)
        self.play(
            self.teacher.change, "raise_right_hand",
            self.change_students(
                "pondering", "erm", "pondering",
                look_at=self.hold_up_spot,
            ),
            FadeOut(self.students[2].bubble, shift=DOWN, scale=0.5)
        )
        self.play(
            self.students[2].change, "thinking",
            self.hold_up_spot + UP,
        )
        self.wait(3)
