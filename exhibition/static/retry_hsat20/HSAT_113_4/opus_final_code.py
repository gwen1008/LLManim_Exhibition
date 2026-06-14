from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("求 x 的個數", font_size=40).to_edge(UP)
        problem = MathTex(
            r"\sin\!\left(x+\tfrac{\pi}{6}\right)=\sin x+\sin\tfrac{\pi}{6},",
            r"\quad 0\le x<2\pi",
            font_size=40,
        )
        problem.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(Write(problem))
        self.wait(1)

        step1 = MathTex(
            r"\sin\!\left(x+\tfrac{\pi}{6}\right)-\sin x=\sin\tfrac{\pi}{6}",
            font_size=38,
        ).next_to(problem, DOWN, buff=0.6)
        self.play(Write(step1))
        self.wait(1)

        note = VGroup(
            Text("和差化積：", font_size=26, color=YELLOW),
            MathTex(r"\sin A-\sin B=2\cos\tfrac{A+B}{2}\sin\tfrac{A-B}{2}",
                    font_size=30, color=YELLOW),
        ).arrange(RIGHT, buff=0.2).next_to(step1, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(1)

        step2 = MathTex(
            r"2\cos\!\left(x+\tfrac{\pi}{12}\right)\sin\tfrac{\pi}{12}"
            r"=2\sin\tfrac{\pi}{12}\cos\tfrac{\pi}{12}",
            font_size=34,
        ).next_to(note, DOWN, buff=0.5)
        self.play(Write(step2))
        self.wait(1)

        step3 = MathTex(
            r"\cos\!\left(x+\tfrac{\pi}{12}\right)=\cos\tfrac{\pi}{12}",
            font_size=38,
        ).next_to(step2, DOWN, buff=0.5)
        self.play(TransformFromCopy(step2, step3))
        self.wait(1)

        self.play(
            FadeOut(note), FadeOut(step1), FadeOut(step2),
            step3.animate.next_to(problem, DOWN, buff=0.6),
        )
        self.wait(0.5)

        sol = MathTex(
            r"x+\tfrac{\pi}{12}=\pm\tfrac{\pi}{12}+2k\pi",
            font_size=38,
        ).next_to(step3, DOWN, buff=0.6)
        self.play(Write(sol))
        self.wait(1)

        case1 = MathTex(r"x=0", font_size=40, color=GREEN)
        case2 = MathTex(r"x=-\tfrac{\pi}{6}+2\pi=\tfrac{11\pi}{6}", font_size=40, color=GREEN)
        cases = VGroup(case1, case2).arrange(DOWN, buff=0.4).next_to(sol, DOWN, buff=0.6)
        self.play(Write(case1))
        self.wait(0.5)
        self.play(Write(case2))
        self.wait(1)

        box = SurroundingRectangle(cases, color=BLUE, buff=0.3)
        answer = Text("共有 2 個解", font_size=40, color=RED).next_to(box, RIGHT, buff=0.6)
        self.play(Create(box), Write(answer))
        self.wait(2)

        self.play(
            FadeOut(VGroup(title, problem, step3, sol, cases, box, answer))
        )
        final = MathTex(r"\boxed{2}", font_size=120, color=YELLOW)
        self.play(Write(final))
        self.wait(2)