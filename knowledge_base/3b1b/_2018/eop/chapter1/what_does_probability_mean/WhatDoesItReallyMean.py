# Source: 3b1b/_2018/eop/chapter1/what_does_probability_mean.py
# Description: [3b1b translated] 展示老師與學生討論「機率」真正含義的對話場景，包含對話泡泡和角色表情變化。



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
        student_q = Text(
            "What does \"probability\"\nactually mean?",
            color=WHITE
        )
        # 手動設定部分文字顏色
        student_q_parts = student_q.text.split("\"probability\"")
        if len(student_q_parts) == 2:
            student_q = VGroup(
                Text(student_q_parts[0], color=WHITE),
                Text("\"probability\"", color=YELLOW),
                Text(student_q_parts[1], color=WHITE)
            ).arrange(RIGHT, buff=0.05)
        
        self.student_says(student_q, target_mode="sassy")
        self.wait()
        self.play(
            self.students[1].animate.change("confused")
        )
        self.wait(2)
        
        student_bubble = self.students[1].bubble
        self.students[1].bubble = None
        student_bubble.add(student_bubble.content)
        self.play(
            student_bubble.animate.scale(0.5).to_corner(UL),
        )
        
        self.teacher_says(
            "Don't worry -- philosophy\ncan come later!",
            added_anims=[self.change_students(*3 * ["happy"])],
        )
        self.wait(2)
        
        # 移除老師的對話泡泡
        self.play(FadeOut(self.teacher.bubble), FadeOut(self.teacher.bubble.content))
        self.teacher.bubble = None
        
        self.play(*[
            pi.animate.look_at(ORIGIN) for pi in self.get_pi_creatures()
        ])
        
        # 所有學生變為思考表情
        for student in self.students:
            student.change("pondering")
        self.play_all_student_changes("pondering", look_at=UP)
        self.wait(3)
        
        self.play_student_changes("confused", look_at=UP)
        self.wait(3)
