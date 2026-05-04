# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個標題為「微積分本質」的文字，並在其下方創建一個螢幕矩形。



from manim import *
class EoCWrapper(Scene):
    def construct(self):
        title = Text("Essence of calculus")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(Create(rect))
        self.wait()
