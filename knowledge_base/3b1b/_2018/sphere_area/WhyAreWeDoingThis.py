# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示老師與學生互動的場景，學生提出疑問，老師回應並引導學生思考。



from manim import *
class WhyAreWeDoingThis(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Hang on, what \\\\ are we doing?",
            index=2,
            bubble_config={"direction": LEFT},
            target_mode="hesitant"
        )
        self.play_student_changes(
            "maybe", "pondering", "hesitant",
            added_anims=[self.teacher.change, "tease"]
        )
        self.wait(3)
        self.play(
            RemovePiCreatureBubble(self.students[2]),
            self.teacher.change, "raise_right_hand",
            self.play_student_changes(*2 * ["pondering"])
        )
        self.look_at(self.screen)
        self.wait(2)
