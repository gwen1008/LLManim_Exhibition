# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示 Linus 角色在不同情緒模式間切換並眨眼的動畫序列。



from manim import *
class LinusReactions(Scene):
    def construct(self):
        linus = Linus()
        for mode in "confused", "sad", "erm", "angry", "pleading":
            self.play(linus.change, mode, 2 * RIGHT)
            self.wait()
            self.play(Blink(linus))
            self.wait()
