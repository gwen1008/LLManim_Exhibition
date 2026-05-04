# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示一個黃色矩形從無到有被繪製出來，然後淡出消失的過程。



from manim import *
class ShowRectangleCreation(Scene):
    def construct(self):
        rect = ScreenRectangle(height=2)
        rect.set_stroke(YELLOW, 6)
        self.play(Create(rect))
        self.play(FadeOut(rect))
