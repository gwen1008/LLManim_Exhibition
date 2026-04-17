# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 老師對學生說「情況變得更糟了」，學生們表現出猶豫、懇求和困惑的反應。



from manim import *
class ItGetsWorse(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("It gets\\\\worse")
        self.play_student_changes(
            "hesitant", "pleading", "erm"
        )
        self.wait(5)
