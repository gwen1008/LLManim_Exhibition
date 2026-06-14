from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("抽發財金的期望值", font_size=44, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            Text("抽兩次籤", font_size=30),
            MathTex(r"P(\text{吉}) = \frac{1}{3}, \quad P(\text{祥}) = \frac{1}{3}", font_size=34),
        ).arrange(DOWN, buff=0.4)
        setup.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(setup, shift=UP))
        self.wait(1)

        # Case 1: both 吉
        case1 = MathTex(
            r"P(\text{吉},\text{吉}) = \frac{1}{3} \times \frac{1}{3} = \frac{1}{9}",
            font_size=34, color=GREEN,
        )
        prize1 = MathTex(r"\Rightarrow \text{獎金 } 180 \text{ 元}", font_size=30, color=GREEN)
        g1 = VGroup(case1, prize1).arrange(RIGHT, buff=0.4)
        g1.next_to(setup, DOWN, buff=0.6)
        self.play(Write(case1))
        self.play(FadeIn(prize1, shift=RIGHT))
        self.wait(1)

        # Case 2: both 祥
        case2 = MathTex(
            r"P(\text{祥},\text{祥}) = \frac{1}{3} \times \frac{1}{3} = \frac{1}{9}",
            font_size=34, color=BLUE,
        )
        prize2 = MathTex(r"\Rightarrow \text{獎金 } 90 \text{ 元}", font_size=30, color=BLUE)
        g2 = VGroup(case2, prize2).arrange(RIGHT, buff=0.4)
        g2.next_to(g1, DOWN, buff=0.5)
        self.play(Write(case2))
        self.play(FadeIn(prize2, shift=RIGHT))
        self.wait(1)

        # Expected value
        ev_label = Text("期望值 E", font_size=32, color=YELLOW)
        ev = MathTex(
            r"E = 180 \times \frac{1}{9} + 90 \times \frac{1}{9}",
            font_size=36,
        )
        ev_calc = MathTex(r"= 20 + 10 = 30", font_size=36, color=YELLOW)
        ev_group = VGroup(ev, ev_calc).arrange(DOWN, buff=0.35)
        ev_group.next_to(g2, DOWN, buff=0.6)

        self.play(Write(ev))
        self.wait(0.8)
        self.play(Write(ev_calc))
        self.wait(0.8)

        box = SurroundingRectangle(ev_calc, color=RED, buff=0.15)
        ans = Text("期望值 = 30 元", font_size=34, color=RED)
        ans.next_to(box, DOWN, buff=0.3)
        self.play(Create(box))
        self.play(FadeIn(ans, shift=UP))
        self.wait(2)