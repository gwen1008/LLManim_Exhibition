# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示雷達發射長脈衝與短脈衝時，多個移動物體回波在時間域和頻率域的模糊性對比，以及傅立葉變換如何揭示頻率擴散。


from manim import *
import numpy as np

class AmbiguityInLongEchos(Scene):
    def __init__(
        self,
        object_x_coords=[7, 4, 6, 9, 8],
        frequency_spread_factor=200,
        n_pulse_singletons=16,
        pulse_frequency=0.025,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.object_x_coords = object_x_coords
        self.frequency_spread_factor = frequency_spread_factor
        self.n_pulse_singletons = n_pulse_singletons
        self.pulse_frequency = pulse_frequency

    def construct(self):
        self.setup_axes()
        self.setup_objects()
        self.send_long_pulse_single_echo()
        self.introduce_multiple_objects()
        self.use_short_pulse()
        self.fourier_transform_of_one_pulse()
        self.show_echos_of_moving_objects()
        self.overlapping_frequenies_of_various_objects()
        self.echos_of_long_pure_signal_in_frequency_space()
        self.concentrated_fourier_requires_long_time()

    def setup_axes(self):
        axes = self.axes = Axes(
            x_range=[0, 10],
            y_range=[-1.5, 1.5],
            axis_config={"include_numbers": False},
        )
        time_label = Text("Time")
        time_label.next_to(axes.x_axis.get_right(), UP)
        axes.add(time_label)
        axes.center()
        axes.shift(DOWN)
        self.add(axes)

        dish = self.dish = self.create_radar_dish()
        dish.move_to(axes, LEFT)
        dish.to_edge(UP, buff=LARGE_BUFF)
        self.add(dish)

    def create_radar_dish(self):
        # 簡化雷達天線表示
        circle = Circle(radius=0.3, color=BLUE)
        line = Line(ORIGIN, RIGHT*0.5).rotate(PI/4)
        line.move_to(circle.get_center())
        dish = VGroup(circle, line)
        return dish

    def setup_objects(self):
        objects = self.objects = VGroup(
            self.create_plane(),
            self.create_svg_object("blimp", BLUE_C, 0.5),
            self.create_svg_object("biplane", RED_D, 0.5),
            self.create_svg_object("helicopter", GREY_B, 0.5).rotate(-TAU/24),
            self.create_falcon_heavy(),
        )
        y_shifts = [0.25, 0, 0.5, 0.25, -0.5]
        for x, y, obj in zip(self.object_x_coords, y_shifts, objects):
            obj.move_to(self.axes.c2p(x, 0))
            obj.align_to(self.dish)
            obj.shift(y*UP)

        self.object_velocities = [
            0.7*LEFT,
            0.1*RIGHT,
            0.4*LEFT,
            0.4*RIGHT,
            0.5*UP,
        ]

    def create_plane(self):
        # 簡化飛機表示
        triangle = Triangle(color=WHITE, fill_opacity=1)
        triangle.scale(0.3)
        triangle.rotate(PI/2)
        return triangle

    def create_svg_object(self, name, color, height):
        # 簡化SVG物體表示
        if name == "blimp":
            ellipse = Ellipse(width=1, height=0.5, color=color, fill_opacity=1)
            return ellipse
        elif name == "biplane":
            rect = Rectangle(width=0.8, height=0.3, color=color, fill_opacity=1)
            return rect
        elif name == "helicopter":
            circle = Circle(radius=0.25, color=color, fill_opacity=1)
            rect = Rectangle(width=0.6, height=0.2, color=color, fill_opacity=1)
            rect.next_to(circle, RIGHT, buff=0)
            return VGroup(circle, rect)
        return Circle(radius=0.2, color=color)

    def create_falcon_heavy(self):
        # 簡化火箭表示
        rect = Rectangle(width=0.3, height=0.8, color=WHITE, fill_opacity=1)
        triangle = Triangle(color=RED, fill_opacity=1)
        triangle.scale(0.2)
        triangle.rotate(PI)
        triangle.next_to(rect, DOWN, buff=0)
        return VGroup(rect, triangle)

    def send_long_pulse_single_echo(self):
        x = self.object_x_coords[0]
        plane = self.objects[0]
        self.add(plane)
        
        # 移除PiCreature（原代碼中有）
        # randy = self.pi_creature
        # self.remove(randy)

        pulse_graph = self.get_frequency_pulse_graph(x)

        pulse = self.get_pulse(self.dish, plane)

        brace = Brace(
            Line(
                self.axes.c2p(x-1, 1),
                self.axes.c2p(x+1, 1),
            ), UP
        )
        words = brace.get_text("Spread over time")

        self.add(pulse)
        self.wait()
        squished_rate_func = squish_rate_func(smooth, 0.6, 0.9)
        self.play(
            Create(pulse_graph, rate_func=linear),
            GrowFromCenter(brace, rate_func=squished_rate_func),
            Write(words, rate_func=squished_rate_func),
            run_time=3,
        )
        self.remove(pulse)
        
        # 簡化PiCreature相關動畫
        # self.play(FadeIn(randy))
        # ... 省略PiCreature氣泡對話
        
        self.curr_graph = pulse_graph

    def introduce_multiple_objects(self):
        objects = self.objects
        x_coords = self.object_x_coords
        curr_graph = self.curr_graph
        
        graphs = VGroup(*[
            self.get_frequency_pulse_graph(x)
            for x in x_coords
        ])
        graphs.set_color_by_gradient(BLUE, YELLOW)
        
        def sum_func(t):
            return sum([graph.underlying_function(t) for graph in graphs])
        
        sum_graph = self.axes.plot(
            sum_func,
            x_range=[0, 10],
            color=WHITE
        )

        noise_function = lambda t: np.sum([
            0.5*np.sin(f*t)/f 
            for f in (2, 3, 5, 7, 11, 13)
        ])
        
        def noisy_func(t):
            return sum_graph.underlying_function(t)*(1+noise_function(t))
        
        noisy_graph = self.axes.plot(
            noisy_func,
            x_range=[0, 10],
            color=WHITE
        )

        pulses = self.get_pulses()

        self.play(
            LaggedStartMap(GrowFromCenter, objects[1:]),
            FadeOut(curr_graph),
            # randy.change, "pondering"  # 省略PiCreature
        )
        self.add(*pulses)
        self.wait(0.5)
        self.play(
            Create(
                sum_graph,
                rate_func=linear,
                run_time=3.5,
            ),
            # randy.change, "confused"  # 省略PiCreature
        )
        self.remove(*pulses)
        # self.play(randy.change, "pondering")  # 省略PiCreature
        self.play(Transform(
            sum_graph, noisy_graph,
            rate_func=lambda t: wiggle(t, 4),
            run_time=3
        ))
        self.wait(2)

        self.curr_graph = sum_graph

    def use_short_pulse(self):
        curr_graph = self.curr_graph
        objects = self.objects
        x_coords = self.object_x_coords
        
        self.frequency_spread_factor = 10
        self.n_pulse_singletons = 4
        self.pulse_frequency = 0.015

        graphs = VGroup(*[
            self.get_frequency_pulse_graph(x)
            for x in x_coords
        ])
        
        def sum_func(t):
            return sum([graph.underlying_function(t) for graph in graphs])
        
        sum_graph = self.axes.plot(
            sum_func,
            x_range=[0, 10],
            color=WHITE
        )

        pulses = self.get_pulses()

        self.play(FadeOut(curr_graph))
        self.add(*pulses)
        self.wait(0.5)
        self.play(
            Create(
                sum_graph,
                rate_func=linear,
                run_time=3.5,
            ),
            # randy.change, "happy"  # 省略PiCreature
        )
        self.wait()

        self.curr_graph = sum_graph
        self.first_echo_graph = graphs[0]
        self.first_echo_graph.set_color(YELLOW)

    def fourier_transform_of_one_pulse(self):
        frequency_axes = Axes(
            x_range=[0, 20],
            y_range=[-0.01, 0.01],
            x_length=10,  # 對應原unit_size=0.5
            y_length=2.2,  # 對應原unit_size=110
            axis_config={
                "include_numbers": False,
            }
        )
        frequency_label = Text("Frequency")
        frequency_label.next_to(frequency_axes.x_axis.get_right(), UP)
        frequency_axes.add(frequency_label)
        first_echo_graph = self.first_echo_graph

        self.play(
            VGroup(self.axes, first_echo_graph).animate.to_edge(
                UP, buff=SMALL_BUFF
            ).set_rate_func(squish_rate_func(smooth, 0.5, 1)),
            LaggedStartMap(FadeOut, self.objects),
            LaggedStartMap(FadeOut, VGroup(
                self.curr_graph, self.dish
            )),
            run_time=2
        )

        frequency_axes.next_to(self.axes, DOWN, LARGE_BUFF, LEFT)
        
        # 簡化傅立葉變換圖形
        def fourier_func(f):
            x = 8  # 中心頻率
            sigma = 2  # 寬度
            return 0.008 * np.exp(-((f - x) ** 2) / (2 * sigma ** 2))
        
        fourier_graph = frequency_axes.plot(
            fourier_func,
            x_range=[0, 20],
            color=BLUE
        )
        fourier_graph.save_state()
        fourier_graph.move_to(first_echo_graph)
        h_vect = 4*RIGHT
        fourier_graph.shift(h_vect)
        fourier_graph.set_opacity(0)

        f = 8
        v_line = DashedLine(
            frequency_axes.c2p(f, 0),
            frequency_axes.c2p(f, frequency_axes.y_range[1]),
        )
        v_lines = VGroup(
            v_line.copy().shift(2*LEFT),
            v_line.copy().shift(2*RIGHT),
        )
        rect = Rectangle(stroke_width=0, fill_color=YELLOW, fill_opacity=0.25)
        rect.replace(v_lines, stretch=True)
        rect.save_state()
        rect.stretch(0, 0)

        self.play(Write(frequency_axes, run_time=1))
        
        # 創建過渡動畫
        temp_graph = first_echo_graph.copy()
        self.add(temp_graph)
        self.play(
            temp_graph.animate.move_to(fourier_graph.saved_state).shift(-h_vect).set_opacity(0),
            fourier_graph.animate.restore()
        )
        self.remove(temp_graph)
        
        self.wait()
        self.play(Create(v_line))
        self.play(
            ReplacementTransform(VGroup(v_line), v_lines),
            rect.animate.restore()
        )
        self.wait()
        self.play(FadeOut(v_lines), FadeOut(rect))

        self.frequency_axes = frequency_axes
        self.fourier_graph = fourier_graph

    def show_echos_of_moving_objects(self):
        objects = self.objects
        objects.save_state()
        object_velocities = self.object_velocities

        movements = self.object_movements = []
        for v, obj in zip(object_velocities, objects):
            # 簡化持續移動動畫
            movement = obj.add_updater(
                lambda m, dt, vel=v: m.shift(vel * dt)
            )
            movements.append(movement)
        
        pulses = self.get_pulses()
        continual_anims = pulses + movements
        
        self.play(
            FadeOut(self.axes),
            FadeOut(self.first_echo_graph),
            LaggedStartMap(FadeIn, objects),
            FadeIn(self.dish)
        )
        self.add(*continual_anims)
        self.wait(4)
        
        # 淡出物體
        for obj in objects:
            obj.add_updater(lambda m, dt: None)  # 停止移動
        self.play(*[
            obj.animate.set_opacity(0)
            for obj in objects
        ])
        
        # 移除持續動畫
        for movement in movements:
            obj.remove_updater(movement)
        for pulse in pulses:
            self.remove(pulse)
            
        self.wait()

    def overlapping_frequenies_of_various_objects(self):
        frequency_axes = self.frequency_axes
        fourier_graph = self.fourier_graph
        shifted_graphs = self.get_shifted_frequency_graphs(fourier_graph)
        color = fourier_graph.get_color()
        shifted_graphs.set_color_by_gradient(
            average_color(color, WHITE), 
            color,
            average_color(color, BLACK),
        )
        sum_graph = self.get_sum_graph(frequency_axes, shifted_graphs)
        sum_graph.match_style(fourier_graph)

        shifted_graphs.save_state()

        self.play(ReplacementTransform(
            VGroup(fourier_graph), shifted_graphs,
            lag_ratio=0.5,
            run_time=2
        ))
        self.wait()
        self.play(
            shifted_graphs.animate.arrange(DOWN).move_to(fourier_graph, DOWN),
        )
        self.wait()
        self.play(shifted_graphs.animate.restore())
        self.play(ReplacementTransform(
            shifted_graphs, VGroup(sum_graph),
        ))
        self.wait()

        self.curr_fourier_graph = sum_graph

    def echos_of_long_pure_signal_in_frequency_space(self):
        curr_fourier_graph = self.curr_fourier_graph
        f_max = self.frequency_axes.y_range[1]
        
        def new_func(x):
            return f_max * np.exp(-100*(x-8)**2)
        
        new_fourier_graph = self.frequency_axes.plot(
            new_func,
            x_range=self.frequency_axes.x_range,
            color=PINK
        )

        self.play(
            FadeOut(curr_fourier_graph),
            FadeIn(new_fourier_graph),
        )
        self.fourier_graph = new_fourier_graph
        self.overlapping_frequenies_of_various_objects()

    def concentrated_fourier_requires_long_time(self):
        objects = self.objects
        objects.restore()
        object_movements = self.object_movements
        self.n_pulse_singletons = 32
        pulses = self.get_pulses()
        
        # 重新設置移動動畫
        movements = []
        for v, obj in zip(self.object_velocities, objects):
            movement = obj.add_updater(
                lambda m, dt, vel=v: m.shift(vel * dt)
            )
            movements.append(movement)
        
        continual_anims = movements + pulses
        
        self.add(*continual_anims)
        
        # 淡入物體
        self.play(*[
            obj.animate.set_opacity(1)
            for obj in objects
        ])
        self.wait(2)
        self.wait()
        
        # 淡出物體
        self.play(*[
            obj.animate.set_opacity(0)
            for obj in objects
        ])
        self.wait()
        
        # 清理動畫
        for movement in movements:
            for obj in objects:
                obj.remove_updater(movement)
        for pulse in pulses:
            self.remove(pulse)

    def get_frequency_pulse_graph(self, x, freq=25, **kwargs):
        # 簡化脈衝圖形
        def pulse_func(t):
            center = x
            width = 2.0
            return np.exp(-((t - center) ** 2) / (2 * width ** 2)) * np.sin(freq * t)
        
        graph = self.axes.plot(
            pulse_func,
            x_range=[0, 10],
            color=BLUE
        )
        return graph

    def get_pulse(self, dish, echo_object):
        # 簡化雷達脈衝表示
        pulse = Circle(radius=0.1, color=YELLOW, fill_opacity=0.5)
        pulse.move_to(dish.get_center())
        
        def update_pulse(mob, alpha):
            mob.move_to(interpolate(
                dish.get_center(),
                echo_object.get_center(),
                alpha
            ))
            mob.set_opacity(1 - alpha)
        
        return UpdateFromAlphaFunc(pulse, update_pulse)

    def get_pulses(self):
        pulses = []
        for obj in self.objects:
            pulse = self.get_pulse(self.dish.copy(), obj)
            pulses.append(pulse)
        return pulses

    def get_shifted_frequency_graphs(self, fourier_graph):
        frequency_axes = self.frequency_axes
        
        def get_func(v):
            return lambda f: fourier_graph.underlying_function(
                np.clip(f - 5*v[0], frequency_axes.x_range[0], frequency_axes.x_range[1])
            )
        
        shifted_graphs = VGroup()
        for v in self.object_velocities:
            func = get_func(v)
            graph = frequency_axes.plot(
                func,
                x_range=frequency_axes.x_range,
                color=fourier_graph.get_color()
            )
            shifted_graphs.add(graph)
        
        return shifted_graphs

    def get_sum_graph(self, axes, graphs):
        def sum_func(t):
            return sum([graph.underlying_function(t) for graph in graphs])
        
        return axes.plot(
            sum_func,
            x_range=axes.x_range,
            color=graphs[0].get_color()
        )
