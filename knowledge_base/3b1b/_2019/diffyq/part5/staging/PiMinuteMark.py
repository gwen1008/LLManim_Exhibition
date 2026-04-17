# Source: 3b1b/_2019/diffyq/part5/staging.py
# Description: [3b1b translated] 展示一個帶有黑色填充和白色邊框的矩形框，從上方淡入並包圍著顯示 "π minutes ≈ 3:08" 的數學文字。



from manim import *
class PiMinuteMark(Scene):
    def construct(self):
        text = MathTex(
            "\\pi \\text{ minutes} \\approx \\text{3:08}"
        )
        rect = SurroundingRectangle(text)
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 2)

        self.play(
            FadeIn(rect, shift=DOWN),
            FadeIn(text, shift=DOWN),
        )
        self.wait()
