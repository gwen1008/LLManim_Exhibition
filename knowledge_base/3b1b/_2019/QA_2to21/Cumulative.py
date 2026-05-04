# Source: 3b1b/_2019/QA_2to21.py
# Description: [3b1b translated] 展示一組矩形從上到下依序填充顏色並標記勾號，中間有一個矩形被移除後再恢復，其後的矩形從叉號轉為勾號的動態過程。


from manim import *
import random
import itertools as it

class Cumulative(Scene):
    def construct(self):
        colors = list(Color(BLUE_B).range_to(BLUE_D, 20))
        rects = VGroup(*[
            Rectangle(
                height=0.3, width=4,
                fill_color=random.choice(colors),
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=1,
            )
            for i, color in zip(range(20), it.cycle(colors))
        ])
        rects.arrange(UP, buff=0)

        check = MathTex("\\checkmark").set_color(GREEN)
        cross = MathTex("\\times").set_color(RED)
        checks, crosses = [
            VGroup(*[
                mob.copy().next_to(rect, RIGHT, SMALL_BUFF)
                for rect in rects
            ])
            for mob in [check, cross]
        ]

        rects.set_fill(opacity=0)
        self.add(rects)

        for i in range(7):
            self.play(
                rects[i].animate.set_fill(opacity=1.0),
                Write(checks[i]),
                run_time=0.5,
            )
        self.play(FadeOut(rects[7], shift=2 * LEFT))
        self.play(
            LaggedStartMap(Write, crosses[8:]),
            LaggedStartMap(
                lambda m: m.animate.set_fill(opacity=0.2),
                rects[8:],
            )
        )
        self.wait()
        rects[7].set_opacity(1)
        self.play(
            FadeIn(rects[7], shift=2 * LEFT),
            FadeIn(checks[7], shift=2 * LEFT),
        )
        self.play(
            LaggedStartMap(
                lambda m: m.animate.set_fill(opacity=1.0),
                rects[8:],
            ),
            LaggedStart(*[
                ReplacementTransform(cross, check)
                for cross, check in zip(crosses[8:], checks[8:])
            ])
        )
        self.wait()
