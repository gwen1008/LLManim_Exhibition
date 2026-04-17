# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示標準導數視覺化，包括函數圖形、切線斜率、以及輸入微小變化對輸出的影響。



from manim import *
class StandardDerivativeVisual(Scene):
    def __init__(self, y_max=8, y_axis_height=5, **kwargs):
        super().__init__(**kwargs)
        self.y_max = y_max
        self.y_axis_height = y_axis_height

    def construct(self):
        self.add_title()
        self.show_function_graph()
        self.show_slope_of_graph()
        self.encourage_not_to_think_of_slope_as_definition()
        self.show_sensitivity()

    def add_title(self):
        title = self.title = Text("Standard derivative visual")
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)
        h_line.next_to(title, DOWN)

        self.add(title, h_line)

    def show_function_graph(self):
        # 創建坐標軸
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, self.y_max, 1],
            axis_config={"include_numbers": True},
            y_length=self.y_axis_height,
        )
        self.add(ax)
        
        def func(x):
            x -= 5
            return 0.1 * (x + 3) * (x - 3) * x + 3
        
        graph = ax.plot(func, color=BLUE)
        graph_label = MathTex("f(x)").next_to(
            ax.c2p(9.5, func(9.5)), RIGHT
        )

        input_tracker = ValueTracker(4)

        def get_x_value():
            return input_tracker.get_value()

        def get_y_value():
            return func(get_x_value())

        def get_x_point():
            return ax.c2p(get_x_value(), 0)

        def get_y_point():
            return ax.c2p(0, get_y_value())

        def get_graph_point():
            return ax.c2p(get_x_value(), get_y_value())

        def get_v_line():
            return DashedLine(get_x_point(), get_graph_point(), stroke_width=2)

        def get_h_line():
            return DashedLine(get_graph_point(), get_y_point(), stroke_width=2)

        input_triangle = Triangle(start_angle=PI/2)
        output_triangle = Triangle(start_angle=0)
        for triangle in [input_triangle, output_triangle]:
            triangle.set_fill(WHITE, 1)
            triangle.set_stroke(width=0)
            triangle.scale(0.1)

        input_triangle.add_updater(
            lambda m: m.move_to(get_x_point(), UP)
        )
        output_triangle.add_updater(
            lambda m: m.move_to(get_y_point(), RIGHT)
        )

        x_label = MathTex("x")
        x_label.add_updater(
            lambda m: m.next_to(input_triangle, DOWN, SMALL_BUFF)
        )

        output_label = MathTex("f(x)")
        output_label.add_updater(
            lambda m: m.next_to(output_triangle, LEFT, SMALL_BUFF)
        )

        v_line = get_v_line()
        v_line.add_updater(
            lambda vl: vl.become(get_v_line())
        )

        h_line = get_h_line()
        h_line.add_updater(
            lambda hl: hl.become(get_h_line())
        )

        graph_dot = Dot(color=YELLOW)
        graph_dot.add_updater(
            lambda m: m.move_to(get_graph_point())
        )

        self.play(
            Create(graph),
            Write(graph_label),
        )
        self.play(
            DrawBorderThenFill(input_triangle, run_time=1),
            Write(x_label),
            Create(v_line),
            GrowFromCenter(graph_dot),
        )
        self.add_foreground_mobjects(graph_dot)
        self.play(
            Create(h_line),
            Write(output_label),
            DrawBorderThenFill(output_triangle, run_time=1)
        )
        self.add(
            input_triangle,
            x_label,
            graph_dot,
            v_line,
            h_line,
            output_triangle,
            output_label,
        )
        self.play(
            input_tracker.animate.set_value(8),
            run_time=6,
            rate_func=there_and_back
        )

        self.input_tracker = input_tracker
        self.graph = graph
        self.ax = ax

    def show_slope_of_graph(self):
        input_tracker = self.input_tracker
        deriv_input_tracker = ValueTracker(input_tracker.get_value())

        # Slope line
        def get_slope_line():
            x = deriv_input_tracker.get_value()
            dx = 0.01
            point = self.ax.c2p(x, self.graph.underlying_function(x))
            secant_line = Line(
                point - 2 * RIGHT,
                point + 2 * RIGHT,
                color=GREEN
            )
            # 計算斜率
            slope = (self.graph.underlying_function(x + dx) - self.graph.underlying_function(x)) / dx
            secant_line.rotate(np.arctan(slope / self.ax.x_axis.unit_size))
            secant_line.move_to(point)
            secant_line.slope = slope
            return secant_line

        slope_line = get_slope_line()
        slope_line.add_updater(
            lambda sg: sg.become(get_slope_line())
        )

        def position_deriv_label(deriv_label):
            deriv_label.next_to(slope_line, UP)
            return deriv_label
        
        deriv_label = MathTex(
            "\\frac{df}{dx}(x) =", "\\text{Slope}", "="
        )
        deriv_label[1].set_color(GREEN)
        deriv_label.add_updater(position_deriv_label)

        slope_decimal = DecimalNumber(slope_line.slope, color=GREEN)
        slope_decimal.add_updater(
            lambda d: d.set_value(slope_line.slope)
        )
        slope_decimal.add_updater(
            lambda d: d.next_to(
                deriv_label, RIGHT, SMALL_BUFF
            ).shift(0.2 * SMALL_BUFF * DOWN)
        )

        self.play(
            Create(slope_line),
            Write(deriv_label),
            Write(slope_decimal),
            run_time=1
        )
        self.wait()
        self.add(
            slope_line,
            deriv_label,
        )
        for x in [9, 2, 4]:
            self.play(
                input_tracker.animate.set_value(x),
                deriv_input_tracker.animate.set_value(x),
                run_time=3
            )
            self.wait()

        self.deriv_input_tracker = deriv_input_tracker

    def encourage_not_to_think_of_slope_as_definition(self):
        # 簡化版本：用文字代替角色
        text = Text("Don't think of this\nas the definition", font_size=24)
        text.to_corner(DR)
        
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))

    def show_sensitivity(self):
        input_tracker = self.input_tracker
        deriv_input_tracker = self.deriv_input_tracker

        self.wiggle_input()
        for x in [9, 7, 2]:
            self.play(
                input_tracker.animate.set_value(x),
                deriv_input_tracker.animate.set_value(x),
                run_time=3
            )
            self.wiggle_input()

    def wiggle_input(self, dx=0.5, run_time=3):
        input_tracker = self.input_tracker

        x = input_tracker.get_value()
        x_min = x - dx
        x_max = x + dx
        y = self.graph.underlying_function(x)
        y_min = self.graph.underlying_function(x_min)
        y_max = self.graph.underlying_function(x_max)
        
        x_line = Line(
            self.ax.c2p(x_min, 0),
            self.ax.c2p(x_max, 0),
        )
        y_line = Line(
            self.ax.c2p(0, y_min),
            self.ax.c2p(0, y_max),
        )

        x_rect, y_rect = rects = VGroup(Rectangle(), Rectangle())
        rects.set_stroke(width=0)
        rects.set_fill(YELLOW, 0.5)
        x_rect.match_width(x_line)
        x_rect.stretch_to_fit_height(0.25)
        x_rect.move_to(x_line)
        y_rect.match_height(y_line)
        y_rect.stretch_to_fit_width(0.25)
        y_rect.move_to(y_line)

        self.play(
            input_tracker.animate.set_value(x + dx),
            FadeIn(
                rects,
                rate_func=lambda t: squish_rate_func(smooth, 0, 0.33)(t),
            ),
            run_time=run_time,
        )
        self.play(FadeOut(rects))
        self.play(input_tracker.animate.set_value(x))
