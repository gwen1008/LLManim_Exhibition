# Source: 3b1b/_2018/fc1.py
# Description: [3b1b translated] 展示一個標題和一個螢幕矩形從上到下出現的簡單場景。



from manim import *
class GeneralWrapper(Scene):
    def __init__(self, title_text="", **kwargs):
        super().__init__(**kwargs)
        self.title_text = title_text

    def construct(self):
        title = Text(self.title_text)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6.5)
        rect.next_to(title, DOWN)
        self.play(Write(title), Create(rect))
        self.wait()
