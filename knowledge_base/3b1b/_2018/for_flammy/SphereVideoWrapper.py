# Source: 3b1b/_2018/for_flammy.py
# Description: [3b1b translated] 展示一個標題為「球體表面積」的場景，並在標題下方創建一個矩形區域。



from manim import *
class SphereVideoWrapper(Scene):
    def construct(self):
        title = MathTex(r"\text{Surface area of a sphere}")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)
        self.add(title)
        self.play(Create(rect))
        self.wait()
