# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個帶有標題的螢幕矩形，標題位於上方，矩形位於標題下方。



from manim import *
class Wrapper(Scene):
    def __init__(self, title="", title_kwargs={}, screen_height=6, wait_time=2, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.title_kwargs = title_kwargs
        self.screen_height = screen_height
        self.wait_time = wait_time

    def construct(self):
        rect = self.rect = ScreenRectangle(height=self.screen_height)
        title = self.title = Text(self.title, **self.title_kwargs)
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(Create(rect))
        self.wait(self.wait_time)
