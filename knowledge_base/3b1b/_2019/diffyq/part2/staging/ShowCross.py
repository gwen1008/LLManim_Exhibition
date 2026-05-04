# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示一個十字交叉圖形從無到有動態繪製的過程。



from manim import *
class ShowCross(Scene):
    def construct(self):
        cross = Cross(Square())
        cross.set_width(3)
        cross.set_height(1, stretch=True)
        self.play(Create(cross))
