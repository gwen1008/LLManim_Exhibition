# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個多變量函數將平面上的點進行非線性變換的動畫過程。


from manim import *
import numpy as np

class ExampleMultivariableFunction(Scene):
    def __init__(self, show_basis_vectors=False, show_coordinates=True, **kwargs):
        super().__init__(**kwargs)
        self.show_basis_vectors = show_basis_vectors
        self.show_coordinates = show_coordinates
        
    def construct(self):
        # 創建坐標軸
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": BLUE},
        )
        
        # 添加坐標軸標籤
        axis_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # 創建網格
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        
        # 添加所有元素到場景
        self.add(grid, axes, axis_labels)
        
        # 定義非線性變換函數
        def example_function(point):
            x, y = point[:2]  # 只取前兩個坐標
            return np.array([
                x + np.sin(y),
                y + np.sin(x),
                0
            ])
        
        # 創建變換動畫
        self.wait()
        
        # 應用非線性變換
        # 在ManimCE中，我們需要手動創建變換動畫
        # 這裡使用ApplyPointwiseFunction來模擬非線性變換
        self.play(
            ApplyPointwiseFunction(
                lambda point: example_function(point),
                VGroup(grid, axes, axis_labels)
            ),
            run_time=5
        )
        
        self.wait()
