# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示貝葉斯定理的視覺化推導，從1000個個體中，透過疾病檢測的準確率和偽陽性率，計算後驗機率並與先驗機率對比。


from manim import *
import itertools as it

class ShowRestrictedSpace(Scene):
    def __init__(self, n_rows=25, n_cols=40, n_false_positives=10, false_positive_color=YELLOW_E, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_false_positives = n_false_positives
        self.false_positive_color = false_positive_color

    def construct(self):
        self.add_all_creatures()
        self.show_accurate_positive_result()
        self.show_false_positive_conditional()
        self.show_false_positive_individuals()
        self.fade_out_negative_result_individuals()
        self.show_posterior_probability()
        self.contrast_with_prior()

    def add_all_creatures(self):
        title = Text("1,000 individuals")
        title.to_edge(UP)
        all_creatures = self.get_all_creatures()
        sick_one = all_creatures.sick_one
        healthy_creatures = all_creatures.healthy_creatures

        sick_one.save_state()
        sick_one_words = Text("1 sick")
        sick_one_words.next_to(sick_one, RIGHT)
        sick_one_words.to_edge(RIGHT)
        sick_one_words.set_color(GREEN)
        sick_one_arrow = Arrow(
            sick_one_words.get_bottom(), sick_one.get_top(),
            color = GREEN
        )

        healthy_words = Text("999 healthy")
        healthy_words.next_to(sick_one_words, UP, buff=MED_LARGE_BUFF)
        healthy_words.shift_onto_screen()
        healthy_words.set_color(BLUE)

        self.add(title)
        self.play(LaggedStartMap(FadeIn, all_creatures))
        self.play(
            FadeIn(sick_one_words),
            Create(sick_one_arrow)
        )
        self.play(
            sick_one.animate.set_height(2),
            sick_one.animate.next_to(sick_one_words, DOWN),
            sick_one.animate.to_edge(RIGHT),
        )
        self.wait()
        self.play(sick_one.restore)
        self.play(
            Write(healthy_words),
            LaggedStartMap(
                ApplyMethod, healthy_creatures,
                lambda m : (m.shift, MED_SMALL_BUFF*UP),
                rate_func = there_and_back,
                lag_ratio = 0.2,
            )
        )
        self.wait()
        self.play(FadeOut(title))

        self.all_creatures = all_creatures
        self.healthy_creatures = healthy_creatures
        self.sick_one = sick_one
        self.sick_one_label = VGroup(sick_one_words, sick_one_arrow)
        self.healthy_ones_label = healthy_words

    def show_accurate_positive_result(self):
        equation = MathTex(
            "P(", "\\text{Test positive }", "|", 
            "\\text{ sick}", ")", "=", "100\\%"
        )
        equation.set_color_by_tex("positive", YELLOW)
        equation.set_color_by_tex("sick", GREEN)
        equation.to_corner(UL)

        self.play(Write(equation, run_time = 1))
        self.wait(2)

        self.disease_conditional = equation

    def show_false_positive_conditional(self):
        equation = MathTex(
            "P(", "\\text{Test positive }", "|", 
            "\\text{ healthy}", ")", "=", "1\\%"
        )
        equation.set_color_by_tex("positive", YELLOW)
        equation.set_color_by_tex("healthy", BLUE)
        equation.to_corner(UL)

        self.play(ReplacementTransform(
            self.disease_conditional, equation
        ))
        self.wait()

        self.healthy_conditional = equation

    def show_false_positive_individuals(self):
        all_creatures = self.all_creatures
        false_positives = VGroup(
            *all_creatures[-1][1:1+self.n_false_positives]
        )
        self.healthy_creatures.remove(*false_positives)
        brace = Brace(false_positives, RIGHT)
        words = Text("10 False positives")
        words.scale(0.8)
        words.next_to(brace, RIGHT)

        self.play(
            GrowFromCenter(brace),
            LaggedStartMap(
                ApplyMethod, false_positives,
                lambda pi : (pi.set_color, self.false_positive_color),
                run_time = 1
            )
        )
        self.play(Write(words))
        self.wait()

        self.false_positives = false_positives
        self.false_positives_brace = brace
        self.false_positives_words = words

    def fade_out_negative_result_individuals(self):
        to_fade = VGroup(
            self.healthy_creatures,
            self.healthy_conditional,
            self.sick_one_label,
            self.healthy_ones_label,
        )
        movers = VGroup(self.sick_one, *self.false_positives)
        movers.generate_target()
        movers.target.set_width(1)
        movers.target.arrange(RIGHT)
        movers.target.shift(DOWN)
        brace = Brace(VGroup(*movers.target[1:]))

        words = Text("You are one of these")
        words.to_edge(UP)
        arrows = [
            Arrow(words.get_bottom(), movers.target[i].get_top())
            for i in (0, -1)
        ]

        self.play(FadeOut(to_fade))
        self.play(
            MoveToTarget(movers),
            ReplacementTransform(self.false_positives_brace, brace),
            self.false_positives_words.animate.next_to(brace, DOWN)
        )
        self.play(
            Write(words, run_time = 2),
            Create(arrows[0])
        )
        self.play(Transform(
            arrows[0], arrows[1], run_time = 4, rate_func = there_and_back
        ))
        self.play(*list(map(FadeOut, [words, arrows[0]])))

        self.brace = brace

    def show_posterior_probability(self):
        posterior = MathTex(
            "P(", "\\text{Sick }", "|", 
            "\\text{ Positive test result}", ")",
            "\\approx \\frac{1}{11}", "\\approx 9\\%"
        )
        posterior.set_color_by_tex("Sick", GREEN)
        posterior.set_color_by_tex("Positive", YELLOW)
        posterior.to_edge(UP)
        posterior.shift(LEFT)

        self.play(FadeIn(posterior))
        self.wait(2)

        self.posterior = posterior

    def contrast_with_prior(self):
        prior = MathTex(
            "P(", "\\text{Sick}", ")", "= 0.1\\%"
        )
        prior.set_color_by_tex("Sick", GREEN)
        prior.move_to(self.posterior, UP+RIGHT)

        self.revert_to_original_skipping_status()
        self.play(
            Write(prior, run_time = 1),
            self.posterior.animate.shift(DOWN),
        )
        arrow = Arrow(
            prior.get_right(), self.posterior.get_right(),
            path_arc = -PI,
        )
        times_90 = MathTex("\\times 90")
        times_90.next_to(arrow, RIGHT)
        self.play(Create(arrow))
        self.play(Write(times_90, run_time = 1))
        self.wait(2)

    ######

    def get_all_creatures(self):
        creature = PiCreature()
        all_creatures = VGroup(*[
            VGroup(*[
                creature.copy()
                for y in range(self.n_rows)
            ]).arrange(DOWN, buff=SMALL_BUFF)
            for x in range(self.n_cols)
        ]).arrange(RIGHT, buff=SMALL_BUFF)
        all_creatures.set_height(5)
        all_creatures.center().to_edge(LEFT)

        healthy_creatures = VGroup(*it.chain(*all_creatures))
        sick_one = all_creatures[-1][0]
        sick_one.change_mode("sick")
        sick_one.set_color(GREEN)
        healthy_creatures.remove(sick_one)
        all_creatures.sick_one = sick_one
        all_creatures.healthy_creatures = healthy_creatures
        return all_creatures
