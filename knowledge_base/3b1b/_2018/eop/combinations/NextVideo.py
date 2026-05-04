# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示下一個影片標題和一個代表影片畫面的矩形框。



from manim import *
class NextVideo(Scene):
    def construct(self):
        title = Text("Next video: Binomial distribution")
        title.to_edge(UP)
        screen = ScreenRectangle(height=6)
        screen.next_to(title, DOWN)

        self.play(Write(title), Create(screen))
        self.wait()
