# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個標題為 "NightHawkInLight" 的文字和一個下方出現的矩形螢幕區域。



from manim import *
class NightHawkInLightWrapper(Scene):
    def construct(self):
        title = Text("NightHawkInLight")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)
        self.add(title)
        self.play(Create(rect))
        self.wait()
