# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一輛汽車從左側移動到右側的動畫過程。



from manim import *
class MovingCar(Scene):
    def construct(self):
        car = Car()
        x = 3
        car.move_to(x * LEFT)
        self.play(car.animate.move_to(x * RIGHT), run_time=4)
