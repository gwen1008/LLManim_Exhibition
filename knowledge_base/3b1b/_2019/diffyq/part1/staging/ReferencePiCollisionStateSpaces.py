# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示兩個黑色矩形框並排，邊界有動畫效果，標題為「The block collision puzzle」。



from manim import *
class ReferencePiCollisionStateSpaces(Scene):
    def __init__(self, camera_config={"background_color": GREY_E}, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        title = Text("The block collision puzzle")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)

        frames = VGroup(*[
            ScreenRectangle(
                height=3.5,
                fill_opacity=1,
                fill_color=BLACK,
                stroke_width=0,
            )
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)
        boundary = AnimatedBoundary(frames)
        self.add(frames, boundary)
        self.wait(15)
