# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示在受限邊界條件下，不同頻率的餘弦波在坐標軸上的動態繪製過程。


from manim import *
import numpy as np

class WhichWavesAreAvailable(Scene):
    def __init__(
        self,
        axes_config=None,
        n_axes=5,
        trig_func=np.cos,
        trig_func_tex="\\cos",
        bc_words="Restricted by\\\\boundary conditions",
        **kwargs
    ):
        super().__init__(**kwargs)
        if axes_config is None:
            axes_config = {
                "x_range": [0, TAU],
                "y_range": [-1.5, 1.5],
                "x_length": 1,
                "y_length": 1,
                "axis_config": {
                    "stroke_width": 2,
                    "include_tip": False,
                },
                "x_axis_config": {
                    "tick_frequency": PI / 2,
                },
                "y_axis_config": {
                    "tick_frequency": 0.5,
                },
            }
        self.axes_config = axes_config
        self.n_axes = n_axes
        self.trig_func = trig_func
        self.trig_func_tex = trig_func_tex
        self.bc_words = bc_words

    def construct(self):
        self.setup_little_axes()
        self.show_cosine_waves()

    def setup_little_axes(self):
        axes_group = VGroup(*[
            Axes(**self.axes_config)
            for n in range(self.n_axes)
        ])
        axes_group.set_stroke(width=2)
        axes_group.arrange(DOWN, buff=1)
        axes_group.set_height(config.frame_height - 1.25)
        axes_group.to_edge(RIGHT)
        axes_group.to_edge(UP, buff=MED_SMALL_BUFF)
        dots = Tex("\\vdots")
        dots.next_to(axes_group, DOWN)
        dots.shift_onto_screen()

        self.add(axes_group)
        self.add(dots)

        self.axes_group = axes_group

    def show_cosine_waves(self):
        axes_group = self.axes_group
        colors = [BLUE, GREEN, RED, YELLOW, PINK]

        graphs = VGroup()
        h_lines = VGroup()
        func_labels = VGroup()
        for k, axes, color in zip(range(1, len(axes_group)+1), axes_group, colors):
            L = axes.x_range[1]  # x_max
            graph = axes.plot(
                lambda x: self.trig_func(x * k * PI / L),
                color=color
            )
            graph.set_stroke(width=2)
            graphs.add(graph)

            func_label = MathTex(
                self.trig_func_tex + "\\left(",
                str(k),
                "(\\pi / L)x\\right)",
                tex_to_color_map={
                    str(k): color,
                }
            )
            func_label.scale(0.7)
            func_label.next_to(axes, LEFT)
            func_labels.add(func_label)

            hl1 = DashedLine(LEFT, RIGHT)
            hl1.set_length(0.5)
            hl1.set_stroke(WHITE, 2)
            hl1.move_to(graph.get_start())
            hl2 = hl1.copy()
            hl2.move_to(graph.get_end())
            h_lines.add(hl1, hl2)

        words = Tex(self.bc_words)
        words.next_to(axes_group, LEFT)
        words.to_edge(UP)

        self.play(
            FadeIn(words),
            LaggedStartMap(
                Create, graphs,
            )
        )
        self.play(Write(h_lines))
        self.play(FadeOut(h_lines))
        self.wait()
        self.play(
            words.animate.next_to(func_labels, LEFT),
            words.animate.to_edge(UP),
            LaggedStartMap(
                FadeIn, func_labels,
                lag_ratio=0.1,
                shift=RIGHT
            )
        )
        self.wait()
