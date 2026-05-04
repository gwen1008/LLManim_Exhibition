# Source: 3b1b/_2019/clacks/solution2/pi_creature_scenes.py
# Description: [3b1b translated] 展示教師與學生場景中，學生提出問題後，教師舉手引導學生思考的互動過程。



from manim import *
class ReplaceOneTrickySceneWithAnother(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "This replaces one tricky\\\\problem with another",
            index=1,
            target_mode="sassy",
            added_anims=[self.teacher.animate.change("happy")],
        )
        self.play_student_changes("erm", "sassy", "angry")
        self.wait(4)
        self.play(
            FadeOut(self.students[1].bubble),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(*3 * ["pondering"])
        )
        self.look_at(self.hold_up_spot + 2 * UP)
        self.wait(5)
