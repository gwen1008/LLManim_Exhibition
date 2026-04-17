# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示傅立葉變換視覺化的縮圖，包含原始信號圖形、繞線圖形和傅立葉變換圖形，並用標籤和連接線標示對應關係。


from manim import *
import numpy as np

class Thumbnail(Scene):
    def construct(self):
        title = Tex("Fourier\\\\", "Visualized")
        title.set_color(YELLOW)
        title.set_stroke(RED, 2)
        title.scale(2.5)
        title.add_background_rectangle()

        def func(t):
            return np.cos(2*TAU*t) + np.cos(3*TAU*t) + np.cos(5*t)
        
        # 定義傅立葉變換函數（簡化版本）
        def fourier(f):
            # 簡化的傅立葉變換計算
            t_vals = np.linspace(-5, 5, 1000)
            dt = t_vals[1] - t_vals[0]
            integral = np.sum(func(t_vals) * np.exp(-complex(0, TAU*f*t_vals))) * dt
            return abs(integral)
        
        # 創建原始函數圖形
        graph = FunctionGraph(
            func,
            x_range=[-5, 5, 0.01],
            color=BLUE
        )
        graph.stretch_to_fit_height(2)
        graph.stretch_to_fit_width(10)
        graph.set_stroke(width=6)
        
        # 創建傅立葉變換圖形
        fourier_graph = FunctionGraph(
            lambda x: fourier(x),
            x_range=[0, 6, 0.01],
            color=YELLOW
        )
        fourier_graph.stretch_to_fit_height(2)
        fourier_graph.stretch_to_fit_width(10)
        fourier_graph.set_stroke(width=6)

        # 創建繞線圖形組
        pol_graphs = VGroup()
        for f in np.linspace(1.98, 2.02, 5):
            def param_func(t, f=f):
                r = 2 + np.cos(2*TAU*t) + np.cos(3*TAU*t)
                x = r * np.cos(-TAU*f*t)
                y = r * np.sin(-TAU*f*t)
                return np.array([x, y, 0])
            
            pol_graph = ParametricFunction(
                param_func,
                t_range=[-5, 5, 0.01],
                color=BLUE
            )
            pol_graph.stretch_to_fit_height(2)
            pol_graphs.add(pol_graph)
        
        # 設置繞線圖形組的樣式
        pol_graphs.arrange(RIGHT, buff=LARGE_BUFF)
        pol_graphs.set_color_by_gradient(BLUE_C, TEAL, GREEN)
        pol_graphs.match_width(graph)
        pol_graphs.set_stroke(width=1)

        # 組合所有部分
        parts = VGroup(graph, pol_graphs, fourier_graph)
        parts[1].set_width(parts[0].get_width() - 1)
        parts.arrange(
            DOWN, buff=LARGE_BUFF,
            aligned_edge=RIGHT
        )
        parts.to_edge(RIGHT)
        self.add(parts)

        # 添加標籤
        words = VGroup(TexText("Signal"), TexText("Winding"), TexText("Transform"))
        for word, part in zip(words, parts):
            word.scale(1.5)
            word.next_to(part, LEFT)
            word.to_edge(LEFT, buff=MED_LARGE_BUFF)

        self.add(words)

        # 添加連接線和標記
        rect = SurroundingRectangle(pol_graphs[2])
        rect.set_stroke(RED, 2)
        
        # 計算傅立葉圖形上的點
        t_param = 2 / 6
        fourier_point = fourier_graph.point_from_proportion(t_param)
        dot = Dot(fourier_point, color=RED)
        dot.set_stroke(BLACK, 3, background=True)
        dot.shift(0.01 * RIGHT)
        
        line = Line(dot.get_center(), rect.get_corner(DL), buff=0.1)
        line.set_stroke(RED, 2)

        self.add(dot, line, rect)
