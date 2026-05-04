# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一個帶有「Coming up」標題和動態邊框的黑色矩形螢幕。



from manim import *
class ComingUp(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        frame = Rectangle(
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=1,
            height=6,
            width=16/9 * 6  # 保持 16:9 寬高比
        )
        title = Text("Coming up")
        title.scale(1.5)
        title.to_edge(UP)
        frame.next_to(title, DOWN)
        animated_frame = AnimatedBoundary(frame)
        self.add(frame, title, animated_frame)
        self.wait(10)
