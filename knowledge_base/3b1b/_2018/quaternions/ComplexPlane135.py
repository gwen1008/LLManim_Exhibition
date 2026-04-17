# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示複數平面上一個點從實軸旋轉到 135 度位置，並標示其複數表示式的動畫過程。



from manim import *
class ComplexPlane135(Scene):
    def construct(self):
        plane = ComplexPlane(unit_size=2)
        plane.add_coordinates()
        for mob in plane.coordinate_labels:
            mob.scale(2, about_edge=UR)

        angle = 3 * TAU / 8
        circle = Circle(radius=2, color=YELLOW)
        arc = Arc(angle, radius=0.5)
        angle_label = Integer(0, unit="^\\circ")
        angle_label.next_to(arc.point_from_proportion(0.5), UR, buff=SMALL_BUFF)
        line = Line(ORIGIN, 2 * RIGHT)

        point = circle.point_from_proportion(angle / TAU)
        dot = Dot(point, color=PINK)
        arrow = Vector(DR)
        arrow.next_to(dot, UL, buff=SMALL_BUFF)
        arrow.set_color(dot.get_color())
        label = MathTex("-\\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{2}}{2} i")
        label.next_to(arrow.get_start(), UP, buff=SMALL_BUFF)
        label.set_background_stroke(width=0)

        self.add(plane, circle, line, dot, label, arrow)
        self.play(
            Rotate(line, angle, about_point=ORIGIN),
            Create(arc),
            ChangeDecimalToValue(angle_label, 135),
            run_time=3
        )
        self.wait()
