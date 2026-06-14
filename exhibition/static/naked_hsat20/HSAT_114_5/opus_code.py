from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title(r"求解 $\sin 2\theta > \sin\theta$ 且 $\cos 2\theta > \cos\theta$")
        self.play(Write(title))
        self.wait(0.5)

        # First inequality
        ineq1 = MathTex(r"\sin 2\theta > \sin\theta").scale(0.9)
        step1a = MathTex(r"2\sin\theta\cos\theta - \sin\theta > 0").scale(0.9)
        step1b = MathTex(r"\sin\theta\,(2\cos\theta - 1) > 0").scale(0.9)

        g1 = VGroup(ineq1, step1a, step1b).arrange(DOWN, buff=0.35)
        g1.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)

        self.play(Write(ineq1))
        self.play(TransformFromCopy(ineq1, step1a))
        self.play(TransformFromCopy(step1a, step1b))
        self.wait(0.5)

        # Second inequality
        ineq2 = MathTex(r"\cos 2\theta > \cos\theta").scale(0.9)
        step2a = MathTex(r"2\cos^2\theta - 1 - \cos\theta > 0").scale(0.9)
        step2b = MathTex(r"(2\cos\theta + 1)(\cos\theta - 1) > 0").scale(0.9)

        g2 = VGroup(ineq2, step2a, step2b).arrange(DOWN, buff=0.35)
        g2.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.8)

        self.play(Write(ineq2))
        self.play(TransformFromCopy(ineq2, step2a))
        self.play(TransformFromCopy(step2a, step2b))
        self.wait(0.5)

        # Analysis line
        self.play(FadeOut(g1), FadeOut(g2))

        a2 = MathTex(
            r"\cos\theta - 1 \le 0 \;\Rightarrow\; 2\cos\theta + 1 < 0",
            r"\;\Rightarrow\; \cos\theta < -\tfrac{1}{2}",
        ).scale(0.85)
        a2_res = MathTex(r"\frac{2\pi}{3} < \theta < \frac{4\pi}{3}").scale(0.95)
        groupB = VGroup(a2, a2_res).arrange(DOWN, buff=0.4)
        groupB.next_to(title, DOWN, buff=0.7)

        self.play(Write(a2))
        self.play(Write(a2_res))
        self.wait(0.8)
        self.play(groupB.animate.scale(0.8).to_edge(LEFT, buff=0.6))

        a1 = MathTex(
            r"2\cos\theta - 1 < 0 \;\Rightarrow\; \sin\theta < 0",
        ).scale(0.85)
        a1_res = MathTex(r"\pi < \theta < 2\pi").scale(0.95)
        groupA = VGroup(a1, a1_res).arrange(DOWN, buff=0.4)
        groupA.to_edge(RIGHT, buff=0.6).shift(UP * 0.5)

        self.play(Write(a1))
        self.play(Write(a1_res))
        self.wait(0.8)

        # Intersection
        inter = MathTex(r"\Rightarrow\; \pi < \theta < \frac{4\pi}{3}").scale(1.1)
        inter.set_color(YELLOW)
        inter.move_to(DOWN * 1.8)
        self.play(Write(inter))
        self.wait(0.8)

        self.play(
            FadeOut(groupA), FadeOut(groupB),
            inter.animate.move_to(UP * 1.2).scale(1.1),
        )

        ab = MathTex(r"a = 1, \quad b = \frac{4}{3}").scale(1.1)
        ab.next_to(inter, DOWN, buff=0.6)
        self.play(Write(ab))
        self.wait(0.5)

        ans = MathTex(r"b - a = \frac{4}{3} - 1 = \frac{1}{3}").scale(1.2)
        ans.set_color(GREEN)
        ans.next_to(ab, DOWN, buff=0.6)
        box = SurroundingRectangle(ans, color=GREEN, buff=0.25)
        self.play(Write(ans))
        self.play(Create(box))
        self.wait(2)