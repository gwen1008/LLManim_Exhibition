# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個假設「順序不重要」的場景，包含標題、概率等式群組、相關性問題，以及最後的「即將推出」提示。



from manim import *
class AssumeOrderDoesntMatter(Scene):
    def construct(self):
        self.force_skipping()

        self.add_title()
        self.show_equality()
        self.mention_correlation()

        self.revert_to_original_skipping_status()
        self.coming_soon()

    def add_title(self):
        title = Text(
            "Softer simplifying assumption: Order doesn't matter",
            font_size=36
        )
        title.to_edge(UP)

        self.add(title)
        self.title = title

    def show_equality(self):
        n = 3
        # 由於 get_probability_of_slot_group 未定義，這裡用占位符
        # 假設它返回一個 MathTex 對象
        def get_probability_of_slot_group(t):
            # 占位符：實際應根據 t 生成概率表達式
            return MathTex(r"P(\cdots)")

        prob_groups = VGroup(*[
            VGroup(*list(map(
                get_probability_of_slot_group,
                [t for t in it.product(*[[True, False]]*n) if sum(t) == k]
            )))
            for k in range(n+1)
        ])
        for prob_group in prob_groups:
            for prob in prob_group[:-1]:
                equals = MathTex("=")
                equals.next_to(prob, RIGHT)
                prob.add(equals)
            prob_group.arrange(RIGHT)
            max_width = config.frame_width - 1
            if prob_group.get_width() > max_width:
                prob_group.set_width(max_width)
        prob_groups.arrange(DOWN, buff=0.7)
        prob_groups.next_to(self.title, DOWN, buff=MED_LARGE_BUFF)

        self.play(FadeIn(
            prob_groups[1],
            run_time=2,
            lag_ratio=0.5
        ))
        self.wait(2)
        self.play(FadeIn(
            VGroup(prob_groups[0], *prob_groups[2:]),
            run_time=3,
            lag_ratio=0.5
        ))
        self.wait()

        self.prob_groups = prob_groups

    def mention_correlation(self):
        assumption_group = VGroup(*self.mobjects)
        question = Text(
            "But what is ``correlation''?",
            font_size=36,
            color=BLUE
        )
        question.to_edge(UP)
        bottom = question.get_bottom()

        self.play(
            Write(question),
            assumption_group.animate.next_to(bottom, DOWN, buff=LARGE_BUFF)
        )
        self.wait()

        self.assumption_group = assumption_group
        self.question = question

    def coming_soon(self):
        self.play(
            LaggedStartMap(
                lambda m: m.animate.shift(config.frame_height * DOWN),
                self.assumption_group,
                remover=True,
            ),
            self.question.animate.center().set_rate_func(
                lambda t: squish_rate_func(smooth, 0.5, 1)(t)
            ),
            run_time=2
        )

        # 由於 Text 沒有 get_part_by_tex，我們假設 question 是單個對象
        # 這裡用整個 question 來模擬
        part = self.question
        brace = Brace(part, UP)
        words = brace.get_text("Coming soon!")
        self.play(
            GrowFromCenter(brace),
            part.animate.set_color(YELLOW)
        )
        self.play(Write(words))
        self.wait()
