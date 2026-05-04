# Source: 3b1b/_2019/diffyq/part4/long_fourier_scenes.py
# Description: [3b1b translated] 展示傅立葉級數的向量和圓圈動畫，並使用移動相機進行局部放大效果。



from manim import *
class ZoomedInFourierSeriesExample(FourierSeriesExampleWithRectForZoom, MovingCameraScene):
    def __init__(
        self,
        vector_config={
            "max_tip_length_to_length_ratio": 0.15,
            "tip_length": 0.05,
        },
        parametric_function_step_size=0.001,
        **kwargs
    ):
        super().__init__(
            vector_config=vector_config,
            parametric_function_step_size=parametric_function_step_size,
            **kwargs
        )
    
    def setup(self):
        # 在 ManimCE 中，setup() 方法通常不需要顯式調用父類的 setup()
        # 初始化邏輯移到 construct() 或 __init__ 中
        pass
    
    def construct(self):
        # 調用父類的 construct 方法來建立基本場景
        super().construct()
    
    def get_rect(self):
        return self.camera.frame
    
    def add_vectors_circles_path(self):
        super().add_vectors_circles_path()
        for v in self.vectors:
            if v.get_stroke_width() < 1:
                v.set_stroke(width=1)
