# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一個帶有驚嘆號三角形警告標誌的「劇透警告」文字，並從上方淡入貝葉斯公式。



from manim import *
class SpoilerAlert(Scene):
    def construct(self):
        sa_words = Text("Spoiler Alert")
        sa_words.scale(2)
        sa_words.to_edge(UP)
        sa_words.set_color(RED)

        alert = Triangle(start_angle=90 * DEGREES)
        alert.set_stroke(RED, 8)
        alert.set_height(sa_words.get_height())
        alert.round_corners(0.1)
        bang = Text("!")
        bang.set_color(RED)
        bang.scale(1.5)
        bang.move_to(alert)
        alert.add(bang)

        alert.next_to(sa_words, LEFT)
        sa_words.add(alert.copy())
        alert.next_to(sa_words, RIGHT)
        sa_words.add(alert)

        formula = get_bayes_formula()
        formula_words = Text("This is secretly ")
        formula_words.scale(1.5)
        formula_group = VGroup(formula_words, formula)
        formula_group.arrange(DOWN, buff=MED_LARGE_BUFF)
        formula_group.next_to(sa_words, DOWN, LARGE_BUFF)

        self.add(sa_words)
        self.wait()
        self.play(FadeIn(formula_group, shift=UP))
        self.wait()
