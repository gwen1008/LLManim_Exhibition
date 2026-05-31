from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
        ).add_coordinates()
        self.play(Create(plane))

        circle = Circle(radius=plane.x_length / 4, color=YELLOW).move_to(plane.get_origin())
        self.play(Create(circle))

        title = MathTex("z^8 = 1").to_corner(UL)
        self.play(Write(title))

        origin = plane.get_origin()
        roots = []
        vectors = []
        dots = []
        labels = []

        for k in range(8):
            theta = 2 * np.pi * k / 8
            point = plane.n2p(np.cos(theta) + 1j * np.sin(theta))
            arrow = Arrow(origin, point, buff=0, color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.15)
            dot = Dot(point, color=RED)
            label = MathTex(f"\\omega_{k}").scale(0.6).next_to(point, point - origin, buff=0.15)
            roots.append(point)
            vectors.append(arrow)
            dots.append(dot)
            labels.append(label)

        for arrow, dot, label in zip(vectors, dots, labels):
            self.play(GrowArrow(arrow), FadeIn(dot), Write(label), run_time=0.5)

        formula = MathTex(r"\omega_k = e^{2\pi i k/8}").to_corner(UR)
        self.play(Write(formula))
        self.wait(2)