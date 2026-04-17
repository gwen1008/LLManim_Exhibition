# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示文字從下方淡入，同時箭頭從左側生長出來的動畫效果。



from manim import *
class LeftEdge(Scene):
    def __init__(self, text="Left edge", vect=LEFT, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.vect = vect

    def construct(self):
        words = Text(self.text)
        arrow = Vector(self.vect)
        arrow.match_width(words)
        arrow.next_to(words, DOWN)

        self.play(
            FadeIn(words, shift=DOWN),
            GrowArrow(arrow)
        )
        self.wait()
