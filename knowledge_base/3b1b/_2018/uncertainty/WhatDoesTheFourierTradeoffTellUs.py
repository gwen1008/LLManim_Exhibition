# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 老師向學生提問傅立葉權衡告訴我們什麼，學生們陷入思考。



from manim import *
class WhatDoesTheFourierTradeoffTellUs(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "So! What does \\\\ the Fourier trade-off \\\\ tell us?",
            target_mode = "surprised",
            bubble_config = {"width" : 4, "height" : 3}
        )
        self.play_student_changes(*["thinking"]*3)
        self.wait(4)
