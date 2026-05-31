from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Text("直線與圓的交點", font="PingFang SC").to_edge(UP)
        self.play(Write(title))

        # Axes and plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_opacity": 0.3},
        ).to_edge(LEFT, buff=0.5)

        circle = Circle(radius=2, color=BLUE).move_to(plane.c2p(0, 0))
        circle.set_stroke(width=3)
        # scale radius to plane units
        circle = Circle().set_stroke(BLUE, width=3)
        circle.width = plane.c2p(2, 0)[0] - plane.c2p(0, 0)[0]
        circle.height = circle.width
        circle.move_to(plane.c2p(0, 0))

        line = plane.plot(lambda x: x + 1, x_range=[-3, 2.5], color=YELLOW)

        circle_lbl = MathTex("x^2+y^2=4", color=BLUE).scale(0.7)
        line_lbl = MathTex("y=x+1", color=YELLOW).scale(0.7)

        self.play(Create(plane))
        self.play(Create(circle), Write(circle_lbl.next_to(plane, UP, buff=0.1).shift(LEFT*1.5)))
        self.play(Create(line), Write(line_lbl.next_to(plane, UP, buff=0.1).shift(RIGHT*1.5)))
        self.wait(0.5)

        # Right side derivation
        steps = VGroup(
            MathTex(r"x^2+(x+1)^2=4"),
            MathTex(r"2x^2+2x-3=0"),
            MathTex(r"\Delta=2^2-4(2)(-3)=28>0"),
            MathTex(r"x=\frac{-1\pm\sqrt{7}}{2}"),
        ).scale(0.7).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        steps.to_edge(RIGHT, buff=0.5)

        two_pts = Text("兩個交點", font="PingFang SC", color=GREEN).scale(0.5)
        two_pts.next_to(steps[2], RIGHT, buff=0.3)

        for s in steps:
            self.play(Write(s), run_time=0.9)
            if s is steps[2]:
                self.play(FadeIn(two_pts, shift=RIGHT*0.2))
        self.wait(0.5)

        # Intersection points
        s7 = np.sqrt(7)
        x1 = (-1 + s7) / 2
        x2 = (-1 - s7) / 2
        y1 = x1 + 1
        y2 = x2 + 1

        d1 = Dot(plane.c2p(x1, y1), color=RED, radius=0.08)
        d2 = Dot(plane.c2p(x2, y2), color=RED, radius=0.08)

        c1 = MathTex(r"\left(\tfrac{-1+\sqrt{7}}{2},\ \tfrac{1+\sqrt{7}}{2}\right)").scale(0.45)
        c2 = MathTex(r"\left(\tfrac{-1-\sqrt{7}}{2},\ \tfrac{1-\sqrt{7}}{2}\right)").scale(0.45)
        c1.next_to(d1, UR, buff=0.05)
        c2.next_to(d2, DL, buff=0.05)

        self.play(FlashAround(steps[3]), GrowFromCenter(d1), GrowFromCenter(d2))
        self.play(FadeIn(c1), FadeIn(c2))
        self.wait(2)