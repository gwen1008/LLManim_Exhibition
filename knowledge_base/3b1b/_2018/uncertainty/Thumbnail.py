# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示量子力學中不確定性原理的視覺化縮圖，包含高斯波包、傅立葉變換圖形和機率點雲，並以交叉和「NOT」文字強調原理的非直覺性。


from manim import *
import numpy as np

class Thumbnail(Scene):
    def construct(self):
        uncertainty_principle = Text("Uncertainty\nprinciple", font_size=72)
        uncertainty_principle[1].shift(SMALL_BUFF * UP)
        quantum = Text("Quantum", font_size=72)
        VGroup(uncertainty_principle, quantum).scale(2.5)
        uncertainty_principle.to_edge(UP, buff=MED_LARGE_BUFF)
        quantum.to_edge(DOWN, buff=MED_LARGE_BUFF)

        arrow = MathTex("\\Downarrow")
        arrow.scale(4)
        arrow.move_to(Line(
            uncertainty_principle.get_bottom(),
            quantum.get_top(),
        ))

        cross = Cross(arrow)
        cross.set_stroke(RED, 20)

        is_word, not_word = is_not = Text("is NOT", font_size=72)
        is_not.scale(3)
        is_word.move_to(arrow)
        not_word.set_color(RED)
        not_word.set_stroke(RED, 3)
        not_word.rotate(10 * DEGREES, about_edge=DOWN + LEFT)
        not_word.next_to(is_word, DOWN, buff=0.1 * SMALL_BUFF)

        # 創建點雲（ManimCE 中沒有 ProbabalisticDotCloud，用 DotCloud 替代）
        dot_cloud = DotCloud(
            points=np.random.randn(1000, 3) * 0.5,
            color=BLUE,
        )
        dot_cloud.scale(2)
        dot_cloud.rotate(25 * DEGREES)
        dot_cloud.move_to(quantum)

        def get_func(a):
            return lambda t: 0.5 * np.exp(-a * t**2) * np.cos(TAU * t)
        
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-1, 1, 0.5],
            x_length=3,
            y_length=1.5,
        )
        graphs = VGroup(*[
            axes.plot(get_func(a), color=BLUE)
            for a in (10, 3, 1, 0.3, 0.1,)
        ])
        graphs.arrange(DOWN, buff=0.6)
        graphs.to_corner(UL)
        graphs.set_color_by_gradient(BLUE_B, BLUE_D)

        frequency_axes = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 1, 0.5],
            x_length=2,
            y_length=1,
        )
        
        # 定義傅立葉變換圖形（簡化版本）
        def get_fourier_graph(axes, func, t_min=-10, t_max=10):
            # 這裡使用簡化的高斯函數近似傅立葉變換
            return axes.plot(
                lambda x: np.exp(-x**2),
                x_range=[0, 2],
                color=GREEN,
            )
        
        fourier_graphs = VGroup(*[
            get_fourier_graph(frequency_axes, graph.underlying_function)
            for graph in graphs
        ])
        
        for graph, fourier_graph in zip(graphs, fourier_graphs):
            fourier_graph.scale(3)
            fourier_graph.stretch(3, 1)
            fourier_graph.move_to(graph)
            fourier_graph.to_edge(RIGHT)

        self.add(graphs, fourier_graphs)
        self.add(dot_cloud)
        self.add(uncertainty_principle, quantum)
        self.add(arrow, cross)
        self.add(is_not)
