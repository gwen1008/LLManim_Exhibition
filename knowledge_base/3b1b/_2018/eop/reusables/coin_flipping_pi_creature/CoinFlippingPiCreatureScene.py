# Source: 3b1b/_2018/eop/reusables/coin_flipping_pi_creature.py
# Description: [3b1b translated] 展示一個 Pi 生物角色進行擲硬幣動畫的場景。



from manim import *
class CoinFlippingPiCreatureScene(Scene):
    def construct(self):
        randy = CoinFlippingPiCreature(color=MAROON_E)
        self.add(randy)
        self.play(FlipCoin(randy, run_time=3))
