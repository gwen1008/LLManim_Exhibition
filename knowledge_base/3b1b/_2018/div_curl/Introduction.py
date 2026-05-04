# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示向量場的散度與旋度，先顯示散度場的流線動畫，再轉換為旋度場並顯示其流線動畫。



from manim import *
class Introduction(MovingCameraScene):
    def __init__(
        self,
        stream_lines_config={
            "start_points_generator_config": {
                "delta_x": 1.0 / 8,
                "delta_y": 1.0 / 8,
                "y_min": -8.5,
                "y_max": 8.5,
            }
        },
        vector_field_config={},
        virtual_time=3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.stream_lines_config = stream_lines_config
        self.vector_field_config = vector_field_config
        self.virtual_time = virtual_time

    def construct(self):
        # Divergence
        def div_func(p):
            return p / 3
        
        # 注意：ManimCE 沒有內建的 VectorField 和 StreamLines 類別
        # 這裡保留原類別名稱，實際使用時需要自定義或使用替代方案
        div_vector_field = VectorField(
            div_func, **self.vector_field_config
        )
        stream_lines = StreamLines(
            div_func, **self.stream_lines_config
        )
        stream_lines.shuffle()
        div_title = self.get_title("Divergence")

        self.add(div_vector_field)
        self.play(
            LaggedStartMap(ShowPassingFlash, stream_lines),
            FadeIn(div_title[0]),
            *[GrowFromCenter(part) for part in div_title[1:]]
        )

        # Curl
        def curl_func(p):
            return rotate_vector(p / 3, 90 * DEGREES)

        curl_vector_field = VectorField(
            curl_func, **self.vector_field_config
        )
        stream_lines = StreamLines(
            curl_func, **self.stream_lines_config
        )
        stream_lines.shuffle()
        curl_title = self.get_title("Curl")

        self.play(
            ReplacementTransform(div_vector_field, curl_vector_field),
            ReplacementTransform(
                div_title, curl_title,
                path_arc=90 * DEGREES
            ),
        )
        self.play(ShowPassingFlash(stream_lines, run_time=3))
        self.wait()

    def get_title(self, word):
        title = Text(word)  # 使用 Text 替代 OldTexText
        title.scale(2)
        title.to_edge(UP)
        title.add_background_rectangle()
        return title
