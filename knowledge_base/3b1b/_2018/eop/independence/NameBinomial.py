# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示二項分佈的概念，從對勾/叉號的隨機過程轉換為男孩/女孩的性別例子，並在長條圖中動態更新概率分佈。


from manim import *
import numpy as np

def get_binomial_distribution(n, p):
    from math import comb
    return lambda k: comb(n, k) * (p**k) * ((1-p)**(n-k))

class NameBinomial(Scene):
    def __init__(self, flip_indices=[0, 2, 4, 5, 6, 7], **kwargs):
        super().__init__(**kwargs)
        self.flip_indices = flip_indices
    
    def construct(self):
        self.name_distribution()
        self.add_quiz_questions()
        self.change_to_gender()
        self.change_bar_chart_for_gender_example()
        self.point_out_example_input()
        self.write_probability_of_girl()
        self.think_through_probabilities()

    def name_distribution(self):
        ns = [3, 10]
        p = 0.65
        charts = VGroup()
        for n in ns:
            dist = get_binomial_distribution(n, p)
            values = list(map(dist, list(range(n+1))))
            chart = BarChart(
                values, 
                bar_names=[str(i) for i in range(n+1)]
            )
            chart.to_edge(LEFT)
            charts.add(chart)

        probability = MathTex(
            "P(", "\\checkmark", ")", "=", str(p)
        )
        probability.set_color_by_tex("checkmark", GREEN)
        probability.move_to(charts, UP)

        title = Tex("``Binomial distribution''")
        title.next_to(charts, UP)
        title.to_edge(UP)
        formula = MathTex(
            "P(X=", "k", ")=", 
            "{n \\choose k}", 
            "p", "^k",
            "(1-", "p", ")", "^{n-", "k}",
        )
        formula.set_color_by_tex("p", YELLOW)
        formula.set_color_by_tex("k", GREEN)
        # 在 ManimCE 中，get_part_by_tex 可能不可用，改用索引
        # choose_part = formula.get_part_by_tex("choose")
        # choose_part.set_color(WHITE)
        # choose_part[-2].set_color(GREEN)
        formula.to_corner(UP+RIGHT)

        self.add(charts[0], probability)
        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(ReplacementTransform(charts[0], charts[1]))
        self.play(Write(formula))
        self.wait()
        self.play(
            formula.animate.scale(0.7).next_to(charts[1], DOWN)
        )

        self.chart = charts[1]
        self.probability = probability
        self.title = title
        self.formula = formula

    def add_quiz_questions(self):
        n = 10
        checkmarks = VGroup(*[
            MathTex("\\checkmark").set_color(GREEN)
            for x in range(n)
        ])
        checkmarks.arrange(DOWN, buff=0.3)
        crosses = VGroup()
        arrows = VGroup()
        for checkmark in checkmarks:
            cross = MathTex("\\times")
            cross.set_color(RED)
            cross.next_to(checkmark, RIGHT, buff=LARGE_BUFF)
            crosses.add(cross)
            arrow = Arrow(
                checkmark.get_center(), cross.get_center(),
                tip_length=0.15,
                color=WHITE
            )
            arrows.add(arrow)
        full_group = VGroup(checkmarks, crosses, arrows)
        full_group.center().to_corner(UP + RIGHT, buff=MED_LARGE_BUFF)
        flip_indices = self.flip_indices
        flipped_arrows = VGroup(*[arrows[i] for i in flip_indices])
        faded_crosses = VGroup(*[crosses[i] for i in flip_indices])
        full_checks = VGroup(*[checkmarks[i] for i in flip_indices])
        faded_checkmarks = VGroup(*[m for i, m in enumerate(checkmarks) if i not in flip_indices])

        self.play(*[
            LaggedStart(
                *[Write(mob) for mob in group],
                run_time=3,
                lag_ratio=0.3
            )
            for group in full_group
        ])
        self.wait()
        self.play(
            LaggedStart(
                *[Rotate(arrow, angle=PI, about_point=arrow.get_center()) for arrow in flipped_arrows],
                run_time=2,
                lag_ratio=0.5
            ),
            faded_crosses.animate.set_opacity(0.5),
            faded_checkmarks.animate.set_opacity(0.5),
        )
        self.wait()

        self.checkmarks = checkmarks
        self.crosses = crosses
        self.arrows = arrows

    def change_to_gender(self):
        flip_indices = self.flip_indices
        male = self.get_male()
        female = self.get_female()

        girls = VGroup(*[
            female.copy().move_to(mob)
            for mob in self.checkmarks
        ])
        boys = VGroup(*[
            male.copy().move_to(mob)
            for mob in self.crosses
        ])
        for i in range(len(boys)):
            mob = boys[i] if i in flip_indices else girls[i]
            mob.set_opacity(0.5)

        brace = Brace(girls, LEFT)
        words = brace.get_text("$n$ children")

        self.play(
            GrowFromCenter(brace),
            FadeIn(words)
        )
        self.play(ReplacementTransform(
            self.crosses, boys,
            lag_ratio=0.5,
            run_time=3
        ))
        self.play(ReplacementTransform(
            self.checkmarks, girls,
            lag_ratio=0.5,
            run_time=3
        ))
        self.wait()

        self.boys = boys
        self.girls = girls
        self.children_brace = brace
        self.n_children_words = words

    def change_bar_chart_for_gender_example(self):
        checkmark = self.probability[1]  # 原本是 get_part_by_tex("checkmark")
        p_mob = self.probability[-1]

        female = self.get_female()
        female.move_to(checkmark)
        new_p_mob = MathTex("0.49")
        new_p_mob.move_to(p_mob, LEFT)

        dist = get_binomial_distribution(10, 0.49)
        values = list(map(dist, list(range(11))))

        self.play(
            Transform(checkmark, female),
            Transform(p_mob, new_p_mob),
        )
        # ManimCE 的 BarChart 沒有 change_bar_values 方法，我們重新創建
        new_chart = BarChart(
            values,
            bar_names=[str(i) for i in range(11)]
        )
        new_chart.to_edge(LEFT)
        self.play(ReplacementTransform(self.chart, new_chart))
        self.chart = new_chart
        self.wait()

    def point_out_example_input(self):
        boy_girl_groups = VGroup(*[
            VGroup(boy, girl)
            for boy, girl in zip(self.boys, self.girls)
        ])
        girl_rects = VGroup(*[
            SurroundingRectangle(
                boy_girl_groups[i], 
                color=MAROON_B,
                buff=SMALL_BUFF,
            )
            for i in sorted(self.flip_indices)
        ])

        chart = self.chart
        n_girls = len(girl_rects)
        chart_rect = SurroundingRectangle(
            VGroup(chart.bars[n_girls], chart.x_axis.labels[n_girls]),
            buff=SMALL_BUFF
        )

        prob = MathTex(
            "P(", "\\# \\text{Girls}", "=", "6", ")"
        )
        prob.set_color_by_tex("Girls", MAROON_B)
        arrow = Arrow(UP, ORIGIN, tip_length=0.15)
        arrow.set_color(MAROON_B)
        arrow.next_to(prob, DOWN)
        prob.add(arrow)
        prob.next_to(chart_rect, UP)
        girls = VGroup(*[self.girls[i] for i in self.flip_indices])

        self.play(Create(chart_rect))
        self.play(LaggedStart(
            *[Create(rect) for rect in girl_rects],
            run_time=2,
            lag_ratio=0.5,
        ))
        self.wait()

        self.play(Write(prob))
        self.play(LaggedStart(
            *[Indicate(girl) for girl in girls],
            run_time=3,
            lag_ratio=0.3,
            rate_func=there_and_back
        ))
        self.play(FadeOut(prob))
        self.wait()

        self.chart_rect = chart_rect
        self.girl_rects = girl_rects

    def write_probability_of_girl(self):
        probability = self.probability
        probability_copies = VGroup(*[
            probability.copy().scale(0.7).next_to(
                girl, LEFT, buff=MED_LARGE_BUFF
            )
            for girl in self.girls
        ])

        self.play(Indicate(probability))
        self.play(Indicate(probability[-1]))
        self.wait()
        self.play(
            ReplacementTransform(
                probability.copy(), probability_copies
            ),
            FadeOut(self.children_brace),
            FadeOut(self.n_children_words),
        )
        self.wait()

        self.probability_copies = probability_copies

    def think_through_probabilities(self):
        randy = Randolph().scale(0.5)
        randy.next_to(self.probability_copies, LEFT, buff=LARGE_BUFF)

        self.play(FadeIn(randy))
        self.play(randy.animate.change("thinking"))
        self.play(Blink(randy))
        self.wait()

    def get_male(self):
        return MathTex("\\male").scale(1.3).set_color(BLUE)

    def get_female(self):
        return MathTex("\\female").scale(1.3).set_color(MAROON_B)
