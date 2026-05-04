# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示魔術方塊分別沿著 z 軸後 x 軸，以及 x 軸後 z 軸旋轉的順序差異，並在 3D 空間中比較兩種旋轉結果。



from manim import *
class RotationsOfCube(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(**self.get_default_camera_position())
        self.begin_ambient_camera_rotation(0.0001)
        cube = RubiksCube()
        cube2 = cube.copy()
        axes = ThreeDAxes()
        axes.scale(0.75)

        label1 = TexText(
            "z-axis\\\\",
            "then x-axis"
        )
        label2 = TexText(
            "x-axis\\\\",
            "then z-axis"
        )
        for label in [label1, label2]:
            for part in label:
                part.add_background_rectangle()
            label.rotate(90 * DEGREES, RIGHT)
            label.move_to(3 * OUT + 0.5 * IN)

        self.add(axes, cube)
        self.play(
            Rotate(cube, 90 * DEGREES, OUT, run_time=2),
            FadeIn(label1[0], shift=IN),
        )
        self.play(
            Rotate(cube, 90 * DEGREES, RIGHT, run_time=2),
            FadeIn(label1[1], shift=IN),
        )
        self.wait()
        self.play(
            cube.animate.shift(5 * RIGHT),
            label1.animate.shift(5 * RIGHT),
            Write(cube2, run_time=1)
        )
        self.play(
            Rotate(cube2, 90 * DEGREES, RIGHT, run_time=2),
            FadeIn(label2[0], shift=IN),
        )
        self.play(
            Rotate(cube2, 90 * DEGREES, OUT, run_time=2),
            FadeIn(label2[1], shift=IN),
        )
        self.wait(5)
