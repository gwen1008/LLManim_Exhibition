# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示複數平面上一個點 (4, 1) 繞原點旋轉 30 度，並用複數乘法解釋旋轉對應的運算。


from manim import *
import numpy as np

class ComplexNumberRotation(Scene):
    def __init__(self, angle=30 * DEGREES, **kwargs):
        super().__init__(**kwargs)
        self.angle = angle

    def construct(self):
        self.add_plane()
        self.add_number()
        self.show_complex_unit()
        self.show_product()

    def add_plane(self):
        plane = self.plane = ComplexPlane()
        self.play(Write(plane))

    def add_number(self):
        plane = self.plane
        origin = plane.c2p(0, 0)
        angle = self.angle

        point = plane.c2p(4, 1)
        dot = Dot(point, color=YELLOW)
        label = MathTex("(4, 1)")
        label.next_to(dot, UR, buff=0)
        line = DashedLine(origin, point)
        rotated_line = line.copy().rotate(angle, about_point=origin)
        rotated_line.set_color(GREY)
        rotated_dot = dot.copy().rotate(angle, about_point=origin)
        rotated_dot.set_color(YELLOW_E)
        mystery_label = MathTex("(?, ?)")
        mystery_label.next_to(rotated_dot, UR, buff=0)

        arc = Arc(
            start_angle=line.get_angle(),
            angle=angle,
            radius=0.75
        )
        angle_tex = str(int(np.round(angle / DEGREES))) + "^\\circ"
        angle_label = MathTex(angle_tex)
        angle_label.next_to(
            arc.point_from_proportion(0.3),
            UR, buff=SMALL_BUFF
        )

        self.play(
            FadeIn(label, shift=DOWN),
            GrowFromCenter(dot),
            Create(line)
        )
        self.wait()
        self.play(
            Create(arc),
            FadeIn(angle_label, shift=DOWN),
            TransformFromCopy(line, rotated_line),
            TransformFromCopy(dot, rotated_dot),
            path_arc=angle,
        )
        self.play(Write(mystery_label))
        self.wait()

        self.rotation_mobs = VGroup(
            arc, angle_label,
            rotated_line, rotated_dot,
            mystery_label
        )
        self.angle_tex = angle_tex
        self.number_label = label

    def show_complex_unit(self):
        plane = self.plane
        angle = self.angle
        angle_tex = self.angle_tex
        complex_coordinate_labels = plane.get_coordinate_labels()
        unit_circle = Circle(radius=1, color=YELLOW)

        origin = plane.n2p(0)
        z_point = plane.c2p(np.cos(angle), np.sin(angle))
        one_point = plane.n2p(1)
        z_dot = Dot(z_point, color=WHITE)
        one_dot = Dot(one_point, color=WHITE)
        one_dot.set_opacity(0)
        z_line = Line(origin, z_point)
        one_line = Line(origin, one_point)
        VGroup(z_dot, one_dot, z_line, one_line).set_color(BLUE)

        cos_tex = "\\cos(" + angle_tex + ")"
        sin_tex = "\\sin(" + angle_tex + ")"
        label = MathTex(
            cos_tex, "+", sin_tex, "i",
            tex_to_color_map={cos_tex: GREEN, sin_tex: RED}
        )
        label.add_background_rectangle()
        label.scale(0.8)
        label.next_to(plane.c2p(0, 1), UR, SMALL_BUFF)
        arrow = Arrow(label.get_bottom(), z_point)

        number_label = self.number_label
        new_number_label = MathTex(
            "4 + 1i", tex_to_color_map={"4": GREEN, "1": RED}
        )
        new_number_label.move_to(number_label, LEFT)
        new_number_label.add_background_rectangle()

        self.play(
            Write(complex_coordinate_labels, run_time=2),
            FadeOut(self.rotation_mobs)
        )
        self.play(Create(unit_circle))
        self.play(
            TransformFromCopy(one_dot, z_dot),
            TransformFromCopy(one_line, z_line),
            FadeIn(label, shift=DOWN),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(FadeOut(number_label, shift=DOWN))
        self.play(FadeIn(new_number_label, shift=DOWN))
        self.wait()

        self.left_z_label = label
        self.right_z_label = new_number_label
        self.cos_tex = cos_tex
        self.sin_tex = sin_tex
        self.unit_z_group = VGroup(
            unit_circle, z_line, z_dot, label, arrow
        )

    def show_product(self):
        plane = self.plane
        cos_tex = self.cos_tex
        sin_tex = self.sin_tex
        angle = self.angle

        line = Line(
            config.frame_width * LEFT / 2 + config.frame_height * UP / 2,
            plane.c2p(-0.5, 1.5)
        )
        rect = BackgroundRectangle(line, buff=0)

        left_z = self.left_z_label
        right_z = self.right_z_label
        new_left_z = left_z.copy()
        new_right_z = right_z.copy()

        lp1, rp1, lp2, rp2 = parens = MathTex("()()")
        top_line = VGroup(
            lp1, new_left_z, rp1,
            lp2, new_right_z, rp2,
        )
        top_line.arrange(RIGHT, buff=SMALL_BUFF)
        top_line.set_width(rect.get_width() - 1)
        top_line.next_to(rect.get_top(), DOWN, MED_SMALL_BUFF)

        mid_line = MathTex(
            "\\big(", "4", cos_tex, "-", "1", sin_tex, "\\big)", "+",
            "\\big(", "1", cos_tex, "+", "4", sin_tex, "\\big)", "i",
            tex_to_color_map={
                cos_tex: GREEN,
                sin_tex: RED,
                "4": GREEN,
                "1": RED,
            }
        )
        mid_line.set_width(rect.get_width() - 0.5)
        mid_line.next_to(top_line, DOWN, MED_LARGE_BUFF)

        new_z = np.exp(angle * complex(0, 1)) * complex(4, 1)
        low_line = MathTex(
            "\\approx",
            str(np.round(new_z.real, 2)), "+",
            str(np.round(new_z.imag, 2)), "i",
        )
        low_line.next_to(mid_line, DOWN, MED_LARGE_BUFF)

        self.play(FadeIn(rect))
        self.play(
            TransformFromCopy(left_z, new_left_z),
            TransformFromCopy(right_z, new_right_z),
            Write(parens)
        )
        self.wait()
        self.play(FadeIn(mid_line, shift=UP))
        self.wait()
        self.play(FadeIn(low_line, shift=UP))
        self.wait(2)
        self.play(FadeOut(self.unit_z_group))
        self.rotation_mobs.save_state()
        self.rotation_mobs.rotate(-angle, about_point=ORIGIN)
        self.rotation_mobs.set_opacity(0)
        self.play(Restore(self.rotation_mobs))
        self.wait()

        mystery_label = self.rotation_mobs[-1]
        result = low_line[1:].copy()
        result.add_background_rectangle()
        self.play(
            result.animate.move_to(mystery_label, LEFT),
            FadeOut(mystery_label, shift=DOWN),
        )
        self.wait()
