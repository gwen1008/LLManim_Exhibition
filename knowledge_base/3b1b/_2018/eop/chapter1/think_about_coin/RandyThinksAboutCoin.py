# Source: 3b1b/_2018/eop/chapter1/think_about_coin.py
# Description: [3b1b translated] 展示一個 PiCreature 角色思考硬幣正反面的動畫，硬幣圖案上下浮動。



from manim import *
class RandyThinksAboutCoin(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.center()
        self.add(randy)
        self.wait()
        
        # 創建硬幣正反面選項
        heads = UprightHeads().scale(3)
        tails = UprightTails().scale(3)
        h_or_t = BinaryOption(heads, tails, text_scale=1.5)
        
        # 顯示思考泡泡
        self.pi_creature_says(
            h_or_t,
            target_mode="thinking",
            bubble_kwargs={"direction": LEFT}
        )
        
        v = 0.3
        # 使用 animate 語法進行移動動畫
        self.play(
            h_or_t[0].animate.shift(v * UP),
            h_or_t[2].animate.shift(v * DOWN),
        )
        self.play(
            h_or_t[0].animate.shift(2 * v * DOWN),
            h_or_t[2].animate.shift(2 * v * UP),
        )
        self.play(
            h_or_t[0].animate.shift(v * UP),
            h_or_t[2].animate.shift(v * DOWN),
        )
        
        self.wait()
