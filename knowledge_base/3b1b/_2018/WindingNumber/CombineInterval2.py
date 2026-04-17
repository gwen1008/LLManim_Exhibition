# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示兩個帶有正號標記的線段從左右兩側移動到中間，並用圓圈標示端點的過程。



from manim import *
class CombineInterval2(Scene):
    def construct(self):
        plus_sign = MathTex("+", color=BLUE)  # 假設 positive_color 為 BLUE

        def make_interval(a, b):
            line = Line(a, b)
            start_dot = Dot(a, color=BLUE)
            end_dot = Dot(b, color=BLUE)
            start_sign = plus_sign.copy().next_to(start_dot, UP)
            end_sign = plus_sign.copy().next_to(end_dot, UP)
            return Group(start_sign, end_sign, line, start_dot, end_dot)

        def pair_indicate(a, b):
            self.play(
                Indicate(a, scale_factor=1.2),  # 替代 CircleIndicate
                Indicate(b, scale_factor=1.2)
            )

        left_interval = make_interval(2 * LEFT, LEFT)
        right_interval = make_interval(RIGHT, 2 * RIGHT)

        self.play(FadeIn(left_interval), FadeIn(right_interval))

        pair_indicate(left_interval[0], left_interval[1])

        pair_indicate(right_interval[0], right_interval[1])

        self.play(
            left_interval.animate.shift(RIGHT),
            right_interval.animate.shift(LEFT),
        )

        pair_indicate(left_interval[0], right_interval[1])

        self.wait()
