# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一系列以歐拉命名的公式和概念，從上到下依次淡入顯示。



from manim import *
class ThingsNamedAfterEuler(Scene):
    def construct(self):
        group = VGroup(*[
            Text("Euler's formula (Complex analysis)"),
            Text("Euler's formula (Graph theory)"),
            Text("Euler's formula (Mechanical engineering)"),
            Text("Euler's formula (Analytical number theory)"),
            Text("Euler's formula (Continued fractions)"),
            Text("Euler-Lagrance equations (mechanics)"),
            Text("Euler number (topology)"),
            Text("Euler equations (fluid dynamics)"),
            Text("Euler angles (rigid-body mechanics)"),
            Text("Euler totient function (number theory)"),
        ])
        group.arrange(DOWN, aligned_edge=LEFT)
        group.set_height(config.frame_height - 1)

        self.play(LaggedStart(
            *[FadeIn(text) for text in group],
            lag_ratio=0.2,
            run_time=12
        ))
        self.wait()
