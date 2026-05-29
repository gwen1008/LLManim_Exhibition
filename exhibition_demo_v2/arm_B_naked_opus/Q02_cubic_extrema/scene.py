from manim import *


class MainScene(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("Local Extrema of a Cubic Function", font_size=40, color=BLUE)
        subtitle = MathTex("f(x) = x^3 - 6x^2 + 9x", font_size=44, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(title.animate.scale(0.6).to_edge(UP), FadeOut(subtitle))
        self.wait(0.3)

        # ---------- Axes & plot ----------
        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-2, 6, 2],
            x_length=6,
            y_length=5,
            tips=True,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(LEFT, buff=0.6)
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        def f(x):
            return x**3 - 6 * x**2 + 9 * x

        graph = axes.plot(f, x_range=[-0.4, 4.2], color=GREEN, stroke_width=4)
        graph_label = MathTex("f(x)", color=GREEN, font_size=30).next_to(
            axes.c2p(0.4, f(0.4)), UL, buff=0.1
        )

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), FadeIn(graph_label))
        self.wait(0.5)

        # ---------- Steps panel (right) ----------
        def step_tex(s, **kw):
            return MathTex(s, font_size=30, **kw)

        d1 = VGroup(
            Text("1st derivative:", font_size=24, color=BLUE_B),
            step_tex("f'(x) = 3x^2 - 12x + 9"),
        ).arrange(RIGHT, buff=0.2)
        d2 = step_tex("= 3(x-1)(x-3)", color=TEAL)
        d3 = step_tex("f'(x)=0 \\Rightarrow x=1,\\; x=3", color=YELLOW)
        d4 = VGroup(
            Text("2nd derivative:", font_size=24, color=BLUE_B),
            step_tex("f''(x) = 6x - 12"),
        ).arrange(RIGHT, buff=0.2)
        e1 = step_tex("f''(1) = -6 < 0 \\;\\Rightarrow\\; \\text{max}", color=RED)
        e2 = step_tex("f''(3) = 6 > 0 \\;\\Rightarrow\\; \\text{min}", color=ORANGE)

        steps = VGroup(d1, d2, d3, d4, e1, e2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        steps.scale(0.8).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)

        self.play(Write(d1))
        self.wait(0.6)
        self.play(Write(d2))
        self.wait(0.6)
        self.play(Write(d3))
        self.wait(0.6)
        self.play(Write(d4))
        self.wait(0.6)
        self.play(Write(e1))
        self.wait(0.4)
        self.play(Write(e2))
        self.wait(0.5)

        # ---------- Mark extrema points ----------
        # local max at (1, 4)
        max_dot = Dot(axes.c2p(1, 4), color=RED, radius=0.09)
        max_lbl = MathTex("(1,4)", font_size=26, color=RED).next_to(max_dot, UP, buff=0.15)
        # local min at (3, 0)
        min_dot = Dot(axes.c2p(3, 0), color=ORANGE, radius=0.09)
        min_lbl = MathTex("(3,0)", font_size=26, color=ORANGE).next_to(
            min_dot, DOWN, buff=0.15
        )

        # horizontal tangent lines
        tan_max = Line(
            axes.c2p(0.1, 4), axes.c2p(1.9, 4), color=RED_A, stroke_width=3
        )
        tan_min = Line(
            axes.c2p(2.1, 0), axes.c2p(3.9, 0), color=ORANGE, stroke_width=3
        )

        self.play(GrowFromCenter(max_dot), Create(tan_max), FadeIn(max_lbl))
        self.wait(0.4)
        self.play(GrowFromCenter(min_dot), Create(tan_min), FadeIn(min_lbl))
        self.wait(0.5)

        self.play(Indicate(max_dot, color=RED), Indicate(min_dot, color=ORANGE))
        self.wait(2)