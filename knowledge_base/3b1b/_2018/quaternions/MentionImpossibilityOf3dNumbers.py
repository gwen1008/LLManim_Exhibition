# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示老師向學生解釋三維數字沒有良好乘法規則的場景，包含公式和對話泡泡。



from manim import *
class MentionImpossibilityOf3dNumbers(TeacherStudentsScene):
    def construct(self):
        equations = VGroup(
            MathTex("ij = ?"),
            MathTex("ji = ?"),
        )
        equations.arrange(RIGHT, buff=LARGE_BUFF)
        equations.scale(1.5)
        equations.to_edge(UP)
        self.add(equations)

        why = Text("Why not?")
        why.next_to(self.students[1], UP)

        self.teacher_says(
            "Such 3d numbers \\\\ have no good \\\\ multiplication rule",
            bubble_config={"width": 4, "height": 3},
        )
        self.play_all_student_changes("confused")
        self.wait(2)
        self.play(
            self.students[1].change, "maybe",
            FadeIn(why, scale=0.5),
        )
        self.wait(4)
