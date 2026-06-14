from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\text{直線 } 2x+y=10 \text{ 被兩平行線所截的線段 } S").scale(0.7)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        plane = NumberPlane(
            x_range=[-2, 8, 1],
            y_range=[-2, 10, 2],
            x_length=7,
            y_length=6.5,
            background_line_style={"stroke_opacity": 0.3},
        ).to_edge(DOWN, buff=0.3).shift(LEFT * 2.5)
        self.play(Create(plane), run_time=1.5)

        def to_pt(x, y):
            return plane.c2c(x, y) if hasattr(plane, "c2c") else plane.coords_to_point(x, y)

        c2p = plane.coords_to_point

        # 主直線 2x+y=10  => y = 10 - 2x
        main_line = plane.plot(lambda x: 10 - 2 * x, x_range=[1, 5], color=YELLOW)
        main_lbl = MathTex(r"2x+y=10", color=YELLOW).scale(0.55)
        main_lbl.next_to(c2p(1, 8), UP)

        # 平行線 x-2y+15=0 => y=(x+15)/2 ;  x-2y=0 => y=x/2
        par1 = plane.plot(lambda x: (x + 15) / 2, x_range=[-2, 5], color=BLUE)
        par2 = plane.plot(lambda x: x / 2, x_range=[-2, 8], color=GREEN)
        par1_lbl = MathTex(r"x-2y+15=0", color=BLUE).scale(0.5).next_to(c2p(-2, 6.5), RIGHT)
        par2_lbl = MathTex(r"x-2y=0", color=GREEN).scale(0.5).next_to(c2p(6, 3), RIGHT)

        self.play(Create(main_line), Write(main_lbl))
        self.play(Create(par1), Write(par1_lbl))
        self.play(Create(par2), Write(par2_lbl))
        self.wait(0.5)

        # 端點 A=(1,8), B=(4,2)
        A = c2p(1, 8)
        B = c2p(4, 2)
        dotA = Dot(A, color=RED)
        dotB = Dot(B, color=RED)
        lblA = MathTex("A(1,8)").scale(0.5).next_to(dotA, LEFT)
        lblB = MathTex("B(4,2)").scale(0.5).next_to(dotB, RIGHT)
        seg = Line(A, B, color=ORANGE, stroke_width=8)

        self.play(FadeIn(dotA, dotB), Write(lblA), Write(lblB))
        self.play(Create(seg))
        seg_lbl = MathTex(r"S", color=ORANGE).scale(0.7).next_to(seg.get_center(), UR)
        self.play(Write(seg_lbl))
        self.wait(0.5)

        # 右側說明
        info = VGroup(
            MathTex(r"3x-y=c"),
            MathTex(r"A:\;3(1)-8=-5"),
            MathTex(r"B:\;3(4)-2=10"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.6)
        info.to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        self.play(Write(info[0]))

        # 動態直線 3x-y=c => y = 3x - c
        c_tracker = ValueTracker(10)

        moving = always_redraw(
            lambda: plane.plot(
                lambda x: 3 * x - c_tracker.get_value(),
                x_range=[0, 6],
                color=PURPLE,
            )
        )
        c_disp = always_redraw(
            lambda: MathTex(f"c={c_tracker.get_value():.1f}", color=PURPLE)
            .scale(0.7)
            .to_edge(RIGHT, buff=0.4)
            .shift(DOWN * 1.5)
        )
        self.play(Create(moving), Write(c_disp))
        self.wait(0.3)

        # 掃過 B 端 (c=10)
        self.play(Write(info[2]))
        self.wait(0.3)

        # 移動到 A 端 (c=-5) 取得最小值
        self.play(c_tracker.animate.set_value(-5), run_time=3)
        self.play(Write(info[1]))
        self.wait(0.5)

        result = MathTex(r"c_{\min}=-5", color=RED).scale(0.9)
        result.to_edge(RIGHT, buff=0.4).shift(DOWN * 3)
        box = SurroundingRectangle(result, color=RED)
        self.play(Indicate(dotA), Write(result), Create(box))
        self.wait(2)