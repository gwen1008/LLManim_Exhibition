# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示二項分佈隨著機率參數 p 變化的動態條形圖，並引入獨立性假設及其失效的視覺效果。


from manim import *
import numpy as np
import itertools as it

def get_binomial_distribution(n, p):
    from math import comb
    def dist(k):
        return comb(n, k) * (p**k) * ((1-p)**(n-k))
    return dist

class IntroduceBinomial(Scene):
    def __init__(self, n=8, p=0.7, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.p = p

    def construct(self):
        self.add_title()
        self.add_bar_chart()
        self.add_p_slider()
        self.write_independence_assumption()
        self.play_with_p_value(0.2, 0.5)
        self.cross_out_assumption()
        self.play_with_p_value(0.8, 0.4)
        self.shift_weight_to_tails()

    def add_title(self):
        title = Text("Binomial distribution")
        title.scale(1.3)
        title.to_edge(RIGHT)
        title.shift(2*UP)

        formula = MathTex(
            "P(X=", "k", ")=", 
            "{n \\choose k}", 
            "p", "^k",
            "(1-", "p", ")", "^{n-", "k}",
        )
        formula.set_color_by_tex("k", BLUE)
        formula.set_color_by_tex("p", YELLOW)
        choose_part = formula.get_part_by_tex("choose")
        choose_part.set_color(WHITE)
        choose_part[-2].set_color(BLUE)
        formula.next_to(title, DOWN, buff=MED_LARGE_BUFF)

        self.formula = formula
        self.title = title
        self.add(title, formula)

    def add_bar_chart(self):
        n, p = self.n, self.p
        dist = get_binomial_distribution(n, p)
        chart = BarChart(
            [dist(k) for k in range(n+1)],
            bar_names=[str(k) for k in range(n+1)],
        )
        chart.to_edge(LEFT)
        self.bar_chart = chart

        self.play(LaggedStartMap(
            FadeIn, VGroup(*it.chain(*chart)), 
            run_time=2
        ))

    def add_p_slider(self):
        interval = NumberLine(
            x_range=[0, 1, 1],
            length=4,
            color=GREY_B,
            include_numbers=True,
            numbers_with_elongated_ticks=[0, 1],
        )
        interval.next_to(
            VGroup(self.bar_chart.x_axis, self.bar_chart.y_axis), 
            UP, buff=MED_LARGE_BUFF
        )
        triangle = Triangle(
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=1,
        )
        triangle.rotate(-PI/2)
        triangle.set_height(0.25)
        triangle.move_to(interval.number_to_point(self.p), DOWN)
        label = MathTex("p")
        label.next_to(triangle, UP, buff=SMALL_BUFF)
        label.set_color(triangle.get_color())

        self.p_slider = VGroup(interval, triangle, label)
        self.play(Write(self.p_slider, run_time=1))

    def play_with_p_value(self, *values):
        for value in values:
            self.change_p(value)
            self.wait()

    def write_independence_assumption(self):
        assumption = Text("Independence assumption")
        assumption.scale(1.2)
        assumption.next_to(self.formula, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        assumption.set_color(GREEN_C)

        self.play(Write(assumption, run_time=2))
        self.wait()

        self.assumption = assumption

    def cross_out_assumption(self):
        cross = Cross(self.assumption)
        cross.set_color(GREY)
        self.bar_chart.save_state()

        self.play(Create(cross))
        self.play(self.bar_chart.animate.set_opacity(0.3))
        self.wait(2)
        self.play(Restore(self.bar_chart))

    def shift_weight_to_tails(self):
        chart = self.bar_chart
        chart_copy = chart.copy()
        dist = get_binomial_distribution(self.n, self.p)
        values = np.array(list(map(dist, list(range(self.n+1)))))
        values += 0.1
        values /= sum(values)

        old_bars = chart.bars
        old_bars.generate_target()
        new_bars = chart_copy.bars
        for bars, vect in (old_bars.target, LEFT), (new_bars, RIGHT):
            for bar in bars:
                corner = bar.get_corner(DOWN+vect)
                bar.stretch(0.5, 0)
                bar.move_to(corner, DOWN+vect)
        old_bars.target.set_color(RED)
        old_bars.target.set_opacity(0.3)

        self.play(
            MoveToTarget(old_bars),
            ReplacementTransform(
                old_bars.copy().set_fill(opacity=0),
                new_bars
            )
        )
        self.play(
            chart_copy.animate.change_bar_values(values)
        )
        self.wait(2)

    def change_p(self, p):
        interval, triangle, p_label = self.p_slider
        alt_dist = get_binomial_distribution(self.n, p)
        self.play(
            self.bar_chart.animate.change_bar_values(
                [alt_dist(k) for k in range(self.n+1)]
            ),
            triangle.animate.move_to(interval.number_to_point(p), DOWN),
            MaintainPositionRelativeTo(p_label, triangle)
        )
        self.p = p
