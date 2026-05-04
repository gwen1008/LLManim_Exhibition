# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示一個巨大的紅色叉號覆蓋全螢幕，同時文字從上方淡入的視覺效果。



from manim import *
class GiantCross(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        cross = Cross(rect)
        cross.set_stroke(RED, 25)

        words = Text("This wouldn't\nhappen!")
        words.scale(2)
        words.set_color(RED)
        words.to_edge(UP)

        self.play(
            FadeIn(words, shift=DOWN),
            Create(cross),
        )
        self.wait()
