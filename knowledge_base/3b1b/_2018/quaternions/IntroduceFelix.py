# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示一個名為 Felix 的角色在二維平面上，然後過渡到三維空間並旋轉一個球體。



from manim import *
class IntroduceFelix(PiCreatureScene, ThreeDScene):
    def setup(self):
        PiCreatureScene.setup(self)
        ThreeDScene.setup(self)

    def construct(self):
        self.introduce_felix()
        self.add_plane()
        self.show_in_three_d()

    def introduce_felix(self):
        felix = self.felix = self.pi_creature

        arrow = Arrow(start=felix.get_center(), end=felix.get_center() + DL, color=WHITE)
        arrow.next_to(felix, UR)

        label = Text("Felix the Flatlander")
        label.next_to(arrow.get_start(), UP)

        self.add(felix)
        self.play(
            felix.animate.change("wave_1", label),
            Write(label),
            GrowArrow(arrow),
        )
        self.play(Blink(felix))
        self.play(felix.animate.change("thinking", label))

        self.to_fade = VGroup(label, arrow)

    def add_plane(self):
        plane = NumberPlane(y_range=(-10, 10), x_range=(-10, 10))
        axes = ThreeDAxes()
        to_fade = self.to_fade
        felix = self.felix

        self.add(axes, plane, felix)
        self.play(
            Create(axes),
            Create(plane),
            FadeOut(to_fade),
        )
        self.wait()

        self.plane = plane
        self.axes = axes

    def show_in_three_d(self):
        felix = self.pi_creature
        plane = self.plane
        axes = self.axes

        sphere = Sphere(radius=1).set_color(BLUE_E).set_opacity(0.5)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-110 * DEGREES)
        self.play(
            FadeOut(plane),
            run_time=2
        )
        self.begin_ambient_camera_rotation(rate=0.1)
        self.add(axes, sphere)
        self.play(
            Write(sphere),
            felix.animate.change("confused")
        )
        self.wait()

        axis_angle_pairs = [
            (RIGHT, 90 * DEGREES),
            (OUT, 45 * DEGREES),
            (UR + OUT, 120 * DEGREES),
            (RIGHT, 90 * DEGREES),
        ]
        for axis, angle in axis_angle_pairs:
            self.play(Rotate(
                sphere, angle=angle, axis=axis,
                run_time=2,
            ))
        self.wait(2)

    def create_pi_creature(self):
        return Felix().move_to(4 * LEFT + 2 * DOWN)
