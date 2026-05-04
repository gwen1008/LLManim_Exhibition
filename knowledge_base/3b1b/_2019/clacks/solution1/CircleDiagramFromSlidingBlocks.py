# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示滑塊碰撞系統對應的圓形圖，隨著時間在圓上繪製線段並移動紅點，模擬碰撞過程。


from manim import *
import numpy as np

class CircleDiagramFromSlidingBlocks(Scene):
    def __init__(
        self,
        BlocksAndWallSceneClass=None,
        circle_config=None,
        lines_style=None,
        axes_config=None,
        end_zone_style=None,
        show_dot=True,
        show_vector=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.BlocksAndWallSceneClass = BlocksAndWallSceneClass or BlocksAndWallExampleMass1e1
        self.circle_config = circle_config or {
            "radius": 2,
            "stroke_color": YELLOW,
            "stroke_width": 3,
        }
        self.lines_style = lines_style or {
            "stroke_color": WHITE,
            "stroke_width": 2,
        }
        self.axes_config = axes_config or {
            "style": {
                "stroke_color": GREY_B,
                "stroke_width": 1,
            },
            "width": 5,
            "height": 4.5,
        }
        self.end_zone_style = end_zone_style or {
            "stroke_width": 0,
            "fill_color": GREEN,
            "fill_opacity": 0.3,
        }
        self.show_dot = show_dot
        self.show_vector = show_vector

    def construct(self):
        sliding_blocks_scene = self.BlocksAndWallSceneClass(
            show_flash_animations=False,
            write_to_movie=False,
            wait_time=0,
            file_writer_config={
                "output_directory": ".",
            }
        )
        blocks = sliding_blocks_scene.blocks
        times = [pair[1] for pair in blocks.clack_data]
        self.mass_ratio = 1 / blocks.mass_ratio
        self.show_circle_lines(
            times=times,
            slope=(-1 / np.sqrt(blocks.mass_ratio))
        )

    def show_circle_lines(self, times, slope):
        circle = self.get_circle()
        axes = self.get_axes()
        lines = self.get_lines(circle.radius, slope)
        end_zone = self.get_end_zone()

        dot = Dot(color=RED, radius=0.06)
        dot.move_to(lines[0].get_start())

        vector = Arrow(start=ORIGIN, end=lines[0].get_start(), buff=0)
        vector.set_color(RED)
        vector.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN, dot.get_center()
        ))
        vector.set_stroke(BLACK, 2, background=True)

        dot.set_opacity(int(self.show_dot))
        vector.set_opacity(int(self.show_vector))

        self.add(end_zone, axes, circle, dot, vector)

        last_time = 0
        for time, line in zip(times, lines):
            if time > 300:
                time = last_time + 1
            self.wait(time - last_time)
            last_time = time
            dot.move_to(line.get_end())
            self.add(line, dot, vector)
        self.wait()

    def get_circle(self):
        circle = Circle(**self.circle_config)
        circle.rotate(PI)  # Nice to have start point on left
        return circle

    def get_axes(self):
        config = self.axes_config
        axes = VGroup(
            Line(LEFT, RIGHT).set_width(config["width"]),
            Line(DOWN, UP).set_height(config["height"])
        )
        axes.set_style(**config["style"])
        return axes

    def get_lines(self, radius, slope):
        theta = np.arctan(-1 / slope)
        n_clacks = int(PI / theta)
        points = []
        for n in range(n_clacks + 1):
            theta_mult = (n + 1) // 2
            angle = 2 * theta * theta_mult
            if n % 2 == 0:
                angle *= -1
            new_point = radius * np.array([
                -np.cos(angle), -np.sin(angle), 0
            ])
            points.append(new_point)

        lines = VGroup(*[
            Line(p1, p2)
            for p1, p2 in zip(points, points[1:])
        ])
        lines.set_style(**self.lines_style)
        return lines

    def get_end_zone(self):
        slope = 1 / np.sqrt(self.mass_ratio)
        x = self.axes_config["width"] / 2
        zone = Polygon(
            ORIGIN, x * RIGHT, x * RIGHT + slope * x * UP,
        )
        zone.set_style(**self.end_zone_style)
        return zone
