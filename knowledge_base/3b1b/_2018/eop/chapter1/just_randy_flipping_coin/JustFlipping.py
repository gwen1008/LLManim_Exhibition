# Source: 3b1b/_2018/eop/chapter1/just_randy_flipping_coin.py
# Description: [3b1b translated] 展示一個紫色生物反覆拋擲硬幣的動畫場景。



from manim import *
class JustFlipping(Scene):
    def construct(self):
        # 創建拋硬幣的生物，設定顏色和拋擲高度，並向下移動
        randy = CoinFlippingPiCreature(color=MAROON_E, flip_height=1).shift(2 * DOWN)
        self.add(randy)

        self.wait(2)

        # 重複10次拋硬幣動畫
        for i in range(10):
            self.wait()
            self.play(FlipCoin(randy))
