from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("三次多項式的對稱中心", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: division relation
        eq1 = MathTex(r"f(x) = (x+6)\,q(x) + 3", font_size=44)
        eq1.next_to(title, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(0.8)

        note1 = Text("f 為三次  →  q 為二次", font_size=30, color=YELLOW)
        note1.next_to(eq1, DOWN, buff=0.4)
        self.play(FadeIn(note1, shift=UP * 0.3))
        self.wait(1)

        # Step 2: q(x) vertex form
        eq2 = MathTex(r"q(x) = a(x+6)^2 + 8,\quad a<0", font_size=42)
        eq2.next_to(note1, DOWN, buff=0.5)
        cond = Text("在 x = -6 有最大值 8", font_size=28, color=BLUE)
        cond.next_to(eq2, DOWN, buff=0.35)
        self.play(Write(eq2))
        self.play(FadeIn(cond, shift=UP * 0.3))
        self.wait(1.2)

        self.play(
            FadeOut(note1), FadeOut(cond),
            eq2.animate.next_to(eq1, DOWN, buff=0.5),
        )
        self.wait(0.3)

        # Step 3: substitute
        eq3 = MathTex(
            r"f(x) = (x+6)\big[a(x+6)^2 + 8\big] + 3",
            font_size=40,
        )
        eq3.next_to(eq2, DOWN, buff=0.6)
        self.play(Write(eq3))
        self.wait(1)

        eq4 = MathTex(
            r"f(x) = a(x+6)^3 + 8(x+6) + 3",
            font_size=42,
        )
        eq4.next_to(eq3, DOWN, buff=0.5)
        self.play(TransformFromCopy(eq3, eq4))
        self.wait(1.2)

        # Step 4: substitution u = x+6
        self.play(
            FadeOut(eq1), FadeOut(eq2), FadeOut(eq3),
            eq4.animate.next_to(title, DOWN, buff=0.6),
        )
        u_eq = MathTex(r"u = x+6:\quad g(u) = a\,u^3 + 8u + 3", font_size=42)
        u_eq.next_to(eq4, DOWN, buff=0.6)
        self.play(Write(u_eq))
        self.wait(0.8)

        odd = Text("a u³ + 8u 為奇函數，關於原點對稱", font_size=30, color=YELLOW)
        odd.next_to(u_eq, DOWN, buff=0.4)
        self.play(FadeIn(odd, shift=UP * 0.3))
        self.wait(1)

        center_u = MathTex(r"\Rightarrow\ \text{對稱中心 } u=0,\ y=3", font_size=40, color=GREEN)
        center_u.next_to(odd, DOWN, buff=0.4)
        self.play(Write(center_u))
        self.wait(1)

        # Final answer
        box = SurroundingRectangle(center_u, color=GREEN, buff=0.2)
        answer = MathTex(r"\boxed{(-6,\ 3)}", font_size=60, color=GOLD)
        answer.next_to(center_u, DOWN, buff=0.7)
        self.play(Create(box))
        self.play(Write(answer))
        self.wait(2)

        self.play(
            FadeOut(VGroup(eq4, u_eq, odd, center_u, box, title))
        )
        self.play(answer.animate.move_to(ORIGIN).scale(1.3))
        self.wait(2)