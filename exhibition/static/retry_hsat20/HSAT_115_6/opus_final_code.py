from manim import *


class GeneratedScene(Scene):
    def construct(self):
        # Coordinate system
        plane = NumberPlane(
            x_range=[-9, 7, 1],
            y_range=[-8, 4, 1],
            x_length=11,
            y_length=8,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
        ).add_coordinates()
        plane.scale(0.85).to_edge(LEFT, buff=0.3)

        def P(x, y):
            return plane.c2p(x, y)

        title = Text("y = -6 上使 △ABC 為等腰三角形的點 C", font_size=26)
        title.to_edge(UP, buff=0.2)
        self.play(Create(plane), Write(title))
        self.wait(0.3)

        # Points A, B
        A = Dot(P(2, -2), color=YELLOW)
        B = Dot(P(-1, 2), color=GREEN)
        A_lab = MathTex("A(2,-2)", font_size=28, color=YELLOW).next_to(A, RIGHT, buff=0.1)
        B_lab = MathTex("B(-1,2)", font_size=28, color=GREEN).next_to(B, LEFT, buff=0.1)
        self.play(FadeIn(A, B), Write(A_lab), Write(B_lab))

        AB = Line(P(2, -2), P(-1, 2), color=WHITE)
        AB_len = MathTex(r"AB=5", font_size=28).next_to(AB.get_center(), UR, buff=0.15)
        self.play(Create(AB), Write(AB_len))
        self.wait(0.5)

        # Line y = -6
        line = DashedLine(P(-9, -6), P(7, -6), color=BLUE_B)
        line_lab = MathTex("y=-6", font_size=28, color=BLUE_B).next_to(P(7, -6), UP, buff=0.1)
        self.play(Create(line), Write(line_lab))
        self.wait(0.5)

        # Case 1: CA = CB (perpendicular bisector)
        case1 = VGroup(
            VGroup(
                Text("(1) ", font_size=24),
                MathTex(r"CA=CB", font_size=24),
            ).arrange(RIGHT, buff=0.1),
            Text("C 在 AB 中垂線", font_size=22),
            MathTex(r"\Rightarrow x=-7.5", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        case1.to_edge(RIGHT, buff=0.3).shift(UP * 2.2)
        self.play(Write(case1))

        C1 = Dot(P(-7.5, -6), color=RED)
        # perpendicular bisector through (0.5,0) slope 3/4
        bis = Line(P(-8, 0.75 * (-8 - 0.5)), P(4, 0.75 * (4 - 0.5)), color=RED, stroke_opacity=0.6)
        self.play(Create(bis))
        self.play(
            FadeIn(C1, scale=1.5),
            Create(Line(P(-7.5, -6), P(2, -2), color=RED, stroke_width=2)),
            Create(Line(P(-7.5, -6), P(-1, 2), color=RED, stroke_width=2)),
        )
        self.wait(0.6)
        self.play(FadeOut(bis))

        # Case 2: AB = AC
        case2 = VGroup(
            VGroup(
                Text("(2) ", font_size=24),
                MathTex(r"AB=AC=5", font_size=24),
            ).arrange(RIGHT, buff=0.1),
            MathTex(r"(x-2)^2+16=25", font_size=22),
            MathTex(r"\Rightarrow x=5,\ -1", font_size=22, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        case2.next_to(case1, DOWN, buff=0.4).to_edge(RIGHT, buff=0.3)
        self.play(Write(case2))

        circleA = Circle(color=ORANGE, stroke_opacity=0.5).move_to(P(2, -2))
        circleA.width = Line(P(2, -2), P(7, -2)).get_length() * 2
        self.play(Create(circleA))

        C2a = Dot(P(5, -6), color=ORANGE)
        C2b = Dot(P(-1, -6), color=ORANGE)
        self.play(
            FadeIn(C2a, C2b, scale=1.5),
            Create(Line(P(2, -2), P(5, -6), color=ORANGE, stroke_width=2)),
            Create(Line(P(2, -2), P(-1, -6), color=ORANGE, stroke_width=2)),
        )
        self.wait(0.6)
        self.play(FadeOut(circleA))

        # Case 3: AB = BC (no solution)
        case3 = VGroup(
            VGroup(
                Text("(3) ", font_size=24),
                MathTex(r"AB=BC=5", font_size=24),
            ).arrange(RIGHT, buff=0.1),
            MathTex(r"(x+1)^2+64=25", font_size=22),
            VGroup(
                MathTex(r"\Rightarrow", font_size=22, color=GREY),
                Text("無解", font_size=22, color=GREY),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        case3.next_to(case2, DOWN, buff=0.4).to_edge(RIGHT, buff=0.3)
        self.play(Write(case3))
        self.wait(0.6)

        # Conclusion
        conclusion = Text("共 3 個點", font_size=34, color=YELLOW)
        conclusion.next_to(case3, DOWN, buff=0.4).to_edge(RIGHT, buff=0.3)
        box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.15)
        self.play(Write(conclusion), Create(box))
        self.play(
            Indicate(C1, color=RED),
            Indicate(C2a, color=ORANGE),
            Indicate(C2b, color=ORANGE),
        )
        self.wait(2)