# Source: 3b1b/_2018/for_flammy.py
# Description: [3b1b translated] 展示 Mortimer 角色從生氣到猶豫再到聳肩的表情變化動畫。



from manim import *
class MadAtMathologer(PiCreatureScene):
    def create_pi_creature(self):
        return Mortimer().to_corner(DR)

    def construct(self):
        morty = self.pi_creature
        self.play(morty.animate.change("angry"))
        self.wait(3)
        self.play(morty.animate.change("hesitant"))
        self.wait(2)
        self.play(morty.animate.change("shruggie"))
        self.wait(3)
