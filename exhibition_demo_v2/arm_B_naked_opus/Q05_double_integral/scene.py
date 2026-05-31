from manim import *


class MainScene(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("Double Integral over a Triangular Region", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---------- Axes and triangular region ----------
        axes = Axes(
            x_range=[0, 1.2, 0.25],
            y_range=[0, 1.2, 0.25],
            x_length=4.5,
            y_length=4.5,
            tips=True,
            axis_config={"include_numbers": False, "color": GREY_B},
        ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)

        x_lbl = axes.get_x_axis_label(MathTex("x"))
        y_lbl = axes.get_y_axis_label(MathTex("y"))

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl))

        # vertices of triangle: (0,0), (1,0), (1,1)
        p0 = axes.c2p(0, 0)
        p1 = axes.c2p(1, 0)
        p2 = axes.c2p(1, 1)
        triangle = Polygon(p0, p1, p2, color=BLUE, fill_opacity=0.5, stroke_color=BLUE_E)

        line_yx = Line(axes.c2p(0, 0), axes.c2p(1, 1), color=GREEN)
        line_lbl = MathTex("y = x", color=GREEN, font_size=30).next_to(line_yx.get_center(), UL, buff=0.1)

        self.play(GrowFromPoint(triangle, p0))
        self.play(Create(line_yx), Write(line_lbl))
        self.wait(0.5)

        # ---------- Right side: setup integral ----------
        setup = MathTex(
            r"\iint_R xy \, dA = \int_0^1 \int_0^x xy \, dy \, dx",
            font_size=40,
        )
        setup.to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
        self.play(Write(setup))
        self.wait(0.8)

        # Step 3: inner integral wrt y
        step3 = MathTex(
            r"= \int_0^1 \left[\frac{x y^2}{2}\right]_0^x dx",
            font_size=40,
        ).next_to(setup, DOWN, buff=0.5).align_to(setup, LEFT)
        self.play(Write(step3))
        self.wait(0.6)

        step3b = MathTex(
            r"= \int_0^1 \frac{x^3}{2} \, dx",
            font_size=40,
        ).next_to(step3, DOWN, buff=0.5).align_to(setup, LEFT)
        self.play(Write(step3b))
        self.wait(0.8)

        # Step 4: integrate wrt x
        step4 = MathTex(
            r"= \left[\frac{x^4}{8}\right]_0^1",
            font_size=40,
        ).next_to(step3b, DOWN, buff=0.5).align_to(setup, LEFT)
        self.play(Write(step4))
        self.wait(0.6)

        # Step 5: final answer
        answer = MathTex(
            r"= \frac{1}{8}",
            font_size=48,
            color=YELLOW,
        ).next_to(step4, DOWN, buff=0.5).align_to(setup, LEFT)
        self.play(Write(answer))

        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
        )
        final = MathTex(r"\iint_R xy \, dA = \frac{1}{8}", font_size=60, color=YELLOW)
        self.play(Write(final))
        self.wait(2)