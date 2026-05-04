# Source: 3b1b/_2019/diffyq/part3/pi_creature_scenes.py
# Description: [3b1b translated] 展示一位學生說「我聽說過這個！」然後另一位學生說「但誰在乎？」的課堂場景，包含老師和學生的表情變化與對話泡泡動畫。



from manim import *
class IveHeardOfThis(TeacherStudentsScene):
    def construct(self):
        point = VectorizedPoint()
        point.move_to(3 * RIGHT + 2 * UP)
        self.student_says(
            "I've heard\\\\", "of this!",
            student_index=1,
            target_mode="hooray",
            bubble_config={
                "height": 3,
                "width": 3,
                "direction": RIGHT,
            },
            run_time=1,
        )
        self.play_student_changes(
            "thinking", "hooray", "thinking",
            look_at=point,
            added_anims=[self.teacher.animate.change("happy")]
        )
        self.wait(3)
        self.student_says(
            "But who\\\\", "cares?",
            student_index=1,
            target_mode="maybe",
            bubble_config={
                "direction": RIGHT,
                "width": 3,
                "height": 3,
            },
            run_time=1,
        )
        self.play_student_changes(
            "pondering", "maybe", "pondering",
            look_at=point,
            added_anims=[self.teacher.animate.change("guilty")]
        )
        self.wait(5)
