# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示不確定性原理，通過高斯函數及其傅立葉變換的動態變化，說明位置與動量的互補關係。



from manim import *
class ShowUncertaintyPrinciple(Scene):
    def construct(self):
        title = Tex("Uncertainty principle")
        self.add(title)
        
        # 創建上下兩個坐標軸
        top_axes = Axes(
            x_range=[-config.frame_width/2, config.frame_width/2, 1],
            y_range=[0, 3, 1],
            y_length=0.6*3,
            tips=False,
        )
        bottom_axes = top_axes.copy()
        
        # 創建連接兩個坐標軸的箭頭
        arrow = Arrow(start=UP, end=DOWN, color=WHITE)
        
        # 將所有元素垂直排列
        group = VGroup(title, top_axes, arrow, bottom_axes)
        group.arrange(DOWN, buff=0.5)
        title.shift(0.3*UP)  # MED_SMALL_BUFF 約為 0.3
        group.to_edge(UP)
        
        # 添加傅立葉變換標籤
        fourier_word = Tex("Fourier transform")
        fourier_word.next_to(arrow, RIGHT)
        
        self.add(group, fourier_word)
        
        # 創建一個隱形的點來控制函數寬度
        ghost_dot = Dot(RIGHT, fill_opacity=0)
        
        # 高斯函數定義
        def get_bell_func(factor=1):
            return lambda x: 2*np.exp(-factor*x**2)
        
        # 創建初始圖形
        top_graph = top_axes.plot(get_bell_func(), color=YELLOW)
        bottom_graph = bottom_axes.plot(get_bell_func(), color=RED)
        
        # 更新函數，根據 ghost_dot 的位置調整高斯函數的寬度
        def get_update_func(axes, is_bottom=False):
            def update_graph(graph):
                f = ghost_dot.get_center()[0]
                if is_bottom:
                    f = 1./f if f != 0 else 1000  # 避免除以零
                new_graph = axes.plot(get_bell_func(f), color=graph.get_color())
                graph.set_points(new_graph.get_points())
            return update_graph
        
        # 測試的寬度因子
        factors = [0.3, 0.1, 2, 10, 100, 0.01, 0.5]
        
        # 動畫序列
        self.play(Create(top_graph))
        self.play(TransformFromCopy(top_graph, bottom_graph))
        self.wait(2)
        
        # 添加更新器
        top_graph.add_updater(get_update_func(top_axes, False))
        bottom_graph.add_updater(get_update_func(bottom_axes, True))
        
        # 動態改變高斯函數的寬度
        for factor in factors:
            self.play(
                ghost_dot.animate.move_to(factor*RIGHT),
                run_time=2
            )
            self.wait()
        
        # 移除更新器（可選）
        top_graph.clear_updaters()
        bottom_graph.clear_updaters()
