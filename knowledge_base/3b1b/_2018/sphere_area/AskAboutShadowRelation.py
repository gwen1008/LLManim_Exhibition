# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示球體表面積等於四個圓形陰影面積的視覺化證明，透過分解球面與圓形區域的對應關係。


from manim import *
import numpy as np

class AskAboutShadowRelation(ThreeDScene):
    def __init__(self, R_color=YELLOW, space_out_factor=1.15, **kwargs):
        super().__init__(**kwargs)
        self.R_color = R_color
        self.space_out_factor = space_out_factor

    def construct(self):
        self.show_surface_area()
        self.show_four_circles()
        self.ask_why()
        self.show_all_pieces()

    def show_surface_area(self):
        sphere = self.get_sphere()
        sphere.set_fill(BLUE_E, opacity=0.5)
        sphere.add_updater(
            lambda s, dt: s.rotate(0.1 * dt, axis=OUT)
        )
        pieces = sphere.copy()
        pieces.space_out_submobjects(1.5)
        pieces.shift(IN)
        pieces.set_color(GREEN)

        sa_equation = MathTex(
            "\\text{Surface area} = 4\\pi R^2",
            tex_to_color_map={"R": BLUE}
        )
        sa_equation.scale(1.5)
        sa_equation.to_edge(UP)

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-90 * DEGREES,
        )
        self.add_fixed_in_frame_mobjects(sa_equation)
        self.play(
            Create(sphere, stroke_width=1),
            FadeIn(sa_equation, shift=DOWN),
        )
        self.play(LaggedStart(
            *[UpdateFromAlphaFunc(sphere, lambda m, a: m.set_fill(
                color=interpolate_color(BLUE_E, YELLOW, a),
                opacity=interpolate(0.5, 1, a)
            ))],
            rate_func=there_and_back,
            lag_ratio=0.1,
            run_time=4
        ))
        self.play(
            sphere.animate.scale(0.75).shift(3 * LEFT),
            sa_equation.animate.shift(3 * LEFT),
        )
        self.wait(2)

        self.sphere = sphere
        self.sa_equation = sa_equation

    def show_four_circles(self):
        sphere = self.sphere
        shadow = Circle(
            radius=sphere.get_width() / 2,
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLUE_E,
            fill_opacity=1,
        )
        radial_line = Line(
            shadow.get_center(),
            shadow.get_right(),
            color=YELLOW
        )
        R_label = MathTex("R").set_color(self.R_color)
        R_label.scale(0.8)
        R_label.next_to(radial_line, DOWN, SMALL_BUFF)
        shadow.add(radial_line, R_label)
        shadow.move_to(sphere.get_center())

        shadows = VGroup(*[shadow.copy() for x in range(4)])
        shadows.arrange_in_grid(buff=MED_LARGE_BUFF)
        shadows.to_edge(RIGHT)

        area_label = MathTex(
            "\\pi R^2",
            tex_to_color_map={"R": self.R_color}
        )
        area_label.scale(1.2)
        area_labels = VGroup(*[
            area_label.copy().move_to(interpolate(
                mob.get_center(), mob.get_top(), 0.5
            ))
            for mob in shadows
        ])

        self.add_fixed_in_frame_mobjects(shadow)
        self.play(DrawBorderThenFill(shadow))
        anims = []
        for new_shadow in shadows:
            old_shadow = shadow.copy()
            self.add_fixed_in_frame_mobjects(old_shadow)
            anims.append(Transform(
                old_shadow, new_shadow, remover=True
            ))
        self.remove(shadow)
        self.play(*anims)
        self.add_fixed_in_frame_mobjects(shadows, area_labels)
        self.play(LaggedStart(*[FadeIn(label, scale=2) for label in area_labels]))
        self.wait()

        self.shadows = shadows
        self.shadow_area_labels = area_labels

    def ask_why(self):
        pass

    def show_all_pieces(self):
        shadows = self.shadows
        area_labels = self.shadow_area_labels
        sphere = self.sphere

        shadow_pieces_group = VGroup()
        for shadow in shadows:
            pieces = Surface(
                lambda u, v: np.array([
                    u * np.cos(TAU * v),
                    u * np.sin(TAU * v),
                    0,
                ]),
                u_range=[0, 1],
                v_range=[0, 1],
                resolution=(12, 24)
            )
            pieces.replace(shadow)
            pieces.set_style(fill_color=BLUE_E, fill_opacity=0.5, stroke_color=WHITE)
            shadow_pieces_group.add(pieces)

        self.add_fixed_in_frame_mobjects(shadow_pieces_group)
        self.play(
            FadeOut(shadows),
            FadeOut(area_labels),
            FadeIn(shadow_pieces_group)
        )
        self.show_area_pieces(sphere)
        self.wait()
        self.show_area_pieces(*shadow_pieces_group)
        self.wait(2)
        self.unshow_area_pieces(sphere, *shadow_pieces_group)
        self.wait(3)

    def show_area_pieces(self, *mobjects):
        for mob in mobjects:
            mob.generate_target()
            mob.target.space_out_submobjects(self.space_out_factor)
        self.play(*[MoveToTarget(mob) for mob in mobjects])
        self.play(*[
            LaggedStart(
                *[mob.animate.set_fill(YELLOW, 1) for mob in mob.submobjects],
                rate_func=there_and_back,
                lag_ratio=0.25,
                run_time=1.5
            )
            for mob in mobjects
        ])

    def unshow_area_pieces(self, *mobjects):
        self.play(*[
            mob.animate.space_out_submobjects(1.0 / self.space_out_factor)
            for mob in mobjects
        ])

    def get_sphere(self):
        return Sphere(radius=1, resolution=(24, 48)).set_style(
            fill_color=BLUE_E, fill_opacity=0.5, stroke_color=WHITE
        )
