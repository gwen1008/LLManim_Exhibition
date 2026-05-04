# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示一個文字物件出現在畫面上方，說明3D方向插值有時很棘手。



from manim import *
class InterpolationFail(Scene):
    def construct(self):
        words = Text(
            "Sometimes interpolating 3d\norientations is tricky...",
            font_size=36
        )
        words.to_edge(UP)
        self.add(words)
