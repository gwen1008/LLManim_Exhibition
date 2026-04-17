# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個黃色的 Pi 生物角色從驚訝、困惑到沉思的表情變化動畫。



from manim import *
class ConfusedPiCreature(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        morty.set_color(YELLOW_E)
        morty.flip()
        morty.center()

        self.play(morty.animate.change("awe", DOWN + 3 * RIGHT))
        self.wait(2)
        self.play(morty.animate.change("confused"))
        self.wait(2)
        self.play(morty.animate.change("pondering"))
        self.wait(2)
