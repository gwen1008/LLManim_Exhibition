# Source: 3b1b/_2018/eop/pascal.py
# Description: [3b1b translated] 展示帕斯卡三角形網絡的生成過程，每一層的線條根據位置使用彩虹色著色，並在特定間隔添加白色連線和點。


from manim import *
import numpy as np

class PascalNetScene(Scene):
    def construct(self):
        # 假設 nb_levels, dev_y_step, dev_x_step 已在外部定義
        # 這裡使用合理的預設值
        nb_levels = 10
        dev_y_step = 2
        dev_x_step = 1
        
        unit_width = 0.25
        top_height = 4.0
        level_height = 2.0 * top_height / nb_levels

        start_points = np.array([[0, top_height, 0]])  # 轉換為二維陣列

        dev_start = start_points[0]

        j = 0

        for n in range(nb_levels):
            half_width = 0.5 * (n + 0.5) * unit_width

            stop_points_left = start_points.copy()
            stop_points_left[:, 0] -= 0.5 * unit_width
            stop_points_left[:, 1] -= level_height

            stop_points_right = start_points.copy()
            stop_points_right[:, 0] += 0.5 * unit_width
            stop_points_right[:, 1] -= level_height
            
            for (p, q) in zip(start_points, stop_points_left):
                alpha = np.abs((p[0] + q[0]) / 2) / half_width
                # 假設 rainbow_color 函數已定義，這裡使用漸層色
                color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 10)[int(alpha * 9)]
                line = Line(p, q, stroke_color=color)
                self.add(line)

            for (i, (p, q)) in enumerate(zip(start_points, stop_points_right)):
                alpha = np.abs((p[0] + q[0]) / 2) / half_width
                color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 10)[int(alpha * 9)]
                line = Line(p, q, stroke_color=color)
                self.add(line)

            if (n + 1) % dev_y_step == 0 and n != 1:
                j += dev_x_step
                dev_stop = stop_points_left[j]
                line = Line(dev_start, dev_stop, stroke_color=WHITE)
                self.add(line)
                dot = Dot(dev_stop, color=WHITE)
                self.add(dot)  # ManimCE 沒有 add_foreground_mobject，直接 add
                dev_start = dev_stop

            start_points = np.append(stop_points_left, [stop_points_right[-1]], axis=0)

        self.wait()
