# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示老師向學生講解狄利克雷定理的數學表達式，並以 x=10^6 為例逐步構建極限公式，最後動態更新 x 值並淡出範例。



from manim import *
class PhraseDirichletsTheoremFor10(TeacherStudentsScene):
    def construct(self):
        expression = MathTex(
            "\\lim_{x \\to \\infty}",
            "\\left(",
            "{\\text{\\# of primes $p$ where $p \\le x$} \\text{ and $p \\equiv 1$ mod 10}",
            "\\over",
            "\\text{\\# of primes $p$ where $p \\le x$}}",
            "\\right)",
            "=",
            "\\frac{1}{4}",
        )
        lim, lp, num, over, denom, rp, eq, fourth = expression
        expression.shift(UP)

        denom.save_state()
        denom.move_to(self.hold_up_spot, DOWN)
        denom.shift_onto_screen()

        num[len(denom):].set_color(YELLOW)

        x_example = VGroup(
            Text("Think, for example, $x = $"),
            Integer(int(1e6)),
        )
        x_example.arrange(RIGHT)
        x_example.scale(1.5)
        x_example.to_edge(UP)

        #
        teacher = self.teacher
        students = self.students
        self.play(
            FadeIn(denom, shift=DOWN),
            teacher.animate.change("raise_right_hand"),
            self.change_students(*["pondering"] * 3),
        )
        self.wait()
        self.play(FadeIn(x_example, shift=DOWN))
        self.wait()
        self.play(
            Restore(denom),
            teacher.animate.change("thinking"),
        )
        self.play(
            TransformFromCopy(denom, num[:len(denom)]),
            Write(over),
        )
        self.play(
            Write(num[len(denom):]),
            students[0].animate.change("confused"),
            students[2].animate.change("erm"),
        )
        self.wait(2)
        self.play(
            Write(lp),
            Write(rp),
            Write(eq),
        )
        self.play(FadeIn(fourth, shift=LEFT))
        self.play(FadeIn(lim, shift=RIGHT))
        self.play(
            ChangeDecimalToValue(
                x_example[1], int(1e7),
                run_time=8,
                rate_func=linear,
            ),
            VFadeOut(x_example, run_time=8),
            self.change_students(*["thinking"] * 3),
            Blink(
                teacher,
                run_time=4,
                rate_func=squish_rate_func(there_and_back, 0.65, 0.7)
            ),
        )
