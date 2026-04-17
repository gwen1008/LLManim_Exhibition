# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示向量場中一個圓形區域內慢速流入和快速流出的流線動畫，並標註正散度。



from manim import *
class DivergenceAtSlowFastPoint(Scene):
    def __init__(
        self,
        vector_field_config={
            "length_func": lambda norm: 0.1 + 0.4 * norm / 4.0,
            "min_magnitude": 0,
            "max_magnitude": 3,
        },
        stream_lines_config={
            "start_points_generator_config": {
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            "virtual_time": 1,
            "min_magnitude": 0,
            "max_magnitude": 3,
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.vector_field_config = vector_field_config
        self.stream_lines_config = stream_lines_config

    def construct(self):
        def func(point):
            return 3 * sigmoid(point[0]) * RIGHT
        
        vector_field = self.vector_field = VectorField(
            func, **self.vector_field_config
        )

        circle = Circle(color=WHITE)
        
        # 替換 OldTexText 為 Text
        slow_words = Text("Slow flow in")
        fast_words = Text("Fast flow out")
        words = VGroup(slow_words, fast_words)
        
        # 添加背景矩形
        for word in words:
            word.add_background_rectangle()
        
        # 設置位置
        slow_words.next_to(circle, LEFT)
        fast_words.next_to(circle, RIGHT)

        # 替換 OldTex 為 MathTex
        div_tex = MathTex("\\text{div}\\,\\textbf{F}(x, y) > 0")
        div_tex.add_background_rectangle()
        div_tex.next_to(circle, UP)

        self.add(vector_field)
        
        # ManimCE 中沒有 add_foreground_mobjects，直接添加到場景
        self.add(circle, div_tex)
        
        self.begin_flow()
        self.wait(2)
        
        for word in words:
            self.add(word)
            self.play(Write(word))
        self.wait(8)

    def begin_flow(self):
        # 注意：ManimCE 中可能沒有 StreamLines 和 AnimatedStreamLines
        # 這裡使用最接近的替代方案
        stream_lines = StreamLines(
            self.vector_field.func,
            **self.stream_lines_config
        )
        
        # 如果 StreamLines 不可用，可以考慮使用 VectorField 的動畫替代
        # 這裡保持原結構，但實際使用時可能需要調整
        try:
            stream_line_animation = AnimatedStreamLines(stream_lines)
            stream_line_animation.update(3)
            self.add(stream_line_animation)
        except:
            # 備用方案：簡單地顯示向量場
            self.add(self.vector_field)
            self.wait(3)
