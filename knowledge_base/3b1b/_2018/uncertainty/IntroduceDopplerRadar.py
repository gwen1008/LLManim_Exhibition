# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示雷達發射脈衝信號、接收回波，並在時域和頻域分析頻率偏移的過程。


from manim import *
import numpy as np

class IntroduceDopplerRadar(Scene):
    def __init__(self, frequency_spread_factor=100, **kwargs):
        super().__init__(**kwargs)
        self.frequency_spread_factor = frequency_spread_factor

    def construct(self):
        self.setup_axes()
        self.measure_distance_with_time()
        self.show_frequency_shift()
        self.show_frequency_shift_in_fourier()

    def setup_axes(self):
        self.dish = RadarDish()
        self.dish.to_corner(UP+LEFT)
        axes = Axes(
            x_range=[0, 10],
            y_range=[-1.5, 1.5],
            axis_config={"include_numbers": False}
        )
        axes.move_to(DOWN)
        time_label = Text("Time")
        time_label.next_to(axes.x_axis.get_right(), UP)
        axes.time_label = time_label
        axes.add(time_label)
        self.axes = axes

        self.add(self.dish)
        self.add(axes)

    def measure_distance_with_time(self):
        dish = self.dish
        axes = self.axes
        distance = 5
        time_diff = 5
        speed = (2*distance)/time_diff
        randy = Randolph().flip()
        randy.match_height(dish)
        randy.move_to(dish.get_right(), LEFT)
        randy.shift(distance*RIGHT)

        pulse_graph, echo_graph, sum_graph = \
            self.get_pulse_and_echo_graphs(
                self.get_single_pulse_graph,
                (1,), (1+time_diff,)
            )
        words = ["Original signal", "Echo"]
        for graph, word in zip([pulse_graph, echo_graph], words):
            arrow = Arrow(ORIGIN, DOWN, buff=0)
            arrow.next_to(graph.peak_point, UP, SMALL_BUFF)
            arrow.set_color(graph.get_color())
            graph.arrow = arrow
            label = Text(word)
            label.next_to(arrow.get_start(), UP, SMALL_BUFF)
            label.set_color(graph.get_color())
            graph.label = label

        double_arrow = DoubleArrow(
            pulse_graph.peak_point,
            echo_graph.peak_point,
            color=WHITE
        )
        distance_text = MathTex("2 \\times \\text{distance}/(\\text{signal speed})")
        distance_text.set_width(0.9*double_arrow.get_width())
        distance_text.next_to(double_arrow, UP, SMALL_BUFF)

        pulse = RadarPulseSingleton(
            dish, randy, 
            speed=0.97*speed,  # Just needs slightly better alignment
        )
        
        # 模擬 turn_animation_into_updater
        sum_graph_copy = sum_graph.copy()
        self.add(sum_graph_copy)
        self.play(
            Create(sum_graph_copy, rate_func=linear, run_time=0.97*axes.x_range[1]),
            run_time=0.97*axes.x_range[1]
        )
        self.remove(sum_graph_copy)
        self.add(sum_graph)
        
        randy_look_at = randy.add_updater(lambda pi: pi.look_at(pulse.mobject))

        self.add(randy_look_at)
        self.wait(0.5)
        self.add(pulse)
        self.play(
            Write(pulse_graph.label),
            GrowArrow(pulse_graph.arrow),
            run_time=1,
        )
        self.play(randy.animate.change("pondering"))
        self.wait(time_diff - 2)
        self.play(
            Write(echo_graph.label),
            GrowArrow(echo_graph.arrow),
            run_time=1
        )
        self.wait()
        self.play(
            GrowFromCenter(double_arrow),
            FadeIn(distance_text)
        )
        self.wait()

        randy_look_at.clear_updaters()
        self.remove(pulse)
        self.play(LaggedStart(*[
            FadeOut(mob) for mob in [
                sum_graph, randy,
                pulse_graph.arrow, pulse_graph.label,
                echo_graph.arrow, echo_graph.label,
                double_arrow, distance_text
            ]
        ]))

    def show_frequency_shift(self):
        axes = self.axes
        dish = self.dish
        plane = NumberPlane()
        plane.flip()
        plane.move_to(dish)
        plane.to_edge(RIGHT)

        time_diff = 6

        pulse_graph, echo_graph, sum_graph = graphs = \
            self.get_pulse_and_echo_graphs(
                self.get_frequency_pulse_graph,
                (1,25), (1+time_diff,50)
            )
        for graph in graphs:
            graph.set_stroke(width=3)
        signal_graph = self.get_frequency_pulse_graph(1)

        pulse_brace = Brace(Line(ORIGIN, RIGHT), UP)
        pulse_brace.move_to(axes.c2p(1, 1.2))
        echo_brace = pulse_brace.copy()
        echo_brace.stretch(0.6, 0)
        echo_brace.move_to(axes.c2p(7, 1.2))
        pulse_text = pulse_brace.get_text("Original signal")
        pulse_text.add_background_rectangle()
        echo_text = echo_brace.get_text("Echo")
        echo_subtext = Text("(Higher frequency)")
        echo_subtext.next_to(echo_text, RIGHT)
        echo_subtext.set_color(echo_graph.get_color())

        # 模擬 turn_animation_into_updater
        sum_graph_copy = sum_graph.copy()
        self.add(sum_graph_copy)
        self.play(
            Create(sum_graph_copy, run_time=8, rate_func=linear),
            run_time=8
        )
        self.remove(sum_graph_copy)
        self.add(sum_graph)
        
        pulse = RadarPulse(dish, plane, n_pulse_singletons=12)
        plane.add_updater(lambda m, dt: m.shift(LEFT * 1.5 * dt))

        self.add(pulse, plane)
        self.play(UpdateFromAlphaFunc(
            plane, lambda m, a: m.set_fill(opacity=a)
        ))
        self.play(
            GrowFromCenter(pulse_brace),
            FadeIn(pulse_text),
        )
        self.wait(3)
        self.play(
            GrowFromCenter(echo_brace),
            GrowFromCenter(echo_text),
        )
        self.play(UpdateFromAlphaFunc(
            plane, lambda m, a: m.set_fill(opacity=1-a)
        ))
        plane.clear_updaters()
        self.wait(0.1)
        self.play(Write(echo_subtext, run_time=1))
        self.wait()
        self.remove(pulse, plane)

        pulse_graph.set_stroke(width=0)
        echo_graph.set_stroke(width=0)
        self.time_graph_group = VGroup(
            axes, pulse_brace, pulse_text,
            echo_brace, echo_text, echo_subtext,
            pulse_graph, echo_graph, sum_graph,
        )
        self.sum_graph = sum_graph
        self.pulse_graph = pulse_graph
        self.echo_graph = echo_graph
        self.pulse_brace = pulse_brace
        self.pulse_text = pulse_text
        self.echo_brace = echo_brace
        self.echo_text = echo_text
        self.echo_subtext = echo_subtext

    def show_frequency_shift_in_fourier(self):
        sum_graph = self.sum_graph
        pulse_graph = self.pulse_graph
        pulse_label = VGroup(self.pulse_brace, self.pulse_text)
        echo_graph = self.echo_graph
        echo_label = VGroup(
            self.echo_brace, self.echo_text, self.echo_subtext
        )

        # Setup all fourier graph stuff
        f_max = 0.02
        frequency_axes = Axes(
            x_range=[0, 20],
            y_range=[-f_max, f_max],
            axis_config={
                "x_axis_config": {"unit_size": 0.5},
                "y_axis_config": {
                    "unit_size": 50,
                    "tick_frequency": 0.01,
                },
            }
        )
        frequency_axes.move_to(self.axes, LEFT)
        frequency_axes.to_edge(DOWN)
        frequency_label = Text("Frequency")
        frequency_label.next_to(
            frequency_axes.x_axis.get_right(), UP,
        )
        frequency_label.to_edge(RIGHT)
        frequency_axes.add(frequency_label)

        for graph in [pulse_graph, echo_graph, sum_graph]:
            graph.fourier_transform = self.get_fourier_graph(
                frequency_axes, graph.underlying_function,
                frequency_axes.x_range[0], 25,
            )

        # Braces labeling F.T.
        original_fourier_brace = Brace(
            Line(
                frequency_axes.c2p(7, 0.9*f_max),
                frequency_axes.c2p(9, 0.9*f_max),
            ),
            UP,
        ).set_color(BLUE)
        echo_fourier_brace = Brace(
            Line(
                frequency_axes.c2p(14, 0.4*f_max),
                frequency_axes.c2p(18, 0.4*f_max),
            ),
            UP,
        ).set_color(YELLOW)
        
        fourier_label = MathTex("\\|\\text{Fourier transform}\\|")
        fourier_label.next_to(frequency_axes.y_axis, UP, buff=SMALL_BUFF)
        fourier_label.shift_onto_screen()
        fourier_label.set_color(RED)

        # v_lines
        v_line = DashedLine(
            frequency_axes.c2p(8, 0),
            frequency_axes.c2p(8, 1.2*f_max),
            color=YELLOW,
            dash_length=0.025,
        )
        v_line_pair = VGroup(*[
            v_line.copy().shift(u*0.6*RIGHT)
            for u in (-1, 1)
        ])
        v_line = VGroup(v_line)

        double_arrow = DoubleArrow(
            frequency_axes.c2p(8, 0.007),
            frequency_axes.c2p(16, 0.007),
            buff=0,
            color=WHITE
        )

        self.play(
            self.time_graph_group.animate.to_edge(UP),
            self.dish.animate.shift(2*UP),
            FadeIn(frequency_axes)
        )
        self.wait()
        self.play(
            FadeOut(sum_graph),
            FadeOut(echo_label),
            pulse_graph.animate.set_stroke(width=3),
        )
        self.play(
            ReplacementTransform(
                pulse_label[0].copy(),
                original_fourier_brace
            ),
            Create(pulse_graph.fourier_transform)
        )
        self.play(Write(fourier_label))
        self.wait()
        self.play(Create(v_line))
        self.wait()
        self.play(ReplacementTransform(v_line, v_line_pair))
        self.wait()
        self.play(FadeOut(v_line_pair))
        self.wait()

        self.play(
            FadeOut(pulse_graph),
            FadeIn(sum_graph),
            ReplacementTransform(
                pulse_graph.fourier_transform,
                sum_graph.fourier_transform
            )
        )
        self.play(FadeIn(echo_label))
        self.play(ReplacementTransform(
            echo_label[0].copy(),
            echo_fourier_brace,
        ))
        self.wait(2)
        self.play(GrowFromCenter(double_arrow))
        self.wait()

    def get_graph(self, func, **kwargs):
        graph = self.axes.plot(func, **kwargs)
        graph.peak_point = self.get_peak_point(graph)
        graph.underlying_function = func
        return graph

    def get_single_pulse_graph(self, x, **kwargs):
        return self.plot(self.get_single_pulse_function(x), **kwargs)

    def get_single_pulse_function(self, x):
        return lambda t: -2*np.sin(10*(t-x))*np.exp(-100*(t-x)**2)

    def get_frequency_pulse_graph(self, x, freq=50, **kwargs):
        return self.plot(
            self.get_frequency_pulse_function(x, freq), 
            **kwargs
        )

    def get_frequency_pulse_function(self, x, freq):
        factor = self.frequency_spread_factor
        return lambda t: (
            2*np.cos(2*freq*(t-x)) *
            min(np.exp(-(freq**2/factor)*(t-x)**2), 0.5)
        )

    def get_peak_point(self, graph):
        anchors = graph.get_anchors()
        return anchors[np.argmax([p[1] for p in anchors])]

    def get_pulse_and_echo_graphs(self, func, args1, args2):
        pulse_graph = func(*args1, color=BLUE)
        echo_graph = func(*args2, color=YELLOW)
        sum_graph = self.axes.plot(
            lambda x: (
                pulse_graph.underlying_function(x) +
                echo_graph.underlying_function(x)
            ),
            color=WHITE
        )
        sum_graph.underlying_function = lambda x: (
            pulse_graph.underlying_function(x) +
            echo_graph.underlying_function(x)
        )
        return pulse_graph, echo_graph, sum_graph

    def get_fourier_graph(self, axes, func, x_min, x_max, **kwargs):
        # 簡化的傅立葉變換圖形生成
        # 實際實現需要更複雜的數學計算
        return axes.plot(
            lambda x: 0.01 * np.exp(-0.1*(x-8)**2),
            color=RED
        )

# 需要定義的輔助類別
class RadarDish(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 簡化的雷達天線表示
        circle = Circle(radius=0.5, color=BLUE)
        line = Line(ORIGIN, UP*0.7, color=BLUE)
        self.add(circle, line)

class Randolph(VMobject):
    # 簡化的角色表示
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        circle = Circle(radius=0.3, color=GREEN)
        self.add(circle)

class RadarPulseSingleton(VGroup):
    def __init__(self, dish, target, speed=1, **kwargs):
        super().__init__(**kwargs)
        self.dish = dish
        self.target = target
        self.speed = speed

class RadarPulse(VGroup):
    def __init__(self, dish, plane, n_pulse_singletons=12, **kwargs):
        super().__init__(**kwargs)
        self.dish = dish
        self.plane = plane
