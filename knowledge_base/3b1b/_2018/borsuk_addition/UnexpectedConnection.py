# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示質數序列與圓周率之間的數學聯繫，通過旋轉半徑動態繪製圓弧，並揭示歐拉乘積公式。



from manim import *
class UnexpectedConnection(Scene):
    def construct(self):
        primes = MathTex(
            "2,", "3,", "5,", "7,", "11,", "13,", "17,", "\\dots"
        )
        primes.move_to(2.5 * UP)

        circle = Circle(
            color=YELLOW,
            stroke_width=1,
            radius=1.5,
        )
        circle.shift(1.5 * DOWN)
        center = circle.get_center()
        center_dot = Dot(center)
        radius = Line(center, circle.get_right())
        radius.set_stroke(WHITE, 3)

        arrow = DoubleArrow(primes.get_bottom(), circle.get_top())
        arrow.tip[1].shift(SMALL_BUFF * UP)
        arrow.save_state()
        arrow.rotate(90 * DEGREES)
        arrow.scale(1.5)
        arrow.set_opacity(0)

        formula = MathTex(
            "\\frac{\\pi^2}{6} = \\prod_{p \\text{ prime}}"
            "\\frac{1}{1 - p^{-2}}"
        )
        formula.next_to(arrow.get_center(), RIGHT)

        def get_arc():
            angle = radius.get_angle()
            return Arc(
                start_angle=0,
                angle=angle,
                radius=circle.radius,
                stroke_color=YELLOW,
                stroke_width=5
            ).shift(center)

        arc = always_redraw(get_arc)

        decimal = DecimalNumber(0)
        decimal.add_updater(
            lambda d: d.move_to(interpolate(
                radius.get_start(),
                radius.get_end(),
                1.5,
            )),
        )
        decimal.add_updater(
            lambda d: d.set_value(radius.get_angle())
        )
        pi = MathTex("\\pi")
        pi.scale(2)
        pi.next_to(circle, LEFT)

        self.add(circle, radius, center_dot, decimal, arc)
        self.play(
            Rotate(radius, PI - 1e-7, about_point=center),
            LaggedStart(*[FadeIn(p, shift=DOWN) for p in primes]),
            run_time=4
        )
        self.remove(decimal)
        self.add(pi)
        self.wait()
        self.play(
            Restore(arrow),
            FadeIn(formula, shift=LEFT)
        )
        self.wait()
