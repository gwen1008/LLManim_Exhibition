# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示兩個名字以淡入動畫從右側依次出現並垂直排列的過程。



from manim import *
class MathExchangeNames(Scene):
    def construct(self):
        names = VGroup(
            Text("dwymark"),
            Text("Greg Martin"),
        )
        names.arrange(DOWN, buff=1)
        for name in names:
            self.play(FadeIn(name, shift=RIGHT))
            self.wait()
