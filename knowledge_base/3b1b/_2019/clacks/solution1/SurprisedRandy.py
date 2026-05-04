# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示 Randolph 角色從出現到驚訝、眨眼、思考，最後消失的動畫過程。



from manim import *
class SurprisedRandy(Scene):
    def construct(self):
        randy = Randolph()
        self.play(FadeIn(randy))
        self.play(randy.animate.change("surprised", 3 * UR))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.animate.change("pondering", 3 * UR))
        self.play(Blink(randy))
        self.wait(2)
        self.play(FadeOut(randy))
