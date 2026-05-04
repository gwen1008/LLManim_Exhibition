# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示貝葉斯定理中先驗機率、假陽性率與後驗機率的文字說明，並用箭頭標示對應關係。



from manim import *
class RephraseQuestion(Scene):
    def construct(self):
        words = VGroup(*[
            TexText(r"1 in $1{,000}$ chance \\ of having disease"),
            TexText(r"1 in $100$ \\ false positive rate."),
            TexText(r"""\underline{\phantom{1 in 10}} chance \\
                of having disease \\
                after testing positive.
            """),
        ])
        words.arrange(RIGHT, buff=LARGE_BUFF)
        words.set_width(2 * (config.frame_width / 2 - MED_LARGE_BUFF))

        prior = TexText("Prior")
        prior.set_color(GREEN)
        prior.next_to(words[0], UP, buff=1.5 * LARGE_BUFF)
        prior_arrow = Arrow(prior.get_bottom(), words[0].get_top())
        prior_arrow.set_color(prior.get_color())

        posterior = TexText("Posterior")
        posterior.next_to(words[2], UP)
        posterior.shift(
            (prior.get_center() - posterior.get_center())[1] * UP
        )
        posterior.set_color(YELLOW)
        posterior_arrow = Arrow(posterior.get_bottom(), words[2].get_top())
        posterior_arrow.set_color(posterior.get_color())

        self.add(words[0])
        self.play(
            LaggedStart(*[FadeIn(prior)]),
            Create(prior_arrow),
            run_time=1
        )
        self.wait()
        self.play(FadeIn(words[1]))
        self.wait()
        self.play(FadeIn(words[2]))
        self.play(
            LaggedStart(*[FadeIn(posterior)]),
            Create(posterior_arrow),
            run_time=1
        )
        self.wait(2)
