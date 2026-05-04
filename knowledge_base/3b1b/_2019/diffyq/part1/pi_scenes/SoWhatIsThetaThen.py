# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 展示教師與學生對話的場景，教師在黑板上寫有微分方程，學生提問後教師回應並改變學生表情。



from manim import *
class SoWhatIsThetaThen(TeacherStudentsScene):
    def construct(self):
        ode = get_ode()  # 假設 get_ode() 返回一個 Mobject
        ode.to_corner(UL)
        self.add(ode)

        self.student_says(
            "Okay, but then\\\\"
            "what \\emph{is} $\\theta(t)$?"
        )
        self.wait()
        self.play(self.teacher.animate.change("happy"))
        self.wait(2)
        self.teacher_says(
            "First, you must appreciate\\\\"
            "a deep truth...",
            added_anims=[self.change_students(
                *3 * ["confused"]
            )]
        )
        self.wait(4)
