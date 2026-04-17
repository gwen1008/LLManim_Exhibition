# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示函數圖形、導數（切線斜率）與積分（黎曼和面積）的視覺化直覺，並伴隨文字動畫說明。



from manim import *
class GraphicalIntuitions(Scene):
    def __init__(self, func=lambda x: 0.1 * (x - 2) * (x - 5) * (x - 7) + 4, **kwargs):
        super().__init__(**kwargs)
        self.func = func

    def construct(self):
        # 建立坐標軸
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            x_axis_config={"numbers_to_include": list(range(1, 10))}
        )
        axes.center()
        
        # 繪製函數圖形
        graph = axes.plot(self.func, color=BLUE)
        
        # 建立切線斜率組（在 x=8 處）
        x_val = 8
        dx = 0.01
        secant_line_length = 6
        
        # 計算切線的兩個端點
        point1 = axes.c2p(x_val, self.func(x_val))
        point2 = axes.c2p(x_val + dx, self.func(x_val + dx))
        
        # 建立切線（紅色）
        secant_line = Line(
            point1 - (point2 - point1) * secant_line_length/2,
            point1 + (point2 - point1) * secant_line_length/2,
            color=RED
        )
        
        # 建立切點
        dot = Dot(point1, color=RED)
        
        # 將切線和點分組
        ss_group = VGroup(secant_line, dot)
        
        # 建立黎曼矩形（近似積分面積）
        x_min, x_max = 2, 8
        dx_rect = 0.01
        
        # 建立矩形列表
        rects = VGroup()
        x = x_min
        while x < x_max:
            rect = Rectangle(
                width=axes.c2p(dx_rect, 0)[0] - axes.c2p(0, 0)[0],
                height=axes.c2p(0, self.func(x))[1] - axes.c2p(0, 0)[1],
                stroke_width=0,
                fill_color=GREEN,
                fill_opacity=0.5
            )
            rect.move_to(axes.c2p(x + dx_rect/2, self.func(x)/2), aligned_edge=DL)
            rects.add(rect)
            x += dx_rect
        
        # 建立文字說明
        deriv_text = Text("Derivative → slope", color=WHITE)
        deriv_text.set_color_by_tex("slope", RED)
        deriv_text.to_edge(UP)
        
        integral_text = Text("Integral → area", color=WHITE)
        integral_text.set_color_by_tex("area", GREEN)
        integral_text.next_to(deriv_text, DOWN)
        
        # 動畫序列
        self.play(Write(axes), Create(graph, run_time=2))
        self.play(self.get_graph_words_anim())
        
        # 動畫：切線從 x=8 移動到 x=2
        self.play(
            Write(deriv_text),
            FadeIn(ss_group, run_time=2)
        )
        
        # 更新切線位置到 x=2
        target_x = 2
        new_point1 = axes.c2p(target_x, self.func(target_x))
        new_point2 = axes.c2p(target_x + dx, self.func(target_x + dx))
        new_secant_line = Line(
            new_point1 - (new_point2 - new_point1) * secant_line_length/2,
            new_point1 + (new_point2 - new_point1) * secant_line_length/2,
            color=RED
        )
        new_dot = Dot(new_point1, color=RED)
        
        self.play(
            Transform(secant_line, new_secant_line),
            Transform(dot, new_dot),
            run_time=2.5,
            rate_func=smooth
        )
        
        # 顯示積分文字
        self.play(FadeIn(integral_text))
        
        # 顯示黎曼矩形（從下往上生長）
        self.play(
            LaggedStart(
                *[GrowFromEdge(rect, DOWN) for rect in rects],
                lag_ratio=0.01
            ),
            run_time=3
        )
        
        self.wait(2)

    def get_graph_words_anim(self):
        words = VGroup(
            Text("Graphs,"),
            Text("graphs,"),
            Text("non-stop graphs"),
            Text("all day"),
            Text("every day"),
            Text("as if to visualize is to graph"),
        )
        
        # 為每個文字添加背景矩形
        for word in words:
            word.add_background_rectangle(buff=0.1, color=BLACK, opacity=0.7)
        
        words.arrange(DOWN, aligned_edge=LEFT)
        words.to_edge(UP)
        
        # 創建淡入淡出動畫序列
        anims = []
        for i, word in enumerate(words):
            anims.append(
                FadeIn(word, rate_func=there_and_back, run_time=0.8)
            )
        
        return AnimationGroup(*anims, lag_ratio=0.6)
