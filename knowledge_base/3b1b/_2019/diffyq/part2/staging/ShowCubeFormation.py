# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示一個立方體從零維點逐漸拉伸成一維線段、二維正方形、三維立方體的動畫過程，並在三維空間中旋轉視角。



from manim import *
class ShowCubeFormation(ThreeDScene):
    def __init__(self, color=False, **kwargs):
        super().__init__(**kwargs)
        self.color = color

    def construct(self):
        # 在 ManimCE 中，光源控制方式不同，通常使用 ThreeDLight 或預設光源
        # 這裡移除對 light_source 的直接操作，使用預設光源
        
        cube = Cube(
            side_length=4,
            fill_color=GREY,
            stroke_color=WHITE,
            stroke_width=0.5,
            fill_opacity=1.0  # 直接設定填充不透明度
        )
        
        if self.color:
            # 在 ManimCE 中，可以使用漸變色
            cube.set_color_by_gradient(BLUE, RED)
        
        cube_3d = cube.copy()
        cube_2d = cube_3d.copy().stretch(0, 2)  # 沿 z 軸壓縮為 0
        cube_1d = cube_2d.copy().stretch(0, 1)  # 沿 y 軸壓縮為 0
        cube_0d = cube_1d.copy().stretch(0, 0)  # 沿 x 軸壓縮為 0
        
        cube.become(cube_0d)
        
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-145 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.05)
        
        for target in [cube_1d, cube_2d, cube_3d]:
            self.play(
                Transform(cube, target, run_time=1.5)
            )
        self.wait(8)
