# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示球體截面中兩個相似三角形的幾何關係，透過動態調整角度參數並標記角度，說明高度壓縮的數學原理。


from manim import *
import numpy as np

class JustifyHeightSquish(MovingCameraScene):
    def __init__(
        self,
        top_phi=0.5242654422649652,  # As measured from previous scene
        low_phi=0.655081802831207,
        radius=2,
        R_color=RED,
        d_color=WHITE,
        little_triangle_color=BLUE,
        big_triangle_color=GREY_BROWN,
        alpha_color=WHITE,
        beta_color=WHITE,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.top_phi = top_phi
        self.low_phi = low_phi
        self.radius = radius
        self.R_color = R_color
        self.d_color = d_color
        self.little_triangle_color = little_triangle_color
        self.big_triangle_color = big_triangle_color
        self.alpha_color = alpha_color
        self.beta_color = beta_color

    def construct(self):
        self.recreate_cross_section()
        self.show_little_triangle()
        self.show_tangent_to_radius()
        self.tweak_parameter()
        self.label_angles()

    def recreate_cross_section(self):
        axes = Axes(
            axis_config={
                "unit_size": 2,
            }
        )
        circle = Circle(
            radius=self.radius,
            stroke_color=PINK,
            stroke_width=2,
        )
        R_line = self.get_R_line(90 * DEGREES)
        R_line.set_color(self.R_color)
        R_label = MathTex("R")
        R_label.next_to(R_line, DOWN, buff=SMALL_BUFF)
        d_lines = VGroup(*[
            self.get_d_line(phi)
            for phi in [self.low_phi, self.top_phi]
        ])
        d_line = d_lines[0]
        d_line.set_color(self.d_color)
        d_label = MathTex("d")
        d_label.next_to(d_line, DOWN, buff=SMALL_BUFF)

        proj_lines = VGroup(*[
            self.get_R_line(phi)
            for phi in [self.top_phi, self.low_phi]
        ])
        proj_lines.set_stroke(YELLOW, 1)

        s_rect_line, c_rect_line = [
            Line(
                *[l.get_end() for l in lines],
                stroke_color=YELLOW,
                stroke_width=2,
            )
            for lines in [d_lines, proj_lines]
        ]

        mobjects = [
            axes, circle,
            R_line, d_line,
            R_label, d_label,
            proj_lines,
            s_rect_line, c_rect_line,
        ]
        self.add(*mobjects)
        self.axes = axes
        self.circle = circle
        self.R_line = R_line
        self.d_line = d_line
        self.R_label = R_label
        self.d_label = d_label
        self.proj_lines = proj_lines
        self.s_rect_line = s_rect_line
        self.c_rect_line = c_rect_line

    def show_little_triangle(self):
        phi = self.low_phi
        d_phi = abs(self.low_phi - self.top_phi)
        tri_group = self.get_double_triangle_group(phi, d_phi)
        lil_tri, big_tri = tri_group
        frame = self.camera.frame
        frame.save_state()
        scale_factor = 0.1
        sw_sf = 0.2  # stroke_width scale factor
        d_sf = 0.3  # d_label scale factor

        hyp = lil_tri.hyp
        leg = lil_tri.leg2
        leg.rotate(PI)
        VGroup(hyp, leg).set_stroke(YELLOW, 1)
        hyp_word = Text("Rectangle height $\\rightarrow$")
        leg_word = Text("$\\leftarrow$ Projection")
        words = VGroup(hyp_word, leg_word)
        words.set_height(0.4 * lil_tri.get_height())
        words.set_background_stroke(width=0)
        hyp_word.next_to(hyp.get_center(), LEFT, buff=0.05)
        leg_word.next_to(leg, RIGHT, buff=0.02)

        stroke_width_changers = VGroup()
        for mob in self.mobjects:
            if mob in [self.d_label, frame]:
                continue
            mob.generate_target()
            mob.save_state()
            mob.target.set_stroke(
                width=sw_sf * mob.get_stroke_width()
            )
            stroke_width_changers.add(mob)

        self.play(
            frame.animate.scale(scale_factor).move_to(lil_tri),
            self.d_label.animate.scale(d_sf).shift(UP * 0.1),
            *[mob.animate.move_to(mob.target) for mob in stroke_width_changers]
        )
        self.play(Create(lil_tri, stroke_width=0.5))
        self.wait()
        self.play(
            Create(hyp),
            LaggedStartMap(
                Create, hyp_word,
                stroke_width=0.5,
                run_time=1,
            ),
        )
        self.wait()
        self.play(TransformFromCopy(hyp, leg))
        self.play(TransformFromCopy(
            hyp_word, leg_word,
            path_arc=-PI / 2,
        ))
        self.wait()
        self.play(
            frame.animate.restore(),
            self.d_label.animate.scale(1 / d_sf).shift(UP * 0.1),
            *[Restore(mob) for mob in stroke_width_changers],
            run_time=3
        )

        self.hyp_word = hyp_word
        self.leg_word = leg_word
        self.tri_group = tri_group

    def show_tangent_to_radius(self):
        tri_group = self.tri_group
        lil_tri, big_tri = tri_group
        lil_hyp = lil_tri.hyp
        phi = self.low_phi
        circle_point = self.get_circle_point(phi)

        tangent = lil_hyp.copy()
        tangent.set_stroke(WHITE, 2)
        tangent.scale(5 / tangent.get_length())
        tangent.move_to(circle_point)

        R_line = self.R_line
        R_label = self.R_label
        d_label = self.d_label
        elbow = Elbow(angle=(-phi - PI / 2), width=0.15)
        elbow.shift(circle_point)
        elbow.set_stroke(WHITE, 1)
        self.tangent_elbow = elbow

        self.play(GrowFromPoint(tangent, circle_point))
        self.wait()
        self.play(
            Rotate(
                R_line, 90 * DEGREES - phi,
                about_point=ORIGIN,
            ),
            R_label.animate.next_to(0.5 * circle_point, DR, buff=0),
            d_label.animate.shift(SMALL_BUFF * UL),
        )
        self.play(Create(elbow))
        self.wait()
        self.add(big_tri, d_label, R_line, elbow)
        d_label.set_background_stroke(width=0)
        self.play(Create(big_tri))
        self.wait()

        self.tangent = tangent
        self.elbow = elbow

    def tweak_parameter(self):
        tri_group = self.tri_group
        lil_tri = tri_group[0]
        d_label = self.d_label
        d_line = self.d_line
        R_label = self.R_label
        R_line = self.R_line
        frame = self.camera.frame

        to_fade = VGroup(
            self.proj_lines,
            self.s_rect_line, self.c_rect_line,
            self.hyp_word, self.leg_word,
            lil_tri.hyp, lil_tri.leg2,
        )
        rad_tangent = VGroup(
            R_line,
            self.tangent,
            self.elbow,
        )

        phi_tracker = ValueTracker(self.low_phi)

        self.play(
            frame.animate.scale(0.6).shift(UR),
            R_label.animate.scale(0.6).shift(UL * 0.1),
            d_label.animate.scale(0.6).shift(DOWN * SMALL_BUFF),
            *[FadeOut(mob) for mob in to_fade],
        )

        curr_phi = self.low_phi
        d_phi = abs(self.top_phi - self.low_phi)
        alt_phis = [
            80 * DEGREES,
            20 * DEGREES,
            50 * DEGREES,
            curr_phi
        ]
        for new_phi in alt_phis:
            self.add(tri_group, d_label)
            self.play(
                phi_tracker.set_value(new_phi),
                UpdateFromFunc(
                    tri_group,
                    lambda tg: tg.become(
                        self.get_double_triangle_group(
                            phi_tracker.get_value(),
                            d_phi
                        )
                    )
                ),
                Rotate(
                    rad_tangent,
                    -(new_phi - curr_phi),
                    about_point=ORIGIN,
                ),
                MaintainPositionRelativeTo(R_label, R_line),
                UpdateFromFunc(
                    d_line,
                    lambda dl: dl.become(
                        self.get_d_line(phi_tracker.get_value())
                    ),
                ),
                MaintainPositionRelativeTo(d_label, d_line),
                run_time=2
            )
            self.wait()
            curr_phi = new_phi
        for tri in tri_group:
            self.play(Indicate(tri))
        self.wait()
        self.play(*[FadeIn(mob) for mob in to_fade])
        self.remove(phi_tracker)

    def label_angles(self):
        # Getting pretty hacky here...
        tri_group = self.tri_group
        lil_tri, big_tri = tri_group
        d_label = self.d_label
        R_label = self.R_label
        frame = self.camera.frame

        alpha = self.low_phi
        beta = 90 * DEGREES - alpha
        circle_point = self.get_circle_point(alpha)
        alpha_arc = Arc(
            start_angle=90 * DEGREES,
            angle=-alpha,
            radius=0.2,
            stroke_width=2,
        )
        beta_arc = Arc(
            start_angle=PI,
            angle=beta,
            radius=0.2,
            stroke_width=2,
        )
        beta_arc.shift(circle_point)
        alpha_label = MathTex("\\alpha")
        alpha_label.scale(0.5)
        alpha_label.set_color(self.alpha_color)
        alpha_label.next_to(alpha_arc, UP, buff=SMALL_BUFF)
        alpha_label.shift(0.05 * DR)
        beta_label = MathTex("\\beta")
        beta_label.scale(0.5)
        beta_label.set_color(self.beta_color)
        beta_label.next_to(beta_arc, LEFT, buff=SMALL_BUFF)
        beta_label.shift(0.07 * DR)
        VGroup(alpha_label, beta_label).set_background_stroke(width=0)

        elbow = Elbow(width=0.15, angle=-90 * DEGREES)
        elbow.shift(big_tri.get_corner(UL))
        elbow.set_stroke(width=2)

        equation = MathTex(
            "\\alpha", "+", "\\beta", "+",
            "90^\\circ", "=", "180^\\circ"
        )
        equation.scale(0.6)
        equation.next_to(frame.get_corner(UR), DL)

        movers = VGroup(
            alpha_label.copy(), beta_label.copy(),
            elbow.copy()
        )
        indices = [0, 2, 4]
        for mover, index in zip(movers, indices):
            mover.target = VGroup(equation[index])

        # Show equation
        self.play(
            FadeOut(d_label),
            FadeOut(R_label),
            Create(alpha_arc),
            Create(beta_arc),
        )
        self.wait()
        self.play(FadeIn(alpha_label, shift=UP))
        self.wait()
        self.play(FadeIn(beta_label, shift=LEFT))
        self.wait()
        self.play(Create(elbow))
        self.wait()

        self.play(
            LaggedStartMap(MoveToTarget, movers),
            LaggedStartMap(FadeIn, equation[1:4:2], shift=DOWN)
        )
        self.wait()
        self.play(FadeIn(equation[-2:], shift=LEFT))
        self.remove(equation, movers)
        self.add(equation)
        self.wait()

        # Zoom in
        self.remove(self.tangent_elbow)
        stroke_width_changers = VGroup(*[
            mob for mob in self.mobjects
            if mob not in [
                beta_arc, beta_label, frame, equation,
            ]
        ])
        for mob in stroke_width_changers:
            mob.generate_target()
            mob.save_state()
            mob.target.set_stroke(
                width=0.3 * mob.get_stroke_width()
            )
        equation.set_background_stroke(width=0)
        scaled_arcs = VGroup(beta_arc, self.tangent_elbow)
        beta_label.set_background_stroke(color=BLACK, width=0.3)
        self.play(
            VGroup(frame, equation).animate.scale(0.15).shift(
                circle_point + 0.1 * LEFT - frame.get_center()
            ),
            beta_label.animate.scale(0.3).move_to(
                circle_point + (beta_label.get_center() - circle_point) * 0.3
            ),
            scaled_arcs.animate.set_stroke(width=0.3).scale(0.3, about_point=circle_point),
            *[mob.animate.move_to(mob.target) for mob in stroke_width_changers]
        )

        # Show small triangle angles
        words = VGroup(self.hyp_word, self.leg_word)
        alpha_arc1 = Arc(
            start_angle=90 * DEGREES + beta,
            angle=0.95 * alpha,
            radius=0.3 * 0.2,
            stroke_width=beta_arc.get_stroke_width(),
        ).shift(circle_point)
        alpha_arc2 = Arc(
            start_angle=0,
            angle=-0.95 * alpha,
            radius=0.3 * 0.2,
            stroke_width=beta_arc.get_stroke_width(),
        ).shift(lil_tri.hyp.get_end())
        beta_arc1 = Arc(
            start_angle=90 * DEGREES,
            angle=beta,
            radius=0.3 * 0.2,
            stroke_width=beta_arc.get_stroke_width(),
        ).shift(circle_point)
        deg90 = MathTex("90^\\circ")
        deg90.set_height(0.8 * beta_label.get_height())
        deg90.next_to(self.tangent_elbow, DOWN, buff=0.025)
        q_mark = MathTex("?")
        q_mark.set_height(0.5 * beta_label.get_height())
        q_mark.next_to(alpha_arc1, LEFT, buff=0.025)
        q_mark.shift(0.01 * UP)
        alpha_label1 = MathTex("\\alpha")
        alpha_label1.set_height(0.7 * q_mark.get_height())
        alpha_label1.move_to(q_mark)

        alpha_label2 = alpha_label1.copy()
        alpha_label2.next_to(
            alpha_arc2, RIGHT, buff=0.01
        )
        alpha_label2.set_background_stroke(color=BLACK, width=0.3)

        beta_label1 = beta_label.copy()
        beta_label1.scale(0.7)
        beta_label1.set_background_stroke(color=BLACK, width=0.3)
        beta_label1.next_to(
            beta_arc1, UP, buff=0.01
        )
        beta_label1.shift(0.01 * LEFT)

        self.play(FadeOut(words))
        self.play(FadeIn(deg90, shift=0.1 * UP))
        self.wait(0.25)
        self.play(Wiggle(beta_label))
        self.wait(0.25)
        self.play(
            Create(alpha_arc1),
            FadeIn(q_mark, shift=0.1 * RIGHT)
        )
        self.wait()
        self.play(Create(
            self.tangent.copy().scale(0.1).set_stroke(PINK, 0.5)
        ))
        self.wait()
        self.play(ReplacementTransform(q_mark, alpha_label1))
        self.play(CreateThenFadeAround(
            equation,
            surrounding_rectangle_config={
                "buff": 0.015,
                "stroke_width": 0.5,
            },
        ))
        self.wait()
        self.play(
            Create(alpha_arc2),
            FadeIn(alpha_label2),
        )
        self.play(
            Create(beta_arc1),
            FadeIn(beta_label1),
        )
        self.wait()

    #
    def get_double_triangle_group(self, phi, d_phi):
        p0 = self.get_circle_point(phi)
        p1 = self.get_circle_point(phi - d_phi)
        p2 = np.array(p1)
        p2[0] = p0[0]

        little_triangle = Polygon(
            p0, p1, p2,
            stroke_width=0,
            fill_color=self.little_triangle_color,
            fill_opacity=1,
        )
        big_triangle = Polygon(
            p0, ORIGIN, p0 - p0[0] * RIGHT,
            stroke_width=0,
            fill_color=self.big_triangle_color,
            fill_opacity=1
        )
        result = VGroup(little_triangle, big_triangle)
        for tri in result:
            p0, p1, p2 = tri.get_anchors()[:3]
            tri.hyp = Line(p0, p1)
            tri.leg1 = Line(p1, p2)
            tri.leg2 = Line(p2, p0)
            tri.side_lines = VGroup(
                tri.hyp, tri.leg1, tri.leg2
            )
            tri.side_lines.set_stroke(WHITE, 1)
        result.set_stroke(width=0)
        return result

    def get_R_line(self, phi):
        y = self.radius * np.cos(phi)
        x = self.radius
        return Line(ORIGIN, x * RIGHT).shift(y * UP)

    def get_d_line(self, phi):
        end = self.get_circle_point(phi)
        start = np.array(end)
        start[0] = 0
        return Line(start, end)

    def get_circle_point(self, phi):
        return rotate_vector(self.radius * UP, -phi)
