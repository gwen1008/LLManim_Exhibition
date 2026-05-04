# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個時鐘的指針隨著時間轉動，並根據旋轉角度改變顏色的動畫。



from manim import *
class TickingClock(Scene):
    def __init__(self, run_time=90, **kwargs):
        super().__init__(**kwargs)
        self.run_time = run_time

    def construct(self):
        clock = Clock()
        clock.set_height(config.frame_height - 1)
        clock.to_edge(LEFT)
        lines = [clock.hour_hand, clock.minute_hand]
        
        def update_line(line):
            rev = line.get_angle() / TAU
            line.set_color(color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, RED], 100)[int(rev * 100) % 100])
        
        for line in lines:
            line.add_updater(update_line)
            self.add(line)

        self.play(
            Rotate(clock.hour_hand, angle=0.1 * self.run_time * TAU, about_point=clock.get_center(), run_time=self.run_time),
            Rotate(clock.minute_hand, angle=0.1 * self.run_time * TAU * 12, about_point=clock.get_center(), run_time=self.run_time)
        )
        self.wait()
