# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示教師向學生逐步講解演算法步驟的教學場景，每個步驟以文字形式淡入並伴隨師生互動動畫。



from manim import *
class StepsOfTheAlgorithm(TeacherStudentsScene):
    def construct(self):
        steps = self.get_steps()
        steps.arrange(
            DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        steps.to_corner(UL)
        steps.scale(0.8)

        for step in steps:
            self.play(
                FadeIn(step[0], shift=DOWN),
                self.teacher.animate.change("raise_right_hand")
            )
            self.play(
                Write(step[1], run_time=2),
                self.change_students(
                    *["pondering"] * 3,
                    look_at=step,
                )
            )
            self.wait()
        self.play_student_changes(
            "sassy", "erm", "confused",
            look_at=steps,
            added_anims=[self.teacher.animate.change("happy")]
        )
        self.wait(3)

    def get_steps(self):
        return VGroup(
            Text("Step 1:", "Implement a physics engine"),
            MathTex(
                "Step 2:",
                r"Choose the number of digits, $d$,\\",
                r"of $\pi$ that you want to compute"
            ),
            MathTex(
                "Step 3:",
                r"Set one mass to $100^{d - 1}$,\\",
                r"the other to $1$"
            ),
            Text("Step 4:", "Count collisions"),
        )
