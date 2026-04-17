# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示二項分佈的機率值、與巴斯卡三角形對應項的比較、中間值的集中趨勢、推廣到一般形式，以及改變 p 值對分佈的影響。


from manim import *
import numpy as np

def get_binomial_distribution(n, p):
    from math import comb
    def dist(k):
        return comb(n, k) * (p**k) * ((1-p)**(n-k))
    return dist

class GeneralBinomialDistributionValues(Scene):
    def __init__(self, n=10, alt_n=8, p=0.49, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.alt_n = alt_n
        self.p = p

    def construct(self):
        self.add_chart()
        self.show_a_few_values()
        self.compare_to_pascal_row()
        self.mention_center_concentration()
        self.generalize()
        self.play_with_p_value()

    def add_chart(self):
        dist = get_binomial_distribution(self.n, self.p)
        values = list(map(dist, list(range(self.n+1))))
        chart = BarChart(
            values,
            bar_names=[str(i) for i in range(self.n+1)]
        )
        chart.to_edge(LEFT)

        full_probability = self.get_probability_expression(
            "10", "k", "(0.49)", "(0.51)"
        )
        full_probability.next_to(chart, UP, aligned_edge=LEFT)

        self.add(chart)

        self.chart = chart
        self.full_probability = full_probability

    def show_a_few_values(self):
        chart = self.chart
        probabilities = VGroup()
        for i, bar in enumerate(chart.bars):
            prob = self.get_probability_expression(
                "10", str(i), "(0.49)", "(0.51)",
                full=False
            )
            arrow = Arrow(
                UP, DOWN, 
                color=WHITE,
                tip_length=0.15
            )
            arrow.next_to(bar, UP, buff=SMALL_BUFF)
            prob.next_to(arrow, UP, buff=SMALL_BUFF)
            ##
            prob.shift(LEFT)
            self.bring_to_front(prob)
            prob.shift(RIGHT)
            ##
            prob.add(arrow)            
            probabilities.add(prob)
        shown_prob = probabilities[6].copy()

        self.play(FadeIn(shown_prob))
        self.wait()
        self.play(LaggedStart(
            *[FadeIn(part) for part in self.full_probability],
            run_time=4,
            lag_ratio=0.5,
        ))
        self.wait()
        last_k = 6
        for k in [3, 8, 5, 9, 6]:
            self.play(Transform(
                shown_prob, probabilities[k],
                path_arc=-np.pi/6 if k > last_k else np.pi/6
            ))
            self.wait(2)
            last_k = k

        self.shown_prob = shown_prob

    def compare_to_pascal_row(self):
        # 注意：ManimCE 沒有內建的 PascalTriangle，這裡用替代方案
        # 建立一個簡單的三角形表示
        triangle = VGroup()
        nrows = 11
        for n in range(nrows):
            row = VGroup()
            for k in range(n+1):
                from math import comb
                num = comb(n, k)
                mob = Text(str(num), font_size=24)
                row.add(mob)
            row.arrange(RIGHT, buff=0.3)
            triangle.add(row)
        triangle.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        triangle.set_width(6)
        triangle.to_corner(UP+RIGHT)
        
        last_row = triangle[-1]
        ten_choose_ks = VGroup()
        for k, mob in enumerate(last_row):
            ten_choose_k = MathTex(f"{{10 \\choose {k}}}")
            ten_choose_k.scale(0.5)
            ten_choose_k.stretch(0.8, 0)
            ten_choose_k.next_to(mob, DOWN)
            ten_choose_ks.add(ten_choose_k)
        ten_choose_ks.set_color_by_gradient(BLUE, YELLOW)

        self.play(
            LaggedStart(*[FadeIn(row) for row in triangle], lag_ratio=0.1),
            FadeOut(self.shown_prob)
        )
        self.play(
            last_row.animate.set_color_by_gradient(BLUE, YELLOW),
            Write(ten_choose_ks, run_time=2)
        )
        self.wait()
        self.play(ApplyWave(self.chart.bars, direction=UP))
        self.play(Indicate(last_row))
        self.play(LaggedStart(
            *[mob.animate.scale(1.2) for mob in last_row],
            rate_func=there_and_back,
        ))
        self.wait()

        self.pascals_triangle = triangle
        self.ten_choose_ks = ten_choose_ks

    def mention_center_concentration(self):
        bars = self.chart.bars
        bars.generate_target()
        bars.save_state()
        bars.target.arrange(UP, buff=0)
        bars.target.stretch_to_fit_height(self.chart.height)
        bars.target.move_to(
            self.chart.x_axis.point_from_proportion(0.05),
            DOWN
        )
        brace = Brace(VGroup(*bars.target[4:7]), RIGHT)
        words = brace.get_text("Most probability \\\\ in middle values")

        self.play(MoveToTarget(bars))
        self.play(
            GrowFromCenter(brace),
            FadeIn(words)
        )
        self.wait(2)
        self.play(
            Restore(bars),
            *[FadeOut(mob) for mob in [
                brace, words, 
                self.pascals_triangle,
                self.ten_choose_ks
            ]]
        )

    def generalize(self):
        alt_n = self.alt_n
        dist = get_binomial_distribution(alt_n, self.p)
        values = list(map(dist, list(range(alt_n + 1))))
        alt_chart = BarChart(
            values, bar_names=[str(i) for i in range(alt_n + 1)]
        )
        alt_chart.move_to(self.chart)

        alt_probs = [
            self.get_probability_expression("n", "k", "(0.49)", "(0.51)"),
            self.get_probability_expression("n", "k", "p", "(1-p)"),
        ]
        for prob in alt_probs:
            prob.move_to(self.full_probability)

        choose_part = None
        for part in self.full_probability:
            if "choose" in part.get_tex_string():
                choose_part = part
                break
        if choose_part:
            self.play(Indicate(choose_part))
        
        self.play(
            ReplacementTransform(self.chart, alt_chart),
            Transform(self.full_probability, alt_probs[0])
        )
        self.chart = alt_chart
        self.wait(2)
        self.play(Transform(self.full_probability, alt_probs[1]))
        self.wait()

    def play_with_p_value(self):
        p = self.p
        interval = NumberLine(
            x_range=[0, 1, 0.5],
            length=5,
            include_numbers=True,
            numbers_with_elongated_ticks=[0, 0.5, 1],
        )
        interval.next_to(self.full_probability, DOWN, buff=LARGE_BUFF)
        triangle = Triangle(
            fill_color=MAROON_B,
            fill_opacity=1,
            stroke_width=0,
        )
        triangle.rotate(-PI/2)
        triangle.set_height(0.25)
        triangle.move_to(interval.number_to_point(p), DOWN)
        p_mob = MathTex("p")
        p_mob.set_color(MAROON_B)
        p_mob.next_to(triangle, UP, buff=SMALL_BUFF)
        triangle.add(p_mob)

        new_p_values = [0.8, 0.4, 0.2, 0.9, 0.97, 0.6]

        self.play(
            Create(interval),
            Write(triangle, run_time=1)
        )
        self.wait()
        for new_p in new_p_values:
            p = new_p
            dist = get_binomial_distribution(self.alt_n, p)
            values = list(map(dist, list(range(self.alt_n + 1))))
            self.play(
                self.chart.animate.change_bar_values(values),
                triangle.animate.move_to(interval.number_to_point(p), DOWN)
            )
            self.wait()

    def get_probability_expression(
        self, n="n", k="k", p="p", q="(1-p)",
        full=True
        ):
        if full:
            tex_string = f"P(\\# \\text{{Girls}} = {k}) = {{{n} \\choose {k}}} {p}^{{{k}}} {q}^{{{n}-{k}}}"
        else:
            tex_string = f"{{{n} \\choose {k}}} {p}^{{{k}}} {q}^{{{n}-{k}}}"
        
        result = MathTex(tex_string)
        color_map = {
            "Girls": MAROON_B,
            n: WHITE,
            k: YELLOW,
            p: MAROON_B,
            q: BLUE,
        }
        
        # 手動設置顏色
        for tex, color in color_map.items():
            for part in result:
                if tex in part.get_tex_string():
                    part.set_color(color)
        
        # 特別處理組合符號的部分
        for part in result:
            if "choose" in part.get_tex_string():
                part.set_color(WHITE)
                # 嘗試設置 n 和 k 的顏色
                for subpart in part:
                    if n in subpart.get_tex_string():
                        subpart.set_color(color_map[n])
                    if k in subpart.get_tex_string():
                        subpart.set_color(color_map[k])
        
        return result
