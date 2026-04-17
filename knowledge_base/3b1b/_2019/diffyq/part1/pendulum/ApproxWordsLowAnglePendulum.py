# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 展示低角度近似下單擺週期公式及其正確性標記。



from manim import *
class ApproxWordsLowAnglePendulum(Scene):
    def construct(self):
        period = MathTex(
            "\\text{Period}", "\\approx",
            "2\\pi \\sqrt{\\,{L} / {g}}",
        )
        checkmark = MathTex("\\checkmark")
        checkmark.set_color(GREEN)
        checkmark.scale(2)
        checkmark.next_to(period, RIGHT, buff=MED_LARGE_BUFF)

        self.add(period, checkmark)
