# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個「Frictionless」文字標籤從右向左平滑移動並淡入淡出的過程。



from manim import *
class NoFrictionLabel(Scene):
    def construct(self):
        words = Text("Frictionless")
        words.shift(2 * RIGHT)
        words.add_updater(
            lambda m, dt: m.shift(dt * LEFT)
        )

        self.play(FadeIn(words))
        self.wait(2)
        self.play(FadeOut(words))
