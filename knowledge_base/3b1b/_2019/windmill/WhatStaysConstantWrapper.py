# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個標題從「什麼保持不變？」過渡到「找到一個『不變量』」的動畫，下方有一個黑色矩形框。



from manim import *
class WhatStaysConstantWrapper(Scene):
    def __init__(self, camera_config={"background_color": GREY_E}, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        rect = ScreenRectangle()
        rect.set_height(6)
        rect.set_stroke(WHITE, 2)
        rect.set_fill(BLACK, 1)
        title1 = Text("What stays constant?", font_size=96)
        title2 = Text("Find an ", "``invariant''", font_size=96)
        title2[1].set_color(YELLOW)
        for title in [title1, title2]:
            title.to_edge(UP)
        rect.next_to(title1, DOWN)

        self.add(rect)
        self.play(FadeIn(title1, shift=DOWN))
        self.wait()
        self.play(
            FadeOut(title1, shift=UP),
            FadeIn(title2, shift=DOWN),
        )
        self.wait()
