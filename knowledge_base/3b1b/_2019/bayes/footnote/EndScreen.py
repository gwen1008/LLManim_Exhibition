# Source: 3b1b/_2019/bayes/footnote.py
# Description: [3b1b translated] 展示一個灰色背景的結束畫面，包含一個黑色矩形區域和動態邊界效果，以及日期和社群媒體標籤文字。



from manim import *
class EndScreen(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        width = (475 / 1280) * config.frame_width
        height = width * (323 / 575)
        video_rect = Rectangle(
            width=width,
            height=height,
            fill_color=BLACK,
            fill_opacity=1,
        )
        video_rect.shift(UP)

        date = MathTex(
            "\\text{Solution will be}\\\\",
            "\\text{posted}", "1/20/19",
        )
        date[2].set_color(YELLOW)
        date.set_width(video_rect.get_width() - 2 * MED_SMALL_BUFF)
        date.move_to(video_rect)

        handle = Text("@3blue1brown")
        handle.next_to(video_rect, DOWN, buff=MED_LARGE_BUFF)

        self.add(video_rect, handle)
        self.add(AnimatedBoundary(video_rect))
        self.wait(20)
