# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個指數衰減曲線及其黎曼和面積，並討論最大化觸及人數與最大化總價值之間的權衡，最後將曲線變形為更陡峭的衰減。


from manim import *
import numpy as np

class PeopleValueGraph(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 原 CONFIG 中的參數轉為實例變數
        self.x_min = 0
        self.x_max = 12
        self.y_max = 8
        self.graph_origin = 2 * DOWN + 5 * LEFT
        self.riemann_rectangles_config = {
            "dx": 0.01,
            "stroke_width": 0,
            "start_color": GREEN,
            "end_color": BLUE,
        }
        # 坐標軸標籤
        self.x_axis_label = "People reached"
        self.y_axis_label = "Value per person"

    def construct(self):
        self.setup_axes()
        self.tweak_labels()
        self.add_curve()
        self.comment_on_incentives()
        self.change_curve()

    def setup_axes(self):
        # 在 ManimCE 中，使用 Axes 類別
        self.axes = Axes(
            x_range=[self.x_min, self.x_max, 1],
            y_range=[0, self.y_max, 1],
            axis_config={"include_numbers": True},
            x_length=11,
            y_length=5,
        )
        # 移動到指定的原點位置
        self.axes.shift(self.graph_origin - self.axes.c2p(0, 0))
        self.add(self.axes)

        # 添加坐標軸標籤
        self.x_axis_label_mob = Text(self.x_axis_label, font_size=24)
        self.y_axis_label_mob = Text(self.y_axis_label, font_size=24)
        # 將 x 軸標籤放在 x 軸右側下方
        self.x_axis_label_mob.next_to(self.axes.x_axis.get_right(), DOWN, buff=0.3)
        # 將 y 軸標籤放在 y 軸頂部左側
        self.y_axis_label_mob.next_to(self.axes.y_axis.get_top(), LEFT, buff=0.3)
        self.add(self.x_axis_label_mob, self.y_axis_label_mob)

    def tweak_labels(self):
        # 將 x 軸標籤移到前景（原 add_foreground_mobjects 功能）
        self.x_axis_label_mob.set_z_index(10)
        # 將 y 軸標籤移到左邊緣（原 to_edge(LEFT)）
        self.y_axis_label_mob.to_edge(LEFT)

    def add_curve(self):
        # 定義指數衰減函數
        def func(x):
            return 7 * np.exp(-0.5 * x)

        # 繪製曲線
        self.graph = self.axes.plot(func, color=WHITE)
        self.play(
            Create(self.graph),
            rate_func=bezier([0, 0, 1, 1]),
            run_time=3
        )

    def comment_on_incentives(self):
        # 創建 "Maximize reach?" 箭頭和文字
        reach_arrow = Arrow(
            start=self.axes.c2p(7, 0) + 0.5 * DOWN,
            end=self.axes.c2p(12, 0) + 0.5 * DOWN,
            buff=0,
            color=WHITE
        )
        reach_words = Text("Maximize reach?", font_size=24)
        reach_words.next_to(reach_arrow, DOWN, buff=SMALL_BUFF)
        reach_words.set_color(WHITE)

        # 計算黎曼和面積（近似積分）
        self.area = self.get_riemann_rectangles(self.graph)
        area_words = Text("Maximize this area", font_size=24)
        area_words.set_color(BLUE)
        # 將文字移動到坐標 (4, 5) 的位置
        area_words.move_to(self.axes.c2p(4, 5))
        area_arrow = Arrow(
            start=area_words.get_bottom(),
            end=self.axes.c2p(1.5, 2),
            buff=0.2,
            color=BLUE
        )

        # 播放動畫
        self.play(GrowArrow(reach_arrow))
        self.play(Write(reach_words))
        self.wait()
        self.play(
            LaggedStartMap(DrawBorderThenFill, self.area),
            Animation(self.graph),
            Animation(self.axes),
            Write(area_words),
            GrowArrow(area_arrow),
        )
        self.wait()

        self.area_label_group = VGroup(area_words, area_arrow)

    def get_riemann_rectangles(self, graph):
        """生成黎曼矩形來近似曲線下的面積"""
        x_range = [self.x_min, self.x_max, self.riemann_rectangles_config["dx"]]
        rectangles = self.axes.get_riemann_rectangles(
            graph,
            x_range=x_range,
            stroke_width=self.riemann_rectangles_config["stroke_width"],
            fill_opacity=0.8,
            color_gradient=[GREEN, BLUE]
        )
        return rectangles

    def change_curve(self):
        # 定義新的更陡峭的衰減函數
        def new_func(x):
            # 使用插值從原函數過渡到新函數
            original = 7 * np.exp(-0.01 * x)
            steeper = 7 * np.exp(-3 * x)
            # 平滑過渡函數
            t = np.clip(x / 5, 0, 1)
            smooth_t = t * t * (3 - 2 * t)  # smoothstep 函數
            return interpolate(original, steeper, smooth_t)

        # 創建新曲線和新面積
        new_graph = self.axes.plot(new_func, color=WHITE)
        new_area = self.get_riemann_rectangles(new_graph)

        # 播放變形動畫
        self.play(
            Transform(self.area, new_area),
            Transform(self.graph, new_graph),
            self.area_label_group[0].animate.shift(RIGHT),
            Animation(self.area_label_group),
            Animation(self.axes),
            run_time=4,
        )
        self.wait()
