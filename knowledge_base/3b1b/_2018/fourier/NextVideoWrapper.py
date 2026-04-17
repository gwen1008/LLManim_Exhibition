# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個標題為「Next video」的文字和一個下方動態繪製的矩形螢幕區域。



from manim import *
class NextVideoWrapper(Scene):
    def construct(self):
        title = Text("Next video")
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(title, DOWN)
        self.add(title)
        self.play(Create(screen_rect))
        self.wait(2)
