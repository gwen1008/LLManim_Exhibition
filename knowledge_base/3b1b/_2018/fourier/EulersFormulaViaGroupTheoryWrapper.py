# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個標題和一個矩形螢幕區域，用於說明透過群論介紹歐拉公式的視覺呈現。



from manim import *
class EulersFormulaViaGroupTheoryWrapper(Scene):
    def construct(self):
        title = Text("Euler's formula with introductory group theory")
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(title, DOWN)
        self.add(title)
        self.play(Create(screen_rect))
        self.wait(2)
