# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 教師與學生討論如何「求解」微分方程，包含對話泡泡和角色表情變化。



from manim import *
class AskAboutActuallySolving(TeacherStudentsScene):
    def construct(self):
        ode = get_ode()
        ode.to_corner(UL)
        self.add(ode)
        morty = self.teacher

        self.student_says(
            "Yeah yeah, but how do\\\\"
            "you actually \\emph{solve} it?",
            index=1,
            target_mode="sassy",
            added_anims=[morty.animate.change("thinking")],
        )
        self.play_student_changes(
            "confused", "sassy", "confused",
            look_at=ode,
        )
        self.wait()
        self.teacher_says(
            "What do you mean\\\\ by ``solve''?",
            target_mode="speaking",
            added_anims=[self.change_students(
                *3 * ["erm"]
            )]
        )
        self.play(self.students[1].animate.change("angry"))
        self.wait(3)
