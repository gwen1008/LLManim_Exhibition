# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個參數化曲面從離散碎片組裝成完整表面，並動態改變其形狀的過程。


from manim import *
import numpy as np
import random

class WhatIsSurfaceArea(ThreeDScene):
    def __init__(self, change_power=True, **kwargs):
        super().__init__(**kwargs)
        self.change_power = change_power

    def construct(self):
        title = Text("What is surface area?")
        title.scale(1.5)
        title.to_edge(UP)
        title.shift(0.035 * RIGHT)
        self.add_fixed_in_frame_mobjects(title)

        power_tracker = ValueTracker(1)
        surface = always_redraw(
            lambda: self.get_surface(
                radius=3,
                amplitude=1,
                power=power_tracker.get_value()
            )
        )

        pieces = surface.copy()
        pieces.clear_updaters()
        random.shuffle(pieces.submobjects)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        # self.add(self.get_axes())
        self.play(LaggedStartMap(
            DrawBorderThenFill, pieces,
            lag_ratio=0.2,
        ))
        self.remove(pieces)
        self.add(surface)
        if self.change_power:
            self.play(
                power_tracker.animate.set_value(5),
                run_time=2
            )
            self.play(
                power_tracker.animate.set_value(1),
                run_time=2
            )
        self.wait(2)

    def get_surface(self, radius, amplitude, power):
        def alt_pow(x, y):
            return np.sign(x) * (np.abs(x) ** y)
        return ParametricSurface(
            lambda u, v: radius * np.array([
                v * np.cos(TAU * u),
                v * np.sin(TAU * u),
                0,
            ]) + amplitude * np.array([
                0,
                0,
                (v**2) * alt_pow(np.sin(5 * TAU * u), power),
            ]),
            resolution=(100, 20),
            v_min=0.01
        )
