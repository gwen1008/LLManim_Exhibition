# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一個帶有正負號標記的線段，其中點在正負顏色之間切換，並用問號和圓圈指示動畫來演示可能的符號組合。



from manim import *
class CombineInterval(Scene):
    def construct(self):
        positive_color = GREEN  # 假設正數顏色為綠色
        negative_color = RED    # 假設負數顏色為紅色

        plus_sign = MathTex("+", color=positive_color)
        minus_sign = MathTex("-", color=negative_color)

        left_point = Dot(LEFT, color=positive_color)
        right_point = Dot(RIGHT, color=negative_color)
        line1 = Line(LEFT, RIGHT)
        interval1 = Group(line1, left_point, right_point)

        plus_sign.next_to(left_point, UP)
        minus_sign.next_to(right_point, UP)

        self.add(interval1, plus_sign, minus_sign)
        self.wait()
        self.play(
            Indicate(plus_sign, scale_factor=1.5),
            Indicate(minus_sign, scale_factor=1.5),
        )
        self.wait()

        mid_point = Dot(ORIGIN, color=GREY)

        question_mark = MathTex("?", color=GREY)
        plus_sign_copy = plus_sign.copy()
        minus_sign_copy = minus_sign.copy()
        new_signs = Group(question_mark, plus_sign_copy, minus_sign_copy)
        for sign in new_signs:
            sign.next_to(mid_point, UP)

        self.play(FadeIn(mid_point), FadeIn(question_mark))
        self.wait()

        self.play(
            mid_point.animate.set_color(positive_color),
            ReplacementTransform(question_mark, plus_sign_copy),
        )
        self.play(
            Indicate(plus_sign_copy, scale_factor=1.5),
            Indicate(minus_sign, scale_factor=1.5),
        )

        self.wait()

        self.play(
            mid_point.animate.set_color(negative_color),
            ReplacementTransform(plus_sign_copy, minus_sign_copy),
        )
        self.play(
            Indicate(minus_sign_copy, scale_factor=1.5),
            Indicate(plus_sign, scale_factor=1.5),
        )

        self.wait()
