# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 一架飛機在隨機位置和旋轉角度之間移動，模擬顛簸的飛行過程。


from manim import *
import numpy as np
import random

class BumpyPlaneRide(Scene):
    def construct(self):
        # 使用SVG格式的飛機圖形
        plane = SVGMobject(file_name="plane2")
        self.add(plane)

        total_time = 0
        while total_time < 10:
            # 生成隨機位置（z座標固定為2）
            point = 2 * np.append(np.random.random(2), 2) + DL
            point *= 0.2
            time = 0.2 * random.random()
            total_time += time
            arc = PI * random.random() - PI / 2
            
            # 使用animate語法移動飛機
            self.play(
                plane.animate.move_to(point),
                run_time=time,
                path_arc=arc
            )
