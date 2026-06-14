from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("二次函數平移：求 $\\overline{PQ}$", include_underline=True)
        self.play(Write(title))
        self.wait(0.5)

        # Set up axes
        axes = Axes(
            x_range=[-2.5, 3, 1],
            y_range=[-2, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True, "color": GREY_B},
        ).to_edge(DOWN, buff=0.4).shift(LEFT * 2.2)
        self.play(Create(axes))

        # Line y = 1 + 2x
        line = axes.plot(lambda x: 1 + 2 * x, x_range=[-2.5, 1.7], color=YELLOW)
        line_label = MathTex("y=1+2x", color=YELLOW).scale(0.6)
        line_label.next_to(line.get_end(), UR, buff=0.1)
        self.play(Create(line), Write(line_label))

        # Original parabola: f(x) = -4x^2 + 1
        para1 = axes.plot(lambda x: -4 * x**2 + 1, x_range=[-1.0, 1.0], color=BLUE)
        para1_label = MathTex("\\Gamma:\\,y=-4x^2+1", color=BLUE).scale(0.55)
        para1_label.to_corner(UR).shift(DOWN * 1.2 + LEFT * 0.2)

        # Points A, B, P
        A = axes.c2p(-0.5, 0)
        B = axes.c2p(0.5, 0)
        P = axes.c2p(0, 1)
        dotA = Dot(A, color=GREEN)
        dotB = Dot(B, color=GREEN)
        dotP = Dot(P, color=RED)
        labA = MathTex("A(-\\tfrac12,0)").scale(0.5).next_to(dotA, DL, buff=0.05)
        labB = MathTex("B(\\tfrac12,0)").scale(0.5).next_to(dotB, DR, buff=0.05)
        labP = MathTex("P(0,1)").scale(0.5).next_to(dotP, UL, buff=0.05)

        self.play(Create(para1), Write(para1_label))
        self.play(FadeIn(dotA, dotB), Write(labA), Write(labB))
        self.play(FadeIn(dotP), Write(labP))
        self.wait(0.5)

        # Reasoning panel
        steps = VGroup(
            MathTex("\\text{對稱軸}: x=0"),
            MathTex("P=(0,\\,1)"),
            MathTex("\\text{平移後頂點 } Q=(h,\\,1+2h)"),
            MathTex("y=-4(x-h)^2+1+2h"),
            MathTex("\\text{過 } B:\\ 6h-4h^2=0"),
            MathTex("h=0 \\text{ (即 }P)\\ \\text{ 或 } h=\\tfrac32"),
            MathTex("Q=\\left(\\tfrac32,\\,4\\right)"),
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT)
        steps.to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        for s in steps:
            self.play(Write(s), run_time=0.6)
        self.wait(0.5)

        # Translated parabola
        para2 = axes.plot(lambda x: -4 * (x - 1.5) ** 2 + 4, x_range=[0.5, 2.5], color=ORANGE)
        Q = axes.c2p(1.5, 4)
        dotQ = Dot(Q, color=RED)
        labQ = MathTex("Q(\\tfrac32,4)").scale(0.5).next_to(dotQ, UR, buff=0.05)
        self.play(TransformFromCopy(para1, para2))
        self.play(FadeIn(dotQ), Write(labQ))
        self.wait(0.3)

        # PQ segment
        seg = Line(P, Q, color=PURPLE, stroke_width=5)
        self.play(Create(seg))

        # Distance computation
        dist = VGroup(
            MathTex("\\overline{PQ}=\\sqrt{\\left(\\tfrac32\\right)^2+3^2}"),
            MathTex("=\\sqrt{\\tfrac94+9}=\\sqrt{\\tfrac{45}{4}}"),
            MathTex("=\\dfrac{3\\sqrt5}{2}"),
        ).scale(0.55).arrange(DOWN, aligned_edge=LEFT)
        dist.next_to(steps, DOWN, buff=0.3).align_to(steps, LEFT)

        for d in dist:
            self.play(Write(d), run_time=0.7)

        box = SurroundingRectangle(dist[2], color=YELLOW, buff=0.1)
        self.play(Create(box))
        self.wait(2)

learnt LLManim_Agent (project instructions, checked into the codebase)