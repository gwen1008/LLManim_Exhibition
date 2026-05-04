# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個渦流圖形線條從創建到消失的動畫過程，同時標籤淡入淡出。



from manim import *
class EddyReference(Scene):
    def __init__(self, radius=1, label="", **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.label = label

    def construct(self):
        # 假設 Eddy 是一個自定義的 Mobject，get_lines() 返回其線條部分
        # 由於原代碼未提供 Eddy 類的定義，這裡保留其調用方式
        eddy = Eddy(radius=self.radius)
        new_eddy = eddy.get_lines()
        for line in new_eddy:
            line.set_stroke(
                width=(3 + 3 * random.random())
            )
        # 使用 Text 替代 OldTexText
        label = Text(self.label)
        label.next_to(new_eddy, UP)

        # 使用 Create 替代 ShowCreationThenDestruction
        # 由於 ShowCreationThenDestruction 在 ManimCE 中沒有直接對應，
        # 這裡用 Create 後接 Uncreate 的 LaggedStart 來模擬
        animations = []
        for line in new_eddy:
            animations.append(Create(line))
            animations.append(Uncreate(line))
        # 使用 Succession 來串聯每個線條的創建與銷毀
        line_anim = LaggedStart(*[Succession(Create(line), Uncreate(line)) for line in new_eddy], lag_ratio=0.1)

        self.play(
            line_anim,
            FadeIn(
                label,
                rate_func=there_and_back_with_pause,
            ),
            run_time=3
        )
