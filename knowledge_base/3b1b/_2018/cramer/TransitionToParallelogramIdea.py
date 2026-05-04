# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 老師與學生討論從特定案例轉向幾何視角的過渡，包含對話氣泡和角色表情變化。



from manim import *
class TransitionToParallelogramIdea(TeacherStudentsScene):
    def construct(self):
        teacher_words = MathTex(
            "\\text{Now ask about }",
            "\\text{other geometric }",
            "\\text{views of}",
            "x", "\\text{and}", "y"
        )
        teacher_words.set_color_by_tex("x", X_COLOR)
        teacher_words.set_color_by_tex("y", Y_COLOR)

        self.student_says(
            "\\text{But that's a super }\\\\ \\text{specific case}",
            target_mode="sassy",
            added_anims=[self.teacher.animate.change("guilty")]
        )
        self.play_student_changes("confused", "sassy", "angry")
        self.wait()
        self.teacher_says(
            teacher_words,
            added_anims=[self.change_students(*["pondering"] * 3)]
        )
        self.wait()
