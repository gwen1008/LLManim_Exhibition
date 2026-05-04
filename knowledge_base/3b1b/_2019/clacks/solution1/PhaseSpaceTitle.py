# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一個標題為 "Phase space" 的文字，下方有一個矩形區域，標題以書寫動畫出現。



from manim import *
class PhaseSpaceTitle(Scene):
    def construct(self):
        title = Text("Phase space")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)
        self.add(rect)
        self.play(Write(title, run_time=1))
        self.wait()
