# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示長除法的視覺化過程，包括除數、被除數、商、減去的乘積和餘數的逐步出現。



from manim import *
class SimpleLongDivision(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        divisor = Integer(6)
        num = Integer(20)
        quotient = Integer(num.get_value() // divisor.get_value())
        to_subtract = Integer(-1 * quotient.get_value() * divisor.get_value())
        remainder = Integer(num.get_value() + to_subtract.get_value())

        div_sym = VMobject()
        div_sym.set_points_as_corners([0.2 * UP, UP, UP + 3 * RIGHT])

        divisor.next_to(div_sym, LEFT, buff=MED_SMALL_BUFF)
        num.next_to(divisor, RIGHT, buff=MED_LARGE_BUFF)
        to_subtract.next_to(num, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        h_line = Line(LEFT, RIGHT)
        h_line.next_to(to_subtract, DOWN, buff=MED_SMALL_BUFF)
        remainder.next_to(to_subtract, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        quotient.next_to(num, UP, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)

        remainder_rect = SurroundingRectangle(remainder)
        remainder_rect.set_color(RED)

        frame = self.camera.frame
        frame.scale(0.7, about_point=ORIGIN)

        divisor.set_color(YELLOW)
        num.set_color(RED)

        self.add(divisor)
        self.add(div_sym)
        self.add(num)
        self.play(FadeIn(quotient, shift=DOWN))
        self.play(
            TransformFromCopy(divisor, to_subtract.copy()),
            TransformFromCopy(quotient, to_subtract),
        )
        self.play(Create(h_line))
        self.play(Write(remainder))
        self.play(Create(remainder_rect))
        self.wait()
        self.play(FadeOut(remainder_rect))
