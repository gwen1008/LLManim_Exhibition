# Source: 3b1b/_2019/clacks/solution2/pi_creature_scenes.py
# Description: [3b1b translated] 老師對學生們說「現在是精彩的部分！」，並伴隨角色表情變化。



from manim import *
class NowForTheGoodPart(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            r"Now for the \\ good part!",
            target_mode="hooray",
            added_anims=[self.change_students(
                "hooray", "surprised", "happy"
            )],
        )
        self.wait(2)
