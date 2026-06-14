from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("線性規劃：求 c 的最小值", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Coordinate system
        ax = Axes(
            x_range=[-2, 7, 1],
            y_range=[-2, 10, 2],
            x_length=6.5,
            y_length=5.5,
            axis_config={"include_numbers": False, "include_tip": False},
        ).to_edge(DOWN, buff=0.4).shift(LEFT * 2.2)
        self.play(Create(ax))

        # Line 2x+y=10 -> y = 10 - 2x
        main_line = ax.plot(lambda x: 10 - 2 * x, x_range=[0.5, 4.5], color=YELLOW)
        main_label = MathTex("2x+y=10", font_size=28).next_to(
            ax.coords_to_point(0.7, 10 - 2 * 0.7), UR, buff=0.1
        )

        # Parallel boundary lines: x-2y+15=0 -> y=(x+15)/2 ; x-2y=0 -> y=x/2
        b1 = ax.plot(lambda x: (x + 15) / 2, x_range=[-2, 7], color=BLUE_D)
        b2 = ax.plot(lambda x: x / 2, x_range=[-2, 7], color=BLUE_D)

        self.play(Create(main_line), Write(main_label))
        self.play(Create(b1), Create(b2))
        self.wait(0.3)

        # Endpoints A=(1,8), B=(4,2)
        A = ax.coords_to_point(1, 8)
        B = ax.coords_to_point(4, 2)
        dotA = Dot(A, color=RED)
        dotB = Dot(B, color=RED)
        labA = MathTex("A(1,8)", font_size=26).next_to(dotA, UP)
        labB = MathTex("B(4,2)", font_size=26).next_to(dotB, RIGHT)

        seg = Line(A, B, color=ORANGE, stroke_width=6)
        seg_lbl = MathTex("S", font_size=30, color=ORANGE).next_to(seg.get_center(), LEFT)

        self.play(FadeIn(dotA, dotB), Write(labA), Write(labB))
        self.play(Create(seg), Write(seg_lbl))
        self.wait(0.5)

        # Side panel: objective c = 3x - y
        panel = VGroup(
            VGroup(Text("目標：", font_size=26), MathTex("c=3x-y", font_size=28)).arrange(RIGHT, buff=0.1),
            VGroup(Text("在 A：", font_size=24), MathTex("c=3(1)-8=-5", font_size=26)).arrange(RIGHT, buff=0.1),
            VGroup(Text("在 B：", font_size=24), MathTex("c=3(4)-2=10", font_size=26)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        panel.to_edge(RIGHT, buff=0.4).shift(UP * 0.5)

        self.play(Write(panel[0]))
        self.wait(0.3)

        # Show line 3x - y = c sweeping; c = 3x - y -> y = 3x - c
        c_tracker = ValueTracker(10)
        moving = always_redraw(
            lambda: ax.plot(
                lambda x: 3 * x - c_tracker.get_value(),
                x_range=[0.5, 4.5],
                color=GREEN,
            )
        )
        c_text = always_redraw(
            lambda: MathTex(
                f"c={c_tracker.get_value():.1f}", font_size=30, color=GREEN
            ).to_corner(UL).shift(DOWN * 0.8)
        )
        self.play(Create(moving), Write(c_text))
        self.wait(0.3)

        self.play(Write(panel[2]))
        self.wait(0.2)
        # Sweep to minimum at A
        self.play(c_tracker.animate.set_value(-5), run_time=3)
        self.play(Write(panel[1]))
        self.play(Indicate(dotA, color=RED, scale_factor=1.8))
        self.wait(0.4)

        result = VGroup(
            Text("c 最小值 ", font_size=32, color=RED),
            MathTex("=-5", font_size=36, color=RED),
        ).arrange(RIGHT, buff=0.15)
        result.next_to(panel, DOWN, buff=0.6)
        self.play(Write(result))
        self.wait(2)