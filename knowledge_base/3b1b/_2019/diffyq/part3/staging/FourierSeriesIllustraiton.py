# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示傅立葉級數如何將一系列正弦波疊加逼近一個階梯函數，並在兩個坐標軸之間用箭頭連接，同時顯示對應的數學公式。


from manim import *
import itertools as it
import numpy as np

class FourierSeriesIllustraiton(Scene):
    def __init__(
        self,
        n_range=range(1, 31, 2),
        axes_config={
            "axis_config": {
                "include_tip": False,
            },
            "x_axis_config": {
                "tick_frequency": 1 / 4,
                "unit_size": 4,
            },
            "x_range": [0, 1],
            "y_range": [-1, 1],
        },
        colors=[BLUE, GREEN, RED, YELLOW, PINK],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.n_range = n_range
        self.axes_config = axes_config
        self.colors = colors

    def construct(self):
        aaa_group = self.get_axes_arrow_axes()
        aaa_group.shift(2 * UP)
        # shift_onto_screen 在 CE 中通常不需要
        axes1, arrow, axes2 = aaa_group

        axes2.add(self.get_target_func_graph(axes2))

        sine_graphs = self.get_sine_graphs(axes1)
        partial_sums = self.get_partial_sums(axes1, sine_graphs)

        sum_tex = self.get_sum_tex()
        sum_tex.next_to(axes1, DOWN, buff=LARGE_BUFF)
        sum_tex.shift(RIGHT)
        eq = MathTex("=")
        target_func_tex = self.get_target_func_tex()
        target_func_tex.next_to(axes2, DOWN)
        target_func_tex.match_y(sum_tex)
        eq.move_to(midpoint(
            target_func_tex.get_left(),
            sum_tex.get_right()
        ))

        range_words = TexText(
            "For $0 \\le x \\le 1$"
        )
        range_words.next_to(
            VGroup(sum_tex, target_func_tex),
            DOWN,
        )

        rects = it.chain(
            [
                SurroundingRectangle(piece)
                for piece in self.get_sum_tex_pieces(sum_tex)
            ],
            it.cycle([None])
        )

        self.add(axes1, arrow, axes2)
        self.add(sum_tex, eq, target_func_tex)
        self.add(range_words)

        curr_partial_sum = axes1.plot(lambda x: 0)
        curr_partial_sum.set_stroke(width=1)
        for sine_graph, partial_sum, rect in zip(sine_graphs, partial_sums, rects):
            anims1 = [
                Create(sine_graph)
            ]
            partial_sum.set_stroke(BLACK, 4, background=True)
            anims2 = [
                curr_partial_sum.animate.set_stroke(width=1, opacity=0.5),
                curr_partial_sum.animate.set_stroke(width=0, background=True),
                ReplacementTransform(
                    sine_graph, partial_sum,
                    remover=True
                ),
            ]
            if rect:
                rect.match_style(sine_graph)
                anims1.append(Create(rect))
                anims2.append(FadeOut(rect))
            self.play(*anims1)
            self.play(*anims2)
            curr_partial_sum = partial_sum

    def get_axes_arrow_axes(self):
        axes1 = Axes(**self.axes_config)
        # 在 CE 中，add_numbers 方法已棄用，改用 add_labels
        # 這裡簡化處理，只添加必要的刻度標籤
        axes1.add(axes1.get_x_axis_label("x"))
        axes1.add(axes1.get_y_axis_label("y"))
        axes2 = axes1.copy()

        arrow = Arrow(LEFT, RIGHT, color=WHITE)
        group = VGroup(axes1, arrow, axes2)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        return group

    def get_sine_graphs(self, axes):
        sine_graphs = VGroup(*[
            axes.plot(self.generate_nth_func(n))
            for n in self.n_range
        ])
        sine_graphs.set_stroke(width=3)
        for graph, color in zip(sine_graphs, it.cycle(self.colors)):
            graph.set_color(color)
        return sine_graphs

    def get_partial_sums(self, axes, sine_graphs):
        partial_sums = VGroup(*[
            axes.plot(self.generate_kth_partial_sum_func(k + 1))
            for k in range(len(self.n_range))
        ])
        partial_sums.match_style(sine_graphs)
        return partial_sums

    def get_sum_tex(self):
        return MathTex(
            "\\frac{4}{\\pi} \\left(",
            "\\frac{\\cos(\\pi x)}{1}",
            "-\\frac{\\cos(3\\pi x)}{3}",
            "+\\frac{\\cos(5\\pi x)}{5}",
            "- \\cdots \\right)"
        ).scale(0.75)

    def get_sum_tex_pieces(self, sum_tex):
        return sum_tex[1:4]

    def get_target_func_tex(self):
        step_tex = MathTex(
            """
            1 \\quad \\text{if } x < 0.5 \\\\
            0 \\quad \\text{if } x = 0.5 \\\\
            -1 \\quad \\text{if } x > 0.5 \\\\
            """
        )
        lb = Brace(step_tex, LEFT, buff=SMALL_BUFF)
        step_tex.add(lb)
        return step_tex

    def get_target_func_graph(self, axes):
        # 使用自定義函數繪製階梯函數
        def step_func(x):
            if x < 0.5:
                return 1
            elif x > 0.5:
                return -1
            else:
                return 0
        
        graph = axes.plot(step_func, color=YELLOW, stroke_width=3)
        # 添加不連續點
        dot = Dot(axes.c2p(0.5, 0), color=graph.get_color())
        dot.scale(0.5)
        graph.add(dot)
        return graph

    def generate_nth_func(self, n):
        return lambda x: np.prod([
            (4 / PI),
            (1 / n) * (-1)**((n - 1) / 2),
            np.cos(PI * n * x)
        ])

    def generate_kth_partial_sum_func(self, k):
        return lambda x: np.sum([
            self.generate_nth_func(n)(x)
            for n in list(self.n_range)[:k]
        ])
