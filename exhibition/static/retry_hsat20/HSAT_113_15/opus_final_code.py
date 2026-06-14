from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("摸彩箱期望值問題", font_size=42).to_edge(UP)
        line = Line(LEFT, RIGHT).set_width(config.frame_width - 1).next_to(title, DOWN, buff=0.15)
        self.play(Write(title), Create(line))
        self.wait(0.5)

        # Step 1: total balls from probability
        s1a = MathTex(r"P = \frac{10}{N} = 0.4\% = 0.004")
        s1b = MathTex(r"N = \frac{10}{0.004} = 2500")
        s1 = VGroup(s1a, s1b).arrange(DOWN, buff=0.4).next_to(line, DOWN, buff=0.6)
        self.play(Write(s1a))
        self.wait(0.5)
        self.play(Write(s1b))
        self.wait(1)
        self.play(FadeOut(s1))

        # Step 2: ball composition
        comp_title = Text("獎球組成：", font_size=30)
        c1 = MathTex(r"5000 \times 5")
        c2 = MathTex(r"8000 \times 5")
        c3 = MathTex(r"2500 - 10 = 2490")
        c3_lbl = Text("未中獎", font_size=26)
        c3row = VGroup(c3_lbl, c3).arrange(RIGHT, buff=0.3)
        comp = VGroup(comp_title, c1, c2, c3row).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        comp.next_to(line, DOWN, buff=0.5)
        for m in comp:
            self.play(Write(m), run_time=0.6)
        self.wait(1)
        self.play(FadeOut(comp))

        # Step 3: after 100 draws
        cond = Text("前 100 位：1 人中 5000 元，0 人中 8000 元", font_size=26)
        cond.next_to(line, DOWN, buff=0.5)
        self.play(Write(cond))
        self.wait(0.5)

        r0 = MathTex(r"\text{drawn}: 1 \times 5000 + 99 \times (\text{none})")
        r1 = MathTex(r"2500 - 100 = 2400")
        rlbl = Text("剩餘總數", font_size=26)
        r1row = VGroup(rlbl, r1).arrange(RIGHT, buff=0.3)
        removed = VGroup(r0, r1row).arrange(DOWN, buff=0.4).next_to(cond, DOWN, buff=0.5)
        self.play(Write(r0))
        self.wait(0.5)
        self.play(Write(r1row))
        self.wait(1)
        self.play(FadeOut(cond), FadeOut(removed))

        # Step 4: remaining composition
        rem_title = Text("剩餘獎球", font_size=28)
        rm1 = MathTex(r"5000: 5-1 = 4")
        rm2 = MathTex(r"8000: 5")
        rm3 = MathTex(r"\text{none}: 2391")
        rem = VGroup(rem_title, rm1, rm2, rm3).arrange(DOWN, buff=0.35).next_to(line, DOWN, buff=0.5)
        for m in rem:
            self.play(Write(m), run_time=0.6)
        self.wait(1)
        self.play(rem.animate.scale(0.7).to_edge(LEFT))

        # Step 5: expected value
        ev0 = MathTex(r"E = \frac{4}{2400}\cdot 5000 + \frac{5}{2400}\cdot 8000")
        ev1 = MathTex(r"= \frac{20000 + 40000}{2400}")
        ev2 = MathTex(r"= \frac{60000}{2400} = 25")
        ev = VGroup(ev0, ev1, ev2).arrange(DOWN, buff=0.4).scale(0.85)
        ev.next_to(rem, RIGHT, buff=0.6)
        self.play(Write(ev0))
        self.wait(0.6)
        self.play(Write(ev1))
        self.wait(0.6)
        self.play(Write(ev2))
        self.wait(0.8)

        box = SurroundingRectangle(ev2, color=YELLOW)
        ans = Text("期望值 = 25 元", font_size=36, color=YELLOW)
        ans.next_to(ev, DOWN, buff=0.5)
        self.play(Create(box), Write(ans))
        self.wait(2)