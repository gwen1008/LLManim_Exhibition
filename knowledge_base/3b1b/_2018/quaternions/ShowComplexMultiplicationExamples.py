# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示複數平面上乘以不同複數時，平面如何旋轉與伸縮，並標示乘數的實部與虛部。



from manim import *
class ShowComplexMultiplicationExamples(Scene):
    def __init__(
        self,
        plane_config={
            "x_range": [-9, 9],
            "y_range": [-9, 9],
            "x_length": 18,
            "y_length": 18,
            "stroke_width": 3,
        },
        background_plane_config={
            "x_range": [-9, 9],
            "y_range": [-9, 9],
            "x_length": 18,
            "y_length": 18,
            "color": GREY_B,
            "secondary_color": GREY_D,
            "stroke_width": 0.5,
            "stroke_opacity": 0.5,
            "axis_config": {"stroke_opacity": 0.5},
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.plane_config = plane_config
        self.background_plane_config = background_plane_config

    def construct(self):
        self.add_planes()
        z_tuples = [
            (complex(2, 1), "2 + i", UP),
            (complex(5, 2), "5 + 2i", LEFT),
            (
                complex(-np.sqrt(2) / 2, np.sqrt(2) / 2),
                "-\\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{2}}{2} i",
                LEFT,
            ),
            (complex(-4, 1.5), "-4 + 1.5i", RIGHT),
            (complex(3, 0), "3 + 0i", UP),
            (complex(4, -3), "4 + -3i", UP),
        ]

        for z, z_tex, label_vect in z_tuples:
            self.show_multiplication(z, z_tex, label_vect)

    def add_planes(self, include_title=True):
        plane = ComplexPlane(**self.plane_config)
        self.plane = plane
        background_plane = ComplexPlane(**self.background_plane_config)
        background_plane.add_coordinates()
        self.background_plane = background_plane

        self.add(background_plane)
        self.add(plane)

        if include_title:
            title = Text("Complex plane")
            title.scale(1.5)
            title.to_corner(UL, buff=MED_LARGE_BUFF)
            title.shift(SMALL_BUFF * UR)
            self.title = title
            self.add(title)

    def show_multiplication(self, z, z_tex, label_vect):
        z_color = WHITE
        plane = self.plane
        new_plane = plane.copy()
        real_tex, imag_tex = z_tex.split("+")
        label = MathTex(
            "\\text{Multiply by}\\\\",
            real_tex, "+", imag_tex,
        )
        label[1].set_color(GREEN)
        label[3].set_color(RED)
        label.scale(1.2)

        h_line = Line(
            plane.n2p(0),
            plane.n2p(z.real),
            color=GREEN,
            stroke_width=5,
        )
        v_line = Line(
            plane.n2p(z.real),
            plane.n2p(z),
            color=RED,
            stroke_width=5,
        )
        lines = VGroup(h_line, v_line)

        z_point = plane.n2p(z)
        z_dot = Dot(z_point)
        z_dot.set_color(z_color)
        label[1:].next_to(z_dot, label_vect)
        label[0].next_to(label[1:], UP)
        for mob in label:
            label.add_to_back(BackgroundRectangle(mob))

        one_dot = Dot(plane.n2p(1))
        one_dot.set_color(YELLOW)
        for dot in z_dot, one_dot:
            dot.save_state()
            dot.scale(5)
            dot.set_fill(opacity=0)
            dot.set_stroke(width=1, opacity=0.5)
        to_fade_out = VGroup(
            plane, label, lines, z_dot, one_dot
        )

        self.play(
            Create(lines),
            FadeIn(label, shift=DOWN),
            Restore(z_dot),
        )
        self.play(Restore(one_dot))
        angle = np.log(z).imag
        self.play(
            one_dot.animate.move_to(z_dot),
            plane.animate.apply_complex_function(lambda w: z * w),
            run_time=3,
            path_arc=angle,
        )
        self.wait()
        self.play(
            FadeOut(to_fade_out),
            FadeIn(new_plane),
        )
        self.plane = new_plane
