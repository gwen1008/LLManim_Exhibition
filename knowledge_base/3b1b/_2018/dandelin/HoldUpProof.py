# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 老師舉起右手展示一個證明，學生們從困惑轉為開心的反應。



from manim import *
class HoldUpProof(TeacherStudentsScene):
    def construct(self):
        title = TexText("One of my all-time favorite proofs")
        title.to_edge(UP)
        self.add(title)

        self.play(
            self.teacher.animate.change("raise_right_hand", self.screen),
            self.change_students(
                "pondering", "confused", "maybe",
                look_at=title
            )
        )
        self.look_at(title)
        self.wait(5)
        self.play_student_changes(
            "happy", "thinking", "hooray",
            look_at=title
        )
        self.wait(5)
