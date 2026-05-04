# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示標題 "Gaussian Elimination" 從上方淡入，同時一條水平線在標題下方繪製出來的過程。



from manim import *
class GaussTitle(Scene):
    def construct(self):
        title = Text("Gaussian Elimination")
        title.scale(1.5)
        title.to_edge(UP)
        line = Line(LEFT, RIGHT).scale(7)
        line.next_to(title, DOWN)
        self.play(
            FadeIn(title, lag_ratio=0.2),
            Create(line),
        )
        self.wait()
