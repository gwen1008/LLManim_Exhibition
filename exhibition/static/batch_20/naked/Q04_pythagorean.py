from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Text("畢氏定理：a² + b² = c²", font_size=36).to_edge(UP)
        self.play(Write(title))

        a, b = 3, 4
        c = 5
        scale = 0.6

        # Triangle vertices (right angle at origin)
        A = np.array([0, 0, 0])
        B = np.array([a * scale, 0, 0])
        C = np.array([0, b * scale, 0])

        offset = LEFT * 1.5 + DOWN * 0.5
        A += offset
        B += offset
        C += offset

        triangle = Polygon(A, B, C, color=WHITE, fill_opacity=0.3, fill_color=GREY)

        # Right angle marker
        ra_size = 0.2
        ra = Polygon(
            A,
            A + RIGHT * ra_size,
            A + RIGHT * ra_size + UP * ra_size,
            A + UP * ra_size,
            color=YELLOW,
        )

        label_a = MathTex("a", color=BLUE).next_to(Line(A, B), DOWN, buff=0.1)
        label_b = MathTex("b", color=GREEN).next_to(Line(A, C), LEFT, buff=0.1)
        label_c = MathTex("c", color=RED).next_to(Line(B, C).get_center(), UR, buff=0.1)

        self.play(Create(triangle), Create(ra))
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait(0.5)

        # Square on side a (below AB)
        sq_a = Polygon(
            A, B, B + DOWN * a * scale, A + DOWN * a * scale,
            color=BLUE, fill_opacity=0.5, fill_color=BLUE,
        )
        # Square on side b (left of AC)
        sq_b = Polygon(
            A, C, C + LEFT * b * scale, A + LEFT * b * scale,
            color=GREEN, fill_opacity=0.5, fill_color=GREEN,
        )
        # Square on hypotenuse (outside the triangle)
        # BC direction
        BC = C - B
        # Outward normal (rotate BC by -90deg)
        normal = np.array([BC[1], -BC[0], 0])
        normal = normal / np.linalg.norm(normal) * c * scale
        sq_c = Polygon(
            B, C, C + normal, B + normal,
            color=RED, fill_opacity=0.5, fill_color=RED,
        )

        self.play(FadeIn(sq_a, shift=DOWN * 0.3))
        area_a = MathTex("a^2", color=WHITE).move_to(sq_a.get_center())
        self.play(Write(area_a))

        self.play(FadeIn(sq_b, shift=LEFT * 0.3))
        area_b = MathTex("b^2", color=WHITE).move_to(sq_b.get_center())
        self.play(Write(area_b))

        self.play(FadeIn(sq_c, shift=normal * 0.1))
        area_c = MathTex("c^2", color=WHITE).move_to(sq_c.get_center())
        self.play(Write(area_c))
        self.wait(0.5)

        # Equation on right
        eq = MathTex(
            "a^2", "+", "b^2", "=", "c^2",
            font_size=56,
        ).to_edge(RIGHT, buff=1).shift(UP * 0.5)
        eq[0].set_color(BLUE)
        eq[2].set_color(GREEN)
        eq[4].set_color(RED)

        self.play(
            TransformFromCopy(area_a, eq[0]),
            TransformFromCopy(area_b, eq[2]),
            TransformFromCopy(area_c, eq[4]),
            Write(eq[1]),
            Write(eq[3]),
        )

        # Numeric verification
        nums = MathTex(
            "3^2", "+", "4^2", "=", "5^2",
            font_size=44,
        ).next_to(eq, DOWN, buff=0.5)
        nums[0].set_color(BLUE)
        nums[2].set_color(GREEN)
        nums[4].set_color(RED)
        result = MathTex("9 + 16 = 25", font_size=40, color=YELLOW).next_to(nums, DOWN, buff=0.4)

        self.play(Write(nums))
        self.play(Write(result))
        self.wait(2)