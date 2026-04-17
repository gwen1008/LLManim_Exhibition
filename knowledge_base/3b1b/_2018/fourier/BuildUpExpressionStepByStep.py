# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示傅立葉變換表達式逐步構建的過程，教師向學生逐步展示公式的各個部分。



from manim import *
class BuildUpExpressionStepByStep(TeacherStudentsScene):
    def construct(self):
        expression = MathTex(
            "\\frac{1}{t_2 - t_1}", "\\int_{t_1}^{t_2}",
            "g(t)", "e", "^{-2\\pi i", "f", "t}", "dt"
        )
        frac, integral, g, e, two_pi_i, f, t, dt = expression
        expression.next_to(self.teacher, UP+LEFT)
        t.set_color(YELLOW)
        g[2].set_color(YELLOW)  # 注意：MathTex中索引可能不同，可能需要調整
        dt[1].set_color(YELLOW)  # 注意：MathTex中索引可能不同，可能需要調整
        f.set_color(GREEN)
        t.save_state()
        t.move_to(f, LEFT)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(e),
            FadeIn(two_pi_i),
        )
        self.play(
            self.change_students(*["pondering"]*3),
            FadeIn(t),
        )
        self.play(
            FadeIn(f),
            t.restore,
        )
        self.wait()
        self.play(FadeIn(g), Blink(self.students[1]))
        self.wait()
        self.play(
            FadeIn(integral),
            FadeIn(frac),
            FadeIn(dt),
        )
        self.wait(3)
        self.teacher_says(
            "Just one final \\\\ distinction.",
            bubble_config = {"height" : 2.5, "width" : 3.5},
            added_anims = [expression.to_corner, UP+RIGHT]
        )
        self.wait(3)
