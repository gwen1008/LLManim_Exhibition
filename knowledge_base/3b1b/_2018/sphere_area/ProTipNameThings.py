# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個解題技巧的文字提示，先淡入描述文字，再從下方淡入黃色的重點提示。



from manim import *
class ProTipNameThings(Scene):
    def __init__(self, tip_descriptor="(Deceptively simple) problem solving tip:", tip="Start with names", **kwargs):
        super().__init__(**kwargs)
        self.tip_descriptor = tip_descriptor
        self.tip = tip

    def construct(self):
        words = Text(
            f"{self.tip_descriptor}\n{self.tip}",
            font_size=36
        )
        # 將第二行設為黃色
        lines = words.split("\n")
        if len(lines) > 1:
            lines[1].set_color(YELLOW)
            words = VGroup(*lines)
        
        words.to_edge(UP)

        # 分開淡入兩部分文字
        self.play(FadeIn(lines[0]))
        self.wait()
        self.play(FadeIn(lines[1], shift=DOWN))
        self.wait()
