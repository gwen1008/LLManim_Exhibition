# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示標題 "Turbulence in 2d" 和作者資訊從上方淡入的動畫。



from manim import *
class TurbulenceGifLabel(Scene):
    def construct(self):
        title = Text("Turbulence in 2d")
        title.to_edge(UP)

        attribution = Text(
            "Animation by Gabe Weymouth (@gabrielweymouth)"
        )
        attribution.scale(0.5)
        attribution.to_edge(DOWN)

        self.play(Write(title))
        self.play(FadeIn(attribution, shift=UP))
        self.wait()
