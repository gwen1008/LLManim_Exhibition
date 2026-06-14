from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\sin 2\theta > \sin\theta \quad\text{and}\quad \cos 2\theta > \cos\theta",
                        font_size=40)
        title.to_edge(UP)
        sub = MathTex(r"0 \leq \theta \leq 2\pi", font_size=34, color=YELLOW)
        sub.next_to(title, DOWN, buff=0.25)
        self.play(Write(title))
        self.play(FadeIn(sub, shift=DOWN))
        self.wait(0.5)

        # ---- Inequality 1: sin2θ > sinθ ----
        ineq1_title = Tex("(1)", color=BLUE, font_size=36).to_edge(LEFT).shift(UP * 1.2)
        s1 = MathTex(r"\sin 2\theta - \sin\theta > 0", font_size=34)
        s2 = MathTex(r"2\sin\theta\cos\theta - \sin\theta > 0", font_size=34)
        s3 = MathTex(r"\sin\theta\,(2\cos\theta - 1) > 0", font_size=34)
        for m in (s1, s2, s3):
            m.next_to(ineq1_title, RIGHT, buff=0.4)
        self.play(FadeIn(ineq1_title), Write(s1))
        self.wait(0.4)
        self.play(TransformMatchingShapes(s1, s2))
        self.wait(0.4)
        self.play(TransformMatchingShapes(s2, s3))
        self.wait(0.6)

        # ---- Inequality 2: cos2θ > cosθ ----
        ineq2_title = Tex("(2)", color=GREEN, font_size=36).to_edge(LEFT).shift(DOWN * 0.3)
        c1 = MathTex(r"\cos 2\theta - \cos\theta > 0", font_size=34)
        c2 = MathTex(r"2\cos^2\theta - \cos\theta - 1 > 0", font_size=34)
        c3 = MathTex(r"(2\cos\theta + 1)(\cos\theta - 1) > 0", font_size=34)
        for m in (c1, c2, c3):
            m.next_to(ineq2_title, RIGHT, buff=0.4)
        self.play(FadeIn(ineq2_title), Write(c1))
        self.wait(0.4)
        self.play(TransformMatchingShapes(c1, c2))
        self.wait(0.4)
        self.play(TransformMatchingShapes(c2, c3))
        self.wait(0.6)

        # ---- Deductions ----
        d2 = MathTex(r"\cos\theta < -\tfrac{1}{2}\ \Rightarrow\ \tfrac{2\pi}{3} < \theta < \tfrac{4\pi}{3}",
                     font_size=32, color=GREEN)
        d2.next_to(ineq2_title, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(d2))
        self.wait(0.5)

        d1 = MathTex(r"2\cos\theta - 1 < 0 \Rightarrow \sin\theta < 0 \Rightarrow \pi < \theta < 2\pi",
                     font_size=30, color=BLUE)
        d1.next_to(d2, DOWN, buff=0.35).to_edge(LEFT)
        self.play(Write(d1))
        self.wait(0.6)

        # Clear left text, keep title
        self.play(
            *[FadeOut(m) for m in (ineq1_title, ineq2_title, s3, c3)],
        )
        self.wait(0.3)

        # ---- Unit circle on the right ----
        axes = NumberPlane(
            x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1],
            x_length=3.2, y_length=3.2,
            background_line_style={"stroke_opacity": 0.25},
        ).to_edge(RIGHT).shift(DOWN * 0.4)
        circle = Circle(radius=1.6, color=WHITE).move_to(axes.get_center())
        self.play(Create(axes), Create(circle))

        center = axes.get_center()
        R = 1.6

        def pt(angle):
            return center + R * np.array([np.cos(angle), np.sin(angle), 0])

        # arc for (2): 2π/3 to 4π/3 (green)
        arc2 = Arc(radius=R, start_angle=2 * np.pi / 3,
                   angle=2 * np.pi / 3, color=GREEN, stroke_width=8).move_arc_center_to(center)
        # arc for (1): π to 2π (blue)
        arc1 = Arc(radius=R, start_angle=np.pi,
                   angle=np.pi, color=BLUE, stroke_width=8).move_arc_center_to(center)
        self.play(Create(arc2))
        self.play(Create(arc1))
        self.wait(0.4)

        # Intersection arc: π to 4π/3 (red)
        arc_int = Arc(radius=R, start_angle=np.pi,
                      angle=np.pi / 3, color=RED, stroke_width=12).move_arc_center_to(center)
        self.play(Create(arc_int))
        self.wait(0.4)

        result = MathTex(r"\pi < \theta < \tfrac{4\pi}{3}", font_size=34, color=RED)
        result.next_to(d1, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(result))
        self.wait(0.5)

        # ---- Final answer ----
        ans = MathTex(r"a = 1,\quad b = \tfrac{4}{3}", font_size=36)
        ans.next_to(result, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(ans))
        self.wait(0.3)

        final = MathTex(r"b - a = \frac{4}{3} - 1 = \frac{1}{3}", font_size=44, color=YELLOW)
        box = SurroundingRectangle(final, color=YELLOW, buff=0.2)
        grp = VGroup(final, box).next_to(ans, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(final), Create(box))
        self.wait(2)