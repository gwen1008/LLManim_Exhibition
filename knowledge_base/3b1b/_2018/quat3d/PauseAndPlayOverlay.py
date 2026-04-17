# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示一個暫停符號、箭頭和"Interact..."文字組成的互動提示，最後出現"not yet"文字。



from manim import *
class PauseAndPlayOverlay(Scene):
    def construct(self):
        pause = MathTex("=").rotate(TAU / 4)
        pause.stretch(2, 0)
        pause.scale(1.5)
        arrow = Arrow(start=LEFT, end=RIGHT, color=WHITE)
        interact = Text("Interact...")
        group = VGroup(pause, arrow, interact)
        group.arrange(RIGHT)
        group.scale(2)

        not_yet = Text("...well, not yet")
        not_yet.scale(2)
        not_yet.next_to(group, DOWN, buff=MED_LARGE_BUFF)

        self.play(Write(pause))
        self.play(
            GrowFromPoint(
                interact, arrow.get_left(),
                rate_func=lambda t: squish_rate_func(smooth, 0.3, 1)(t)
            ),
            FadeIn(interact),
            GrowArrow(arrow),
        )
        self.wait(2)
        self.play(Write(not_yet))
        self.wait()
