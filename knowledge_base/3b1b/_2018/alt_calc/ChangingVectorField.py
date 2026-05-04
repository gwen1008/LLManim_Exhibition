# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個隨時間變化的向量場，其中每個向量根據正弦和餘弦函數動態改變方向和顏色。



from manim import *
class ChangingVectorField(Scene):
    def __init__(self, wait_time=30, **kwargs):
        super().__init__(**kwargs)
        self.wait_time = wait_time

    def construct(self):
        plane = self.plane = NumberPlane()
        plane.set_stroke(width=2)
        plane.add_coordinates()
        self.add(plane)

        # Obviously a silly thing to do, but I'm sweeping
        # through trying to make sure old scenes don't
        # completely break in spots which used to have
        # Continual animations
        time_tracker = self.time_tracker = ValueTracker(0)
        time_tracker.add_updater(
            lambda t: t.set_value(self.time)
        )

        vectors = self.get_vectors()
        vectors.add_updater(self.update_vectors)
        self.add(vectors)
        self.wait(self.wait_time)

    def get_vectors(self):
        vectors = VGroup()
        x_max = int(np.ceil(config.frame_width))
        y_max = int(np.ceil(config.frame_height))
        step = 0.5
        for x in np.arange(-x_max, x_max + 1, step):
            for y in np.arange(-y_max, y_max + 1, step):
                point = x * RIGHT + y * UP
                vectors.add(Vector(RIGHT).shift(point))
        vectors.set_color_by_gradient(YELLOW, RED)
        return vectors

    def update_vectors(self, vectors):
        time = self.time_tracker.get_value()
        for vector in vectors:
            point = vector.get_start()
            out_point = self.func(point, time)
            norm = np.linalg.norm(out_point)
            if norm == 0:
                out_point = RIGHT  # Fake it
                vector.set_fill(opacity=0)
            else:
                out_point *= 0.5
                color = interpolate_color(BLUE, RED, norm / np.sqrt(8))
                vector.set_fill(color, opacity=1)
                vector.set_stroke(BLACK, width=1)
            new_x, new_y = out_point[:2]
            vector.put_start_and_end_on(
                point, point + new_x * RIGHT + new_y * UP
            )

    def func(self, point, time):
        x, y, z = point
        return np.array([
            np.sin(time + 0.5 * x + y),
            np.cos(time + 0.2 * x * y + 0.7),
            0
        ])
