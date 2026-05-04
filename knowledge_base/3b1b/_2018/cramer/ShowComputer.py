# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示一台筆記型電腦在3D空間中旋轉並逐漸淡出的動畫。



from manim import *
class ShowComputer(ThreeDScene):
    def construct(self):
        laptop = Laptop()
        laptop.add_updater(lambda m, dt: m.rotate(0.1 * dt, axis=UP))
        self.play(Create(
            laptop,
            lag_ratio=0.1,
            rate_func=smooth
        ))
        self.wait(8)
        self.play(FadeOut(laptop))
