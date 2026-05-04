# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示一個向量場在平面上的動態流線動畫，並可調整參數。



from manim import *
class VectorFieldTest(Scene):
    def construct(self):
        plane = NumberPlane()
        mu_tracker = ValueTracker(1)
        field = VectorField(
            lambda p: pendulum_vector_field_func(
                plane.p2c(p),  # 注意：manimCE 中 point_to_coords 改為 p2c
                mu=mu_tracker.get_value()
            ),
            delta_x=0.5,
            delta_y=0.5,
            max_magnitude=6,
            opacity=0.5,
        )
        field.set_opacity(1)

        self.add(plane, field)
        return  # 以下代碼被註釋掉，因為原代碼在 return 後不會執行

        # 注意：manimCE 中沒有內建的 StreamLines 和 AnimatedStreamLines
        # 以下代碼僅為結構保留，實際運行需要自定義實現或使用替代方案
        # stream_lines = StreamLines(
        #     field.func,
        #     delta_x=0.5,
        #     delta_y=0.5,
        # )
        # animated_stream_lines = AnimatedStreamLines(
        #     stream_lines,
        #     line_anim_class=ShowPassingFlashWithThinningStrokeWidth,
        # )
        # 
        # self.add(plane, field, animated_stream_lines)
        # self.wait(10)
