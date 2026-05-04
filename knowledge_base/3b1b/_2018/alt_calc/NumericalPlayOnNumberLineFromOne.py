# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個紅點在數線上從 1 開始，反覆套用函數 x → 1 + 1/x 進行跳躍，最終趨近於黃金比例 φ 的動態過程。


from manim import *
import numpy as np

class NumericalPlayOnNumberLineFromOne(Scene):
    def __init__(self, starting_value=1, n_jumps=10, func=None, number_line_config=None, **kwargs):
        super().__init__(**kwargs)
        self.starting_value = starting_value
        self.n_jumps = n_jumps
        if func is None:
            self.func = lambda x: 1 + 1.0 / x
        else:
            self.func = func
        if number_line_config is None:
            self.number_line_config = {
                "x_range": [0, 2, 0.25],
                "length": 12,
                "include_numbers": True,
                "numbers_with_elongated_ticks": [0, 1, 2],
            }
        else:
            # 轉換舊的配置格式
            config = number_line_config.copy()
            if "x_min" in config and "x_max" in config:
                x_min = config.pop("x_min")
                x_max = config.pop("x_max")
                config["x_range"] = [x_min, x_max, config.get("tick_frequency", 0.25)]
            if "unit_size" in config:
                config["length"] = config.pop("unit_size") * (config["x_range"][1] - config["x_range"][0])
            if "tick_frequency" in config:
                config.pop("tick_frequency")
            if "big_tick_numbers" in config:
                config["numbers_with_elongated_ticks"] = config.pop("big_tick_numbers")
            self.number_line_config = config

    def construct(self):
        self.add_number_line()
        self.add_phi_label()
        self.add_title()
        self.bounce_around()

    def add_number_line(self):
        number_line = NumberLine(**self.number_line_config)
        number_line.move_to(2 * DOWN)
        self.add(number_line)
        self.number_line = number_line

    def add_phi_label(self):
        number_line = self.number_line
        phi = (1 + np.sqrt(5)) / 2
        phi_point = number_line.number_to_point(phi)
        phi_dot = Dot(phi_point, color=YELLOW)
        arrow = Arrow(start=phi_point, end=phi_point + DL, buff=0)
        phi_label = MathTex("\\varphi = 1.618\\dots")
        phi_label.set_color(YELLOW)
        phi_label.next_to(arrow.get_start(), UP, buff=SMALL_BUFF)

        self.add(phi_dot, phi_label, arrow)

    def add_title(self):
        title = MathTex("x \\rightarrow 1 + \\frac{1}{x}")
        title.to_corner(UL)
        self.add(title)

    def bounce_around(self):
        number_line = self.number_line
        value = self.starting_value
        point = number_line.number_to_point(value)
        dot = Dot(point)
        dot.set_fill(RED, opacity=0.8)
        arrow = Arrow(start=point, end=point + DR, buff=0)
        arrow.set_color(dot.get_color())
        start_here = Text("Start here")
        start_here.next_to(arrow.get_start(), UP, buff=SMALL_BUFF)
        start_here.set_color(dot.get_color())

        self.play(
            FadeIn(start_here),
            GrowArrow(arrow),
            GrowFromPoint(dot, arrow.get_start())
        )
        self.play(
            FadeOut(start_here),
            FadeOut(arrow)
        )
        self.wait()
        for x in range(self.n_jumps):
            new_value = self.func(value)
            new_point = number_line.number_to_point(new_value)
            # 保持原來的 path_arc 邏輯
            path_arc = -120 * DEGREES
            # 使用 ArcBetweenPoints 來創建弧形路徑
            arc = ArcBetweenPoints(point, new_point, angle=path_arc)
            self.play(
                Create(arc, run_time=1.5),
                dot.animate.move_to(new_point).set_path_arc(path_arc),
            )
            self.remove(arc)  # 模擬 ShowCreationThenDestruction
            self.wait(0.5)

            value = new_value
            point = new_point
