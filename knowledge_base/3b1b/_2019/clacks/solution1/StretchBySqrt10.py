# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一個雙箭頭從長度為零拉伸到完整長度，同時在箭頭上方顯示根號10的數學符號。



from manim import *
class StretchBySqrt10(Scene):
    def construct(self):
        arrow = DoubleArrow(2 * LEFT, 2 * RIGHT)
        arrow.tip[1].shift(0.05 * LEFT)
        value = MathTex("\\sqrt{10}")
        value.next_to(arrow, UP)
        arrow.save_state()
        arrow.stretch(0, 0)
        self.play(
            Restore(arrow),
            Write(value, run_time=1),
        )
        self.wait()
