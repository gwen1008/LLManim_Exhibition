# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一個帶有「Later...」文字和黑色矩形框的過場畫面。



from manim import *
class ComingUp(Scene):
    def __init__(self, camera_config={"background_color": GREY_D}, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = camera_config["background_color"]

    def construct(self):
        rect = ScreenRectangle()
        rect.set_height(6)
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 2)

        words = Text("Later...")
        words.scale(2)
        words.to_edge(UP)
        rect.next_to(words, DOWN)

        self.add(rect)
        self.play(FadeIn(words))
        self.wait()
