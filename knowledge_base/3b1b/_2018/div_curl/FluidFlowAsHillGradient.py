# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示三維空間中流體流動的梯度場，從平面視角旋轉到傾斜視角，並持續旋轉觀察。


from manim import *
import numpy as np

class FluidFlowAsHillGradient(ThreeDScene):
    def __init__(self, production_quality_flow=False, **kwargs):
        super().__init__(**kwargs)
        self.production_quality_flow = production_quality_flow

    def construct(self):
        def potential(point):
            x, y = point[:2]
            result = 2 - 0.01 * (
                ((x - 4)**2 + y**2) *
                ((x + 4)**2 + y**2)
            )
            return max(-10, result)

        # 注意：ManimCE 中沒有內建的 negative_gradient 函數
        # 這裡假設 vector_field_func 是一個返回向量場的函數
        # 由於原代碼中 StreamLines 需要 vector_field_func，我們創建一個簡單的替代
        def vector_field_func(point):
            # 簡單的梯度場近似（僅用於演示）
            x, y = point[:2]
            # 計算負梯度
            h = 0.01
            dx = (potential([x+h, y, 0]) - potential([x-h, y, 0])) / (2*h)
            dy = (potential([x, y+h, 0]) - potential([x, y-h, 0])) / (2*h)
            return np.array([-dx, -dy, 0])

        # ManimCE 中沒有 StreamLines 類，使用替代方案
        # 創建一個簡單的向量場表示
        plane = NumberPlane(
            x_range=[-10, 10],
            y_range=[-10, 10],
            faded_line_ratio=1
        )
        
        # 創建向量場
        vector_field = VectorField(
            vector_field_func,
            plane,
            length_func=lambda norm: 0.5 * sigmoid(norm),
            colors=[BLUE, GREEN, YELLOW, RED]
        )

        # 創建勢能曲面
        surface = Surface(
            lambda u, v: plane.c2p(u, v, potential([u, v, 0])),
            u_range=[-10, 10],
            v_range=[-10, 10],
            resolution=(24, 24),
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        self.add(plane)
        self.add(vector_field)
        
        # 添加勢能曲面
        self.play(Create(surface), run_time=2)
        self.wait(1)
        
        # 開始相機旋轉
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # 移動相機到傾斜角度
        self.move_camera(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
            run_time=2
        )
        self.wait(5)
