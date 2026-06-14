from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Text("二次函數平移與 x 軸交點", font_size=36).to_edge(UP)
        self.play(Write(title))

        func_tex = MathTex("y = -(x+6)^2 + 5", font_size=40).next_to(title, DOWN)
        self.play(Write(func_tex))
        self.wait(0.5)

        # Axes (shifted region around x=-6)
        axes = Axes(
            x_range=[-12, 0, 2],
            y_range=[-4, 10, 2],
            x_length=8,
            y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 18},
        ).shift(DOWN * 0.4)

        self.play(Create(axes))

        # Original parabola
        def f(x):
            return -(x + 6) ** 2 + 5

        graph1 = axes.plot(f, x_range=[-12, 0], color=BLUE)
        g1_label = MathTex("y=-(x+6)^2+5", font_size=26, color=BLUE)
        g1_label.next_to(axes.c2p(-6, 5), UP)
        self.play(Create(graph1), FadeIn(g1_label))
        self.wait(0.3)

        # roots a, b
        a, b = -6 - np.sqrt(5), -6 + np.sqrt(5)
        dot_a = Dot(axes.c2p(a, 0), color=YELLOW)
        dot_b = Dot(axes.c2p(b, 0), color=YELLOW)
        lab_a = MathTex("(a,0)", font_size=24, color=YELLOW).next_to(dot_a, DOWN)
        lab_b = MathTex("(b,0)", font_size=24, color=YELLOW).next_to(dot_b, DOWN)
        self.play(FadeIn(dot_a, dot_b), Write(lab_a), Write(lab_b))
        self.wait(0.5)

        # axis of symmetry
        sym_line = DashedLine(
            axes.c2p(-6, -4), axes.c2p(-6, 9), color=GREY
        )
        sym_label = MathTex("x=-6", font_size=24, color=GREY).next_to(
            axes.c2p(-6, -4), DOWN
        )
        self.play(Create(sym_line), Write(sym_label))
        self.wait(0.3)

        note1 = MathTex("a+b = -12", font_size=30, color=YELLOW).to_corner(UR)
        self.play(Write(note1))
        self.wait(0.5)

        # Shift up
        shift_note = Text("往上平移", font_size=28, color=GREEN).next_to(
            note1, DOWN, aligned_edge=RIGHT
        )
        self.play(Write(shift_note))

        def f2(x):
            return -(x + 6) ** 2 + 9

        graph2 = axes.plot(f2, x_range=[-12, 0], color=GREEN)
        g2_label = MathTex("y=-(x+6)^2+9", font_size=26, color=GREEN).next_to(
            axes.c2p(-6, 9), UP
        )
        self.play(
            TransformFromCopy(graph1, graph2),
            FadeIn(g2_label),
            FadeOut(g1_label),
        )
        self.wait(0.3)

        # new roots c, d
        c, d = -9, -3
        dot_c = Dot(axes.c2p(c, 0), color=RED)
        dot_d = Dot(axes.c2p(d, 0), color=RED)
        lab_c = MathTex("(c,0)", font_size=24, color=RED).next_to(dot_c, UP * 0.5 + LEFT * 0.3)
        lab_d = MathTex("(d,0)", font_size=24, color=RED).next_to(dot_d, UP * 0.5 + RIGHT * 0.3)
        self.play(FadeIn(dot_c, dot_d), Write(lab_c), Write(lab_d))
        self.wait(0.5)

        note2 = MathTex("c+d = -12", font_size=30, color=RED).next_to(
            shift_note, DOWN, aligned_edge=RIGHT
        )
        self.play(Write(note2))
        self.wait(0.5)

        # width comparison brackets
        br1 = BraceBetweenPoints(
            axes.c2p(a, 0), axes.c2p(b, 0), direction=DOWN, color=YELLOW
        )
        br1_txt = MathTex("b-a=2\\sqrt5", font_size=24, color=YELLOW).next_to(br1, DOWN)
        self.play(GrowFromCenter(br1), Write(br1_txt))
        self.wait(0.3)

        br2 = BraceBetweenPoints(
            axes.c2p(c, 0), axes.c2p(d, 0), direction=UP, color=RED
        )
        br2_txt = MathTex("d-c=6", font_size=24, color=RED).next_to(br2, UP)
        self.play(GrowFromCenter(br2), Write(br2_txt))
        self.wait(0.5)

        # Conclusion
        conclusion = VGroup(
            MathTex("a+b = c+d", font_size=32, color=WHITE),
            MathTex("b-a < d-c", font_size=32, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT)
        box = SurroundingRectangle(conclusion, color=GOLD, buff=0.2)
        ans = VGroup(conclusion, box).to_edge(DOWN).shift(RIGHT * 3.5)

        self.play(Write(conclusion), Create(box))
        self.wait(0.3)

        final = Text("答案：(A)", font_size=32, color=GOLD).next_to(box, UP)
        self.play(Write(final))
        self.wait(2)