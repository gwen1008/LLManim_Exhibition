# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示積分符號、箭頭和旋轉球體的三維動畫，並用叉號標記積分符號後重新排列元素。



from manim import *
class RoleOfCalculus(ThreeDScene):
    def __init__(self, camera_config=None, **kwargs):
        if camera_config is None:
            camera_config = {"light_source_start_point": [-4, 5, 7]}
        super().__init__(camera_config=camera_config, **kwargs)

    def construct(self):
        calc = MathTex("\\int", "\\int")
        calc.space_out_submobjects(0.4)
        calc.scale(2)
        arrow = Arrow(start=ORIGIN, end=2 * RIGHT, color=WHITE)
        sphere = self.get_sphere()
        sphere.rotate(70 * DEGREES, axis=LEFT)

        group = VGroup(calc, arrow, sphere)
        group.arrange(RIGHT)
        group.shift(0.5 * RIGHT)
        cross = Cross(group[:2], stroke_width=10)

        self.add(calc, arrow)
        self.play(Write(sphere))
        self.wait()
        self.play(Create(cross))
        self.wait()
        self.play(
            sphere.animate.next_to(ORIGIN, LEFT, 1.0),
            arrow.animate.move_to(ORIGIN).align_to(ORIGIN, LEFT),
            calc.animate.next_to(ORIGIN, RIGHT, 2.25),
            FadeOut(cross),
            path_arc=PI,
            run_time=2,
        )
        self.wait()

    def get_sphere(self):
        sphere = Sphere(radius=1, resolution=(24, 24))
        sphere.set_color(BLUE_E)
        sphere.set_opacity(0.8)
        return sphere
