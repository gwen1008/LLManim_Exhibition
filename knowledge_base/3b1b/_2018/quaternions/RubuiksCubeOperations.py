# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示兩個魔術方塊在3D空間中進行不同順序的旋轉操作，並伴隨鏡頭旋轉。



from manim import *
class RubuiksCubeOperations(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(**self.get_default_camera_position())
        self.begin_ambient_camera_rotation()
        cube = RubiksCube()
        cube.shift(2.5 * RIGHT)
        cube2 = cube.copy()

        self.add(cube)
        self.play(
            Rotate(cube.get_face(RIGHT), 90 * DEGREES, axis=RIGHT),
            run_time=2
        )
        self.play(
            Rotate(cube.get_face(DOWN), 90 * DEGREES, axis=UP),
            run_time=2
        )
        self.wait()
        self.play(
            cube.animate.shift(5 * LEFT),
            FadeIn(cube2)
        )
        self.play(
            Rotate(cube2.get_face(DOWN), 90 * DEGREES, axis=UP),
            run_time=2
        )
        self.play(
            Rotate(cube2.get_face(RIGHT), 90 * DEGREES, axis=RIGHT),
            run_time=2
        )
        self.wait(6)
