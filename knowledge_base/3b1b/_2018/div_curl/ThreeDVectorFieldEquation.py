# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個包含三個分量 "yz", "xz", "xy" 的向量矩陣，並將其高度調整為接近畫面高度。



from manim import *
class ThreeDVectorFieldEquation(Scene):
    def construct(self):
        vector = Matrix([
            "yz",
            "xz",
            "xy",
        ])
        vector.set_height(config.frame_height - 1)
        self.add(vector)
