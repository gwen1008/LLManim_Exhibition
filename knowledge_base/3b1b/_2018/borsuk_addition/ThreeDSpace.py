# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 在三維空間中展示三組旋轉交錯的線條網格，並持續旋轉視角。



from manim import *
class ThreeDSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-130 * DEGREES)
        self.begin_ambient_camera_rotation()

        density = 1
        radius = 3
        lines = VGroup(*[
            VGroup(*[
                Line(
                    radius * IN, radius * OUT,
                    stroke_color=WHITE,
                    stroke_width=1,
                    stroke_opacity=0.5,
                ).shift(x * RIGHT + y * UP)
                for x in np.arange(-radius, radius + density, density)
                for y in np.arange(-radius, radius + density, density)
            ]).rotate(n * 120 * DEGREES, axis=[1, 1, 1])
            for n in range(3)
        ])

        self.play(Write(lines))
        self.wait(30)
