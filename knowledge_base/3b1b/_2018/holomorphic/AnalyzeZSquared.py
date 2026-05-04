# Source: 3b1b/_2018/holomorphic.py
# Description: [3b1b translated] 展示複數平面上的 z→z² 變換，並在點 (1+0.5i) 處放大觀察局部行為。


from manim import *
import numpy as np

class AnalyzeZSquared(Scene):
    def __init__(
        self,
        plane_config={"line_frequency": 0.1},
        num_anchors_to_add_per_line=20,
        complex_homotopy=lambda z, t: z ** (1.0 + t),
        zoom_factor=0.05,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.plane_config = plane_config
        self.num_anchors_to_add_per_line = num_anchors_to_add_per_line
        self.complex_homotopy = complex_homotopy
        self.zoom_factor = zoom_factor

    def construct(self):
        self.edit_background_plane()
        self.add_title()
        # self.add_transforming_planes()
        # self.preview_some_numbers()
        self.zoom_in_to_one_plus_half_i()
        self.write_derivative()

    def add_title(self):
        title = MathTex("z \\rightarrow z^2")
        title.add_background_rectangle()
        title.scale(1.5)
        title.to_corner(UL, buff=MED_SMALL_BUFF)
        self.add(title)

    def edit_background_plane(self):
        # 在 ManimCE 中，我們需要創建一個複數平面
        self.background = ComplexPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 2,
                "stroke_opacity": 0.5,
            },
        )
        self.background.add_coordinates()
        self.add(self.background)

    def add_transforming_planes(self):
        self.plane = self.get_plane()
        self.add(self.plane)

    def preview_some_numbers(self):
        dots = VGroup(*[
            Dot().move_to(self.background.n2p(z))
            for z in [
                1, 2, complex(0, 1),
                -1, complex(2, 0.5), complex(-1, -1), complex(3, 0.5),
            ]
        ])
        dots.set_color_by_gradient(RED, YELLOW)
        d_angle = 30 * DEGREES

        dot_groups = VGroup()
        for dot in dots:
            point = dot.get_center()
            z = self.background.p2n(point)
            z_out = self.complex_homotopy(z, 1)
            out_point = self.background.n2p(z_out)
            path_arc = angle_of_vector(point)
            if abs(z - 1) < 0.01:
                # One is special
                arrow = Arc(
                    start_angle=(-90 * DEGREES + d_angle),
                    angle=(360 * DEGREES - 2 * d_angle),
                    radius=0.25
                )
                arrow.add_tip(tip_length=0.15)
                arrow = arrow.partial_curve(0, 0.9)
                arrow.next_to(dot, UP, buff=0)
            else:
                arrow = Arrow(
                    point, out_point,
                    path_arc=path_arc,
                    buff=SMALL_BUFF,
                )
            arrow.set_color(dot.get_color())

            out_dot = dot.copy()
            out_dot.set_stroke(BLUE, 1)
            out_dot.move_to(out_point)
            dot.path_arc = path_arc
            dot.out_dot = out_dot

            dot_group = VGroup(dot, arrow, out_dot)
            dot_groups.add(dot_group)

            dot_copy = dot.copy()
            dot.save_state()
            dot.scale(3)
            dot.set_opacity(0)

            dot_group.anim = Succession(
                Restore(dot),
                AnimationGroup(
                    Create(arrow),
                    Transform(
                        dot_copy, out_dot,
                        path_arc=path_arc
                    )
                )
            )

        for dot_group in dot_groups[:3]:
            self.play(dot_group.anim)
            self.wait()
        self.play(*[dg.anim for dg in dot_groups[3:]])

        # 應用複數同倫變換
        self.play(
            *[
                ApplyPointwiseFunction(
                    lambda p: self.background.n2p(
                        self.complex_homotopy(self.background.p2n(p), 1)
                    ),
                    mob
                )
                for mob in self.mobjects
                if mob != self.background
            ],
            Animation(dot_groups)
        )
        self.wait()
        self.play(FadeOut(dot_groups))
        self.wait()
        self.play(FadeOut(self.plane))
        if hasattr(self, 'transformable_mobjects'):
            self.transformable_mobjects.remove(self.plane)

    def zoom_in_to_one_plus_half_i(self):
        z = complex(1, 0.5)
        point = self.background.n2p(z)
        point_mob = Dot(point, radius=0)
        frame = Square(side_length=2).move_to(point)
        frame.set_stroke(YELLOW, 2)
        
        tiny_plane = ComplexPlane(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            background_line_style={
                "stroke_color": GREEN,
                "stroke_width": 1,
            },
        )
        tiny_plane.move_to(frame)

        plane = self.get_plane()

        words = Tex("What does this look like")
        words.add_background_rectangle()
        words.next_to(frame, LEFT, aligned_edge=UP)
        arrow = Arrow(words.get_bottom(), frame.get_left())
        VGroup(words, arrow).set_color(YELLOW)

        self.play(FadeIn(plane))
        self.play(
            frame.animate.scale(0.5),
            run_time=2
        )
        self.play(Create(tiny_plane))
        self.wait()
        self.add(plane, tiny_plane, point_mob)
        self.add(words, arrow)
        
        # 應用複數變換
        self.play(
            *[
                ApplyPointwiseFunction(
                    lambda p: self.background.n2p(
                        self.complex_homotopy(self.background.p2n(p), 1)
                    ),
                    mob
                )
                for mob in [plane, tiny_plane]
            ],
            Write(words),
            GrowArrow(arrow),
            frame.animate.move_to(point_mob.get_center()),
            run_time=3
        )
        self.wait(2)

    def write_derivative(self):
        pass

    # Helpers

    def get_plane(self):
        top_plane = ComplexPlane(
            x_range=[-8, 8, 0.1],
            y_range=[0, 5, 0.1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
        )
        bottom_plane = ComplexPlane(
            x_range=[-8, 8, 0.1],
            y_range=[-5, 0, 0.1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
        )
        tiny_tiny_buff = 0.001
        top_plane.next_to(ORIGIN, UP, buff=tiny_tiny_buff)
        bottom_plane.next_to(ORIGIN, DOWN, buff=tiny_tiny_buff)
        return VGroup(top_plane, bottom_plane)
