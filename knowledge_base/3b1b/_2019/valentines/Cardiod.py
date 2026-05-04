# Source: 3b1b/_2019/valentines.py
# Description: [3b1b translated] 展示一個小圓沿著大圓滾動時，其上一個點所描繪出的心形線（Cardioid）軌跡。



from manim import *
class Cardiod(Scene):
    def construct(self):
        r = 1
        big_circle = Circle(color=BLUE, radius=r)
        big_circle.set_stroke(width=1)
        big_circle.rotate(-PI / 2)
        time_tracker = ValueTracker()
        get_time = time_tracker.get_value

        def get_lil_circle():
            lil_circle = big_circle.copy()
            lil_circle.set_color(YELLOW)
            time = get_time()
            lil_circle.rotate(time)
            angle = 0.5 * time
            lil_circle.shift(
                rotate_vector(UP, angle) * 2 * r
            )
            return lil_circle
        lil_circle = always_redraw(get_lil_circle)

        cardiod = ParametricFunction(
            lambda t: np.array([
                np.cos(0.5 * t) * (2 * r) - np.cos(1.0 * t) * r,
                np.sin(0.5 * t) * (2 * r) - np.sin(1.0 * t) * r,
                0
            ]),
            t_range=[0, 2 * TAU],
        )
        cardiod.set_color(MAROON_B)

        dot = Dot(color=RED)
        dot.add_updater(lambda m: m.move_to(lil_circle.get_start()))

        self.add(big_circle, lil_circle, dot, cardiod)
        for color in [RED, PINK, MAROON_B]:
            self.play(
                Create(cardiod.copy().set_color(color)),
                time_tracker.animate.increment_value(TAU * 2),
                rate_func=linear,
                run_time=6,
            )
