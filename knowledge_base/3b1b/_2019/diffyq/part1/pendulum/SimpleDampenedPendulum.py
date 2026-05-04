# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 展示一個阻尼擺錘從初始角度開始擺動並逐漸減速的過程。



from manim import *
class SimpleDampenedPendulum(Scene):
    def construct(self):
        pendulum = Pendulum(
            top_point=ORIGIN,
            initial_theta=150 * DEGREES,
            mu=0.5,
        )
        self.add(pendulum)
        pendulum.start_swinging()
        self.wait(20)
