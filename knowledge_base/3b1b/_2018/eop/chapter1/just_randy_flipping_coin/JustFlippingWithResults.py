# Source: 3b1b/_2018/eop/chapter1/just_randy_flipping_coin.py
# Description: [3b1b translated] 展示一個角色連續擲硬幣，並在頂部顯示每次擲出的結果（正面或反面）的動畫過程。


from manim import *
import random

class JustFlippingWithResults(Scene):
    def construct(self):
        # 注意：CoinFlippingPiCreature、FlipCoin、UprightHeads、UprightTails
        # 是原代碼中自定義的類/動畫，ManimCE 中沒有內建。
        # 這裡保留原類名和動畫名，但實際運行需要用戶提供這些自定義物件的定義。
        randy = CoinFlippingPiCreature(color=MAROON_E, flip_height=1).shift(2 * DOWN)
        self.add(randy)

        self.wait(2)

        for i in range(10):
            self.wait()
            self.play(FlipCoin(randy))
            result = random.choice(["H", "T"])
            if result == "H":
                coin = UprightHeads().scale(3)
            else:
                coin = UprightTails().scale(3)
            coin.move_to(2 * UP + 2.5 * LEFT + i * 0.6 * RIGHT)
            self.play(FadeIn(coin))
