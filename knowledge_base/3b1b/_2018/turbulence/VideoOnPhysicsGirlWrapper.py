# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個標題為 "Video on Physics Girl" 的場景，並在標題下方創建一個矩形螢幕區域。



from manim import *
class VideoOnPhysicsGirlWrapper(Scene):
    def construct(self):
        rect = ScreenRectangle(height=6)
        title = Text("Video on Physics Girl")
        title.scale(1.5)
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(Create(rect))
        self.wait()
