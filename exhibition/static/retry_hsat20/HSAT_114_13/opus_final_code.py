from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("三次多項式的對稱中心", font_size=40)
        underline = Line(LEFT, RIGHT).set_width(title.width + 0.5)
        underline.next_to(title, DOWN, buff=0.15)
        title_group = VGroup(title, underline).to_edge(UP, buff=0.4)
        self.play(Write(title_group))
        self.wait(0.5)

        # Step 1: setup the division
        s1 = MathTex(r"f(x) = (x+6)\,q(x) + 3").scale(0.9)
        s1.next_to(title_group, DOWN, buff=0.5)
        self.play(Write(s1))
        self.wait(0.8)

        note = VGroup(
            Text("f(x) 為三次", font_size=26),
            MathTex(r"\Rightarrow").scale(0.7),
            Text("q(x) 為二次", font_size=26),
        ).arrange(RIGHT, buff=0.2)
        note.next_to(s1, DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP))
        self.wait(0.8)

        # Step 2: q(x) has max 8 at x=-6
        s2 = MathTex(r"q(x) = a(x+6)^2 + 8,\quad a<0").scale(0.85)
        s2.next_to(note, DOWN, buff=0.5)
        self.play(Write(s2))
        self.wait(0.8)

        cond = Text("在 x = -6 有最大值 8", font_size=26)
        cond.next_to(s2, DOWN, buff=0.3)
        self.play(FadeIn(cond, shift=UP))
        self.wait(1)

        self.play(FadeOut(VGroup(note, cond)))

        # Step 3: substitute t = x+6
        sub = VGroup(
            Text("令", font_size=28),
            MathTex(r"t = x+6").scale(0.8),
        ).arrange(RIGHT, buff=0.2)
        sub.next_to(s2, DOWN, buff=0.4)
        self.play(Write(sub))
        self.wait(0.6)

        f1 = MathTex(r"f(x) = (x+6)\big[a(x+6)^2 + 8\big] + 3").scale(0.8)
        f1.next_to(sub, DOWN, buff=0.4)
        self.play(Write(f1))
        self.wait(0.8)

        f2 = MathTex(r"f = a\,t^3 + 8\,t + 3").scale(0.9)
        f2.next_to(f1, DOWN, buff=0.4)
        self.play(TransformFromCopy(f1, f2))
        self.wait(1)

        self.play(FadeOut(VGroup(s1, s2, sub, f1)))
        self.play(f2.animate.next_to(title_group, DOWN, buff=0.6))
        self.wait(0.5)

        # Step 4: inflection point => symmetry center
        d1 = MathTex(r"f'' = 6a\,t = 0 \;\Rightarrow\; t = 0").scale(0.85)
        d1.next_to(f2, DOWN, buff=0.5)
        self.play(Write(d1))
        self.wait(0.8)

        d2 = MathTex(r"t = 0 \;\Rightarrow\; x = -6").scale(0.85)
        d2.next_to(d1, DOWN, buff=0.4)
        self.play(Write(d2))
        self.wait(0.6)

        d3 = MathTex(r"f(-6) = a\cdot 0 + 8\cdot 0 + 3 = 3").scale(0.85)
        d3.next_to(d2, DOWN, buff=0.4)
        self.play(Write(d3))
        self.wait(1)

        # Final answer
        ans = VGroup(
            Text("對稱中心 =", font_size=32),
            MathTex(r"(-6,\ 3)").scale(0.9),
        ).arrange(RIGHT, buff=0.2)
        ans.set_color(YELLOW)
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.3)
        ans_group = VGroup(ans, box)
        ans_group.next_to(d3, DOWN, buff=0.5)
        self.play(Write(ans), Create(box))
        self.wait(2)

        self.play(
            FadeOut(VGroup(f2, d1, d2, d3)),
            ans_group.animate.move_to(ORIGIN).scale(1.2),
        )
        self.wait(2)