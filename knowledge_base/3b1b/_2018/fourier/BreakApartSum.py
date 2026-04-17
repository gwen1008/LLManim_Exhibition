# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個由多個餘弦波疊加而成的複合波形，並將其分解為各個頻率分量，最後由角色思考分解的意義。



from manim import *
class BreakApartSum(Scene):
    def __init__(self, frequencies=[0.5, 1.5, 2, 2.5, 5], equilibrium_height=2.0, **kwargs):
        super().__init__(**kwargs)
        self.frequencies = frequencies
        self.equilibrium_height = equilibrium_height

    def construct(self):
        self.show_initial_sound()
        self.decompose_sound()
        self.ponder_question()

    def show_initial_sound(self):
        def func(x):
            return self.equilibrium_height + 0.2 * np.sum([
                np.cos(2 * np.pi * f * x)
                for f in self.frequencies
            ])
        
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1, 5, 1],
            x_length=FRAME_WIDTH - 2,
            y_length=3,
            axis_config={
                "include_tip": False,
            },
            x_axis_config={
                "unit_size": 2.0,
            },
            y_axis_config={
                "unit_size": 0.5,
            },
        )
        axes.center()
        axes.to_edge(LEFT)
        
        graph = axes.plot(func, x_range=[0, 5], color=YELLOW, use_smoothing=True)
        
        v_line = Line(ORIGIN, 4 * UP)
        v_line.move_to(axes.c2p(0, 0), DOWN)
        dot = Dot(color=PINK)
        dot.move_to(graph.point_from_proportion(0))

        self.add(axes, graph)
        self.play(
            v_line.animate.move_to(axes.c2p(5, 0)).align_to(axes.c2p(5, 0), DOWN),
            MoveAlongPath(dot, graph),
            run_time=8,
            rate_func=linear,
        )
        self.play(*[FadeOut(mob) for mob in [dot, v_line]])

        self.axes = axes
        self.graph = graph

    def decompose_sound(self):
        axes, graph = self.axes, self.graph

        pure_graphs = VGroup(*[
            axes.plot(
                lambda x: 0.5 * np.cos(2 * np.pi * freq * x),
                x_range=[0, 5],
                color=color,
                use_smoothing=True
            )
            for freq, color in zip(self.frequencies, color_gradient([BLUE, RED], len(self.frequencies)))
        ])
        pure_graphs.arrange(DOWN, buff=MED_LARGE_BUFF)
        h_line = DashedLine(6 * LEFT, 6 * RIGHT)

        self.play(
            FadeOut(axes),
            graph.animate.to_edge(UP)
        )
        pure_graphs.next_to(graph, DOWN, LARGE_BUFF)
        h_line.next_to(graph, DOWN, MED_LARGE_BUFF)
        self.play(Create(h_line))
        for pure_graph in reversed(pure_graphs):
            self.play(TransformFromCopy(graph, pure_graph))
        self.wait()

        self.all_graphs = VGroup(graph, h_line, pure_graphs)
        self.pure_graphs = pure_graphs

    def ponder_question(self):
        all_graphs = self.all_graphs
        pure_graphs = self.pure_graphs
        randy = Randolph()
        randy.to_corner(DOWN + LEFT)

        self.play(
            FadeIn(randy),
            all_graphs.animate.scale(0.75).to_corner(UP + RIGHT),
        )
        self.play(randy.animate.change("thinking", all_graphs))
        self.play(Blink(randy))
        rect = SurroundingRectangle(pure_graphs, color=WHITE)
        self.play(
            Create(rect),
            LaggedStart(*[
                ApplyFunction(
                    lambda m: m.shift(SMALL_BUFF * UP).set_color(YELLOW),
                    g
                )
                for g in pure_graphs
            ], lag_ratio=0.2, rate_func=wiggle)
        )
        self.play(FadeOut(rect))
        self.play(Blink(randy))
        self.wait()
