# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個角色思考測驗分數分佈的過程，從列出分數機率到繪製二項分佈長條圖，最後顯示單一題目答對機率。



from manim import *
class IntroduceQuiz(PiCreatureScene):
    def construct(self):
        self.add_quiz()
        self.ask_about_probabilities()
        self.show_distribution()
        self.show_single_question_probability()

    def add_quiz(self):
        quiz = self.get_example_quiz()
        quiz.next_to(self.randy, UP+RIGHT)

        self.play(
            Write(quiz),
            self.randy.change, "pondering", quiz
        )
        self.wait()

        self.quiz = quiz

    def ask_about_probabilities(self):
        probabilities, abbreviated_probabilities = [
            VGroup(*[
                MathTex(
                    "P(", s_tex, "=", str(score), ")", rhs
                ).set_color_by_tex_to_color_map({
                    str(score) : YELLOW,
                    "text" : GREEN,
                })
                for score in range(4)
            ])
            for s_tex, rhs in [
                ("\\text{Score}", "= \\, ???"),
                ("\\text{S}", "")
            ]
        ]
        for group in probabilities, abbreviated_probabilities:
            group.arrange(
                DOWN, 
                buff = MED_LARGE_BUFF,
                aligned_edge = LEFT
            )
            group.to_corner(UP+LEFT)

        self.play(
            LaggedStartMap(FadeIn, probabilities, run_time = 3),
            self.quiz.animate.set_height(0.7*self.randy.get_height()),
            self.quiz.animate.next_to(self.randy, RIGHT),
            self.randy.change, "confused", probabilities
        )
        self.wait()

        self.probabilities = probabilities
        self.abbreviated_probabilities = abbreviated_probabilities

    def show_distribution(self):
        dist = get_binomial_distribution(3, 0.7)
        values = list(map(dist, list(range(4))))
        chart = BarChart(
            values, 
            width = 7,
            bar_names = list(range(4))
        )
        chart.to_edge(RIGHT)
        for short_p, bar in zip(self.abbreviated_probabilities, chart.bars):
            short_p.set_width(1.75*bar.get_width())
            short_p.next_to(bar, UP)

        self.play(
            LaggedStartMap(Write, VGroup(
                *[m for m in chart if m is not chart.bars]
            )),
        )
        self.play(*[
            ReplacementTransform(
                bar.copy().stretch_to_fit_height(0).move_to(bar.get_bottom()),
                bar
            )
            for bar in chart.bars
        ])
        self.play(*[
            ReplacementTransform(p.copy(), short_p)
            for p, short_p in zip(
                self.probabilities,
                self.abbreviated_probabilities,
            )
        ])
        self.wait()

        self.bar_chart = chart

    def show_single_question_probability(self):
        prob = MathTex(
            "P(", "\\text{Can answer a given question}", ")",
            "= 0.8"
        )
        prob.to_corner(UP+RIGHT)
        prob.set_color_by_tex("text", GREEN)
        rect = SurroundingRectangle(prob, buff = MED_SMALL_BUFF)

        self.play(
            Write(prob),
            self.randy.change, "happy", prob
        )
        self.play(Create(rect))
        self.wait()

        self.single_question_probability = VGroup(
            prob, rect
        )


    ######

    def create_pi_creature(self):
        randy = Randolph()
        randy.scale(0.7)
        randy.to_corner(DOWN+LEFT)
        self.randy = randy
        return randy

    def get_example_quiz(self):
        return get_quiz(
            "Define ``Brachistochrone'' ",
            "Define ``Tautochrone'' ",
            "Define ``Cycloid'' ",
        )
