# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示在函數圖形上重複應用 f(x) = 1 + 1/x 的過程，透過點在圖形上的垂直和水平移動形成蜘蛛網圖案，同時有角色在旁觀看並變化表情。


from manim import *
import random

class RepeatedApplicationGraphically(Scene):
    def __init__(self, starting_value=1, n_jumps=5, n_times_to_show_identity_property=2, **kwargs):
        super().__init__(**kwargs)
        self.starting_value = starting_value
        self.n_jumps = n_jumps
        self.n_times_to_show_identity_property = n_times_to_show_identity_property
        
    def construct(self):
        # 設置坐標軸
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            axis_config={"include_numbers": True}
        )
        self.add(ax)
        
        # 繪製函數圖形
        func = lambda x: 1 + 1/x if x != 0 else 0
        func_graph = ax.plot(func, x_range=[0.2, 5], color=BLUE)
        identity_graph = ax.plot(lambda x: x, x_range=[0, 5], color=GREEN)
        self.add(func_graph, identity_graph)
        
        # 創建角色
        randy = self.create_pi_creature()
        self.add(randy)
        
        # 繪製蜘蛛網圖案
        self.draw_spider_web(ax, func, randy)
    
    def create_pi_creature(self):
        randy = Randolph(height=2)
        randy.flip()
        randy.to_corner(DR)
        return randy
    
    def get_new_randy_mode(self, randy):
        if not hasattr(self, "n_mode_changes"):
            self.n_mode_changes = 0
        else:
            self.n_mode_changes += 1
        if self.n_mode_changes % 3 != 0:
            return randy.get_mode()
        return random.choice([
            "confused",
            "erm",
            "maybe"
        ])
    
    def draw_spider_web(self, ax, func, randy):
        x_val = self.starting_value
        curr_output = 0
        dot = Dot(color=RED, fill_opacity=0.7)
        dot.move_to(ax.c2p(x_val, curr_output))
        
        self.play(FadeIn(dot, shift=2*UR))
        self.wait()
        
        for n in range(self.n_jumps):
            new_output = func(x_val)
            func_graph_point = ax.c2p(x_val, new_output)
            id_graph_point = ax.c2p(new_output, new_output)
            v_line = DashedLine(dot.get_center(), func_graph_point)
            h_line = DashedLine(func_graph_point, id_graph_point)
            
            curr_output = new_output
            x_val = new_output
            
            for line in v_line, h_line:
                line_end = line.get_end()
                self.play(
                    Create(line),
                    dot.animate.move_to(line_end),
                    randy.animate.change(self.get_new_randy_mode(randy))
                )
                self.wait()
            
            if n < self.n_times_to_show_identity_property:
                x_point = ax.c2p(new_output, 0)
                y_point = ax.c2p(0, new_output)
                lines = VGroup(*[
                    Line(dot.get_center(), point)
                    for point in (x_point, y_point)
                ])
                lines.set_color(YELLOW)
                self.play(Create(lines, run_time=1.5))
                self.play(FadeOut(lines, run_time=0.5))
                self.wait(0.25)
