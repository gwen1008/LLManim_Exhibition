from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("二次函數平移求 PQ", font_size=36)
        title.to_edge(UP)
        underline = Line(title.get_left(), title.get_right(), color=WHITE).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        # Setup axes
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-1, 5, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_tip": True, "include_numbers": False},
        ).to_edge(DOWN, buff=0.5).shift(LEFT * 2.5)
        self.play(Create(axes))

        # Line y = 1 + 2x
        line = axes.plot(lambda x: 1 + 2 * x, x_range=[-1.5, 2.0], color=YELLOW)
        line_label = MathTex("y=1+2x", color=YELLOW).scale(0.6).next_to(line.get_end(), UR, buff=0.1)
        self.play(Create(line), Write(line_label))
        self.wait(0.3)

        # Original parabola f(x) = -4x^2 + 1
        para1 = axes.plot(lambda x: -4 * x**2 + 1, x_range=[-1.0, 1.0], color=BLUE)
        para1_label = MathTex("y=-4x^2+1", color=BLUE).scale(0.55).to_corner(UR).shift(DOWN * 0.8)
        self.play(Create(para1), Write(para1_label))

        # Points A, B, P
        A = Dot(axes.c2p(-0.5, 0), color=RED)
        B = Dot(axes.c2p(0.5, 0), color=RED)
        P = Dot(axes.c2p(0, 1), color=GREEN)
        A_lbl = MathTex(r"A(-\tfrac{1}{2},0)").scale(0.5).next_to(A, DL, buff=0.05)
        B_lbl = MathTex(r"B(\tfrac{1}{2},0)").scale(0.5).next_to(B, DR, buff=0.05)
        P_lbl = MathTex("P(0,1)", color=GREEN).scale(0.55).next_to(P, UP, buff=0.1)
        self.play(FadeIn(A, B), Write(A_lbl), Write(B_lbl))
        self.play(FadeIn(P), Write(P_lbl))
        self.wait(0.5)

        # Steps panel on right
        steps = VGroup(
            VGroup(Text("頂點 Q=", font_size=22), MathTex(r"(h,\,1+2h)").scale(0.55)).arrange(RIGHT, buff=0.1),
            MathTex(r"0=-4(\tfrac{1}{2}-h)^2+1+2h").scale(0.55),
            MathTex(r"6h-4h^2=0").scale(0.55),
            VGroup(MathTex("h=0").scale(0.55), Text("或", font_size=22), MathTex(r"h=\tfrac{3}{2}").scale(0.55)).arrange(RIGHT, buff=0.1),
            MathTex(r"\Rightarrow Q=(\tfrac{3}{2},\,4)").scale(0.55),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR).shift(DOWN * 1.6)

        for s in steps:
            self.play(Write(s), run_time=0.7)
        self.wait(0.3)

        # Translated parabola: vertex Q=(3/2,4) -> y = -4(x-3/2)^2 + 4
        para2 = axes.plot(lambda x: -4 * (x - 1.5)**2 + 4, x_range=[0.5, 2.5], color=ORANGE)
        Q = Dot(axes.c2p(1.5, 4), color=PURPLE)
        Q_lbl = MathTex(r"Q(\tfrac{3}{2},4)", color=PURPLE).scale(0.55).next_to(Q, UP, buff=0.1)
        self.play(TransformFromCopy(para1, para2))
        self.play(FadeIn(Q), Write(Q_lbl))
        self.wait(0.3)

        # PQ segment
        seg = Line(axes.c2p(0, 1), axes.c2p(1.5, 4), color=WHITE, stroke_width=4)
        self.play(Create(seg))
        self.wait(0.3)

        # Final answer
        ans = MathTex(
            r"\overline{PQ}=\sqrt{\left(\tfrac{3}{2}\right)^{2}+3^{2}}=\sqrt{\tfrac{45}{4}}=\tfrac{3\sqrt{5}}{2}"
        ).scale(0.6).to_edge(DOWN, buff=0.15)
        box = SurroundingRectangle(ans, color=GREEN, buff=0.1)
        self.play(Write(ans))
        self.play(Create(box))
        self.wait(2)