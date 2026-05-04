# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示克萊姆法則的縮圖場景，包含向量、平行四邊形變換和標題文字。



from manim import *
class Thumbnail(TransformingAreasYCoord, MovingCameraScene):
    def __init__(self, background_plane_kwargs=None, **kwargs):
        if background_plane_kwargs is None:
            background_plane_kwargs = {"y_max": 6}
        super().__init__(**kwargs)
        self.background_plane_kwargs = background_plane_kwargs

    def construct(self):
        # 繼承自 TransformingAreasYCoord 的設置
        self.matrix = np.array(self.matrix)
        vect = self.add_vector([1, 1.5], color=MAROON_B)
        ip = self.get_input_parallelogram(vect)
        self.add_transformable_mobject(ip)
        self.apply_transposed_matrix([[2, -0.5], [1, 2]])
        self.square.set_fill(opacity=0.7)
        self.square.set_sheen(0.75, UR)
        self.camera.frame.shift(UP)

        # 添加標題文字
        words = Text("Cramer's rule", font_size=96)
        words.set_stroke(BLACK, width=6, background=True)
        words.to_edge(UP, buff=-MED_LARGE_BUFF)
        words.add_background_rectangle()
        self.add(words)
