# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一條線段繞原點旋轉的動畫，旋轉速度隨時間變化。



from manim import *
class TestRotater(Scene):
    def construct(self):
        test_line = Line(ORIGIN, RIGHT)
        # ManimCE 中沒有 FuncRotater，用 Rotate 動畫模擬
        # 使用 lambda x: x % 0.25 控制旋轉速度
        # 這裡用連續的 Rotate 動畫來近似
        self.play(Rotate(test_line, angle=2*PI, run_time=10, rate_func=lambda x: x % 0.25))
