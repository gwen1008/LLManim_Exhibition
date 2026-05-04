# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示老師在課堂上寫出傅立葉變換公式，學生們從困惑轉為思考，最後老師提出聲音編輯的應用。



from manim import *
class BeforeGettingToTheFullMath(TeacherStudentsScene):
    def construct(self):
        formula = MathTex(
            "\\hat{g}(f) = \\int_{-\\infty}^{\\infty}" + \
            "g(t)e^{-2\\pi i f t}dt"
        )
        formula.next_to(self.teacher, UP+LEFT)

        self.play(
            Write(formula),
            self.teacher.change, "raise_right_hand",
            self.change_students(*["confused"]*3)
        )
        self.wait()
        self.play(
            formula.animate.next_to(FRAME_WIDTH/2 * RIGHT, RIGHT).shift(UP * 0.5),
            self.change_students(*["pondering"]*3),
            run_time=2,
            rate_func=rate_functions.rush_into
        )
        self.teacher_says("Consider sound editing\\dots")
        self.wait(3)
