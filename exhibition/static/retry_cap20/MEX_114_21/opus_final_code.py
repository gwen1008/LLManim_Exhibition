from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("二次函數平移與 y 軸交點", font_size=34).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-12, 6, 2],
            y_range=[-40, 16, 8],
            x_length=9,
            y_length=5.5,
            axis_config={"include_numbers": False, "font_size": 18},
            tips=False,
        ).shift(DOWN * 0.4)
        self.play(Create(axes))

        t = ValueTracker(0.0)

        def parabola(tv):
            return axes.plot(
                lambda x: -((x + 7 - tv) ** 2) + 12,
                x_range=[-12 + tv, 4, 0.05],
                color=BLUE,
            )

        graph = always_redraw(lambda: parabola(t.get_value()))

        # P 點：x=0 時的交點
        def p_dot():
            tv = t.get_value()
            y = -((7 - tv) ** 2) + 12
            return Dot(axes.c2p(0, y), color=YELLOW, radius=0.08)

        dot = always_redraw(p_dot)

        def p_label():
            tv = t.get_value()
            y = -((7 - tv) ** 2) + 12
            return MathTex("P", color=YELLOW, font_size=30).next_to(
                axes.c2p(0, y), RIGHT, buff=0.15
            )

        label = always_redraw(p_label)

        eq = always_redraw(
            lambda: MathTex(
                "y=-(x+7-t)^2+12", font_size=30, color=BLUE
            ).to_corner(UL).shift(DOWN * 0.8)
        )

        def info():
            tv = t.get_value()
            y = -((7 - tv) ** 2) + 12
            return VGroup(
                MathTex(f"t={tv:.1f}", font_size=28),
                MathTex(f"P_y={y:.1f}", font_size=28, color=YELLOW),
            ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 0.8)

        info_box = always_redraw(info)

        self.play(Create(graph), FadeIn(dot), FadeIn(label))
        self.play(FadeIn(eq), FadeIn(info_box))

        # 留下 P 的軌跡
        trace = TracedPath(dot.get_center, stroke_color=RED, stroke_width=4)
        self.add(trace)

        self.wait(0.5)
        # 平移 0 -> 10
        self.play(t.animate.set_value(10.0), run_time=8, rate_func=linear)
        self.wait(1)

        note1 = Text("P 由 -37 上升到 12 (t=7)", font_size=26, color=GREEN)
        note2 = Text("再下降到 3 (t=10)", font_size=26, color=ORANGE)
        notes = VGroup(note1, note2).arrange(DOWN).to_edge(DOWN)
        self.play(Write(notes))
        self.wait(1)

        ans = Text("答案：(D) 先向上再向下", font_size=32, color=YELLOW)
        ans.next_to(notes, UP, buff=0.2)
        self.play(FadeOut(notes), Write(ans))
        self.wait(2)