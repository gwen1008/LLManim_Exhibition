# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示向量場中所有箭頭沿著 x 軸方向依序生長和消失的動畫過程。



from manim import *
class XComponentArrows(Scene):
    def construct(self):
        field = VectorField(
            lambda p: np.array([p[1], 0, 0])
        )
        field.set_opacity(0.75)
        for u in (1, -1):
            # 在 ManimCE 中，VectorField 沒有 sort 方法
            # 我們直接使用 field 中的所有向量
            self.play(LaggedStart(
                *[GrowArrow(arrow) for arrow in field],
                lag_ratio=0.1,
                run_time=1
            ))
            self.play(FadeOut(field))
