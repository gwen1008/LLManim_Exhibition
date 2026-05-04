# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一維輸入區域及其邊界對應的輸出值，並動態繪製多條平滑曲線連接這些邊界點。


from manim import *
import numpy as np
import itertools as it

class OneDRegionBoundary(Scene):
    def __init__(self, graph_color=BLUE, region_rect_height=0.1, **kwargs):
        super().__init__(**kwargs)
        self.graph_color = graph_color
        self.region_rect_height = region_rect_height

    def construct(self):
        x0 = self.x0 = 3 
        x1 = self.x1 = 6
        fx0 = self.fx0 = -2
        fx1 = self.fx1 = 2

        axes = self.axes = Axes(
            x_range=[-1, 10],
            y_range=[-3, 3],
            axis_config={"stroke_width": 2}
        )
        axes.center()
        axes.set_stroke(width=2)

        input_word = Text("Input")
        input_word.next_to(axes.x_axis, UP, buff=SMALL_BUFF).align_to(axes.x_axis, RIGHT)
        output_word = Text("Output")
        output_word.next_to(axes.y_axis, UP)
        axes.add(input_word, output_word)
        self.add(axes)

        graph = self.get_graph_part(1, 1)
        alt_graphs = [
            self.get_graph_part(*points)
            for points in [
                (-1, -2),
                (-1, -1, -1),
                (1, 1, 1),
                (-0.75, 0, 1.75),
                (-3, -2, -1),
            ]
        ]

        # Region and boundary
        line = Line(axes.c2p(x0, 0), axes.c2p(x1, 0))
        region = Rectangle(
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.5,
            height=self.region_rect_height
        )
        region.match_width(line, stretch=True)
        region.move_to(line)

        region_words = Text("Input region")
        region_words.set_width(0.8*region.get_width())
        region_words.next_to(region, UP)

        x0_arrow, x1_arrow = arrows = VGroup(*[
            Arrow(
                axes.c2p(x, 0),
                axes.c2p(x, fx),
                color=color,
                buff=0
            )
            for x, fx, color in [(x0, fx0, RED), (x1, fx1, GREEN)]
        ])
        minus = MathTex("-")
        minus.set_color(x0_arrow.get_color())
        minus.next_to(x0_arrow, UP)
        plus = MathTex("+")
        plus.set_color(x1_arrow.get_color())
        plus.next_to(x1_arrow, DOWN)
        signs = VGroup(plus, minus)

        self.play(
            GrowFromCenter(region),
            FadeIn(region_words)
        )
        self.wait()
        self.play(*it.chain(
            list(map(GrowArrow, arrows)),
            list(map(Write, signs))
        ))
        self.wait()
        self.play(
            Create(graph), 
            FadeOut(region_words),
        )
        self.wait()
        for alt_graph in alt_graphs + alt_graphs:
            self.play(Transform(graph, alt_graph, path_arc=0.1*TAU))
        self.wait()

    def get_graph_part(self, *interim_values):
        result = VMobject()
        result.set_stroke(self.graph_color, 3)
        result.set_fill(opacity=0)
        values = [self.fx0] + list(interim_values) + [self.fx1]
        result.set_points_smoothly([
            self.axes.c2p(x, fx)
            for x, fx in zip(
                np.linspace(self.x0, self.x1, len(values)),
                values
            )
        ])
        return result
