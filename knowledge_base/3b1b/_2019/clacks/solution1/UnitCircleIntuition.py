# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示單位圓上角度與正切函數的關係，透過高度與寬度的比例來近似正切值。



from manim import *
class UnitCircleIntuition(Scene):
    def construct(self):
        self.draw_unit_circle()
        self.show_angle()
        self.show_fraction()
        self.show_fraction_approximation()

    def draw_unit_circle(self):
        unit_size = 2.5
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=5 * unit_size,
            y_length=3 * unit_size,
            axis_config={"stroke_width": 1},
        )
        self.add(axes)

        radius_line = Line(ORIGIN, axes.c2p(1, 0))
        radius_line.set_color(BLUE)
        r_label = MathTex("1")
        r_label.add_updater(
            lambda m: m.next_to(radius_line.get_center(), DOWN, SMALL_BUFF)
        )
        circle = Circle(radius=unit_size, color=WHITE)

        self.add(radius_line, r_label)
        self.play(
            Rotating(radius_line, about_point=ORIGIN),
            Create(circle),
            run_time=2,
            rate_func=smooth,
        )

        self.radius_line = radius_line
        self.r_label = r_label
        self.circle = circle
        self.axes = axes

    def show_angle(self):
        circle = self.circle

        tan_eq = MathTex(
            "\\tan", "(", "\\theta", ")", "=",
            tex_to_color_map={"\\theta": RED},
        )
        tan_eq.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        tan_eq.to_edge(UP, buff=LARGE_BUFF)

        theta_tracker = ValueTracker(0)
        get_theta = theta_tracker.get_value

        def get_r_line():
            return Line(
                circle.get_center(),
                circle.point_at_angle(get_theta())
            )
        r_line = always_redraw(get_r_line)

        def get_arc(radius=None, **kwargs):
            if radius is None:
                alpha = inverse_interpolate(0, 20 * DEGREES, get_theta())
                radius = interpolate(2, 1, alpha)
            return Arc(
                radius=radius,
                start_angle=0,
                angle=get_theta(),
                arc_center=circle.get_center(),
                **kwargs
            )
        arc = always_redraw(get_arc)
        self.circle_arc = always_redraw(
            lambda: get_arc(radius=circle.radius, color=RED)
        )

        def get_theta_label():
            label = MathTex("\\theta")
            label.set_height(min(arc.get_height(), 0.3))
            label.set_color(RED)
            center = circle.get_center()
            vect = arc.point_from_proportion(0.5) - center
            vect = (get_norm(vect) + 2 * SMALL_BUFF) * normalize(vect)
            label.move_to(center + vect)
            return label
        theta_label = always_redraw(get_theta_label)

        def get_height_line():
            p2 = circle.point_at_angle(get_theta())
            p1 = np.array(p2)
            p1[1] = circle.get_center()[1]
            return Line(
                p1, p2,
                stroke_color=YELLOW,
                stroke_width=3,
            )
        self.height_line = always_redraw(get_height_line)

        def get_width_line():
            p2 = circle.get_center()
            p1 = circle.point_at_angle(get_theta())
            p1[1] = p2[1]
            return Line(
                p1, p2,
                stroke_color=PINK,
                stroke_width=3,
            )
        self.width_line = always_redraw(get_width_line)

        def get_h_label():
            label = MathTex("h")
            height_line = self.height_line
            label.set_color(height_line.get_color())
            label.set_height(min(height_line.get_height(), 0.3))
            label.set_stroke(BLACK, 3, background=True)
            label.next_to(height_line, RIGHT, SMALL_BUFF)
            return label
        self.h_label = always_redraw(get_h_label)

        def get_w_label():
            label = MathTex("w")
            width_line = self.width_line
            label.set_color(width_line.get_color())
            label.next_to(width_line, DOWN, SMALL_BUFF)
            return label
        self.w_label = always_redraw(get_w_label)

        self.add(r_line, theta_label, arc, self.radius_line)
        self.play(
            FadeIn(tan_eq, shift=DOWN),
            theta_tracker.set_value, 20 * DEGREES,
        )
        self.wait()

        self.tan_eq = tan_eq
        self.theta_tracker = theta_tracker

    def show_fraction(self):
        height_line = self.height_line
        width_line = self.width_line
        h_label = self.h_label
        w_label = self.w_label
        tan_eq = self.tan_eq

        rhs = MathTex(
            "{\\text{height}", "\\over", "\\text{width}}"
        )
        rhs.next_to(tan_eq, RIGHT)
        rhs.get_part_by_tex("height").set_color(height_line.get_color())
        rhs.get_part_by_tex("width").set_color(width_line.get_color())

        for mob in [height_line, width_line, h_label, w_label]:
            mob.update()

        self.play(
            Create(height_line.copy().clear_updaters(), remover=True),
            FadeIn(h_label.copy().clear_updaters(), shift=RIGHT, remover=True),
            Write(rhs[:2])
        )
        self.add(height_line, h_label)
        self.play(
            Create(width_line.copy().clear_updaters(), remover=True),
            FadeIn(w_label.copy().clear_updaters(), shift=UP, remover=True),
            self.r_label.animate.set_opacity(0),
            Write(rhs[2])
        )
        self.add(width_line, w_label)
        self.wait()

        self.rhs = rhs

    def show_fraction_approximation(self):
        theta_tracker = self.theta_tracker
        approx_rhs = MathTex(
            "\\approx", "{\\theta", "\\over", "1}",
        )
        height, over1, width = self.rhs
        approx, theta, over2, one = approx_rhs
        approx_rhs.set_color_by_tex("\\theta", RED)
        approx_rhs.next_to(self.rhs, RIGHT, MED_SMALL_BUFF)

        self.play(theta_tracker.set_value, 5 * DEGREES)
        self.play(Write(VGroup(approx, over2)))
        self.wait()
        self.play(Indicate(width))
        self.play(TransformFromCopy(width, one))
        self.wait()
        self.play(Indicate(height))
        self.play(TransformFromCopy(height, theta))
        self.wait()
