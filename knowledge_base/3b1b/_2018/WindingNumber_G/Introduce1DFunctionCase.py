# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一維函數圖形，從兩個多項式與三角函數的交點問題過渡到求解平方根 2 的二分搜尋過程。


from manim import *
import numpy as np

class Introduce1DFunctionCase(Scene):
    def __init__(
        self,
        search_range_rect_height=0.15,
        arrow_opacity=1,
        show_dotted_line_to_f=True,
        arrow_config=None,
        show_midpoint_value=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        if arrow_config is None:
            arrow_config = {"max_tip_length_to_length_ratio": 0.5}
        self.search_range_rect_height = search_range_rect_height
        self.arrow_opacity = arrow_opacity
        self.show_dotted_line_to_f = show_dotted_line_to_f
        self.arrow_config = arrow_config
        self.show_midpoint_value = show_midpoint_value

    def construct(self):
        self.show_axes_one_at_a_time()
        self.show_two_graphs()
        self.transition_to_sqrt_2_case()
        self.show_example_binary_search()

    def show_axes_one_at_a_time(self):
        axes = Axes(
            x_range=[-1, 3.2, 0.25],
            y_range=[-2, 4.5, 1],
            x_length=3 * (3.2 - (-1)),
            y_length=4.5 - (-2),
            axis_config={
                "include_numbers": True,
                "numbers_to_exclude": [],
            },
        )
        axes.to_corner(DL)
        axes.x_axis.add_numbers(*list(range(-1, 4)))
        axes.y_axis.numbers.set_direction(LEFT)
        axes.y_axis.add_numbers(-1, *list(range(1, 5)))

        inputs = Text("Inputs")
        inputs.next_to(axes.x_axis, UP, aligned_edge=RIGHT)

        outputs = Text("Outputs")
        outputs.next_to(axes.y_axis, UP, buff=SMALL_BUFF)

        self.play(
            Create(axes.x_axis),
            Write(inputs)
        )
        self.wait()
        self.play(
            Create(axes.y_axis),
            FadeOut(axes.x_axis.numbers[1], rate_func=squish_rate_func(smooth, 0, 0.2)),
            Write(outputs)
        )
        self.wait()

        self.axes = axes
        self.inputs_label = inputs
        self.outputs_label = outputs

    def show_two_graphs(self):
        axes = self.axes
        f_graph = axes.plot(
            lambda x: 2 * x * (x - 0.75) * (x - 1.5) + 1,
            color=BLUE
        )
        g_graph = axes.plot(
            lambda x: 1.8 * np.cos(TAU * x / 2),
            color=YELLOW
        )

        label_x_coord = 2
        f_label = MathTex("f(x)")
        f_label.set_color(f_graph.get_color())
        f_point = axes.c2p(label_x_coord, axes.plot(lambda x: 2 * x * (x - 0.75) * (x - 1.5) + 1)(label_x_coord))
        f_label.next_to(f_point, LEFT)

        g_label = MathTex("g(x)")
        g_label.set_color(g_graph.get_color())
        g_point = axes.c2p(label_x_coord, axes.plot(lambda x: 1.8 * np.cos(TAU * x / 2))(label_x_coord))
        g_label.next_to(g_point, UP, buff=SMALL_BUFF)

        solution = 0.24
        cross_point = axes.c2p(solution, axes.plot(lambda x: 2 * x * (x - 0.75) * (x - 1.5) + 1)(solution))
        l_v_line = DashedLine(
            axes.c2p(axes.x_range[0], 0),
            axes.c2p(axes.x_range[0], axes.plot(lambda x: 2 * x * (x - 0.75) * (x - 1.5) + 1)(solution)),
        )
        r_v_line = DashedLine(
            axes.c2p(axes.x_range[1], 0),
            axes.c2p(axes.x_range[1], axes.plot(lambda x: 2 * x * (x - 0.75) * (x - 1.5) + 1)(solution)),
        )
        v_line = DashedLine(
            axes.c2p(solution, 0),
            axes.c2p(solution, axes.plot(lambda x: 2 * x * (x - 0.75) * (x - 1.5) + 1)(solution)),
        )

        equation = MathTex("f(x)", "=", "g(x)")
        equation[0].set_color(f_label.get_color())
        equation[2].set_color(g_label.get_color())
        equation.next_to(cross_point, UP, buff=1.5, aligned_edge=LEFT)
        equation_arrow = Arrow(
            equation.get_bottom(), cross_point,
            buff=SMALL_BUFF,
            color=WHITE
        )
        equation_target = MathTex("x^2", "=", "2")
        equation_target.set_style(equation)
        equation_target.to_edge(UP)

        for graph, label in (f_graph, f_label), (g_graph, g_label):
            self.play(
                Create(graph),
                Write(label, rate_func=squish_rate_func(smooth, 0.5, 1)),
                run_time=2
            )
        self.wait()
        self.play(
            ReplacementTransform(r_v_line.copy().set_opacity(0), v_line),
            ReplacementTransform(l_v_line.copy().set_opacity(0), v_line),
            run_time=2
        )
        self.play(
            ReplacementTransform(f_label.copy(), equation[0]),
            ReplacementTransform(g_label.copy(), equation[2]),
            Write(equation[1]),
            GrowArrow(equation_arrow),
        )
        for x in range(4):
            self.play(
                FadeOut(v_line.copy()),
                Create(v_line, rate_func=squish_rate_func(smooth, 0.5, 1)),
                run_time=1.5
            )
        self.wait()
        self.play(
            Transform(equation, equation_target),
            *[FadeOut(mob) for mob in [equation_arrow, v_line]]
        )

        self.f_graph = f_graph
        self.f_label = f_label
        self.g_graph = g_graph
        self.g_label = g_label
        self.equation = equation_target

    def transition_to_sqrt_2_case(self):
        f_graph = self.f_graph
        f_label = VGroup(self.f_label)
        g_graph = self.g_graph
        g_label = VGroup(self.g_label)
        axes = self.axes
        for label in f_label, g_label:
            for x in range(2):
                label.add(Dot(label.get_center()))
        for number in axes.y_axis.numbers:
            number.add_background_rectangle()

        squared_graph = axes.plot(lambda x: x**2)
        squared_graph.set_style(f_graph)
        two_graph = axes.plot(lambda x: 2)
        two_graph.set_style(g_graph)

        squared_label = MathTex("f(x)", "=", "x^2")
        squared_point = axes.c2p(2, axes.plot(lambda x: x**2)(2))
        squared_label.next_to(squared_point, RIGHT)
        squared_label.set_color(squared_graph.get_color())
        two_label = MathTex("g(x)", "=", "2")
        two_point = axes.c2p(3, axes.plot(lambda x: 2)(3))
        two_label.next_to(two_point, UP)
        two_label.set_color(two_graph.get_color())

        find_sqrt_2 = self.find_sqrt_2 = Text("(Find $\\sqrt{2}$)")
        find_sqrt_2.next_to(self.equation, DOWN)

        self.play(
            ReplacementTransform(f_graph, squared_graph),
            ReplacementTransform(f_label, squared_label),
        )
        self.play(
            ReplacementTransform(g_graph, two_graph),
            ReplacementTransform(g_label, two_label),
            Animation(axes.y_axis.numbers)
        )
        self.wait()
        self.play(Write(find_sqrt_2))
        self.wait()

        self.squared_graph = squared_graph
        self.two_graph = two_graph
        self.squared_label = squared_label
        self.two_label = two_label

    def show_example_binary_search(self):
        self.binary_search(
            self.squared_graph, self.two_graph,
            x0=1, x1=2,
            n_iterations=8
        )

    def binary_search(
        self,
        f_graph, g_graph,
        x0, x1,
        n_iterations,
        n_iterations_with_sign_mention=0,
        zoom=False,
    ):
        axes = self.axes
        rect = self.rect = Rectangle()
        rect.set_stroke(width=0)
        rect.set_fill(YELLOW, 0.5)
        line = Line(
            axes.c2p(x0, 0),
            axes.c2p(x1, 0),
        )
        rect.replace(line, stretch=True)
        rect.stretch_to_fit_height(self.search_range_rect_height)

        mention_signs = n_iterations_with_sign_mention > 0
        kwargs = {"mention_signs": mention_signs}
        leftovers0 = self.compare_graphs_at_x(f_graph, g_graph, x0, **kwargs)
        self.wait()
        leftovers1 = self.compare_graphs_at_x(f_graph, g_graph, x1, **kwargs)
        self.wait()
        self.play(GrowFromCenter(rect))
        self.wait()

        all_leftovers = VGroup(leftovers0, leftovers1)
        end_points = [x0, x1]
        if mention_signs:
            sign_word0 = leftovers0.sign_word
            sign_word1 = leftovers1.sign_word

        midpoint_line = Line(MED_SMALL_BUFF * UP, ORIGIN, color=YELLOW)
        midpoint_line_update = UpdateFromFunc(
            midpoint_line, lambda l: l.move_to(rect)
        )
        decimal = DecimalNumber(
            0,
            num_decimal_places=3,
            show_ellipsis=True,
        )
        decimal.scale(0.7)
        decimal_update = ChangingDecimal(
            decimal, lambda a: axes.x_axis.p2n(rect.get_center()),
            position_update_func=lambda m: m.next_to(
                midpoint_line, DOWN, SMALL_BUFF,
                aligned_edge=decimal[:-1].get_left(),
            ),
        )
        if not self.show_midpoint_value:
            decimal.set_fill(opacity=0)
            midpoint_line.set_stroke(width=0)

        kwargs = {
            "mention_signs": False,
            "show_decimal": zoom,
        }
        for x in range(n_iterations - 1):
            x_mid = np.mean(end_points)
            leftovers_mid = self.compare_graphs_at_x(f_graph, g_graph, x_mid, **kwargs)
            if leftovers_mid.too_high == all_leftovers[0].too_high:
                index_to_fade = 0
            else:
                index_to_fade = 1
            edge = [RIGHT, LEFT][index_to_fade]
            to_fade = all_leftovers[index_to_fade]
            all_leftovers.submobjects[index_to_fade] = leftovers_mid
            end_points[index_to_fade] = x_mid

            added_anims = []
            if mention_signs:
                word = [leftovers0, leftovers1][index_to_fade].sign_word
                if x < n_iterations_with_sign_mention:
                    added_anims = [word.animate.next_to(leftovers_mid[0].get_end(), -edge)]
                elif word in self.mobjects:
                    added_anims = [FadeOut(word)]

            rect.generate_target()
            rect.target.stretch(0.5, 0, about_edge=edge)
            rect.target.stretch_to_fit_height(self.search_range_rect_height)
            self.play(
                MoveToTarget(rect),
                midpoint_line_update,
                decimal_update,
                Animation(all_leftovers),
                FadeOut(to_fade),
                *added_anims
            )
            if zoom:
                factor = 2.0 / rect.get_width()
                everything = VGroup(*self.mobjects)
                decimal_index = everything.submobjects.index(decimal)
                midpoint_line_index = everything.submobjects.index(midpoint_line)
                everything.generate_target()
                everything.target.scale(factor, about_point=rect.get_center())
                everything.target[decimal_index].scale(1. / factor, about_edge=UP)
                everything.target[midpoint_line_index].scale(1. / factor)
                if factor > 1:
                    self.play(
                        everything.animate.scale(factor, about_point=rect.get_center())
                    )
            else:
                self.wait()

    def compare_graphs_at_x(
        self, f_graph, g_graph, x,
        mention_signs=False,
        show_decimal=False,
    ):
        axes = self.axes
        f_point = axes.c2p(x, axes.plot(lambda t: f_graph.underlying_function(t) if hasattr(f_graph, 'underlying_function') else f_graph)(x))
        g_point = axes.c2p(x, axes.plot(lambda t: g_graph.underlying_function(t) if hasattr(g_graph, 'underlying_function') else g_graph)(x))
        arrow = Arrow(
            g_point, f_point, buff=0,
            **self.arrow_config
        )
        too_high = f_point[1] > g_point[1]
        if too_high:
            arrow.set_fill(GREEN, opacity=self.arrow_opacity)
        else:
            arrow.set_fill(RED, opacity=self.arrow_opacity)

        leftovers = VGroup(arrow)
        leftovers.too_high = too_high

        if self.show_dotted_line_to_f:
            v_line = DashedLine(axes.c2p(x, 0), f_point)
            self.play(Create(v_line))
            leftovers.add(v_line)

        added_anims = []
        if show_decimal:
            decimal = DecimalNumber(
                axes.x_axis.p2n(arrow.get_start()),
                num_decimal_places=3,
            )
            height = self.rect.get_height()
            decimal.set_height(height)
            next_to_kwargs = {
                "buff": height,
            }
            if too_high:
                decimal.next_to(arrow, DOWN, **next_to_kwargs)
                if hasattr(self, "last_up_arrow_decimal"):
                    added_anims += [FadeOut(self.last_up_arrow_decimal)]
                self.last_up_arrow_decimal = decimal
            else:
                decimal.next_to(arrow, UP, **next_to_kwargs)
                if hasattr(self, "last_down_arrow_decimal"):
                    added_anims += [FadeOut(self.last_down_arrow_decimal)]
                self.last_down_arrow_decimal = decimal
            line = Line(decimal, arrow, buff=0)
            line.set_stroke(WHITE, 1)
            decimal.add(line)
            added_anims += [FadeIn(decimal)]

        if mention_signs:
            if too_high:
                sign_word = Text("Positive")
                sign_word.set_color(GREEN)
                sign_word.scale(0.7)
                sign_word.next_to(arrow.get_end(), RIGHT)
            else:
                sign_word = Text("Negative")
                sign_word.set_color(RED)
                sign_word.scale(0.7)
                sign_word.next_to(arrow.get_end(), LEFT)
            sign_word.add_background_rectangle()
            added_anims += [FadeIn(sign_word)]
            leftovers.sign_word = sign_word

        self.play(GrowArrow(arrow), *added_anims)

        return leftovers
