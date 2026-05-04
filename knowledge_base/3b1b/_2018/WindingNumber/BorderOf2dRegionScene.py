# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一個二維區域的內部填充和邊界繪製過程，在坐標平面上先淡入填充區域，再創建邊界輪廓。



from manim import *
class BorderOf2dRegionScene(Scene):
    def construct(self):
        num_plane = NumberPlane()
        self.add(num_plane)

        points = standard_rect + 1.5 * UP + 2 * RIGHT
        interior = Polygon(*points, fill_color=neutral_color, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(interior))

        border = Polygon(*points, color=negative_color, stroke_width=border_stroke_width)
        self.play(Create(border))
