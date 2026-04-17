# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示老師與學生互動的場景，學生提問後老師舉手回應，學生表情變化。



from manim import *
class WhyLearnIt(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What?!?  Then why \\\\ learn it?",
            bubble_direction=LEFT,
            student_index=2,
            target_mode="angry",
        )
        self.play_all_student_changes("angry")
        self.wait()
        self.play(
            self.teacher.animate.change("raise_right_hand"),
            self.change_students("erm", "happy", "pondering"),
            FadeOut(self.students[2].bubble, shift=DOWN),
            self.students[2].animate.change("pondering"),
        )
        self.look_at(self.screen)
        self.wait(10)
