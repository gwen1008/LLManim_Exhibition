# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示老師和三名學生在課堂上的情緒變化動畫，從憤怒和懇求轉為疲憊。



from manim import *
class NobodyLikesHomework(TeacherStudentsScene):
    def construct(self):
        self.play_student_changes(
            "angry", "pleading", "angry",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.wait()
        self.play_all_student_changes(
            "tired", look_at=8 * RIGHT + 4 * DOWN,
            added_anims=[self.teacher.change, "tease"]
        )
        self.wait(2)
