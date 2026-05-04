# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示一個困惑的 Pi 生物角色眨眼並改變表情的動畫過程。



from manim import *
class ConfusedPiCreature(Scene):
    def construct(self):
        randy = Randolph(color=GREY_BROWN)
        self.add(randy)
        self.play(Blink(randy))
        self.play(randy.animate.change("confused"))
        self.play(Blink(randy))
        self.wait()
