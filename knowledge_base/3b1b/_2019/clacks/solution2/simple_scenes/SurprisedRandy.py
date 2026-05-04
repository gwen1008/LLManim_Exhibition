# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示 Randy 角色從驚訝到困惑的表情變化，並包含眨眼動畫。



from manim import *
class SurprisedRandy(Scene):
    def construct(self):
        randy = Randolph()
        self.play(randy.animate.change("surprised", 3 * UR))
        self.play(Blink(randy))
        self.play(randy.animate.change("confused"))
        self.play(Blink(randy))
        self.wait()
