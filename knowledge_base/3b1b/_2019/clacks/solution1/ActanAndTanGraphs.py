# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示恆等函數、反正切函數和正切函數在同一坐標系中的圖形，並用垂直虛線動態演示反正切和正切函數的變化。


from manim import *
import numpy as np

class ActanAndTanGraphs(Scene):
    def __init__(
        self,
        x_min=-PI / 8,
        x_max=5 * PI / 8,
        y_min=-PI / 8,
        y_max=4 * PI / 8,
        x_tick_frequency=PI / 8,
        x_leftmost_tick=-PI / 8,
        y_tick_frequency=PI / 8,
        y_leftmost_tick=-PI / 8,
        x_axis_width=10,
        y_axis_height=7,
        graph_origin=2.5 * DOWN + 5 * LEFT,
        num_graph_anchor_points=500,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.x_tick_frequency = x_tick_frequency
        self.x_leftmost_tick = x_leftmost_tick
        self.y_tick_frequency = y_tick_frequency
        self.y_leftmost_tick = y_leftmost_tick
        self.x_axis_width = x_axis_width
        self.y_axis_height = y_axis_height
        self.graph_origin = graph_origin
        self.num_graph_anchor_points = num_graph_anchor_points

    def construct(self):
        # 創建坐標軸
        axes = Axes(
            x_range=[self.x_min, self.x_max, self.x_tick_frequency],
            y_range=[self.y_min, self.y_max, self.y_tick_frequency],
            x_length=self.x_axis_width,
            y_length=self.y_axis_height,
            axis_config={"include_numbers": False},
        ).shift(self.graph_origin)
        
        # 添加刻度標籤
        labels = VGroup(
            MathTex("\\pi / 8"),
            MathTex("\\pi / 4"),
            MathTex("3\\pi / 8"),
            MathTex("\\pi / 2"),
        )
        for n, label in enumerate([1, 2, 3, 4], start=1):
            label.scale(0.75)
            label.next_to(axes.c2p(n * PI / 8, 0), DOWN)
            self.add(label)

        # 創建函數圖形
        id_graph = axes.plot(lambda x: x, x_range=[self.x_min, 1.5], color=BLUE)
        arctan_graph = axes.plot(np.arctan, x_range=[self.x_min, 1.5], color=GREEN)
        tan_graph = axes.plot(np.tan, x_range=[self.x_min, 1.5], color=RED)
        graphs = VGroup(id_graph, arctan_graph, tan_graph)

        # 創建函數標籤
        id_label = MathTex("f(x) = x").set_color(BLUE)
        arctan_label = MathTex("\\arctan(x)").set_color(GREEN)
        tan_label = MathTex("\\tan(x)").set_color(RED)
        labels = VGroup(id_label, arctan_label, tan_label)
        
        # 定位標籤
        for label, graph in zip(labels, graphs):
            label.next_to(graph.get_end(), RIGHT)
            if label.get_bottom()[1] > config.frame_height / 2:
                label.next_to(graph.point_from_proportion(0.75), LEFT)

        # 創建動態垂直線
        arctan_x_tracker = ValueTracker(3 * PI / 8)
        arctan_v_line = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(arctan_x_tracker.get_value(), self.y_min),
                end=axes.c2p(arctan_x_tracker.get_value(), 
                           np.arctan(arctan_x_tracker.get_value())),
                color=WHITE
            )
        )
        
        tan_x_tracker = ValueTracker(2 * PI / 8)
        tan_v_line = always_redraw(
            lambda: DashedLine(
                start=axes.c2p(tan_x_tracker.get_value(), self.y_min),
                end=axes.c2p(tan_x_tracker.get_value(), 
                           np.tan(tan_x_tracker.get_value())),
                color=WHITE
            )
        )

        # 動畫序列
        self.add(axes)
        self.play(
            Create(id_graph),
            Write(id_label)
        )
        self.play(
            Create(arctan_graph),
            Write(arctan_label)
        )
        self.add(arctan_v_line)
        self.play(arctan_x_tracker.animate.set_value(0), run_time=2)
        self.wait()
        self.play(
            TransformFromCopy(arctan_graph, tan_graph),
            TransformFromCopy(arctan_label, tan_label),
        )
        self.add(tan_v_line)
        self.play(tan_x_tracker.animate.set_value(0), run_time=2)
        self.wait()
