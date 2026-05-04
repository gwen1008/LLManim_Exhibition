# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 教師在課堂上展示兩種視覺化類型（普通視覺與轉換視覺）的動畫場景。



from manim import *
class SetTheStage(TeacherStudentsScene):
    def construct(self):
        ordinary = Text("Ordinary visual")
        transformational = Text("Transformational visual")
        for word in ordinary, transformational:
            word.move_to(self.hold_up_spot, DOWN)
            word.shift_onto_screen()

        self.screen.scale(1.25, about_edge=UL)
        self.add(self.screen)
        self.teacher_holds_up(
            ordinary,
            added_anims=[self.change_students(*3 * ["sassy"])]
        )
        self.wait()
        self.play(
            ordinary.animate.shift(UP),
            FadeIn(transformational, shift=DOWN),
            self.teacher.animate.change("hooray"),
            self.change_students(*3 * ["erm"])
        )
        self.wait(3)
        self.play_all_student_changes("pondering", look_at=self.screen)
