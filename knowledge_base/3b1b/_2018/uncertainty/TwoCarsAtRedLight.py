# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示兩輛車在紅綠燈前，透過短時間與長時間的同步閃光信號，從低信心度到高信心度的頻率分析過程。


from manim import *
import numpy as np

class TwoCarsAtRedLight(Scene):
    def __init__(self, text_scale_val=0.75, **kwargs):
        super().__init__(**kwargs)
        self.text_scale_val = text_scale_val

    def construct(self):
        self.pull_up_behind()
        self.flash_in_sync_short_time()
        self.show_low_confidence()
        self.flash_in_sync_long_time()
        self.show_high_confidence()

    def pull_up_behind(self):
        #Setup Traffic light
        traffic_light = TrafficLight()
        traffic_light.move_to(6*RIGHT + 2.5*DOWN, DOWN)
        source_point = Dot(point=traffic_light[2].get_right(), radius=0)
        screen = Line(ORIGIN, UP)
        screen.next_to(source_point, RIGHT, LARGE_BUFF)
        red_light = Spotlight(
            color = RED,
            source_point = source_point,
            radius = 0.5,
            screen = screen,
            num_levels = 20,
            opacity_function = lambda r : 1/(10*r**2+1)
        )
        red_light.set_opacity(0.5)
        red_light.rotate(TAU/2, about_edge = LEFT)
        self.add(red_light, traffic_light)

        #Setup cars
        car1, car2 = cars = self.cars = VGroup(*[
            Car() for x in range(2)
        ])
        cars.arrange(RIGHT, buff = LARGE_BUFF)
        cars.next_to(
            traffic_light, LEFT, 
            buff = LARGE_BUFF, aligned_edge = DOWN
        )
        car2.pi_creature.set_color(GREY_BROWN)
        car1.start_point = car1.get_corner(DOWN+RIGHT)
        car1.shift(FRAME_WIDTH/2*LEFT)

        #Pull up car
        self.add(cars)
        self.play(
            Create(red_light, rate_func = squish_rate_func(smooth, 0, 0.3)),
            Animation(traffic_light),
            self.get_flashes(car2, num_flashes = 3),
            car1.animate.move_to(car1.start_point).set_run_time(3).set_rate_func(rush_from),
        )

    def flash_in_sync_short_time(self):
        car1, car2 = cars = self.cars

        #Setup axes
        axes = Axes(
            x_range = [0, 5, 1],
            y_range = [0, 2, 0.5],
            y_axis_config = {
                "tick_frequency" : 0.5,
            },
        )
        axes.x_axis.add_numbers(numbers=[1, 2, 3])
        time_label = Text("Time")
        time_label.scale(self.text_scale_val)
        time_label.next_to(axes.x_axis.get_right(), DOWN)
        y_title = Text("Signal")
        y_title.scale(self.text_scale_val)
        y_title.next_to(axes.y_axis, UP, SMALL_BUFF)
        axes.add(time_label, y_title)
        axes.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        graph = axes.plot(
            self.get_multispike_function(list(range(1, 4))),
            x_range = [0.8, 3.8],
        )
        graph.set_color(YELLOW)

        #Label short duration
        brace = Brace(Line(
            axes.input_to_graph_point(1, graph),
            axes.input_to_graph_point(3, graph),
        ), UP)
        text = Text("Short duration observation")
        text.scale(self.text_scale_val)
        text.next_to(brace, UP, SMALL_BUFF)
        text.align_to(
            axes.c2p(0.25, 0), LEFT
        )

        self.play(
            self.get_flashes(car1, num_flashes = 2),
            self.get_flashes(car2, num_flashes = 2),
            LaggedStartMap(FadeIn, VGroup(
                axes, time_label, y_title,
            ))
        )
        self.play(
            self.get_flashes(car1, num_flashes = 3),
            self.get_flashes(car2, num_flashes = 3),
            Create(graph, rate_func=linear, run_time = 3)
        )
        self.play(
            self.get_flashes(car1, num_flashes = 10),
            self.get_flashes(car2, num_flashes = 10, run_time_per_flash = 0.98),
            GrowFromCenter(brace),
            Write(text),
        )

        self.time_axes = axes
        self.time_graph = graph
        self.time_graph_label = VGroup(
            brace, text
        )

    def show_low_confidence(self):
        car1, car2 = cars = self.cars
        time_axes = self.time_axes

        #Setup axes
        frequency_axes = Axes(
            x_range = [0, 3, 1],
            y_range = [0, 1.5, 0.5],
            y_axis_config = {
                "tick_frequency" : 0.5,
            }
        )
        frequency_axes.next_to(time_axes, DOWN, LARGE_BUFF)
        frequency_axes.set_color(GREY_B)
        frequency_label = Text("Frequency")
        frequency_label.scale(self.text_scale_val)
        frequency_label.next_to(frequency_axes.x_axis.get_right(), DOWN)
        frequency_axes.add(
            frequency_label,
            Dot(point=frequency_axes.y_axis.get_top(), radius=0)
        )
        frequency_axes.x_axis.add_numbers(numbers=[1, 2])
        frequency_graph = frequency_axes.plot(
            lambda x : np.exp(-4*(x-1)**2),
            x_range = [0, 2],
        )
        frequency_graph.set_color(RED)
        peak_point = frequency_axes.input_to_graph_point(1, frequency_graph)

        #Setup label
        label = Text("Low confidence")
        label.scale(self.text_scale_val)
        label.move_to(peak_point + UP+RIGHT, DOWN)
        label.set_color(frequency_graph.get_color())
        arrow = Arrow(label.get_bottom(), peak_point, buff = 2*SMALL_BUFF)
        arrow.set_color(frequency_graph.get_color())

        self.play(
            ReplacementTransform(
                self.time_axes.copy(), frequency_axes
            ),
            ReplacementTransform(
                self.time_graph.copy(), frequency_graph
            ),
        )
        self.play(
            Write(label), 
            GrowArrow(arrow)
        )
        self.wait()

        self.frequency_axes = frequency_axes
        self.frequency_graph = frequency_graph
        self.frequency_graph_label = VGroup(
            label, arrow
        )

    def flash_in_sync_long_time(self):
        time_graph = self.time_graph
        time_axes = self.time_axes
        frequency_graph = self.frequency_graph
        frequency_axes = self.frequency_axes

        n_spikes = 12
        new_time_graph = time_axes.plot(
            self.get_multispike_function(list(range(1, n_spikes+1))),
            x_range = [0.8, n_spikes + 0.8],
        )
        new_time_graph.set_color(time_graph.get_color())

        new_frequency_graph = frequency_axes.plot(
            lambda x : np.exp(-500*(x-1)**2),
            x_range = [0, 2],
        )
        new_frequency_graph.set_color(self.frequency_graph.get_color())

        def pin_freq_graph_end_points(freq_graph):
            freq_graph.set_points([frequency_axes.c2p(0, 0)] + list(freq_graph.get_points()[1:-1]) + [frequency_axes.c2p(2, 0)])

        self.play(LaggedStartMap(
            FadeOut, VGroup(
                self.time_graph_label,
                self.frequency_graph_label,
                self.time_graph,
            )
        ))
        self.play(
            time_axes.x_axis.animate.stretch(2.5, 0, about_edge=LEFT).set_run_time(4).set_rate_func(squish_rate_func(smooth, 0.3, 0.6)),
            UpdateFromFunc(
                time_axes.x_axis.tip,
                lambda m : m.move_to(
                    time_axes.x_axis.get_right(), 
                    LEFT
                )
            ),
            Create(
                new_time_graph,
                run_time = n_spikes,
                rate_func=linear,
            ),
            frequency_graph.animate.stretch(0.1, 0).set_run_time(n_spikes),
            UpdateFromFunc(frequency_graph, pin_freq_graph_end_points),
            *[
                self.get_flashes(car, num_flashes = n_spikes)
                for car in self.cars
            ]
        )

        self.new_time_graph = new_time_graph
        self.new_frequency_graph = new_frequency_graph

    def show_high_confidence(self):
        #Frequency stuff
        arrow = self.frequency_graph_label[1]
        label = Text("High confidence")
        label.scale(self.text_scale_val)
        label.next_to(arrow.get_start(), UP, SMALL_BUFF)
        label.set_color(arrow.get_color())

        frequency_axes = self.frequency_axes

        #Time stuff
        new_time_graph = self.new_time_graph
        brace = Brace(new_time_graph, UP, buff = SMALL_BUFF)
        text = Text("Long duration observation")
        text.scale(self.text_scale_val)
        text.next_to(brace, UP, buff = SMALL_BUFF)

        self.play(
            FadeIn(label),
            GrowArrow(arrow),
            *list(map(self.get_flashes, self.cars))
        )
        self.play(
            GrowFromCenter(brace),
            Write(text, run_time = 1),
            *list(map(self.get_flashes, self.cars))
        )
        self.play(*[
            self.get_flashes(car, num_flashes = 10)
            for car in self.cars
        ])

    ###

    def get_flashes(self, car, colors = [YELLOW, RED], num_flashes = 1, **kwargs):
        return AnimationGroup(*[
            MultipleFlashes(light, color, num_flashes = num_flashes, **kwargs)
            for light, color in zip(car.get_lights(), colors)
        ])

    def get_multispike_function(self, spike_times):
        return lambda x : sum([
            1.25*np.exp(-100*(x-m)**2)
            for m in spike_times
        ])
