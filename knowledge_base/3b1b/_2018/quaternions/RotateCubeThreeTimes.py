# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示一個內含人偶的立方體在3D空間中繞不同軸旋轉的動畫，同時鏡頭緩慢旋轉。



from manim import *
class RotateCubeThreeTimes(ThreeDScene):
    def construct(self):
        cube = Cube(side_length=2)  # 使用 Cube 替代 RubiksCube
        cube.set_fill(opacity=0.8)
        cube.set_stroke(width=1)
        
        # 使用 SVGMobject 替代 Randolph，或使用 Text 作為替代
        randy = Text("?", font_size=72)  # 簡單替代
        randy.set_height(cube.get_height() - 2 * 0.1)  # 使用 0.1 替代 SMALL_BUFF
        randy.move_to(cube.get_edge_center(OUT))
        randy.set_fill(opacity=0.8)
        cube.add(randy)
        
        axes = ThreeDAxes()
        self.add(axes, cube)
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=-140 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.02)
        self.wait(2)
        
        self.play(Rotate(cube, TAU / 4, axis=RIGHT, run_time=3))
        self.wait(2)
        self.play(Rotate(cube, TAU / 4, axis=UP, run_time=3))
        self.wait(2)
        self.play(Rotate(cube, -TAU / 3, axis=np.ones(3), run_time=3))
        self.wait(7)
