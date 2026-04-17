# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示標題「Pi hiding in prime regularities」和下方一個矩形螢幕的動畫。



from manim import *
class PiHidingWrapper(Scene):
    def construct(self):
        title = Text("Pi hiding in prime regularities")
        title.to_edge(UP)
        screen = ScreenRectangle(height=6)
        screen.next_to(title, DOWN)
        self.add(title)
        self.play(Create(screen))
        self.wait(2)
