# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示圓周角定理，在圓上移動三個點並動態顯示圓周角與圓心角的關係。



from manim import *
class InscribedAngleTheorem(Scene):
    def construct(self):
        self.add_title()
        self.show_circle()
        self.let_point_vary()

    def add_title(self):
        title = Text("Inscribed angle theorem")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)
        self.title = title

    def show_circle(self):
        # Boy is this over engineered...
        circle = self.circle = Circle(
            color=BLUE,
            radius=2,
        )
        center_dot = Dot(circle.get_center(), color=WHITE)
        self.add(circle, center_dot)

        angle_trackers = self.angle_trackers = VGroup(
            ValueTracker(TAU / 4),
            ValueTracker(PI),
            ValueTracker(-TAU / 4),
        )

        def get_point(angle):
            return circle.point_from_proportion(
                (angle % TAU) / TAU
            )

        def get_dot(angle):
            dot = Dot(get_point(angle))
            dot.set_color(RED)
            dot.set_stroke(BLACK, 3, background=True)
            return dot

        def get_dots():
            return VGroup(*[
                get_dot(at.get_value())
                for at in angle_trackers
            ])

        def update_labels(labels):
            center = circle.get_center()
            for dot, label in zip(dots, labels):
                label.move_to(
                    center + 1.2 * (dot.get_center() - center)
                )

        def get_lines():
            lines = VGroup(*[
                Line(d1.get_center(), d2.get_center())
                for d1, d2 in zip(dots, dots[1:])
            ])
            lines.set_stroke(WHITE, 3)
            return lines

        def get_center_lines():
            points = [
                dots[0].get_center(),
                circle.get_center(),
                dots[2].get_center(),
            ]
            lines = VGroup(*[
                Line(p1, p2)
                for p1, p2 in zip(points, points[1:])
            ])
            lines.set_stroke(GREY_B, 3)
            return lines

        def get_angle_label(lines, tex, reduce_angle=True):
            a1 = (lines[0].get_angle() + PI) % TAU
            a2 = lines[1].get_angle()
            diff = (a2 - a1)
            if reduce_angle:
                diff = ((diff + PI) % TAU) - PI
            point = lines[0].get_end()
            arc = Arc(
                start_angle=a1,
                angle=diff,
                radius=0.5,
            )
            arc.shift(point)
            arc_center = arc.point_from_proportion(0.5)
            label = MathTex(tex)
            vect = (arc_center - point)
            vect = (0.3 + get_norm(vect)) * normalize(vect)
            label.move_to(point + vect)
            return VGroup(arc, label)

        def get_theta_label():
            return get_angle_label(lines, "\\theta")

        def get_2theta_label():
            return get_angle_label(center_lines, "2\\theta", False)

        dots = get_dots()
        lines = get_lines()
        center_lines = get_center_lines()
        labels = VGroup(*[
            MathTex("P_{}".format(n + 1))
            for n in range(3)
        ])
        update_labels(labels)
        theta_label = get_theta_label()
        two_theta_label = get_2theta_label()

        self.play(
            FadeIn(labels[0], shift=DOWN),
            FadeIn(dots[0], scale=2),
        )
        self.play(
            TransformFromCopy(labels[0], labels[1]),
            TransformFromCopy(dots[0], dots[1]),
            Create(lines[0]),
        )
        self.play(
            Create(lines[1]),
            TransformFromCopy(labels[1], labels[2]),
            TransformFromCopy(dots[1], dots[2]),
            Write(theta_label),
        )
        self.wait()

        # Add updaters
        labels.add_updater(update_labels)
        dots.add_updater(lambda m: m.become(get_dots()))
        lines.add_updater(lambda m: m.become(get_lines()))
        center_lines.add_updater(lambda m: m.become(get_center_lines()))
        theta_label.add_updater(lambda m: m.become(get_theta_label()))
        two_theta_label.add_updater(lambda m: m.become(get_2theta_label()))

        self.add(labels, lines, dots, theta_label)
        # Further animations
        self.play(
            angle_trackers[0].animate.set_value(TAU / 8),
        )
        self.play(
            angle_trackers[2].animate.set_value(-TAU / 8),
        )
        self.wait()
        center_lines.update()
        two_theta_label.update()
        self.play(
            TransformFromCopy(lines.copy().clear_updaters(), center_lines),
            TransformFromCopy(theta_label.copy().clear_updaters(), two_theta_label),
        )
        self.wait()

        self.add(center_lines, two_theta_label)

    def let_point_vary(self):
        p1_tracker, p2_tracker, p3_tracker = self.angle_trackers

        kwargs = {"run_time": 2}
        for angle in [TAU / 4, 3 * TAU / 4]:
            self.play(
                p2_tracker.animate.set_value(angle),
                **kwargs
            )
            self.wait()
        self.play(
            p1_tracker.animate.set_value(PI),
            **kwargs
        )
        self.wait()
        self.play(
            p3_tracker.animate.set_value(TAU / 3),
            **kwargs
        )
        self.wait()
        self.play(
            p2_tracker.animate.set_value(7 * TAU / 8),
            **kwargs
        )
        self.wait()
