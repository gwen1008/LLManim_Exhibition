# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示如何將不同頻率的正弦波疊加，形成複雜的波形，並在坐標軸上可視化這個過程。


from manim import *
import numpy as np

class AddingPureFrequencies(PiCreatureScene):
    def __init__(
        self,
        A_frequency=2.1,
        A_color=YELLOW,
        D_color=PINK,
        F_color=TEAL,
        C_color=RED,
        sum_color=GREEN,
        equilibrium_height=1.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.A_frequency = A_frequency
        self.A_color = A_color
        self.D_color = D_color
        self.F_color = F_color
        self.C_color = C_color
        self.sum_color = sum_color
        self.equilibrium_height = equilibrium_height

    def construct(self):
        self.add_speaker()
        self.play_A440()
        self.measure_air_pressure()
        self.play_lower_pitch()
        self.play_mix()
        self.separate_out_parts()
        self.draw_sum_at_single_point()
        self.draw_full_sum()
        self.add_more_notes()

    def add_speaker(self):
        speaker = SVGMobject(file_name="speaker")
        speaker.to_edge(DOWN)

        self.add(speaker)
        self.speaker = speaker

    def play_A440(self):
        randy = self.pi_creature
        A_label = Text("A440")
        A_label.set_color(self.A_color)
        A_label.next_to(self.speaker, UP)

        self.broadcast(
            FadeIn(A_label),
            Succession(
                randy.animate.change("pondering"),
                Animation(randy),
                Blink(randy)
            )
        )

        self.A_label = A_label

    def measure_air_pressure(self):
        randy = self.pi_creature
        axes = Axes(
            y_range=[-2, 2],
            x_range=[0, 10],
            axis_config={"include_tip": False},
        )
        axes.stretch_to_fit_height(2)
        axes.to_corner(UP+LEFT)
        axes.shift(LARGE_BUFF*DOWN)
        eh = self.equilibrium_height
        equilibrium_line = DashedLine(
            axes.c2p(0, eh),
            axes.c2p(axes.x_range[1], eh),
            stroke_width=2,
            stroke_color=GREY_B
        )

        frequency = self.A_frequency
        graph = self.get_wave_graph(frequency, axes)
        func = graph.underlying_function
        graph.set_color(self.A_color)
        pressure = Text("Pressure")
        time = Text("Time")
        for label in pressure, time:
            label.scale(0.8)
        pressure.next_to(axes.y_axis, UP)
        pressure.to_edge(LEFT, buff=MED_SMALL_BUFF)
        time.next_to(axes.x_axis.get_right(), DOWN+LEFT)
        axes.labels = VGroup(pressure, time)

        n = 10
        brace = Brace(Line(
            axes.c2p(n/frequency, func(n/frequency)),
            axes.c2p((n+1)/frequency, func((n+1)/frequency)),
        ), UP)
        words = brace.get_text("Imagine 440 per second", buff=SMALL_BUFF)
        words.scale(0.8, about_point=words.get_bottom())

        self.play(
            FadeIn(pressure),
            Create(axes.y_axis)
        )
        self.play(
            Write(time),
            Create(axes.x_axis)
        )
        self.broadcast(
            Create(graph, run_time=4, rate_func=linear),
            Create(equilibrium_line),
        )
        axes.add(equilibrium_line)
        self.play(
            randy.animate.change("erm", graph),
            GrowFromCenter(brace),
            Write(words)
        )
        self.wait()
        graph.save_state()
        self.play(
            FadeOut(brace),
            FadeOut(words),
            VGroup(axes, graph, axes.labels).animate.shift(0.8*UP),
            graph.animate.set_opacity(0.15).shift(0.8*UP),
        )

        graph.saved_state.move_to(graph)
        self.axes = axes
        self.A_graph = graph

    def play_lower_pitch(self):
        axes = self.axes
        randy = self.pi_creature

        frequency = self.A_frequency*(2.0/3.0)
        graph = self.get_wave_graph(frequency, axes)
        graph.set_color(self.D_color)

        D_label = Text("D294")
        D_label.set_color(self.D_color)
        D_label.move_to(self.A_label)

        self.play(
            FadeOut(self.A_label),
            GrowFromCenter(D_label),
        )
        self.broadcast(
            Create(graph, run_time=4, rate_func=linear),
            randy.animate.change("happy"),
            n_circles=6,
        )
        self.play(randy.animate.change("confused", graph))
        self.wait(2)

        self.D_label = D_label
        self.D_graph = graph

    def play_mix(self):
        self.A_graph.restore()
        self.broadcast(
            self.get_broadcast_animation(n_circles=6),
            self.pi_creature.animate.change("thinking"),
            *[
                Create(graph, run_time=4, rate_func=linear)
                for graph in (self.A_graph, self.D_graph)
            ]
        )
        self.wait()

    def separate_out_parts(self):
        axes = self.axes
        speaker = self.speaker
        randy = self.pi_creature

        A_axes = axes.copy()
        A_graph = self.A_graph
        A_label = self.A_label
        D_axes = axes.copy()
        D_graph = self.D_graph
        D_label = self.D_label
        movers = [A_axes, A_graph, A_label, D_axes, D_graph, D_label]
        for mover in movers:
            mover.generate_target()
        D_target_group = VGroup(D_axes.target, D_graph.target)
        A_target_group = VGroup(A_axes.target, A_graph.target)
        D_target_group.next_to(axes, DOWN, MED_LARGE_BUFF)
        A_target_group.next_to(D_target_group, DOWN, MED_LARGE_BUFF)
        A_label.set_opacity(0)
        A_label.target.next_to(A_graph.target, UP)
        D_label.target.next_to(D_graph.target, UP)

        self.play(*[
            MoveToTarget(mover) for mover in movers
        ] + [
            mob.animate.shift(FRAME_HEIGHT*DOWN)
            for mob in (randy, speaker)
        ])
        self.remove(randy, speaker)
        self.wait()

        self.A_axes = A_axes
        self.D_axes = D_axes

    def draw_sum_at_single_point(self):
        axes = self.axes
        A_axes = self.A_axes
        D_axes = self.D_axes
        A_graph = self.A_graph
        D_graph = self.D_graph

        x = 2.85
        A_line = self.get_A_graph_v_line(x)
        D_line = self.get_D_graph_v_line(x)
        lines = VGroup(A_line, D_line)
        sum_lines = lines.copy()
        sum_lines.generate_target()
        self.stack_v_lines(x, sum_lines.target)

        top_axes_point = axes.c2p(x, self.equilibrium_height)
        x_point = np.array(top_axes_point)
        x_point[1] = 0
        v_line = Line(UP, DOWN).scale(FRAME_HEIGHT/2).move_to(x_point)

        self.revert_to_original_skipping_status()
        self.play(GrowFromCenter(v_line))
        self.play(FadeOut(v_line))
        self.play(*[Create(line) for line in lines])
        self.wait()
        self.play(MoveToTarget(sum_lines, path_arc=np.pi/4))
        self.wait(2)
        self.lines_to_fade = VGroup(A_line, D_line, sum_lines)

    def draw_full_sum(self):
        axes = self.axes

        def new_func(x):
            result = self.A_graph.underlying_function(x)
            result += self.D_graph.underlying_function(x)
            result -= self.equilibrium_height
            return result

        sum_graph = axes.plot(new_func)
        sum_graph.set_color(self.sum_color)
        thin_sum_graph = sum_graph.copy().set_opacity(0.3)

        A_graph = self.A_graph
        D_graph = self.D_graph
        D_axes = self.D_axes

        rect = Rectangle(
            height=2.5*FRAME_HEIGHT/2,
            width=MED_SMALL_BUFF,
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.4
        )

        self.play(
            ReplacementTransform(A_graph.copy(), thin_sum_graph),
            ReplacementTransform(D_graph.copy(), thin_sum_graph),
        )
        self.play(
            self.get_graph_line_animation(self.A_axes, self.A_graph),
            self.get_graph_line_animation(self.D_axes, self.D_graph),
            self.get_graph_line_animation(axes, sum_graph.copy()),
            Create(sum_graph),
            run_time=15,
            rate_func=linear
        )
        self.remove(thin_sum_graph)
        self.wait()
        for x in [2.85, 3.57]:
            rect.move_to(D_axes.c2p(x, 0))
            self.play(GrowFromPoint(rect, rect.get_top()))
            self.wait()
            self.play(FadeOut(rect))

        self.sum_graph = sum_graph

    def add_more_notes(self):
        axes = self.axes

        A_group = VGroup(self.A_axes, self.A_graph, self.A_label)
        D_group = VGroup(self.D_axes, self.D_graph, self.D_label)
        squish_group = VGroup(A_group, D_group)
        squish_group.generate_target()
        squish_group.target.stretch(0.5, 1)
        squish_group.target.next_to(axes, DOWN, buff=-SMALL_BUFF)
        for group in squish_group.target:
            label = group[-1]
            bottom = label.get_bottom()
            label.stretch(0.5, 0)
            label.move_to(bottom, DOWN)

        self.play(
            MoveToTarget(squish_group),
            FadeOut(self.lines_to_fade),
        )

        F_axes = self.D_axes.copy()
        C_axes = self.A_axes.copy()
        VGroup(F_axes, C_axes).next_to(squish_group, DOWN)
        F_graph = self.get_wave_graph(self.A_frequency*4.0/5, F_axes)
        F_graph.set_color(self.F_color)
        C_graph = self.get_wave_graph(self.A_frequency*6.0/5, C_axes)
        C_graph.set_color(self.C_color)

        F_label = Text("F349")
        C_label = Text("C523")
        for label, graph in (F_label, F_graph), (C_label, C_graph):
            label.scale(0.5)
            label.set_color(graph.get_color())
            label.next_to(graph, UP, SMALL_BUFF)

        graphs = VGroup(self.A_graph, self.D_graph, F_graph, C_graph)
        def new_sum_func(x):
            result = sum([
                graph.underlying_function(x) - self.equilibrium_height
                for graph in graphs
            ])
            result *= 0.5
            return result + self.equilibrium_height
        new_sum_graph = axes.plot(
            new_sum_func,
            use_smoothing=False
        )
        new_sum_graph.set_color(BLUE_C)
        thin_new_sum_graph = new_sum_graph.copy().set_opacity(0.3)

        self.play(*[
            Create(mob) for mob in [F_axes, C_axes, F_graph, C_graph]
        ] + [
            Write(mob) for mob in [F_label, C_label]
        ] + [
            FadeOut(self.sum_graph)
        ])
        self.play(ReplacementTransform(
            graphs.copy(), thin_new_sum_graph
        ))
        kwargs = {"rate_func": linear, "run_time": 10}
        self.play(Create(new_sum_graph.copy(), **kwargs), *[
            self.get_graph_line_animation(curr_axes, graph, **kwargs)
            for curr_axes, graph in [
                (self.A_axes, self.A_graph),
                (self.D_axes, self.D_graph),
                (F_axes, F_graph),
                (C_axes, C_graph),
                (axes, new_sum_graph),
            ]
        ])
        self.wait()

    ####

    def broadcast(self, *added_anims, **kwargs):
        self.play(self.get_broadcast_animation(**kwargs), *added_anims)

    def get_broadcast_animation(self, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 5)
        kwargs["n_circles"] = kwargs.get("n_circles", 10)
        return Broadcast(self.speaker[1], **kwargs)

    def get_wave_graph(self, frequency, axes):
        tail_len = 3.0
        x_min, x_max = axes.x_range[0], axes.x_range[1]
        def func(x):
            value = 0.7*np.cos(2*np.pi*frequency*x)
            if x - x_min < tail_len:
                value *= smooth((x-x_min)/tail_len)
            if x_max - x < tail_len:
                value *= smooth((x_max - x)/tail_len)
            return value + self.equilibrium_height
        ngp = 2*(x_max - x_min)*frequency + 1
        graph = axes.plot(func, use_smoothing=False)
        graph.underlying_function = func
        return graph

    def get_A_graph_v_line(self, x):
        return self.get_graph_v_line(x, self.A_axes, self.A_graph)

    def get_D_graph_v_line(self, x):
        return self.get_graph_v_line(x, self.D_axes, self.D_graph)

    def get_graph_v_line(self, x, axes, graph):
        result = Line(
            axes.c2p(x, self.equilibrium_height),
            graph.point_from_proportion(float(x)/axes.x_range[1]),
            color=WHITE,
            buff=0,
        )
        return result

    def stack_v_lines(self, x, lines):
        point = self.axes.c2p(x, self.equilibrium_height)
        A_line, D_line = lines
        A_line.shift(point - A_line.get_start())
        D_line.shift(A_line.get_end()-D_line.get_start())
        A_line.set_color(self.A_color)
        D_line.set_color(self.D_color)
        return lines

    def create_pi_creature(self):
        return Randolph().to_corner(DOWN+LEFT)

    def get_graph_line_animation(self, axes, graph, **kwargs):
        line = self.get_graph_v_line(0, axes, graph)
        x_max = axes.x_range[1]
        def update_line(line, alpha):
            x = alpha*x_max
            new_line = self.get_graph_v_line(x, axes, graph)
            line.become(new_line)
            return line

        return UpdateFromAlphaFunc(line, update_line, **kwargs)
