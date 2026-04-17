# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一個向量場從原始縮放版本平滑過渡到歸一化縮放版本的動畫過程。


from manim import *
import numpy as np
import itertools as it

def example_plane_func(point):
    x, y = point
    return np.array([y, -x, 0])

class VectorField(Scene):
    def __init__(self, func=example_plane_func, granularity=10, arrow_scale_factor=0.1, normalized_arrow_scale_factor=5, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.granularity = granularity
        self.arrow_scale_factor = arrow_scale_factor
        self.normalized_arrow_scale_factor = normalized_arrow_scale_factor

    def construct(self):
        num_plane = NumberPlane()
        self.add(num_plane)

        # 計算座標範圍
        x_min, y_min = num_plane.point_to_coords(FRAME_WIDTH * LEFT / 2 + FRAME_HEIGHT * UP / 2)
        x_max, y_max = num_plane.point_to_coords(FRAME_WIDTH * RIGHT / 2 + FRAME_HEIGHT * DOWN / 2)

        x_points = np.linspace(x_min, x_max, self.granularity)
        y_points = np.linspace(y_min, y_max, self.granularity)
        points = it.product(x_points, y_points)

        sized_arrows = Group()
        unsized_arrows = Group()
        for (x, y) in points:
            output = self.func((x, y))
            output_size = np.sqrt(sum(output**2))
            # 假設輸出向量非零
            normalized_output = output * (self.normalized_arrow_scale_factor / output_size)
            arrow = Vector(output * self.arrow_scale_factor)
            normalized_arrow = Vector(normalized_output * self.arrow_scale_factor)
            arrow.move_to(num_plane.coords_to_point(x, y))
            normalized_arrow.move_to(arrow)
            sized_arrows.add(arrow)
            unsized_arrows.add(normalized_arrow)

        self.add(sized_arrows)
        self.wait()

        self.play(ReplacementTransform(sized_arrows, unsized_arrows))
        self.wait()
