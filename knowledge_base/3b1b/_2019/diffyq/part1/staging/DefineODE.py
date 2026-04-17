# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示單擺運動的微分方程定義，包括圖形、斜率、曲率等概念，並說明常微分方程（ODE）的含義與高階例子。


from manim import *
import itertools as it

class DefineODE(Scene):
    def __init__(
        self,
        pendulum_config=None,
        axes_config=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        if pendulum_config is None:
            pendulum_config = {
                "length": 2,
                "top_point": 5 * RIGHT + 2 * UP,
                "initial_theta": 150 * DEGREES,
                "mu": 0.3,
            }
        if axes_config is None:
            axes_config = {
                "y_axis_config": {"unit_size": 0.75},
                "y_max": PI,
                "y_min": -PI,
                "x_max": 10,
                "x_axis_config": {
                    "numbers_to_show": range(2, 10, 2),
                    "unit_size": 1,
                }
            }
        self.pendulum_config = pendulum_config
        self.axes_config = axes_config

    def construct(self):
        self.add_graph()
        self.write_differential_equation()
        self.dont_know_the_value()
        self.show_value_slope_curvature()
        self.write_ode()
        self.show_second_order()
        self.show_higher_order_examples()
        self.show_changing_curvature_group()

    def add_graph(self):
        # 注意：Pendulum 和 ThetaVsTAxes 是自定義類，需自行實現或替換
        pendulum = Pendulum(**self.pendulum_config)
        axes = ThetaVsTAxes(**self.axes_config)

        axes.center()
        axes.to_corner(DL)
        graph = axes.get_live_drawn_graph(pendulum)

        pendulum.start_swinging()
        self.add(axes, pendulum, graph)

        self.pendulum = pendulum
        self.axes = axes
        self.graph = graph

    def write_differential_equation(self):
        de_word = Text("Differential", "Equation")
        de_word.to_edge(UP, buff=MED_SMALL_BUFF)

        equation = get_ode()  # 假設此函數返回一個 MathTex
        equation.next_to(de_word, DOWN)
        thetas = equation.get_parts_by_tex("\\theta")

        lines = VGroup(*[
            Line(v, 1.2 * v)
            for v in [UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL]
        ] * 3)  # 簡化 compass_directions(25)
        lines.replace(equation, stretch=True)
        lines.scale(1.5)
        lines.set_stroke(YELLOW)
        # lines.shuffle()  # ManimCE 無 shuffle，改用隨機排序
        lines = VGroup(*np.random.permutation(lines))

        self.add(equation)
        self.wait(5)
        # ShowPassingFlashWithThinningStrokeWidth 無對應，用 ShowPassingFlash 替代
        self.play(
            ShowPassingFlash(
                lines,
                lag_ratio=0.002,
                run_time=1.5,
                time_width=0.9,
            )
        )
        self.play(FadeIn(de_word, shift=DOWN))
        self.wait(2)
        self.play(
            LaggedStart(*[
                ApplyMethod(theta.shift, 0.25 * DOWN)
                for theta in thetas
            ], lag_ratio=0.1),
            rate_func=there_and_back,
        )
        self.wait()

        self.de_word = de_word
        self.equation = equation

    def dont_know_the_value(self):
        graph = self.graph
        pendulum = self.pendulum

        q_marks = VGroup(*[
            MathTex("?").move_to(
                graph.point_from_proportion(a)
            )
            for a in np.linspace(0, 1, 20)
        ])
        q_marks.set_stroke(width=0, background=True)
        self.play(
            VFadeOut(graph),
            FadeOut(pendulum),
            LaggedStart(*[
                UpdateFromAlphaFunc(
                    q_mark,
                    lambda m, a: m.set_height(
                        0.5 * (1 + a)
                    ).set_opacity(there_and_back(a))
                )
                for q_mark in q_marks
            ], lag_ratio=0.01, run_time=2)
        )
        self.remove(q_marks)

    def show_value_slope_curvature(self):
        axes = self.axes
        p = self.pendulum
        graph = axes.plot(
            lambda t: p.initial_theta * np.cos(
                np.sqrt(p.gravity / p.length) * t
            ) * np.exp(-p.mu * t / 2)
        )

        tex_config = {
            "tex_to_color_map": {
                "{\\theta}": BLUE,
                "{\\dot\\theta}": RED,
                "{\\ddot\\theta}": YELLOW,
            },
            "font_size": 36,
        }
        theta, d_theta, dd_theta = [
            MathTex(
                "{" + s + "\\theta}(t)",
                **tex_config
            )
            for s in ("", "\\dot", "\\ddot")
        ]

        t_tracker = ValueTracker(2.5)
        get_t = t_tracker.get_value

        def get_point(t):
            return graph.point_from_proportion(t / axes.x_max)

        def get_dot():
            return Dot(get_point(get_t())).scale(0.5)

        def get_v_line():
            point = get_point(get_t())
            x_point = axes.x_axis.number_to_point(
                axes.x_axis.point_to_number(point)
            )
            return DashedLine(
                x_point, point,
                dash_length=0.025,
                stroke_color=BLUE,
                stroke_width=2,
            )

        def get_tangent_line(curve, alpha):
            line = Line(
                ORIGIN, 1.5 * RIGHT,
                color=RED,
                stroke_width=1.5,
            )
            da = 0.0001
            p0 = curve.point_from_proportion(alpha)
            p1 = curve.point_from_proportion(alpha - da)
            p2 = curve.point_from_proportion(alpha + da)
            angle = angle_of_vector(p2 - p1)
            line.rotate(angle)
            line.move_to(p0)
            return line

        def get_slope_line():
            return get_tangent_line(
                graph, get_t() / axes.x_max
            )

        def get_curve():
            curve = VMobject()
            t = get_t()
            curve.set_points_as_corners([
                get_point(t + a)
                for a in np.linspace(-0.5, 0.5, 11)
            ])
            curve.set_stroke(YELLOW, 1)
            return curve

        v_line = always_redraw(get_v_line)
        dot = always_redraw(get_dot)
        slope_line = always_redraw(get_slope_line)
        curve = always_redraw(get_curve)

        theta.next_to(v_line, RIGHT, SMALL_BUFF)
        d_theta.next_to(slope_line.get_end(), UP, SMALL_BUFF)
        dd_theta.next_to(curve.get_end(), RIGHT, SMALL_BUFF)
        thetas = VGroup(theta, d_theta, dd_theta)

        words = VGroup(
            Text("= Height").set_color(BLUE),
            Text("= Slope").set_color(RED),
            Text("= ``Curvature''").set_color(YELLOW),
        )
        words.scale(0.75)
        for word, sym in zip(words, thetas):
            word.next_to(sym, RIGHT, buff=2 * SMALL_BUFF)
            sym.word = word

        self.play(
            Create(v_line),
            FadeIn(dot, shift=v_line.get_start()),
            FadeIn(theta, shift=DOWN),
            FadeIn(theta.word, shift=DOWN),
        )
        self.add(slope_line, dot)
        self.play(
            Create(slope_line),
            FadeIn(d_theta, shift=LEFT),
            FadeIn(d_theta.word, shift=LEFT),
        )

        a_tracker = ValueTracker(0)
        curve_copy = curve.copy()
        changing_slope = always_redraw(
            lambda: get_tangent_line(
                curve_copy,
                a_tracker.get_value(),
            ).set_stroke(
                opacity=there_and_back(a_tracker.get_value())
            )
        )
        self.add(curve, dot)
        self.play(
            Create(curve),
            FadeIn(dd_theta, shift=LEFT),
            FadeIn(dd_theta.word, shift=LEFT),
        )
        self.add(changing_slope)
        self.play(
            a_tracker.animate.set_value(1),
            run_time=3,
        )
        self.remove(changing_slope, a_tracker)

        self.t_tracker = t_tracker
        self.curvature_group = VGroup(
            v_line, slope_line, curve, dot
        )
        self.curvature_group_labels = VGroup(thetas, words)
        self.fake_graph = graph

    def write_ode(self):
        equation = self.equation
        axes = self.axes
        de_word = self.de_word

        ts = equation.get_parts_by_tex("{t}")
        t_rects = VGroup(*[SurroundingRectangle(t) for t in ts])
        x_axis = axes.x_axis
        x_axis_line = Line(
            x_axis.get_start(), x_axis.get_end(),
            stroke_color=YELLOW,
            stroke_width=5,
        )

        ordinary = Text("Ordinary")
        de_word.generate_target()
        group = VGroup(ordinary, de_word.target)
        group.arrange(RIGHT)
        group.to_edge(UP)
        ordinary_underline = Line(LEFT, RIGHT)
        ordinary_underline.replace(ordinary, dim_to_match=0)
        ordinary_underline.next_to(ordinary, DOWN, SMALL_BUFF)
        ordinary_underline.set_color(YELLOW)

        self.play(
            Create(t_rects),
            FadeOut(t_rects, lag_ratio=0.8),
            Create(x_axis_line),
            FadeOut(x_axis_line)
        )
        self.play(
            MoveToTarget(de_word),
            FadeIn(ordinary, shift=RIGHT),
            GrowFromCenter(ordinary_underline)
        )
        self.play(FadeOut(ordinary_underline))
        self.wait()

        self.remove(ordinary, de_word)
        ode_word = self.ode_word = VGroup(*ordinary, *de_word)
        ode_initials = VGroup(*[word[0] for word in ode_word])
        ode_initials.generate_target()
        ode_initials.target.scale(1.2)
        ode_initials.target.set_color(PINK)
        ode_initials.target.arrange(
            RIGHT, buff=0.5 * SMALL_BUFF, aligned_edge=DOWN
        )
        ode_initials.target.to_edge(UP, buff=MED_SMALL_BUFF)

        ode_remaining_letters = VGroup(*it.chain(*[
            word[1:] for word in ode_word
        ]))
        ode_remaining_letters.generate_target()
        for mob in ode_remaining_letters.target:
            mob.shift(0.2 * UP)
            mob.set_opacity(0)

        self.play(
            MoveToTarget(ode_initials),
            MoveToTarget(ode_remaining_letters, lag_ratio=0.05),
        )
        self.wait()

        self.ode_initials = ode_initials

    def show_second_order(self):
        so = Text("Second order")
        so.scale(1.4)
        ode = self.ode_initials
        ode.generate_target()
        group = VGroup(so, ode.target)
        group.arrange(RIGHT, aligned_edge=DOWN)
        group.to_edge(UP, buff=MED_SMALL_BUFF)

        second_deriv = self.equation[:5]

        self.play(
            Write(so),
            MoveToTarget(ode),
        )
        self.wait()
        self.play(Indicate(second_deriv))
        self.play(
            Indicate(second_deriv, color=YELLOW),
        )
        self.wait()

        self.second_order_word = so

    def show_higher_order_examples(self):
        main_example = self.get_main_example()
        tex_config = {"tex_to_color_map": {"{x}": BLUE}}
        example3 = VGroup(
            Text("Third order ODE"),
            MathTex(
                "\\dddot {x}(t) + \\dot {x}(t)^2 = 0",
                **tex_config,
            )
        )
        example4 = VGroup(
            Text("Fourth order ODE"),
            MathTex(
                "\\ddddot {x}(t) +",
                "a\\dddot {x}(t) \\dot {x}(t) + ",
                "b \\ddot {x}(t) {x}(t)",
                "= 1",
                **tex_config,
            )
        )
        for example in [example3, example4]:
            example[0].scale(1.2)
            example.arrange(DOWN, buff=MED_LARGE_BUFF)
            example.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(
            FadeOut(main_example),
            FadeIn(example3),
        )
        self.wait(2)
        self.play(
            FadeOut(example3),
            FadeIn(example4),
        )
        self.wait(2)
        self.play(
            FadeOut(example4),
            FadeIn(main_example),
        )
        self.wait(2)

    def get_main_example(self):
        return VGroup(
            self.second_order_word,
            self.ode_initials,
            self.equation
        )

    def show_changing_curvature_group(self):
        t_tracker = self.t_tracker
        curvature_group = self.curvature_group
        labels = self.curvature_group_labels
        graph = VMobject()
        # pointwise_become_partial 無對應，用 set_points 替代
        graph.set_points(
            self.fake_graph.points[
                int(
                    len(self.fake_graph.points)
                    * t_tracker.get_value()
                    / self.axes.x_max
                ):
            ]
        )
        dashed_graph = DashedVMobject(graph, num_dashes=100)
        dashed_graph.set_stroke(GREEN, 1)

        self.play(FadeOut(labels))
        self.add(dashed_graph, curvature_group)
        self.play(
            t_tracker.animate.set_value(10),
            Create(dashed_graph),
            run_time=15,
            rate_func=linear,
        )
        self.wait()
