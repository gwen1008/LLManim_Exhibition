# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一個斜率公式標籤及其下方箭頭的動畫效果。



from manim import *
class SimpleSlopeLabel(Scene):
    def construct(self):
        label = MathTex(
            "\\text{Slope}", "=",
            "-\\frac{\\sqrt{m_1}}{\\sqrt{m_2}}"
        )
        vector = Arrow(start=ORIGIN, end=DOWN + 2 * LEFT, color=WHITE, buff=0)
        vector.move_to(label[0].get_bottom(), aligned_edge=UR)
        vector.shift(SMALL_BUFF * DOWN)
        self.play(
            Write(label),
            GrowArrow(vector),
        )
        self.wait()
