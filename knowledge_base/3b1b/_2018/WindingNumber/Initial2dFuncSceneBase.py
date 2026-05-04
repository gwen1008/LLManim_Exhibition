# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一個基礎的 2D 函數場景，包含繪製紅色邊框線段和一個紅色小圓圈。



from manim import *
class Initial2dFuncSceneBase(Scene):
    def __init__(
        self,
        func=lambda c: c**2 - c**3 / 5 + 1,  # 將 point3d_func_from_complex_func 簡化為直接函數
        **kwargs
    ):
        super().__init__(**kwargs)
        self.func = func

    def show_planes(self):
        print("Error! Unimplemented (pure virtual) show_planes")

    def shared_construct(self):
        points = [LEFT + DOWN, RIGHT + DOWN, LEFT + UP, RIGHT + UP]
        for i in range(len(points) - 1):
            line = Line(points[i], points[i + 1], color=RED)
            self.obj_draw(line)

        def wiggle_around(point):
            radius = 0.2
            small_circle = Circle(radius=radius)  # 替換 cw_circle.copy()
            small_circle.move_to(point + radius * RIGHT)
            small_circle.set_color(RED)
            self.obj_draw(small_circle)

        wiggle_around(points[-1])

    def obj_draw(self, input_object):
        self.play(Create(input_object))  # ShowCreation -> Create

    def construct(self):
        self.show_planes()
        self.shared_construct()
