# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯更新過程，先繪製先驗分佈的黎曼矩形，再轉換為後驗分佈，最後進行歸一化縮放。


from manim import *
import numpy as np
import scipy.integrate

class GlimpseOfNextVideo(Scene):
    def __init__(
        self,
        x_axis_label="",
        y_axis_label="",
        x_min=0,
        x_max=15,
        x_axis_width=12,
        y_min=0,
        y_max=1.0,
        y_axis_height=6,
        y_tick_frequency=0.125,
        add_x_coords=True,
        formula_position=ORIGIN,
        dx=0.2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.x_min = x_min
        self.x_max = x_max
        self.x_axis_width = x_axis_width
        self.y_min = y_min
        self.y_max = y_max
        self.y_axis_height = y_axis_height
        self.y_tick_frequency = y_tick_frequency
        self.add_x_coords = add_x_coords
        self.formula_position = formula_position
        self.dx = dx

    def construct(self):
        # 創建坐標軸
        ax = Axes(
            x_range=[self.x_min, self.x_max, 1],
            y_range=[self.y_min, self.y_max, self.y_tick_frequency],
            x_length=self.x_axis_width,
            y_length=self.y_axis_height,
            axis_config={
                "include_numbers": False,
                "include_tip": False,
            }
        )
        
        # 添加y軸數字
        y_numbers = VGroup()
        for val in [0.25, 0.5, 0.75, 1.0]:
            num = DecimalNumber(val, num_decimal_places=2)
            num.next_to(ax.c2p(0, val), LEFT, buff=0.1)
            y_numbers.add(num)
        
        # 添加x軸數字
        x_numbers = VGroup()
        if self.add_x_coords:
            for i in range(1, 15):
                num = Integer(i)
                num.next_to(ax.c2p(i, 0), DOWN, buff=0.1)
                x_numbers.add(num)
        
        self.add(ax, y_numbers, x_numbers)
        
        # 定義函數
        def f1(x):
            return (x**3 / 6) * np.exp(-x)
        
        def likelihood(x):
            return np.exp(-0.5 * x)
        
        def f2(x):
            return f1(x) * likelihood(x)
        
        # 計算歸一化常數
        pe = scipy.integrate.quad(f2, 0, 20)[0]
        
        # 創建函數圖形
        graph1 = ax.plot(f1, color=YELLOW_D)
        graph2 = ax.plot(f2, color=BLUE)
        
        # 創建黎曼矩形
        rects1 = self.get_riemann_rectangles(ax, f1, dx=self.dx)
        rects2 = self.get_riemann_rectangles(ax, f2, dx=self.dx)
        
        rects1.set_color(YELLOW_D)
        rects2.set_color(BLUE)
        for rects in [rects1, rects2]:
            rects.set_stroke(WHITE, 1)
        
        # 保存初始狀態（壓縮到x軸）
        rects1_initial = rects1.copy()
        for rect in rects1_initial:
            rect.stretch(0, 1, about_edge=DOWN)
        
        # 創建公式
        formula = self.get_formula()
        
        # 動畫序列
        self.play(
            FadeIn(formula[:4], shift=DOWN),
            Transform(rects1_initial, rects1, lag_ratio=0.05, run_time=2)
        )
        self.wait()
        
        # 添加半透明的rects1副本
        rects1_faded = rects1.copy().set_opacity(0.4)
        self.add(rects1_faded)
        
        self.play(
            FadeIn(formula[4:10], shift=DOWN),
            Transform(rects1, rects2),
        )
        self.wait()
        
        # 歸一化縮放
        rects2_scaled = rects2.copy()
        for rect in rects2_scaled:
            rect.stretch(1 / pe, 1, about_edge=DOWN)
        
        self.play(
            Transform(rects1, rects2_scaled),
            Write(formula[10:], run_time=1)
        )
        self.wait()
    
    def get_riemann_rectangles(self, axes, func, dx=0.2):
        """創建黎曼矩形近似"""
        rects = VGroup()
        x_range = np.arange(self.x_min, self.x_max, dx)
        
        for x in x_range:
            x_point = axes.c2p(x, 0)
            y_val = func(x)
            y_point = axes.c2p(x, y_val)
            
            rect = Rectangle(
                width=axes.c2p(dx, 0)[0] - axes.c2p(0, 0)[0],
                height=axes.c2p(0, y_val)[1] - axes.c2p(0, 0)[1],
                stroke_width=1,
                fill_opacity=0.8
            )
            rect.move_to(x_point, aligned_edge=DL)
            rects.add(rect)
        
        return rects
    
    def get_formula(self):
        HYPOTHESIS_COLOR = BLUE
        EVIDENCE_COLOR1 = GREEN
        
        formula = MathTex(
            r"{p(H) p(E|H) \over p(E)}",
            tex_to_color_map={
                "H": HYPOTHESIS_COLOR,
                "E": EVIDENCE_COLOR1,
            }
        )
        formula.move_to(self.formula_position)
        return formula
