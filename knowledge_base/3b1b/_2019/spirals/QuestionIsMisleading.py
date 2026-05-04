# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示老師與學生對話的場景，學生驚訝提問，老師尷尬回應。



from manim import *
class QuestionIsMisleading(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Whoa, is this some\\\\divine hidden structure\\\\in the primes?",
            target_mode="surprised",
            student_index=0,
            added_anims=[
                self.students[1].animate.change("pondering"),
                self.students[2].animate.change("pondering"),
            ]
        )
        self.wait(2)

        self.students[0].bubble = None
        self.teacher_says(
            "Er...not exactly",
            bubble_config={"width": 3, "height": 2},
            target_mode="guilty"
        )
        self.wait(3)
