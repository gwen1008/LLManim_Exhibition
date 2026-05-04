# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示一個標題為「Homework」的場景，並在中央創建一個矩形螢幕區域。



from manim import *
class HomeworkWrapper(Scene):
    def construct(self):
        title = Text("Homework")
        title.to_edge(UP)
        screen = ScreenRectangle(height=6)
        screen.center()
        self.add(title)
        self.play(Create(screen))
        self.wait(5)
