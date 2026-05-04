# Source: 3b1b/_2019/diffyq/part2/heat_equation.py
# Description: [3b1b translated] 展示兩根不同溫度的金屬棒接觸後，溫度隨時間擴散達到平衡的熱傳導過程，並用顏色梯度表示溫度變化。


from manim import *
import numpy as np

class BringTwoRodsTogether(Scene):
    def __init__(
        self,
        step_size=0.05,
        axes_config=None,
        y_labels=None,
        graph_x_min=0,
        graph_x_max=10,
        midpoint=5,
        max_temp=90,
        min_temp=10,
        wait_time=30,
        default_n_rod_pieces=20,
        alpha=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.step_size = step_size
        self.axes_config = axes_config or {
            "x_range": [-1, 11],
            "y_range": [-10, 100],
            "y_length": 6.6,  # 110 * 0.06
            "y_axis_config": {
                "tick_frequency": 10,
            },
        }
        self.y_labels = y_labels or list(range(20, 100, 20))
        self.graph_x_min = graph_x_min
        self.graph_x_max = graph_x_max
        self.midpoint = midpoint
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.wait_time = wait_time
        self.default_n_rod_pieces = default_n_rod_pieces
        self.alpha = alpha

    def construct(self):
        self.setup_axes()
        self.setup_graph()
        self.setup_clock()

        self.show_rods()
        self.show_equilibration()

    def setup_axes(self):
        axes = Axes(**self.axes_config)
        axes.center().to_edge(UP)

        y_label = axes.get_y_axis_label("\\text{Temperature}")
        y_label.to_edge(UP)
        axes.y_axis.label = y_label
        axes.y_axis.add(y_label)
        
        # 添加y軸數字標籤
        for y_val in self.y_labels:
            num = DecimalNumber(y_val, num_decimal_places=0)
            num.scale(0.5)
            num.next_to(axes.c2p(0, y_val), LEFT, buff=0.1)
            axes.y_axis.add(num)

        self.axes = axes
        self.y_label = y_label

    def setup_graph(self):
        graph = self.axes.plot(
            self.initial_function,
            x_range=[self.graph_x_min, self.graph_x_max],
            dt=self.step_size,
            discontinuities=[self.midpoint],
        )
        
        # 使用顏色映射代替背景圖片
        colors = color_gradient([BLUE_C, YELLOW, RED], 256)
        graph.set_color_by_gradient(*colors)

        self.graph = graph

    def setup_clock(self):
        clock = Clock()
        clock.set_height(1)
        clock.to_corner(UR)
        clock.shift(MED_LARGE_BUFF * LEFT)

        time_lhs = Text("Time: ")
        time_label = DecimalNumber(
            0, num_decimal_places=2,
        )
        time_rhs = Text("s")
        time_group = VGroup(
            time_lhs,
            time_label,
            # time_rhs
        )
        time_group.arrange(RIGHT, aligned_edge=DOWN)
        time_rhs.shift(SMALL_BUFF * LEFT)
        time_group.next_to(clock, DOWN)

        self.time_group = time_group
        self.time_label = time_label
        self.clock = clock

    def show_rods(self):
        rod1, rod2 = rods = VGroup(
            self.get_rod(0, 5),
            self.get_rod(5, 10),
        )
        rod1.set_color(rod1[0].get_color())
        rod2.set_color(rod2[-1].get_color())

        rods.save_state()
        rods.space_out_submobjects(1.5)
        rods.center()

        labels = VGroup(
            MathTex("90^\\circ"),
            MathTex("10^\\circ"),
        )
        for rod, label in zip(rods, labels):
            label.next_to(rod, DOWN)
            rod.label = label

        self.play(
            FadeIn(rod1, shift=UP),
            Write(rod1.label),
        )
        self.play(
            FadeIn(rod2, shift=DOWN),
            Write(rod2.label)
        )
        self.wait()

        self.rods = rods
        self.rod_labels = labels

    def show_equilibration(self):
        rods = self.rods
        axes = self.axes
        graph = self.graph
        labels = self.rod_labels
        
        self.play(
            Create(axes),
            rods.animate.restore(),
            rods.animate.space_out_submobjects(1.1),
            FadeIn(self.time_group),
            FadeIn(self.clock),
            *[
                MaintainPositionRelativeTo(
                    rod.label, rod
                )
                for rod in rods
            ],
        )

        br1 = Rectangle(height=0.2, width=1)
        br1.set_stroke(width=0)
        br1.set_fill(BLACK, opacity=1)
        br2 = br1.copy()
        
        def update_br1(b):
            b.move_to(axes.c2p(0, 90))
            b.align_to(rods[0].get_right(), LEFT)
        
        def update_br2(b):
            b.move_to(axes.c2p(0, 10))
            b.align_to(rods[1].get_left(), RIGHT)
            
        br1.add_updater(update_br1)
        br2.add_updater(update_br2)

        self.add(graph, br1, br2)
        self.play(
            Create(graph),
            labels[0].animate.align_to(axes.c2p(0, 87), UP),
            labels[1].animate.align_to(axes.c2p(0, 13), DOWN),
        )
        self.wait()
        self.play(
            rods.animate.restore(),
            rate_func=rush_into,
        )
        self.remove(br1, br2)

        graph.add_updater(self.update_graph)
        self.time_label.add_updater(
            lambda d, dt: d.increment_value(dt)
        )
        rods.add_updater(self.update_rods)

        self.play(
            self.get_clock_anim(self.wait_time),
            FadeOut(labels)
        )

    def get_clock_anim(self, time, **kwargs):
        config = {
            "run_time": time,
            "hours_passed": time,
        }
        config.update(kwargs)
        return ClockPassesTime(self.clock, **config)

    def initial_function(self, x):
        epsilon = 1e-10
        if x < self.midpoint - epsilon:
            return self.max_temp
        elif x > self.midpoint + epsilon:
            return self.min_temp
        else:
            return (self.min_temp + self.max_temp) / 2

    def update_graph(self, graph, dt, alpha=None, n_mini_steps=500):
        if alpha is None:
            alpha = self.alpha
        
        # 獲取當前圖形點
        points = graph.get_points()
        if len(points) < 2:
            return graph
            
        # 重新採樣以獲得均勻間隔的點
        x_min = self.graph_x_min
        x_max = self.graph_x_max
        n_points = int((x_max - x_min) / self.step_size) + 1
        xs = np.linspace(x_min, x_max, n_points)
        ys = np.zeros_like(xs)
        
        # 從當前圖形獲取y值
        for i, x in enumerate(xs):
            alpha_val = (x - x_min) / (x_max - x_min)
            point = graph.point_from_proportion(alpha_val)
            ys[i] = self.axes.p2c(point)[1]
        
        points = np.column_stack([xs, ys])
        
        for k in range(n_mini_steps):
            y_change = np.zeros(points.shape[0])
            dx = points[1][0] - points[0][0]
            for i in range(len(points)):
                p = points[i]
                lp = points[max(i - 1, 0)]
                rp = points[min(i + 1, len(points) - 1)]
                d2y = (rp[1] - 2 * p[1] + lp[1])

                if (0 < i < len(points) - 1):
                    second_deriv = d2y / (dx**2)
                else:
                    second_deriv = 2 * d2y / (dx**2)

                y_change[i] = alpha * second_deriv * dt / n_mini_steps

            points[:, 1] += y_change
        
        # 創建新的圖形
        new_graph = self.axes.plot_line_graph(
            xs, points[:, 1],
            line_color=graph.get_color(),
            add_vertex_dots=False
        )
        graph.become(new_graph)
        return graph

    def get_second_derivative(self, x, dx=0.001):
        graph = self.graph
        x_min = self.graph_x_min
        x_max = self.graph_x_max

        ly, y, ry = [
            graph.point_from_proportion(
                inverse_interpolate(x_min, x_max, alt_x)
            )[1]
            for alt_x in (x - dx, x, x + dx)
        ]

        if x == x_max:
            return (ly - y) / dx
        elif x == x_min:
            return (ry - y) / dx
        else:
            d2y = ry - 2 * y + ly
            return d2y / (dx**2)

    def get_rod(self, x_min, x_max, n_pieces=None):
        if n_pieces is None:
            n_pieces = self.default_n_rod_pieces
        axes = self.axes
        line = Line(axes.c2p(x_min, 0), axes.c2p(x_max, 0))
        rod = VGroup(*[
            Square()
            for n in range(n_pieces)
        ])
        rod.arrange(RIGHT, buff=0)
        rod.match_width(line)
        rod.set_height(0.2, stretch=True)
        rod.move_to(axes.c2p(x_min, 0), LEFT)
        rod.set_fill(opacity=1)
        rod.set_stroke(width=1)
        rod.set_sheen_direction(RIGHT)
        self.color_rod_by_graph(rod)
        return rod

    def update_rods(self, rods):
        for rod in rods:
            self.color_rod_by_graph(rod)

    def color_rod_by_graph(self, rod):
        for piece in rod:
            left_color = self.rod_point_to_color(piece.get_left())
            right_color = self.rod_point_to_color(piece.get_right())
            piece.set_color(color=[left_color, right_color])

    def rod_point_to_graph_y(self, point):
        axes = self.axes
        x = axes.x_axis.p2n(point)

        graph = self.graph
        alpha = inverse_interpolate(
            self.graph_x_min,
            self.graph_x_max,
            x,
        )
        return axes.y_axis.p2n(
            graph.point_from_proportion(alpha)
        )

    def y_to_color(self, y):
        y_max = self.max_temp
        y_min = self.min_temp
        alpha = inverse_interpolate(y_min, y_max, y)
        # 使用溫度到顏色的映射
        return interpolate_color(BLUE_C, RED, alpha)

    def rod_point_to_color(self, point):
        return self.y_to_color(
            self.rod_point_to_graph_y(point)
        )
