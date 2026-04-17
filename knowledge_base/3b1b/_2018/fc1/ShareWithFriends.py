# Source: 3b1b/_2018/fc1.py
# Description: [3b1b translated] 展示兩個 PiCreature 角色對話，其中一個角色詢問關於萊布尼茨級數的數學公式。



from manim import *
class ShareWithFriends(PiCreatureScene):
    def construct(self):
        randy, morty = self.pi_creatures

        self.pi_creature_says(
            randy,
            "Wanna see why \\\\" +
            "$1 - \\frac{1}{3} + \\frac{1}{5}" +
            "- \\frac{1}{7} + \\cdots = \\frac{\\pi}{4}$?",
            target_mode="tease",
            added_anims=[morty.look_at, UP]
        )
        self.play(morty.animate.change("maybe", UP))
        self.wait()

    def create_pi_creatures(self):
        randy = Randolph(color=GREEN)
        morty = Mortimer(color=RED_E)
        randy.to_edge(DOWN).shift(4 * LEFT)
        morty.to_edge(DOWN)
        return randy, morty
