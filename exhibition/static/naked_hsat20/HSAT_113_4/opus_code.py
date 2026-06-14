from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title(r"求解 $\sin\left(x+\frac{\pi}{6}\right)=\sin x+\sin\frac{\pi}{6}$")
        self.play(Write(title))
        self.wait(0.5)

        cond = MathTex(r"0 \le x < 2\pi").scale(0.8).next_to(title, DOWN)
        self.play(FadeIn(cond))
        self.wait(0.5)

        eq1 = MathTex(
            r"\sin\!\left(x+\tfrac{\pi}{6}\right)-\sin x=\sin\tfrac{\pi}{6}"
        ).scale(0.9)
        eq1.next_to(cond, DOWN, buff=0.6)
        self.play(Write(eq1))
        self.wait(0.8)

        note = MathTex(
            r"\sin A-\sin B=2\cos\tfrac{A+B}{2}\sin\tfrac{A-B}{2}"
        ).scale(0.7).set_color(YELLOW)
        note.next_to(eq1, DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(0.8)

        eq2 = MathTex(
            r"2\cos\!\left(x+\tfrac{\pi}{12}\right)\sin\tfrac{\pi}{12}",
            r"=2\sin\tfrac{\pi}{12}\cos\tfrac{\pi}{12}",
        ).scale(0.85)
        eq2.next_to(note, DOWN, buff=0.5)
        self.play(TransformFromCopy(eq1, eq2))
        self.wait(1)

        self.play(FadeOut(note))

        eq3 = MathTex(
            r"\cos\!\left(x+\tfrac{\pi}{12}\right)=\cos\tfrac{\pi}{12}"
        ).scale(0.9)
        eq3.move_to(note.get_center())
        self.play(Write(eq3))
        self.wait(0.8)

        sol = MathTex(
            r"x+\tfrac{\pi}{12}=\pm\tfrac{\pi}{12}+2k\pi"
        ).scale(0.85)
        sol.next_to(eq3, DOWN, buff=0.5)
        self.play(Write(sol))
        self.wait(0.8)

        roots = VGroup(
            MathTex(r"x = 0 \quad\Rightarrow\quad x=0").scale(0.8),
            MathTex(r"x = -\tfrac{\pi}{6}+2k\pi \;\Rightarrow\; x=\tfrac{11\pi}{6}").scale(0.8),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        roots.next_to(sol, DOWN, buff=0.5)
        self.play(LaggedStart(*[Write(r) for r in roots], lag_ratio=0.5))
        self.wait(1)

        box = SurroundingRectangle(roots, color=GREEN, buff=0.2)
        ans = MathTex(r"\Rightarrow\;2\text{ 個實數解}").scale(0.95).set_color(GREEN)
        ans.next_to(box, RIGHT, buff=0.4)
        self.play(Create(box), Write(ans))
        self.wait(2)