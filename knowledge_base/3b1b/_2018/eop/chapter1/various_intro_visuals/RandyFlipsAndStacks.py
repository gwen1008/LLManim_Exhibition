# Source: 3b1b/_2018/eop/chapter1/various_intro_visuals.py
# Description: [3b1b translated] 展示一個紫色生物反覆擲硬幣，並根據結果動態更新正反面計數堆疊的動畫過程。



from manim import *
class RandyFlipsAndStacks(Scene):
    def construct(self):
        randy = CoinFlippingPiCreature(color=MAROON_E)
        randy.scale(0.5).to_edge(LEFT + DOWN)

        heads = tails = 0
        tally = TallyStack(heads, tails, anchor=ORIGIN)

        nb_flips = 10
        flips = np.random.randint(2, size=nb_flips)

        for i in range(nb_flips):
            self.play(FlipCoin(randy))
            self.wait(0.5)

            flip = flips[i]
            if flip == 0:
                heads += 1
            elif flip == 1:
                tails += 1
            else:
                raise Exception("That side does not exist on this coin")

            new_tally = TallyStack(heads, tails, anchor=ORIGIN)

            if tally.nb_heads == 0 and new_tally.nb_heads == 1:
                self.play(FadeIn(new_tally.heads_stack))
            elif tally.nb_tails == 0 and new_tally.nb_tails == 1:
                self.play(FadeIn(new_tally.tails_stack))
            else:
                self.play(Transform(tally, new_tally))

            tally = new_tally
