from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("摸彩箱抽獎期望值問題", font_size=40)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: total participants
        s1 = VGroup(
            Text("中獎機率 = 0.4% = 幸運球數 / 總球數", font_size=28),
            MathTex(r"0.004 = \frac{10}{N} \;\Rightarrow\; N = \frac{10}{0.004} = 2500"),
        ).arrange(DOWN, buff=0.4)
        s1.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(s1[0], shift=UP))
        self.play(Write(s1[1]))
        self.wait(1.2)
        self.play(FadeOut(s1))

        # Step 2: ball composition
        comp = VGroup(
            MathTex(r"\text{總球數} = 2500"),
            MathTex(r"5000\text{元禮券球}: 5 \text{ 顆}"),
            MathTex(r"8000\text{元禮券球}: 5 \text{ 顆}"),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        comp.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(LaggedStartMap(FadeIn, comp, shift=RIGHT, lag_ratio=0.3))
        self.wait(1)

        # Step 3: after first 100 draws
        cond = VGroup(
            Text("前 100 位抽完後：", font_size=26, color=YELLOW),
            MathTex(r"\text{已抽 } 100 \text{ 顆，剩 } 2500-100=2400"),
            MathTex(r"5000\text{球剩}: 5-1=4"),
            MathTex(r"8000\text{球剩}: 5-0=5"),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cond.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.8)
        self.play(LaggedStartMap(FadeIn, cond, shift=LEFT, lag_ratio=0.3))
        self.wait(1.5)

        self.play(FadeOut(comp), FadeOut(cond))

        # Step 4: expected value for person 101
        head = Text("第 101 號的期望值", font_size=30, color=BLUE)
        head.next_to(title, DOWN, buff=0.5)
        self.play(Write(head))

        ev = MathTex(
            r"E", r"=", r"5000\cdot\frac{4}{2400}", r"+", r"8000\cdot\frac{5}{2400}"
        )
        ev.next_to(head, DOWN, buff=0.6)
        self.play(Write(ev))
        self.wait(1)

        ev2 = MathTex(r"E = \frac{20000 + 40000}{2400} = \frac{60000}{2400}")
        ev2.next_to(ev, DOWN, buff=0.5)
        self.play(Write(ev2))
        self.wait(1)

        ans = MathTex(r"E = 25 \text{ 元}", font_size=52, color=GREEN)
        ans.next_to(ev2, DOWN, buff=0.6)
        box = SurroundingRectangle(ans, color=GREEN, buff=0.25)
        self.play(Write(ans))
        self.play(Create(box))
        self.wait(2)