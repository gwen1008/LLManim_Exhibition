# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示 Morty 角色在場景中眨眼並表現出困惑表情的動畫。



from manim import *
class ConfusedPi(Scene):
    def construct(self):
        morty = Mortimer()
        morty.scale(2.5)
        morty.to_corner(UP+LEFT)
        morty.look(UP+LEFT)

        self.add(morty)
        self.play(Blink(morty))
        self.play(morty.animate.change("confused"))
        self.wait()
        self.play(Blink(morty))
        self.wait(2)
