# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示文字上方出現一個白色箭頭，模擬光線在霧粒子間反射的概念。



from manim import *
class LightBouncingOffFogParticle(Scene):
    def construct(self):
        words = Text(
            "Light bouncing\n"
            "off fog particles"
        )
        arrow = Arrow(
            start=ORIGIN,
            end=UP + 0.5 * RIGHT,
            color=WHITE
        )
        arrow.next_to(words, UP)

        self.add(words)
        self.play(GrowArrow(arrow))
        self.wait()
