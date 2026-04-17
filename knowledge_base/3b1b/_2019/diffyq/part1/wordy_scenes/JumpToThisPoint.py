# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一個黃色圓點從巨大尺寸縮小出現，然後一個箭頭和文字從下方淡入指向該圓點的動畫。



from manim import *
class JumpToThisPoint(Scene):
    def construct(self):
        dot = Dot(color=YELLOW)
        dot.scale(0.5)

        arrow = Vector(DR, color=WHITE)
        arrow.next_to(dot, UL, buff=SMALL_BUFF)
        words = Text(
            "Jump directly to\nthis point?",
        )
        words.add_background_rectangle()
        words.next_to(arrow.get_start(), UP, buff=SMALL_BUFF)

        self.play(
            dot.animate.scale(20).set_opacity(0).animate.scale(1/20).set_opacity(1),
            rate_func=rush_into,
        )
        self.play(
            GrowArrow(arrow),
            FadeIn(words, shift=DOWN),
        )
