# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示二項分佈的機率計算過程，從單項機率公式逐步過渡到長條圖，並比較不同成功機率下的分佈變化。


from manim import *
import itertools as it
import numpy as np

class ShowFullDistribution(Scene):
    def construct(self):
        self.add_scores_one_and_two()
        self.add_scores_zero_and_three()
        self.show_bar_chart()
        self.compare_to_binomial_pattern()
        self.show_alternate_values_of_p()

    def add_scores_one_and_two(self):
        scores = VGroup(
            MathTex(
                "P(", "\\text{Score} = 0", ")",
                "=", "(0.2)", "^3",
                "=", "0.008",
            ),
            MathTex(
                "P(", "\\text{Score} = 1", ")",
                "=", "3", "(0.8)", "(0.2)", "^2", 
                "=", "0.096",
            ),
            MathTex(
                "P(", "\\text{Score} = 2", ")",
                "=", "3", "(0.8)", "^2", "(0.2)",
                "=", "0.384",
            ),
            MathTex(
                "P(", "\\text{Score} = 3", ")",
                "=", "(0.8)", "^3",
                "=", "0.512",
            ),
        )
        scores.arrange(
            DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        scores.shift(MED_LARGE_BUFF*UP)
        scores.to_edge(LEFT)
        for score in scores:
            score.set_color_by_tex_to_color_map({
                "0.8" : GREEN,
                "0.2" : RED,
            })
            score[-1].set_color(YELLOW)

        self.add(*scores[1:3])
        self.scores = scores

    def add_scores_zero_and_three(self):
        self.p_slot_groups = VGroup()

        self.wait()
        self.add_edge_score(0, UP, False)
        self.add_edge_score(3, DOWN, True)

    def add_edge_score(self, index, vect, q_bool):
        score = self.scores[index]
        prob = VGroup(*score[:3])
        brace = Brace(prob, vect)
        p_slot_group = get_probability_of_slot_group([q_bool]*3)
        p_slot_group.next_to(brace, vect)
        group = VGroup(*it.chain(p_slot_group, brace, score))

        self.play(LaggedStartMap(
            FadeIn, group,
            run_time = 2,
            lag_ratio = 0.7,
        ))
        self.wait(2)
        self.p_slot_groups.add(brace, p_slot_group)

    def show_bar_chart(self):
        p_terms = VGroup()
        to_fade = VGroup(self.p_slot_groups)
        value_mobs = VGroup()
        for score in self.scores:
            p_terms.add(VGroup(*score[:3]))
            to_fade.add(VGroup(*score[3:-1]))
            value_mobs.add(score[-1])
        dist = get_binomial_distribution(3, 0.8)
        values = list(map(dist, list(range(4))))
        chart = BarChart(
            values, bar_names = list(range(4)),
        )
        chart.shift(DOWN)

        new_p_terms = VGroup(*[
            MathTex("P(", "S=%d"%k, ")")
            for k in range(4)
        ])
        for term, bar in zip(new_p_terms, chart.bars):
            term[1].set_color(YELLOW)
            term.set_width(1.5*bar.get_width())
            term.next_to(bar, UP)

        self.play(
            ReplacementTransform(
                value_mobs, chart.bars,
                lag_ratio = 0.5,
                run_time = 2
            )
        )
        self.play(
            LaggedStartMap(FadeIn, VGroup(*it.chain(*[
                submob 
                for submob in chart
                if submob is not chart.bars
            ]))),
            Transform(p_terms, new_p_terms),
            FadeOut(to_fade),
        )
        self.wait(2)

        chart.bar_top_labels = p_terms
        chart.add(p_terms)
        self.bar_chart = chart

    def compare_to_binomial_pattern(self):
        dist = get_binomial_distribution(3, 0.5)
        values = list(map(dist, list(range(4))))
        alt_chart = BarChart(values)
        alt_chart.move_to(self.bar_chart)
        bars = alt_chart.bars
        bars.set_fill(GREY, opacity = 0.5)
        vect = 4*UP
        bars.shift(vect)
        nums = VGroup(*list(map(Tex, list(map(str, [1, 3, 3, 1])))))
        for num, bar in zip(nums, bars):
            num.next_to(bar, UP)
        bars_copy = bars.copy()

        self.play(
            LaggedStartMap(FadeIn, bars),
            LaggedStartMap(FadeIn, nums),
        )
        self.wait(2)
        self.play(bars_copy.animate.shift(-vect))
        self.play(ReplacementTransform(
            bars_copy, self.bar_chart.bars
        ))
        self.wait(2)
        self.play(
            VGroup(self.bar_chart, bars, nums).animate.to_edge(LEFT)
        )

        self.alt_bars = bars
        self.alt_bars_labels = nums

    def show_alternate_values_of_p(self):
        new_prob = MathTex(
            "P(", "\\text{Correct}", ")", "=", "0.8"
        )
        new_prob.set_color_by_tex("Correct", GREEN)
        new_prob.shift(FRAME_WIDTH/4*RIGHT)
        new_prob.to_edge(UP)

        alt_ps = 0.5, 0.65, 0.25
        alt_rhss = VGroup()
        alt_charts = VGroup()
        for p in alt_ps:
            rhs = MathTex(str(p))
            rhs.set_color(YELLOW)
            rhs.move_to(new_prob[-1])
            alt_rhss.add(rhs)

            dist = get_binomial_distribution(3, p)
            values = list(map(dist, list(range(4))))
            chart = self.bar_chart.copy()
            chart.change_bar_values(values)
            for label, bar in zip(chart.bar_top_labels, chart.bars):
                label.next_to(bar, UP)
            alt_charts.add(chart)

        self.play(FadeIn(new_prob))
        self.play(Transform(new_prob[-1], alt_rhss[0]))
        point_5_probs = self.show_point_5_probs(new_prob)
        self.wait()
        self.play(Transform(self.bar_chart, alt_charts[0]))
        self.wait()
        self.play(FadeOut(point_5_probs))
        for rhs, chart in list(zip(alt_rhss, alt_charts))[1:]:
            self.play(Transform(new_prob[-1], rhs))
            self.play(Transform(self.bar_chart, chart))
            self.wait(2)

    def show_point_5_probs(self, mob):
        probs = VGroup()
        last = mob
        for k in range(4):
            buff = MED_LARGE_BUFF
            for indices in it.combinations(list(range(3)), k):
                bool_list = np.array([False]*3)
                bool_list[list(indices)] = True
                prob = get_probability_of_slot_group(bool_list)
                rhs = MathTex("= (0.5)^3")
                rhs.next_to(prob, RIGHT)
                prob.add(rhs)
                prob.scale(0.9)
                prob.next_to(last, DOWN, buff)
                probs.add(prob)
                last = prob
                buff = SMALL_BUFF

        self.play(LaggedStartMap(FadeIn, probs))
        self.wait()
        return probs
