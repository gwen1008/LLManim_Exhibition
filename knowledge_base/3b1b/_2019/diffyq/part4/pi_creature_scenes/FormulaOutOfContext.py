# Source: 3b1b/_2019/diffyq/part4/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師和學生場景中，一個公式出現在學生上方，學生們露出驚恐表情，老師則露出戲弄表情。



from manim import *
class FormulaOutOfContext(TeacherStudentsScene):
    def construct(self):
        formula = MathTex(
            "c_{n} = \\int_0^1 e^{-2\\pi i {n} {t}}f({t}){dt}",
            tex_to_color_map={
                "{n}": YELLOW,
                "{t}": PINK,
            }
        )
        formula.scale(1.5)
        formula.next_to(self.students, UP, buff=LARGE_BUFF)

        self.add(formula)
        self.play_all_student_changes(
            "horrified",
            look_at=formula,
        )
        self.play(self.teacher.animate.change("tease"))
        self.wait(3)
