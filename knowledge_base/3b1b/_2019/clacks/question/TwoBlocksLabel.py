# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個標題文字「Two sliding blocks」從上方出現，並有兩支紅色箭頭從文字底部分別指向左右兩側的動畫。



from manim import *
class TwoBlocksLabel(Scene):
    def construct(self):
        label = Text("Two sliding\nblocks")  # OldTexText 改為 Text，並用 \n 換行
        label.to_edge(UP)
        arrows = VGroup(*[
            Arrow(label.get_bottom(), point)
            for point in [RIGHT, LEFT]
        ])
        arrows.set_color(RED)
        self.play(
            Write(label),
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.7),
            run_time=1
        )
        self.wait()
