# Source: 3b1b/_2019/clacks/solution2/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師與學生互動的場景，學生提問後老師舉手回應，學生們陷入思考。



from manim import *
class AskAboutEqualMassMomentumTransfer(TeacherStudentsScene):
    def construct(self):
        self.student_says("Why?")
        self.play_student_changes("confused", "confused")
        self.wait()
        self.play(
            RemovePiCreatureBubble(self.students[2]),
            self.teacher.animate.change("raise_right_hand")
        )
        self.play_all_student_changes("pondering")
        self.look_at(self.hold_up_spot + 2 * UP)
        self.wait(5)
