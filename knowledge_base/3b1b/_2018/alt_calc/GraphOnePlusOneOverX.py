# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 在坐標軸上繪製函數 y = 1 + 1/x 和 y = x 的圖形，並展示它們的交點（黃金比例 φ 及其共軛值）。


from manim import *
import numpy as np

class GraphOnePlusOneOverX(Scene):
    def __init__(
        self,
        x_min=-6,
        x_max=6,
        x_axis_width=12,
        y_min=-4,
        y_max=5,
        y_axis_height=8,
        y_axis_label=None,
        graph_origin=0.5 * DOWN,
        num_graph_anchor_points=100,
        func_graph_color=GREEN,
        identity_graph_color=BLUE,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_min = x_min
        self.x_max = x_max
        self.x_axis_width = x_axis_width
        self.y_min = y_min
        self.y_max = y_max
        self.y_axis_height = y_axis_height
        self.y_axis_label = y_axis_label
        self.graph_origin = graph_origin
        self.num_graph_anchor_points = num_graph_anchor_points
        self.func_graph_color = func_graph_color
        self.identity_graph_color = identity_graph_color

    def construct(self):
        self.add_title()
        self.setup_axes()
        self.draw_graphs()
        self.show_solutions()

    def add_title(self):
        title = self.title = MathTex(
            "\\text{Solve: }", "1 + \\frac{1}{x}", "=", "x",
        )
        # 設置顏色
        for part in title:
            if "x" in part.tex_string and "frac" not in part.tex_string:
                part.set_color(self.identity_graph_color)
            if "frac" in part.tex_string:
                part.set_color(self.func_graph_color)
        title.to_corner(UL)
        self.add(title)

    def setup_axes(self):
        # 創建坐標軸
        self.axes = Axes(
            x_range=[self.x_min, self.x_max, 2],
            y_range=[self.y_min, self.y_max, 2],
            x_length=self.x_axis_width,
            y_length=self.y_axis_height,
            axis_config={"include_numbers": False},
            x_axis_config={"numbers_to_include": list(range(-6, 0, 2)) + list(range(2, 7, 2))},
            y_axis_config={"numbers_to_include": list(range(-2, 0, 2)) + list(range(2, 4, 2))},
        )
        self.axes.shift(self.graph_origin)
        self.add(self.axes)

    def draw_graphs(self, animate=True):
        # 定義函數
        def func(x):
            return 1.0 + 1.0 / x
        
        # 創建兩個部分的函數圖形（避開 x=0）
        lower_func_graph = self.axes.plot(
            func,
            x_range=[-10, -0.1],
            color=self.func_graph_color,
            use_smoothing=True
        )
        upper_func_graph = self.axes.plot(
            func,
            x_range=[0.1, 10],
            color=self.func_graph_color,
            use_smoothing=True
        )
        func_graph = VGroup(lower_func_graph, upper_func_graph)
        
        # 添加函數標籤
        func_label = MathTex("y = 1 + \\frac{1}{x}")
        func_label.set_color(self.func_graph_color)
        func_label.next_to(
            self.axes.c2p(6, func(6)),
            UP
        )
        func_graph.label = func_label

        # 創建恆等函數圖形
        identity_graph = self.axes.plot(
            lambda x: x,
            x_range=[self.x_min, self.x_max],
            color=self.identity_graph_color
        )
        
        # 添加恆等函數標籤
        identity_label = MathTex("y = x")
        identity_label.set_color(self.identity_graph_color)
        identity_label.next_to(
            self.axes.c2p(3, 3),
            UL,
            buff=SMALL_BUFF
        )
        identity_graph.label = identity_label

        if animate:
            # 動畫顯示函數圖形
            self.play(
                Create(func_graph),
                Write(func_label),
                run_time=2
            )
            self.play(
                Create(identity_graph),
                Write(identity_label),
                run_time=2
            )
            self.wait()
        else:
            self.add(
                func_graph, func_label,
                identity_graph, identity_label,
            )

        self.func_graph = func_graph
        self.identity_graph = identity_graph
        self.func_label = func_label
        self.identity_label = identity_label

    def show_solutions(self):
        phi = 0.5 * (1 + np.sqrt(5))
        phi_bro = 0.5 * (1 - np.sqrt(5))

        lines = VGroup()
        for num in [phi, phi_bro]:
            line = DashedLine(
                self.axes.c2p(num, 0),
                self.axes.c2p(num, num),
                color=WHITE
            )
            line_copy = line.copy()
            line_copy.set_color(YELLOW)
            line.set_opacity(0.5)
            lines.add(line)
        
        phi_line, phi_bro_line = lines

        decimal_kwargs = {
            "num_decimal_places": 3,
            "include_sign": False,
            "color": YELLOW,
        }
        arrow_kwargs = {
            "buff": SMALL_BUFF,
            "color": WHITE,
            "tip_length": 0.15,
            "stroke_width": 2,
        }

        # φ 的標註
        phi_decimal = DecimalNumber(phi, **decimal_kwargs)
        phi_decimal.next_to(phi_line, DOWN, LARGE_BUFF)
        phi_arrow = Arrow(
            phi_decimal.get_top(),
            phi_line.get_bottom(),
            **arrow_kwargs
        )
        phi_label = MathTex("=", "\\varphi")
        phi_label.next_to(phi_decimal, RIGHT)
        phi_label[1].set_color(YELLOW)

        # φ' 的標註
        phi_bro_decimal = DecimalNumber(phi_bro, **decimal_kwargs)
        phi_bro_decimal.next_to(phi_bro_line, UP, LARGE_BUFF)
        phi_bro_decimal.shift(0.5 * LEFT)
        phi_bro_arrow = Arrow(
            phi_bro_decimal.get_bottom(),
            phi_bro_line.get_top(),
            **arrow_kwargs
        )

        # 文字說明
        brother_words = Tex("$\\varphi$'s little brother")
        brother_words.set_color_by_tex("$\\varphi$", YELLOW)
        brother_words.next_to(
            phi_bro_decimal,
            UP,
            buff=MED_SMALL_BUFF,
            aligned_edge=RIGHT
        )

        # 動畫序列
        self.play(Create(phi_line))
        self.play(
            Write(phi_decimal),
            GrowArrow(phi_arrow),
        )
        self.play(Write(phi_label))
        self.wait(3)
        
        self.play(Create(phi_bro_line))
        self.play(
            Write(phi_bro_decimal),
            GrowArrow(phi_bro_arrow),
        )
        self.wait(4)
        self.play(Write(brother_words))
        self.wait(8)
