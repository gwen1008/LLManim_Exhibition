# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示貝葉斯定理中先驗概率到後驗概率的轉換過程，並用箭頭和文字標註數學公式與直覺的差異。



from manim import *
class SourceOfConfusion(Scene):
    def __init__(self, arrow_width=5, **kwargs):
        super().__init__(**kwargs)
        self.arrow_width = arrow_width

    def construct(self):
        self.add_progression()
        self.ask_question()
        self.write_bayes_rule()
        self.shift_arrow()

    def add_progression(self):
        prior = MathTex("P(", "S", ")", "= 0.001")
        arrow = Arrow(ORIGIN, self.arrow_width*RIGHT)
        posterior = MathTex("P(", "S", "|", "+", ")", "= 0.09")
        for mob in prior, posterior:
            mob.set_color_by_tex("S", GREEN)
            mob.set_color_by_tex("+", YELLOW)
        progression = VGroup(prior, arrow, posterior)
        progression.arrange(RIGHT)
        progression.shift(DOWN)

        bayes_rule_words = Text("Bayes' rule")
        bayes_rule_words.next_to(arrow, UP, buff=0)
        arrow.add(bayes_rule_words)

        for mob, word in (prior, "Prior"), (posterior, "Posterior"):
            brace = Brace(mob, DOWN)
            label = brace.get_text(word)
            mob.add(brace, label)

        self.add(progression)
        self.progression = progression
        self.bayes_rule_words = bayes_rule_words

    def ask_question(self):
        question = Text(
            "Where do math and \\\\ intuition disagree?"
        )
        question.to_corner(UP+LEFT)
        question_arrow = Arrow(
            question.get_bottom(),
            self.bayes_rule_words.get_top(),
            color=WHITE
        )

        self.play(Write(question))
        self.wait()
        self.play(Create(question_arrow))

        self.question = question
        self.question_arrow = question_arrow

    def write_bayes_rule(self):
        words = self.bayes_rule_words
        words_rect = SurroundingRectangle(words)
        rule = MathTex(
            "P(", "S", "|", "+", ")", "=", 
            "P(", "S", ")", 
            "{P(", "+", "|", "S", ")", "\\over",
            "P(", "+", ")}"
        )
        rule.set_color_by_tex("S", GREEN)
        rule.set_color_by_tex("+", YELLOW)
        rule.to_corner(UP+RIGHT)
        rule_rect = SurroundingRectangle(rule)
        rule_rect.set_color(BLUE)
        rule.save_state()
        rule.replace(words_rect)
        rule.scale(0.9)
        rule.set_fill(opacity=0)

        self.play(Create(words_rect))
        self.play(
            ReplacementTransform(words_rect, rule_rect),
            Restore(rule),
            run_time=2
        )
        self.wait(3)

    def shift_arrow(self):
        new_arrow = Arrow(
            self.question.get_bottom(),
            self.progression[0].get_top(),
            color=WHITE
        )

        self.play(Transform(
            self.question_arrow,
            new_arrow
        ))
        self.wait(2)
