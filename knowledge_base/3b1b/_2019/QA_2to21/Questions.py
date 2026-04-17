# Source: 3b1b/_2019/QA_2to21.py
# Description: [3b1b translated] 一系列問題文字從下方淡入，同時上一個問題向上淡出，形成連續的問答展示效果。



from manim import *
class Questions(Scene):
    def construct(self):
        kw = {
            "alignment": ""
        }
        # 在 ManimCE 中，Text 類別直接支援 alignment 參數
        questions = VGroup(
            Text(
                "Who is your favorite mathematician?",
                **kw
            ),
            Text(
                "A teenage kid walks up to you and says they\nhate maths. What do you tell/show them?",
                **kw
            ),
            Text(
                "What advice would you want to give to give a\nmath enthusiast suffering from an anxiety\ndisorder, clinical depression and ADHD?",
                **kw
            ),
            Text(
                "Is Ben, Ben and Blue still a thing?",
                **kw
            ),
            Text(
                "Favorite podcasts?",
                **kw
            ),
            Text(
                "Hey Grant, if you had, both, the responsibility and\nopportunity to best introduce the world of mathematics\nto curious and intelligent minds before they are shaped\nby the antiquated, disempowering and demotivational\neducation system of today, what would you do?  (Asking\nbecause I will soon be a father).",
                **kw
            ),
            Text(
                "What's something you think could've\nbeen discovered long before it was\nactually discovered?",
                **kw
            ),
            Text(
                "Can we fix math on Wikipedia? Really serious\nhere. I constantly go there after your vids for\na bit of deeper dive and learn - nothing more, ever.\nCompared to almost any topic in the natural sciences\nor physics where at least I get an outline of where\nto go next. It's such a shame.",
                **kw
            ),
        )

        last_question = VMobject()
        for question in questions:
            question.set_width(config.frame_width - 1)  # FRAME_WIDTH 改為 config.frame_width
            self.play(
                FadeIn(question, shift=DOWN),  # FadeInFromDown 改為 FadeIn(shift=DOWN)
                FadeOut(last_question, shift=UP)  # FadeOut(UP) 改為 FadeOut(shift=UP)
            )
            last_question = question
            self.wait(2)
