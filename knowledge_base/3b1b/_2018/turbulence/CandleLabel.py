# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示「Candle」文字從上方淡入，同時白色箭頭從左下方向右上方生長的動畫。



from manim import *
class CandleLabel(Scene):
    def construct(self):
        word = Text("Candle")
        arrow = Arrow(start=LEFT, end=RIGHT, color=WHITE, buff=0)
        arrow.rotate(45 * DEGREES)  # 旋轉到 DR 方向
        arrow.move_to(word.get_bottom() + SMALL_BUFF * DOWN, aligned_edge=UL)
        self.play(
            FadeIn(word, shift=DOWN),
            GrowArrow(arrow)
        )
        self.wait()
