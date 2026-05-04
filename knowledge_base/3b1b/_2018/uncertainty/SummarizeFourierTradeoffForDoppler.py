# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示傅立葉變換中時間與頻率解析度的權衡，通過移動控制參數來同時改變時間域和頻率域的高斯函數寬度。



from manim import *
class SummarizeFourierTradeoffForDoppler(Scene):
    def construct(self):
        time_axes = Axes(
            x_range=[0, 12],
            y_range=[-0.5, 1],
        )
        time_axes.center().to_edge(UP, buff=LARGE_BUFF)
        frequency_axes = time_axes.copy()
        frequency_axes.next_to(time_axes, DOWN, buff=2)
        time_label = Text("Time")
        frequency_label = Text("Frequency")
        for label, axes in [(time_label, time_axes), (frequency_label, frequency_axes)]:
            label.next_to(axes.get_right(), UP, buff=SMALL_BUFF)
            axes.add(label)
        frequency_label.shift_onto_screen()
        title = Text("Fourier Trade-off")
        title.next_to(time_axes, DOWN)
        self.add(title)

        # Position determines log of scale value for exponentials
        a_mob = Dot(point=ORIGIN, radius=0)  # 不可見點
        x_values = [3, 5, 6, 7, 8]
        v_values = [5, 5.5, 5.75, 6.5, 7]
        
        def get_top_graphs():
            a = np.exp(a_mob.get_center()[0])
            graphs = VGroup(*[
                time_axes.plot(lambda t: np.exp(-5 * a * (t - x) ** 2))
                for x in x_values
            ])
            graphs.set_color(WHITE)
            # ManimCE 中沒有 color_using_background_image，改用漸變色
            colors = color_gradient([BLUE, YELLOW], len(graphs))
            for graph, color in zip(graphs, colors):
                graph.set_color(color)
            return graphs
        
        def get_bottom_graphs():
            a = np.exp(a_mob.get_center()[0])
            graphs = VGroup(*[
                frequency_axes.plot(lambda t: np.exp(-(5. / a) * (t - v) ** 2))
                for v in v_values
            ])
            graphs.set_color(RED)
            return graphs

        top_graphs = get_top_graphs()
        bottom_graphs = get_bottom_graphs()
        
        # 更新函數
        def update_top_graphs(mob):
            new_graphs = get_top_graphs()
            mob.become(new_graphs)
        
        def update_bottom_graphs(mob):
            new_graphs = get_bottom_graphs()
            mob.become(new_graphs)
        
        top_graphs.add_updater(update_top_graphs)
        bottom_graphs.add_updater(update_bottom_graphs)

        self.add(time_axes, frequency_axes)
        self.add(top_graphs, bottom_graphs)

        shift_vect = 2 * RIGHT
        for s in [1, -2, 1]:
            self.play(a_mob.animate.shift(s * shift_vect), run_time=3)
        
        # 移除更新器
        top_graphs.remove_updater(update_top_graphs)
        bottom_graphs.remove_updater(update_bottom_graphs)
