from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\sin\theta = \frac{1}{2}").scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---------- Unit circle (left) ----------
        circle_center = LEFT * 3.5 + DOWN * 0.3
        radius = 1.8
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2 * radius * 1.5 / 1.5,
            y_length=2 * radius * 1.5 / 1.5,
            tips=False,
            axis_config={"include_numbers": False, "stroke_width": 2},
        ).move_to(circle_center)

        circle = Circle(radius=radius, color=BLUE).move_to(circle_center)
        self.play(Create(axes), Create(circle))

        # half line y=1/2
        y_half = circle_center[1] + radius * 0.5
        half_line = DashedLine(
            start=[circle_center[0] - radius, y_half, 0],
            end=[circle_center[0] + radius, y_half, 0],
            color=YELLOW,
        )
        half_label = MathTex(r"y=\tfrac{1}{2}", color=YELLOW).scale(0.5)
        half_label.next_to(half_line, RIGHT, buff=0.1)
        self.play(Create(half_line), Write(half_label))
        self.wait(0.3)

        def circ_point(deg):
            a = np.deg2rad(deg)
            return circle_center + radius * np.array([np.cos(a), np.sin(a), 0])

        # Point 30 deg
        p30 = Dot(circ_point(30), color=GREEN)
        r30 = Line(circle_center, circ_point(30), color=GREEN)
        l30 = MathTex(r"30^\circ", color=GREEN).scale(0.55).next_to(p30, UR, buff=0.05)

        # Point 150 deg
        p150 = Dot(circ_point(150), color=RED)
        r150 = Line(circle_center, circ_point(150), color=RED)
        l150 = MathTex(r"150^\circ", color=RED).scale(0.55).next_to(p150, UL, buff=0.05)

        self.play(Create(r30), FadeIn(p30), Write(l30))
        self.wait(0.2)
        self.play(Create(r150), FadeIn(p150), Write(l150))
        self.wait(0.3)

        # ---------- Sine curve (right) ----------
        sin_axes = Axes(
            x_range=[0, 360, 90],
            y_range=[-1.2, 1.2, 0.5],
            x_length=5.5,
            y_length=3.2,
            tips=False,
            axis_config={"stroke_width": 2},
            x_axis_config={"include_numbers": True, "numbers_to_include": [90, 180, 270, 360]},
        ).move_to(RIGHT * 3.3 + DOWN * 0.3)
        x_lbl = sin_axes.get_x_axis_label(MathTex(r"\theta").scale(0.7))
        y_lbl = sin_axes.get_y_axis_label(MathTex(r"\sin\theta").scale(0.6))

        sin_graph = sin_axes.plot(
            lambda x: np.sin(np.deg2rad(x)), x_range=[0, 360], color=BLUE
        )
        self.play(Create(sin_axes), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(sin_graph), run_time=1.5)

        # horizontal line y=1/2 on sine
        sin_half = DashedLine(
            start=sin_axes.c2p(0, 0.5),
            end=sin_axes.c2p(360, 0.5),
            color=YELLOW,
        )
        self.play(Create(sin_half))

        # intersection points
        sp30 = Dot(sin_axes.c2p(30, 0.5), color=GREEN)
        sp150 = Dot(sin_axes.c2p(150, 0.5), color=RED)
        self.play(FadeIn(sp30), FadeIn(sp150))

        # connect circle point to curve
        self.play(
            Indicate(p30, color=GREEN),
            Indicate(sp30, color=GREEN),
        )
        self.play(
            Indicate(p150, color=RED),
            Indicate(sp150, color=RED),
        )
        self.wait(0.3)

        # ---------- General solution ----------
        sol1 = MathTex(r"\theta = 30^\circ + 360^\circ k", color=GREEN).scale(0.7)
        sol2 = MathTex(r"\theta = 150^\circ + 360^\circ k", color=RED).scale(0.7)
        note = Tex(r"(週期性 $360^\circ$)").scale(0.55)
        group = VGroup(sol1, sol2, note).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)

        self.play(Write(sol1))
        self.play(Write(sol2))
        self.play(FadeIn(note))
        self.wait(2)