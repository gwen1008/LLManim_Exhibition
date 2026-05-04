# Source: 3b1b/_2019/diffyq/part2/heat_equation.py
# Description: [3b1b translated] 展示一維熱傳導方程中溫度隨時間變化的三維曲面，從初始溫度分佈圖形逐步演變到最終狀態，並包含坐標軸、時間軸和溫度曲面的動態視覺化。


from manim import *
import numpy as np

class TalkThrough1DHeatGraph(Scene):
    def __init__(
        self,
        freq_amplitude_pairs=[
            (1, 0.5),
            (2, 1),
            (3, 0.5),
            (4, 0.3),
            (5, 0.3),
            (7, 0.2),
        ],
        surface_resolution=20,
        graph_slice_step=10 / 20,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.freq_amplitude_pairs = freq_amplitude_pairs
        self.surface_resolution = surface_resolution
        self.graph_slice_step = graph_slice_step
        self.graph_x_min = 0
        self.graph_x_max = 10
        self.step_size = 0.01

    def construct(self):
        self.add_axes()
        self.add_graph()
        self.add_rod()

        self.emphasize_graph()
        self.emphasize_rod()
        self.show_x_axis()
        self.show_changes_over_time()
        self.show_surface()

    def add_axes(self):
        self.axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 20],
            axis_config={"include_numbers": False},
        )
        self.add(self.axes)

    def add_graph(self):
        self.graph = self.plot()
        self.add(self.graph)

    def add_rod(self):
        # 簡化：創建一個代表桿子的矩形
        self.rod = Rectangle(
            width=self.axes.x_axis.x_max - self.axes.x_axis.x_min,
            height=0.2,
            fill_opacity=0.5,
            stroke_width=2,
        )
        self.rod.move_to(self.axes.c2p(5, 0))
        self.add(self.rod)

    def temp_func(self, x, t):
        # 簡化的溫度函數
        result = 0
        for freq, amp in self.freq_amplitude_pairs:
            result += amp * np.exp(-freq**2 * t) * np.sin(freq * x)
        return 50 + 50 * result

    def rod_point_to_color(self, point):
        # 簡化：根據y值返回顏色
        y = point[1]
        if y < 30:
            return BLUE
        elif y < 70:
            return GREEN
        else:
            return RED

    def get_rod(self, x_min, x_max, n_pieces=1):
        # 簡化：創建桿子片段
        rod = Rectangle(
            width=x_max - x_min,
            height=0.2,
            fill_opacity=0.7,
            stroke_width=1,
        )
        rod.move_to(self.axes.c2p((x_min + x_max) / 2, 0))
        return rod

    def color_rod_by_graph(self, rod):
        # 簡化：設置桿子顏色
        rod.set_color_by_gradient(BLUE, RED)

    def emphasize_graph(self):
        graph = self.graph
        q_marks = VGroup(*[
            Text("?").move_to(
                graph.point_from_proportion(a),
                UP,
            ).set_stroke(BLACK, 3, background=True)
            for a in np.linspace(0, 1, 20)
        ])

        self.play(LaggedStart(*[
            Succession(
                FadeInFromLarge(q_mark),
                FadeOut(q_mark, DOWN),
            )
            for q_mark in q_marks
        ]))
        self.wait()

    def emphasize_rod(self):
        alt_rod = self.get_rod(0, 10, 50)
        word = Text("Rod")
        word.scale(2)
        word.next_to(alt_rod, UP, buff=MED_SMALL_BUFF)

        self.play(
            LaggedStart(
                *[
                    Rotate(piece, angle=TAU, rate_func=smooth)
                    for piece in alt_rod
                ],
                run_time=2,
                lag_ratio=0.01,
            ),
            Write(word)
        )
        self.remove(*alt_rod)
        self.wait()

        self.rod_word = word

    def show_x_axis(self):
        rod = self.rod
        axes = self.axes
        graph = self.graph
        x_axis = axes.x_axis
        x_numbers = VGroup(*[
            Integer(i).next_to(x_axis.n2p(i), DOWN)
            for i in range(1, 11)
        ])
        x_axis_label = MathTex("x")
        x_axis_label.next_to(x_axis.get_right(), UP)

        self.play(
            rod.animate.set_opacity(0.5),
            FadeIn(x_axis_label, shift=UL),
            LaggedStartMap(
                FadeIn, x_numbers,
                lambda m: (m, UP),
            )
        )
        self.wait()

        # Show x-values
        triangle = Triangle(
            start_angle=-90 * DEGREES,
            color=GREY_B,
            fill_opacity=1,
        ).scale(0.2)
        x_tracker = ValueTracker(PI)
        get_x = x_tracker.get_value

        def get_x_point():
            return x_axis.n2p(get_x())

        def get_graph_point():
            return graph.point_from_proportion(
                inverse_interpolate(
                    self.graph_x_min,
                    self.graph_x_max,
                    get_x(),
                )
            )

        triangle.add_updater(
            lambda t: t.next_to(get_x_point(), UP)
        )
        x_label = VGroup(
            MathTex("x"),
            MathTex("="),
            DecimalNumber(
                0,
                num_decimal_places=3,
            ).scale(0.9)
        )
        x_label.set_stroke(BLACK, 5, background=True)
        x_label.add_updater(lambda m: m[-1].set_value(get_x()))
        x_label.add_updater(lambda m: m.arrange(RIGHT, buff=SMALL_BUFF))
        x_label.add_updater(lambda m: m[-1].align_to(m[0], DOWN))
        x_label.add_updater(lambda m: m.next_to(triangle, UP, SMALL_BUFF))
        x_label.add_updater(lambda m: m.shift(SMALL_BUFF * RIGHT))
        rod_piece = always_redraw(
            lambda: self.get_rod(
                get_x() - 0.05, get_x() + 0.05,
                n_pieces=1,
            )
        )

        self.play(
            FadeIn(triangle, shift=UP),
            FadeIn(x_label),
            FadeIn(rod_piece),
            FadeOut(self.rod_word),
        )
        for value in [np.exp(2), (np.sqrt(5) + 1) / 2]:
            self.play(x_tracker.animate.set_value(value), run_time=2)
            self.wait()

        # Show graph
        v_line = always_redraw(
            lambda: DashedLine(
                get_x_point(),
                get_graph_point(),
                color=self.rod_point_to_color(get_x_point()),
            )
        )
        graph_dot = Dot()
        graph_dot.add_updater(
            lambda m: m.set_color(
                self.rod_point_to_color(m.get_center())
            )
        )
        graph_dot.add_updater(
            lambda m: m.move_to(get_graph_point())
        )
        t_label = MathTex("T(", "x", ")")
        t_label.set_stroke(BLACK, 3, background=True)
        t_label.add_updater(
            lambda m: m.next_to(graph_dot, UR, buff=0)
        )

        self.add(v_line, rod_piece, x_label, triangle)
        self.play(
            TransformFromCopy(x_label[0], t_label[1]),
            FadeIn(t_label[0::2]),
            Create(v_line),
            GrowFromPoint(graph_dot, get_x_point()),
        )
        self.add(t_label)
        self.wait()
        self.play(
            x_tracker.animate.set_value(TAU),
            run_time=5,
        )

        self.x_tracker = x_tracker
        self.graph_label_group = VGroup(
            v_line, rod_piece, triangle, x_label,
            graph_dot, t_label,
        )
        self.x_numbers = x_numbers
        self.x_axis_label = x_axis_label
        self.t_label = t_label

    def show_changes_over_time(self):
        graph = self.graph
        t_label = self.t_label
        new_t_label = MathTex("T(", "x", ",", "t", ")")
        new_t_label.set_color_by_tex("t", YELLOW)
        
        # 複製更新器
        for updater in t_label.updaters:
            new_t_label.add_updater(updater)

        self.setup_clock()
        clock = self.clock
        time_label = self.time_label
        time_group = self.time_group

        time = 5
        self.play(
            FadeIn(clock),
            FadeIn(time_group),
        )
        
        # 創建時間變化動畫
        old_time = 0
        graph_anim = UpdateFromAlphaFunc(
            graph,
            lambda g, a: g.become(
                self.plot(interpolate(old_time, time, a))
            ),
            run_time=time,
            rate_func=linear
        )
        
        self.play(
            graph_anim,
            ClockPassesTime(clock, run_time=time),
            ChangeDecimalToValue(
                time_label, time,
                rate_func=linear,
            ),
            ReplacementTransform(
                t_label,
                new_t_label,
                rate_func=squish_rate_func(smooth, 0.5, 0.7),
            ),
            run_time=time
        )
        self.play(
            Indicate(new_t_label.get_part_by_tex("t")),
        )
        self.wait()
        self.play(
            FadeOut(clock),
            ChangeDecimalToValue(time_label, 0),
            FadeOut(time_group),
            UpdateFromAlphaFunc(
                graph,
                lambda g, a: g.become(
                    self.plot(interpolate(time, 0, a))
                ),
                run_time=1,
                rate_func=smooth,
            ),
        )

        self.graph_label_group.remove(t_label)
        self.graph_label_group.add(new_t_label)
        self.t_label = new_t_label

    def setup_clock(self):
        # 簡化時鐘設置
        self.clock = Circle(radius=0.5)
        self.time_label = DecimalNumber(0)
        self.time_label.next_to(self.clock, DOWN)
        self.time_group = VGroup(self.clock, self.time_label)

    def show_surface(self):
        axes = self.axes
        graph = self.graph
        t_min = 0
        t_max = 10

        axes_copy = axes.copy()
        self.original_axes = self.axes

        # Set rod final state
        final_graph = self.plot(t_max)
        curr_graph = self.graph
        self.graph = final_graph
        final_rod = self.rod.copy()
        final_rod.set_opacity(1)
        self.color_rod_by_graph(final_rod)
        self.graph = curr_graph

        # Time axis
        t_axis = NumberLine(
            x_range=[t_min, t_max, 1],
            length=10,
            include_numbers=True,
            numbers_with_elongated_ticks=range(1, t_max + 1),
        )
        origin = axes.c2p(0, 0)
        t_axis.shift(origin - t_axis.n2p(0))
        time_label = Text("Time")
        time_label.scale(1.5)
        time_label.next_to(t_axis, UP)
        t_axis.add(time_label)
        t_axis.rotate(90 * DEGREES, axis=UP, about_point=origin)

        # New parts of graph
        step = self.graph_slice_step
        graph_slices = VGroup(*[
            self.plot(time=t).shift(
                t * OUT
            )
            for t in np.arange(0, t_max + step, step)
        ])
        graph_slices.set_stroke(width=1)

        # Input plane (簡化)
        input_plane = Rectangle(
            width=10,
            height=10,
            fill_opacity=0.5,
            fill_color=BLUE_B,
            stroke_width=0.5,
            stroke_color=WHITE,
        )
        input_plane.move_to(axes.c2p(5, 0, 5))

        # Surface (簡化)
        surface = VGroup()
        for t in np.linspace(t_min, t_max, self.surface_resolution):
            slice_graph = self.plot(time=t).shift(t * OUT)
            surface.add(slice_graph)
        surface.set_style(
            fill_opacity=0.1,
            stroke_width=0.5,
            stroke_opacity=0.5,
        )

        # 旋轉到3D視角
        self.set_camera_orientation(phi=80 * DEGREES, theta=-85 * DEGREES)
        
        self.play(
            Write(input_plane),
            Write(t_axis),
            FadeOut(self.graph_label_group),
            self.rod.animate.set_opacity(1),
        )
        
        self.add(graph_slices)
        self.play(
            FadeIn(surface),
            LaggedStart(*[
                TransformFromCopy(graph, graph_slice)
                for graph_slice in graph_slices
            ], lag_ratio=0.02)
        )
        self.wait(4)

        # Show slices
        self.axes = axes_copy
        slicing_plane = Rectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2,
            width=10,
            height=100,
        )
        slicing_plane.move_to(axes_copy.c2p(5, 50, 0))

        def get_time_slice(t):
            new_slice = self.plot(t)
            new_slice.shift(t * OUT)
            return new_slice

        t_tracker = ValueTracker(0)
        graph.add_updater(lambda g: g.become(
            get_time_slice(t_tracker.get_value())
        ))

        final_rod.shift(10 * OUT)
        kw = {"run_time": 10, "rate_func": linear}
        self.rod.save_state()
        self.play(
            t_tracker.animate.set_value(10, **kw),
            Transform(self.rod, final_rod, **kw),
            slicing_plane.animate.shift(10 * OUT, **kw),
        )
        self.wait()

        self.t_axis = t_axis
        self.input_plane = input_plane
        self.surface = surface
        self.graph_slices = graph_slices
        self.slicing_plane = slicing_plane
        self.t_tracker = t_tracker

    def get_graph(self, time=0):
        graph = self.axes.plot(
            lambda x: self.temp_func(x, time),
            x_range=[self.graph_x_min, self.graph_x_max],
        )
        graph.time = time
        # 簡化顏色設置
        graph.set_color_by_gradient(BLUE, RED)
        return graph

    def orient_mobject_for_3d(self, mob):
        mob.rotate(
            90 * DEGREES,
            axis=RIGHT,
            about_point=ORIGIN
        )
        return mob
