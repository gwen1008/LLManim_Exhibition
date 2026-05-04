# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個 3D 球體與四個圓形並排的視覺對比，球體上方有「Why?!」文字，下方有球表面積公式，四個圓形中各有圓面積公式。



from manim import *
class Thumbnail(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.light_source.move_to([-10, 5, 7])

    def construct(self):
        radius = 1.75
        sphere = Sphere(radius=radius)
        sphere.rotate(70 * DEGREES, LEFT)
        sphere.set_color(BLUE_E)
        sphere.set_opacity(1)
        sphere.set_stroke(WHITE, 0.5)

        circles = VGroup(*[
            Circle(radius=radius)
            for x in range(4)
        ])
        circles.set_stroke(WHITE, 2)
        circles.set_fill(BLUE_E, 1)
        circles[0].set_fill(GREY_BROWN)
        circles.arrange_in_grid()
        for circle in circles:
            formula = MathTex("\\pi", "R", "^2")
            formula.set_color_by_tex("R", YELLOW)
            formula.scale(2)
            formula.move_to(circle)
            circle.add(formula)

        equals = MathTex("=")
        equals.scale(3)

        group = VGroup(sphere, equals, circles)
        group.arrange(RIGHT, buff=MED_SMALL_BUFF)
        equals.shift(3 * SMALL_BUFF * RIGHT)

        why = Text("Why?!")
        why.set_color(YELLOW)
        why.scale(2.5)
        why.next_to(sphere, UP)

        sa_formula = MathTex("4\\pi", "R", "^2")
        sa_formula.set_color_by_tex("R", YELLOW)
        sa_formula.scale(2)
        sa_formula.next_to(sphere, DOWN)

        self.set_camera_orientation(phi=0, theta=-90)
        self.add(sphere, equals, circles, why, sa_formula)
