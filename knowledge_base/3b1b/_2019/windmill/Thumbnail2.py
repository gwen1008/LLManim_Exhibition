# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個帶有文字和圖標的縮圖場景，使用灰色到黑色的漸變背景。



from manim import *
class Thumbnail2(Scene):
    def construct(self):
        words = Text("Olympics\nfor\nmath", alignment="left")
        # words.arrange(DOWN, aligned_edge=LEFT)

        words.set_height(config.frame_height - 1.5)
        words.to_edge(LEFT)

        logo = ImageMobject("imo_logo")
        logo.set_height(4.5)
        logo.to_corner(DR, buff=LARGE_BUFF)

        rect = FullScreenRectangle()
        rect.set_fill([GREY, BLACK], opacity=1)
        rect.set_stroke(width=0)

        self.clear()
        self.add(rect)
        self.add(words)
        self.add(logo)
