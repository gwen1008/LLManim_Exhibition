# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個機器對不同頻率的餘弦波信號產生不同反應，通過改變頻率並更新圖形和數字顯示。



from manim import *
class MachineThatTreatsOneFrequencyDifferently(Scene):
    def construct(self):
        graph = self.get_cosine_graph(0.5)
        frequency_mob = DecimalNumber(220, num_decimal_places=0)
        frequency_mob.next_to(graph, UP, buff=MED_LARGE_BUFF)

        self.graph = graph
        self.frequency_mob = frequency_mob
        self.add(graph, frequency_mob)

        arrow1, q_marks, arrow2 = group = VGroup(
            Arrow(start=UP, end=DOWN, color=WHITE),
            Text("???", color=WHITE).scale(1.5),
            Arrow(start=UP, end=DOWN, color=WHITE)
        )
        group.arrange(DOWN)
        group.next_to(graph, DOWN)
        self.add(group)

        self.change_graph_frequency(1)
        graph.set_color(GREEN)
        self.wait()
        graph.set_color(YELLOW)
        self.change_graph_frequency(2)
        self.wait()

    def change_graph_frequency(self, frequency, run_time=2):
        graph = self.graph
        frequency_mob = self.frequency_mob
        curr_frequency = graph.frequency
        self.play(
            UpdateFromAlphaFunc(
                graph, self.get_signal_update_func(graph, frequency),
            ),
            ChangingDecimal(
                frequency_mob,
                lambda a: 440 * interpolate(curr_frequency, frequency, a)
            ),
            run_time=run_time,
        )
        graph.frequency = frequency

    def get_signal_update_func(self, graph, target_frequency):
        curr_frequency = graph.frequency
        def update(graph, alpha):
            frequency = interpolate(curr_frequency, target_frequency, alpha)
            new_graph = self.get_cosine_graph(frequency)
            Transform(graph, new_graph).update(1)
            return graph
        return update

    def get_cosine_graph(self, frequency, num_steps=200, color=YELLOW):
        result = FunctionGraph(
            lambda x: 0.5 * np.cos(2 * np.pi * frequency * x),
            x_range=[-3, 3],
            color=color
        )
        result.frequency = frequency
        result.shift(2 * UP)
        return result
