# Source: 3b1b/_2018/eop/chapter1/stacking_coins.py
# Description: [3b1b translated] 展示隨機拋硬幣的模擬過程，正面和反面的堆疊高度隨著每次拋擲結果動態更新。


from manim import *
import numpy as np

class StackingCoins(Scene):
    def construct(self):
        h = t = 0
        heads_stack = HeadsStack(size=h)
        heads_stack.next_to(0.5*LEFT + 3*DOWN, UP)
        tails_stack = TailsStack(size=t)
        tails_stack.next_to(0.5*RIGHT + 3*DOWN, UP)
        self.add(heads_stack, tails_stack)

        for i in range(120):
            flip = np.random.choice(["H", "T"])
            if flip == "H":
                h += 1
                new_heads_stack = HeadsStack(size=h)
                new_heads_stack.next_to(0.5*LEFT + 3*DOWN, UP)
                self.play(Transform(heads_stack, new_heads_stack),
                          run_time=0.2)
            elif flip == "T":
                t += 1
                new_tails_stack = TailsStack(size=t)
                new_tails_stack.next_to(0.5*RIGHT + 3*DOWN, UP)
                self.play(Transform(tails_stack, new_tails_stack),
                          run_time=0.2)
