# Source: 3b1b/_2018/eop/pascal.py
# Description: [3b1b translated] 展示一個經過縮放的帕斯卡三角形網絡，其中線條根據位置以彩虹色漸變，並在特定間隔添加白色發展線和點。


from manim import *
import numpy as np

class RescaledPascalNetScene(Scene):
    def construct(self):
        # 假設 nb_levels, dev_y_step, dev_x_step 已在外部定義
        # 這裡需要定義它們，否則代碼無法運行
        nb_levels = 10  # 示例值，根據需要調整
        dev_y_step = 2   # 示例值，根據需要調整
        dev_x_step = 1   # 示例值，根據需要調整
        
        half_width = 3.0
        top_height = 4.0
        level_height = 2.0 * top_height / nb_levels

        start_points = np.array([top_height * UP])
        left_edge = top_height * UP + half_width * LEFT
        right_edge = top_height * UP + half_width * RIGHT

        dev_start = start_points[0]

        j = 0

        for n in range(nb_levels):

            if n == 0:
                start_points_left_shift = np.array([left_edge])
            else:
                start_points_left_shift = start_points[:-1]
                start_points_left_shift = np.insert(start_points_left_shift, 0, left_edge, axis=0)
            stop_points_left = 0.5 * (start_points + start_points_left_shift)
            stop_points_left += level_height * DOWN

            
            if n == 0:
                start_points_right_shift = np.array([right_edge])
            else:
                start_points_right_shift = start_points[1:]
                start_points_right_shift = np.append(start_points_right_shift, np.array([right_edge]), axis=0)
            stop_points_right = 0.5 * (start_points + start_points_right_shift)
            stop_points_right += level_height * DOWN

            
            for (i, (p, q)) in enumerate(zip(start_points, stop_points_left)):
                
                color = GREY_B 

                if n % 2 == 0 and i <= n/2:
                    m = n/2 + 0.25
                    jj = i
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                elif n % 2 == 0 and i > n/2:
                    m = n/2 + 0.25
                    jj = n - i + 0.5
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                elif n % 2 == 1 and i <= n/2:
                    m = n/2 + 0.75
                    jj = i
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                elif n % 2 == 1 and i > n/2:
                    m = n/2 + 0.75
                    jj = n - i + 0.5
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                line = Line(p, q, stroke_color=color)
                self.add(line)

            for (i, (p, q)) in enumerate(zip(start_points, stop_points_right)):
                
                color = GREY_B

                if n % 2 == 0 and i < n/2:
                    m = n/2 + 0.25
                    jj = i + 0.5
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                elif n % 2 == 0 and i >= n/2:
                    m = n/2 + 0.25
                    jj = n - i
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                elif n % 2 == 1 and i <= n/2:
                    m = n/2 + 0.75
                    jj = i + 0.5
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]

                elif n % 2 == 1 and i > n/2:
                    m = n/2 + 0.75
                    jj = n - i
                    alpha = 1 - float(jj)/m
                    color = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 100)[int(alpha * 99)]


                line = Line(p, q, stroke_color=color)
                self.add(line)

            if (n + 1) % dev_y_step == 0 and n != 1:
                j += dev_x_step
                dev_stop = stop_points_left[j]
                line = Line(dev_start, dev_stop, stroke_color=WHITE)
                self.add(line)
                dot = Dot(dev_stop, color=WHITE)
                self.add(dot)
                dev_start = dev_stop



            start_points = np.append(stop_points_left, [stop_points_right[-1]], axis=0)
            
            left_edge += level_height * DOWN
            right_edge += level_height * DOWN


        self.wait()
