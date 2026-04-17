# Source: 3b1b/_2019/diffyq/part3/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師與學生場景中，一位學生質疑正弦曲線不現實，老師隨後引導所有學生思考的互動過程。



from manim import *
class SineCurveIsUnrealistic(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But that would\\\\never happen!",
            index=1,
            bubble_config={
                "direction": RIGHT,
                "height": 3,
                "width": 4,
            },
            target_mode="angry"
        )
        self.play_student_changes(
            "guilty", "angry", "hesitant",
            added_anims=[
                self.teacher.change, "tease"
            ]
        )
        self.wait(3)
        self.play(
            FadeOut(self.students[1].bubble),
            self.teacher.change, "raise_right_hand"
        )
        self.play_all_student_changes(
            "pondering",
            look_at=3 * UP,
        )
        self.wait(5)
