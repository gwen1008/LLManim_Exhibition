# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個標題為「Feynman's Lost Lecture」的場景，並在標題下方創建一個矩形螢幕區域。



from manim import *
class FeynmansLostLectureWrapper(Scene):
    def construct(self):
        title = Text("Feynman's Lost Lecture")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(Create(rect))
        self.wait()
