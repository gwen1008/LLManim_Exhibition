# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一個黃色餘弦波圖形以線性速度向右平移的動畫。



from manim import *
class SineWaveResidue(Scene):
    def construct(self):
        f = 2
        wave = FunctionGraph(
            lambda x: np.cos(-0.1 * f * TAU * x),
            x_range=[0, 20],
            color=YELLOW,
        )
        wave.next_to(LEFT_SIDE, LEFT, buff=0)
        time = 10
        self.play(
            wave.animate.shift(time * RIGHT),
            run_time=f * time,
            rate_func=linear,
        )
