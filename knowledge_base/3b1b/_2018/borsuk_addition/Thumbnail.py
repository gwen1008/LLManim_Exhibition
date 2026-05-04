# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示一個旋轉並變形的三維球體表面，作為影片縮圖。


from manim import *
import numpy as np

class Thumbnail(ThreeDScene):
    def construct(self):
        sphere = Surface(
            lambda u, v: 2 * np.array([
                np.cos(v) * np.sin(u) + 0.2 * np.cos(3 * u),
                np.sin(v) * np.sin(u),
                np.cos(u) + 0.2 * np.sin(4 * v) - 0.3 * np.cos(3 * u)
            ]),
            u_range=[0.001, PI - 0.001],
            v_range=[0, TAU],
            resolution=(24, 48),
        )
        sphere.rotate(70 * DEGREES, DOWN)
        
        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-90 * DEGREES,
        )
        # randy = Randolph(mode="telepath")
        # eyes = VGroup(randy.eyes, randy.pupils)
        # eyes.scale(3.5)
        # eyes.rotate(90 * DEGREES, RIGHT)
        # eyes.next_to(sphere, OUT, buff=0)

        self.add(sphere)
