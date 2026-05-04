# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 老師對學生講解繪製向量場的注意事項，學生們呈現困惑、猶豫和俏皮的表情。



from manim import *
class QuickNoteOnDrawingThese(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Quick note on \\\\ drawing vector fields",
            bubble_config={"width": 5, "height": 3},
            added_anims=[self.change_students(
                "confused", "erm", "sassy"
            )]
        )
        self.look_at(self.screen)
        self.wait(3)
