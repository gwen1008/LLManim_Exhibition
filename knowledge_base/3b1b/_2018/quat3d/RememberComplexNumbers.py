# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 老師向學生展示複數公式，並解釋複數如何計算旋轉，學生們呈現不同的思考表情。



from manim import *
class RememberComplexNumbers(TeacherStudentsScene):
    def construct(self):
        complex_number = MathTex(
            "\\cos(\\theta) + \\sin(\\theta)i",
            tex_to_color_map={
                "\\cos(\\theta)": GREEN,
                "\\sin(\\theta)": RED
            }
        )
        complex_number.scale(1.2)
        complex_number.next_to(self.students, UP, buff=MED_LARGE_BUFF)

        self.teacher_says(
            "Remember how \\\\ complex numbers \\\\ compute rotations"
        )
        self.play_all_student_changes("pondering")
        self.wait()
        self.play(
            FadeIn(complex_number, shift=DOWN),
            self.change_students(
                "thinking", "confused", "happy",
                look_at=complex_number.get_center() + UP
            ),
            run_time=2
        )
        self.play_student_changes()
        self.wait(5)
