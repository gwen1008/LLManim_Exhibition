# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示質量比為 16:1 的滑塊碰撞問題在圓形相空間中的幾何分析，包括等弧長分割、角度標記和碰撞次數計數。


from manim import *
import itertools as it

class AnalyzeCircleGeometry(Scene):
    def __init__(
        self,
        mass_ratio=16,
        circle_config={"radius": 3},
        axes_config={"width": config.frame_width, "height": config.frame_height},
        lines_style={"stroke_width": 2},
        **kwargs
    ):
        super().__init__(**kwargs)
        self.mass_ratio = mass_ratio
        self.circle_config = circle_config
        self.axes_config = axes_config
        self.lines_style = lines_style

    def construct(self):
        self.add_mass_ratio_label()
        self.add_circle_with_lines()
        self.show_equal_arc_lengths()
        self.use_arc_lengths_to_count()
        self.focus_on_three_points()
        self.show_likewise_for_all_jumps()
        self.drop_arc_for_each_hop()
        self.try_adding_one_more_arc()
        self.zoom_out()

    def add_mass_ratio_label(self, mass_ratio=None):
        mass_ratio = mass_ratio or self.mass_ratio
        mass_ratio_label = MathTex(
            "\\text{Mass ratio} =", f"{mass_ratio:,} : 1"
        )
        mass_ratio_label.to_corner(UL, buff=MED_SMALL_BUFF)
        self.add(mass_ratio_label)
        self.mass_ratio_label = mass_ratio_label

    def add_circle_with_lines(self):
        circle = self.get_circle()
        axes = self.get_axes()
        axes_labels = self.get_axes_labels(axes)
        slope = -np.sqrt(self.mass_ratio)
        lines = self.get_lines(
            radius=circle.radius,
            slope=slope,
        )
        end_zone = self.get_end_zone()

        end_zone_words = Text("End zone")
        end_zone_words.set_height(0.25)
        end_zone_words.next_to(ORIGIN, UP, SMALL_BUFF)
        end_zone_words.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        end_zone_words.set_color(GREEN)

        self.add(
            axes, axes_labels,
            circle, end_zone, end_zone_words,
        )
        self.play(Create(lines, run_time=3, rate_func=linear))
        self.wait()

        self.circle = circle
        self.axes = axes
        self.lines = lines
        self.end_zone = end_zone
        self.end_zone_words = end_zone_words

    def show_equal_arc_lengths(self):
        circle = self.circle
        radius = circle.radius
        theta = self.theta = np.arctan(1 / np.sqrt(self.mass_ratio))
        n_arcs = int(PI / (2 * theta))

        lower_arcs = VGroup(*[
            Arc(
                start_angle=(PI + n * 2 * theta),
                angle=(2 * theta),
                radius=radius,
                arc_center=circle.get_center()
            )
            for n in range(n_arcs + 1)
        ])
        lower_arcs[0::2].set_color(RED)
        lower_arcs[1::2].set_color(BLUE)

        upper_arcs = lower_arcs.copy()
        upper_arcs.rotate(PI, axis=RIGHT, about_point=ORIGIN)
        upper_arcs[0::2].set_color(BLUE)
        upper_arcs[1::2].set_color(RED)

        all_arcs = VGroup(*it.chain(*zip(lower_arcs, upper_arcs)))
        if int(PI / theta) % 2 == 1:
            all_arcs.remove(all_arcs[-1])

        arc_copies = lower_arcs.copy()
        for arc_copy in arc_copies:
            arc_copy.generate_target()
        for arc in arc_copies:
            arc.target.rotate(-(arc.start_angle - PI + theta))

        equal_signs = VGroup(*[
            MathTex("=") for x in range(len(lower_arcs))
        ])
        equal_signs.scale(0.8)
        for sign in equal_signs:
            sign.generate_target()

        movers = VGroup(*it.chain(*zip(
            arc_copies, equal_signs
        )))
        movers.remove(movers[-1])
        mover_targets = VGroup(*[mover.target for mover in movers])
        mover_targets.arrange(RIGHT, buff=SMALL_BUFF)
        mover_targets.next_to(ORIGIN, DOWN)
        mover_targets.to_edge(LEFT)

        equal_signs.scale(0)
        equal_signs.set_opacity(0)
        equal_signs.move_to(mover_targets)

        all_arcs.save_state()
        for arc in all_arcs:
            arc.rotate(90 * DEGREES)
            arc.set_opacity(0)
            arc.set_stroke(width=20)
        self.play(Restore(
            all_arcs, lag_ratio=0.5,
            run_time=2,
        ))
        self.wait()
        self.play(LaggedStartMap(MoveToTarget, movers))
        self.wait()

        self.arcs_equation = movers
        self.lower_arcs = lower_arcs
        self.upper_arcs = upper_arcs
        self.all_arcs = all_arcs

    def use_arc_lengths_to_count(self):
        all_arcs = self.all_arcs
        lines = self.lines

        arc_counts = VGroup()
        for n, arc in enumerate(all_arcs):
            count_mob = Integer(n + 1)
            count_mob.scale(0.75)
            buff = SMALL_BUFF
            if len(all_arcs) > 100:
                count_mob.scale(0.1)
                count_mob.set_stroke(WHITE, 0.25)
                buff = 0.4 * SMALL_BUFF
            point = arc.point_from_proportion(0.5)
            count_mob.next_to(point, normalize(point), buff)
            arc_counts.add(count_mob)

        self.play(
            FadeOut(lines),
            FadeOut(all_arcs),
            FadeOut(self.arcs_equation),
        )
        self.play(
            ShowIncreasingSubsets(all_arcs),
            ShowIncreasingSubsets(lines),
            ShowIncreasingSubsets(arc_counts),
            run_time=5,
            rate_func=bezier([0, 0, 1, 1])
        )
        self.wait()

        for group in all_arcs, arc_counts:
            targets = VGroup()
            for elem in group:
                elem.generate_target()
                targets.add(elem.target)
            targets.space_out_submobjects(1.2)

        kwargs = {
            "rate_func": there_and_back,
            "run_time": 3,
        }
        self.play(
            LaggedStartMap(MoveToTarget, all_arcs, **kwargs),
            LaggedStartMap(MoveToTarget, arc_counts, **kwargs),
        )

        self.arc_counts = arc_counts

    def focus_on_three_points(self):
        lines = self.lines
        arcs = self.all_arcs
        arc_counts = self.arc_counts
        theta = self.theta

        arc = arcs[4]

        lines.save_state()
        line_pair = lines[3:5]
        lines_to_fade = VGroup(*lines[:3], *lines[5:])

        three_points = [
            line_pair[0].get_start(),
            line_pair[1].get_start(),
            line_pair[1].get_end(),
        ]
        three_dots = VGroup(*[Dot(point) for point in three_points])
        three_dots.set_color(RED)

        theta_arc = Arc(
            radius=1,
            start_angle=-90 * DEGREES,
            angle=theta
        )
        theta_arc.shift(three_points[1])
        theta_label = MathTex("\\theta")
        theta_label.next_to(theta_arc, DOWN, SMALL_BUFF)

        center_lines = VGroup(
            Line(three_points[0], ORIGIN),
            Line(ORIGIN, three_points[2]),
        )
        center_lines.set_style(**self.lines_style)

        two_theta_arc = Arc(
            radius=1,
            start_angle=(center_lines[0].get_angle() + PI),
            angle=2 * theta
        )
        two_theta_label = MathTex("2\\theta")
        arc_center = two_theta_arc.point_from_proportion(0.5)
        two_theta_label.next_to(
            arc_center, normalize(arc_center), SMALL_BUFF
        )
        two_theta_label.shift(SMALL_BUFF * RIGHT)

        to_fade = VGroup(arc_counts, arcs, lines_to_fade)

        self.play(
            LaggedStartMap(
                FadeOut, VGroup(*to_fade)
            )
        )
        lines_to_fade.set_opacity(0)
        self.play(FadeIn(three_dots[0], scale=2))
        self.play(TransformFromCopy(three_dots[0], three_dots[1]))
        self.play(TransformFromCopy(three_dots[1], three_dots[2]))
        self.wait()
        self.play(
            Create(theta_arc),
            FadeIn(theta_label, shift=UP)
        )
        self.wait()
        self.play(
            line_pair.animate.set_stroke(WHITE, 1),
            TransformFromCopy(line_pair, center_lines),
            TransformFromCopy(theta_arc, two_theta_arc),
            TransformFromCopy(theta_label, two_theta_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(two_theta_arc, arc),
            two_theta_label.animate.move_to(2.7 * arc_center),
        )
        self.wait()

        self.three_dots = three_dots
        self.theta_group = VGroup(theta_arc, theta_label)
        self.center_lines_group = VGroup(
            center_lines, two_theta_arc,
        )
        self.two_theta_label = two_theta_label

    def show_likewise_for_all_jumps(self):
        lines = self.lines
        arcs = self.all_arcs

        every_other_line = lines[::2]

        self.play(
            Restore(
                lines,
                lag_ratio=0.5,
                run_time=2
            ),
            FadeOut(self.center_lines_group),
            FadeOut(self.three_dots),
        )
        self.play(LaggedStartMap(
            ApplyFunction, every_other_line,
            lambda line: (
                lambda l: l.scale(10 / l.get_length()).set_stroke(BLUE, 3),
                line
            )
        ))
        self.play(Restore(lines))
        self.wait()

        # Shift theta label
        last_point = lines[3].get_end()
        last_arc = arcs[4]
        two_theta_label = self.two_theta_label
        theta_group_copy = self.theta_group.copy()
        for line, arc in zip(lines[5:10:2], arcs[6:11:2]):
            new_point = line.get_end()
            arc_point = arc.point_from_proportion(0.5)
            self.play(
                theta_group_copy.animate.shift(new_point - last_point),
                two_theta_label.animate.move_to(1.1 * arc_point),
                FadeIn(arc),
                FadeOut(last_arc),
            )
            self.wait()
            last_point = new_point
            last_arc = arc
        self.play(
            FadeOut(theta_group_copy),
            FadeOut(two_theta_label),
            FadeOut(last_arc),
        )
        self.wait()

    def drop_arc_for_each_hop(self):
        lines = self.lines
        arcs = self.all_arcs

        two_theta_labels = VGroup()
        wedges = VGroup()
        for arc in arcs:
            label = MathTex("2\\theta")
            label.scale(0.8)
            label.move_to(1.1 * arc.point_from_proportion(0.5))
            two_theta_labels.add(label)

            wedge = arc.copy()
            wedge.add_line_to(ORIGIN)
            wedge.add_line_to(wedge.get_points()[0])
            wedge.set_stroke(width=0)
            wedge.set_fill(arc.get_color(), 0.2)
            wedges.add(wedge)

        self.remove(lines)
        for line, arc, label, wedge in zip(lines, arcs, two_theta_labels, wedges):
            self.play(
                Create(line),
                FadeIn(arc, shift=normalize(arc.get_center())),
                FadeIn(label, shift=normalize(arc.get_center())),
                FadeIn(wedge),
            )

        self.wedges = wedges
        self.two_theta_labels = two_theta_labels

    def try_adding_one_more_arc(self):
        wedges = self.wedges
        theta = self.theta

        last_wedge = wedges[-1]
        new_wedge = last_wedge.copy()
        new_wedge.set_color(PURPLE)
        new_wedge.set_stroke(WHITE, 1)

        self.play(FadeIn(new_wedge))
        for angle in [-2 * theta, 4 * DEGREES, -2 * DEGREES]:
            self.play(Rotate(new_wedge, angle, about_point=ORIGIN))
            self.wait()
        self.play(
            new_wedge.animate.shift(10 * RIGHT).rotate(-30 * DEGREES),
            rate_func=running_start,
        )
        self.remove(new_wedge)

    def zoom_out(self):
        frame = self.camera.frame
        self.play(
            frame.animate.scale(2, about_point=(TOP + RIGHT_SIDE)),
            run_time=3
        )
        self.wait()

    # Helpers
    def get_axes_labels(self, axes):
        axes_labels = VGroup(
            MathTex("x = ", "\\sqrt{m_1}", "\\cdot", "v_1"),
            MathTex("y = ", "\\sqrt{m_2}", "\\cdot", "v_2"),
        )
        for label in axes_labels:
            label.set_height(0.4)
        axes_labels[0].next_to(ORIGIN, DOWN, SMALL_BUFF)
        axes_labels[0].to_edge(RIGHT, MED_SMALL_BUFF)
        axes_labels[1].next_to(ORIGIN, RIGHT, SMALL_BUFF)
        axes_labels[1].to_edge(UP, SMALL_BUFF)
        return axes_labels

    def get_circle(self):
        return Circle(**self.circle_config)

    def get_axes(self):
        return Axes(
            x_range=[-self.axes_config["width"]/2, self.axes_config["width"]/2, 1],
            y_range=[-self.axes_config["height"]/2, self.axes_config["height"]/2, 1],
            x_length=self.axes_config["width"],
            y_length=self.axes_config["height"],
            axis_config={"stroke_opacity": 0.5}
        )

    def get_lines(self, radius, slope):
        # 簡化實現：創建一組從圓心出發的線段
        lines = VGroup()
        theta = np.arctan(1 / np.sqrt(self.mass_ratio))
        n_lines = int(PI / theta) + 1
        for n in range(n_lines):
            angle = PI + n * 2 * theta
            end_point = radius * np.array([np.cos(angle), np.sin(angle), 0])
            line = Line(ORIGIN, end_point, **self.lines_style)
            lines.add(line)
        return lines

    def get_end_zone(self):
        # 簡化實現：創建一個矩形區域
        return Rectangle(
            width=2, height=1,
            stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.2
        ).to_edge(RIGHT)
