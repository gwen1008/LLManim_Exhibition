# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個標題和一個螢幕矩形，模擬上一個影片的視覺化內容。



from manim import *
class LastVideoWrapper(Scene):
    def construct(self):
        title = Text("Visualizing the Fourier Transform")
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(title, DOWN)

        self.add(title)
        self.play(Create(screen_rect))
        self.wait()
