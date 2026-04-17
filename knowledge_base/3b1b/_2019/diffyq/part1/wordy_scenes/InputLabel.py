# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一個標籤文字從下方淡入，同時箭頭從標籤向上生長的動畫。



from manim import *
class InputLabel(Scene):
    def construct(self):
        label = Text("Input")
        label.scale(1.25)
        arrow = Arrow(start=DOWN, end=UP)
        arrow.next_to(label, UP)
        self.play(
            FadeIn(label, shift=UP),
            GrowArrow(arrow)
        )
        self.wait()
