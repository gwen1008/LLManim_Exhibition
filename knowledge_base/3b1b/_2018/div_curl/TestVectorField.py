# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個向量場的流線動畫，使用閃爍效果顯示流動方向。



from manim import *
class TestVectorField(Scene):
    def __init__(self, func=None, flow_time=15, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.flow_time = flow_time

    def construct(self):
        # 注意：ManimCE 沒有內建的 StreamLines 和 AnimatedStreamLines 類
        # 這裡使用最接近的替代方案 - VectorField 和 StreamLines 動畫
        # 假設 four_swirls_function 已定義
        vector_field = VectorField(
            four_swirls_function,
            min_magnitude=0,
            max_magnitude=2,
        )
        self.add(vector_field)
        
        # 創建流線動畫
        stream_lines = StreamLines(
            four_swirls_function,
            virtual_time=3,
            min_magnitude=0,
            max_magnitude=2,
        )
        
        # 使用 ShowPassingFlash 效果
        self.play(
            ShowPassingFlash(
                stream_lines.copy().set_color(YELLOW),
                time_width=0.5,
                run_time=3
            )
        )
        self.wait(10)
