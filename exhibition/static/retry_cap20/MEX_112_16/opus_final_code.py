from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("套餐問題", font_size=40, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Define variables
        setup = VGroup(
            VGroup(MathTex(r"c = "), Text("單點雞排價", font_size=28)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex(r"k = "), Text("單點可樂價", font_size=28)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(m) for m in setup], lag_ratio=0.5))
        self.wait(0.5)

        # Set meal price
        line1 = VGroup(
            Text("一份套餐", font_size=28),
            MathTex(r"= c + k - 40"),
        ).arrange(RIGHT, buff=0.2)
        line1.next_to(setup, DOWN, buff=0.5)
        self.play(FadeIn(line1))
        self.wait(0.5)

        # Two set meals
        line2 = VGroup(
            Text("兩份套餐", font_size=28),
            MathTex(r"= 2(c+k-40) = 2c + 2k - 80"),
        ).arrange(RIGHT, buff=0.2)
        line2.next_to(line1, DOWN, buff=0.4)
        self.play(FadeIn(line2))
        self.wait(0.5)

        # Single chicken + two colas
        line3 = VGroup(
            Text("雞排+兩可樂", font_size=28),
            MathTex(r"= c + 2k"),
        ).arrange(RIGHT, buff=0.2)
        line3.next_to(line2, DOWN, buff=0.4)
        self.play(FadeIn(line3))
        self.wait(0.5)

        # Condition: cheaper by 10
        cond = MathTex(r"c + 2k = (2c + 2k - 80) - 10")
        cond.next_to(line3, DOWN, buff=0.5)
        self.play(Write(cond))
        self.wait(0.8)

        # Simplify
        step = MathTex(r"c + 2k = 2c + 2k - 90")
        step.next_to(cond, DOWN, buff=0.4)
        self.play(Write(step))
        self.wait(0.6)

        result = MathTex(r"0 = c - 90 \;\Rightarrow\; c = 90")
        result.next_to(step, DOWN, buff=0.4)
        self.play(TransformFromCopy(step, result))
        self.wait(0.6)

        box = SurroundingRectangle(result, color=GREEN, buff=0.15)
        self.play(Create(box))
        self.wait(0.5)

        ans = Text("答案：(C) 單點一片雞排必為 90 元",
                   font_size=30, color=GREEN).to_edge(DOWN)
        self.play(FadeIn(ans, shift=UP))
        self.wait(2)

        self.play(
            *[FadeOut(m) for m in [setup, line1, line2, line3, cond, step]],
            run_time=1,
        )
        result_box = VGroup(result, box)
        self.play(result_box.animate.scale(1.4).move_to(ORIGIN))
        self.wait(2)