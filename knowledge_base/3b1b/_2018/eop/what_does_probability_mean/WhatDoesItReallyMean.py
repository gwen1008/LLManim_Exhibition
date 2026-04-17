# Source: 3b1b/_2018/eop/what_does_probability_mean.py
# Description: [3b1b translated] 展示老師與學生討論「機率」真正含義的對話場景，包含學生提問、老師回應的動畫效果。



from manim import *
class WhatDoesItReallyMean(TeacherStudentsScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": MAROON_E,
            "flip_at_start": True,
        },
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            **kwargs
        )

    def construct(self):
        student_q = TexText("What does", "``probability''", "\\emph{actually}", "mean?")
        student_q.set_color_by_tex("probability", YELLOW)
        self.student_says(student_q, target_mode="sassy")
        self.wait()

        question_bubble = VGroup(student_q, self.students[1].bubble)
        scaled_qb = question_bubble.copy()
        scaled_qb.scale(0.4).to_corner(UL)
        self.play(Transform(question_bubble, scaled_qb))
        self.wait()

        self.teacher_says("Don't worry -- philosophy can come later!")
        self.wait()
