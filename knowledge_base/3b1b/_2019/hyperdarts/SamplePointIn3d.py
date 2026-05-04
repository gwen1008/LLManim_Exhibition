# Source: 3b1b/_2019/hyperdarts.py
# Description: [3b1b translated] 在三維坐標系中展示隨機點在立方體內的分布，並用虛線標示其坐標分量，最後生成大量隨機點的點雲。


from manim import *
import numpy as np

class SamplePointIn3d(ThreeDScene):
    def construct(self):
        axes = self.axes = ThreeDAxes()
        sphere = Sphere(radius=1)
        sphere.set_fill(BLUE_E, 0.25)
        sphere.set_stroke(opacity=0.5)

        cube = Cube(side_length=2)
        cube.move_to(sphere.get_center())
        cube.set_fill(GREY, 0.2)
        cube.set_stroke(WHITE, 1, opacity=0.5)

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-120 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.03)

        dot = Sphere(radius=0.05)
        dot.set_shade_in_3d(True)

        dot.move_to(axes.c2p(*np.random.uniform(-1, 1, size=3)))
        lines = always_redraw(lambda: self.get_lines(dot.get_center()))
        labels = always_redraw(lambda: self.get_labels(lines))

        self.add(axes)
        self.add(cube)

        for line, label in zip(lines, labels):
            self.play(
                Create(line),
                FadeIn(label)
            )
        self.add(lines, labels)
        self.play(GrowFromCenter(dot))
        self.play(Create(sphere, stroke_width=1))
        self.wait(2)

        n_points = 3000
        points = [
            axes.c2p(*np.random.uniform(-1, 1, 3))
            for x in range(n_points)
        ]
        dots = VGroup(*[
            Dot(
                point,
                radius=0.01,
                shade_in_3d=True,
            )
            for point in points
        ])
        dots.set_stroke(WHITE, 2)
        dots.set_opacity(0.5)
        self.play(LaggedStart(
            *[FadeIn(dot) for dot in dots],
            lag_ratio=0.005,
            run_time=9
        ))
        self.wait(4)

        for x in range(6):
            self.play(
                dot.animate.move_to(
                    axes.c2p(*np.random.uniform(-1, 1, size=3))
                )
            )
            self.wait(2)
        self.wait(7)

    def get_lines(self, point):
        axes = self.axes
        x, y, z = axes.p2c(point)
        p0 = axes.c2p(0, 0, 0)
        p1 = axes.c2p(x, 0, 0)
        p2 = axes.c2p(x, y, 0)
        p3 = axes.c2p(x, y, z)
        x_line = DashedLine(p0, p1, color=GREEN)
        y_line = DashedLine(p1, p2, color=RED)
        z_line = DashedLine(p2, p3, color=BLUE)
        lines = VGroup(x_line, y_line, z_line)
        lines.set_shade_in_3d(True)
        return lines

    def get_labels(self, lines):
        x_label = MathTex("x")
        y_label = MathTex("y")
        z_label = MathTex("z")
        result = VGroup(x_label, y_label, z_label)
        result.rotate(90 * DEGREES, RIGHT)
        result.set_shade_in_3d(True)

        x_line, y_line, z_line = lines

        x_label.set_color(x_line.get_color())
        y_label.set_color(y_line.get_color())
        z_label.set_color(z_line.get_color())

        x_label.next_to(x_line, IN, SMALL_BUFF)
        y_label.next_to(y_line, RIGHT + OUT, SMALL_BUFF)
        z_label.next_to(z_line, RIGHT, SMALL_BUFF)

        return result
