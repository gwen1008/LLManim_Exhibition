from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\int_0^{\pi} \sin(x)\,dx", font_size=48).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, np.pi + 0.3, np.pi / 4],
            y_range=[0, 1.3, 0.5],
            x_length=9,
            y_length=4,
            axis_config={"include_tip": True, "include_numbers": False},
        ).to_edge(DOWN, buff=0.8)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        pi_label = MathTex(r"\pi").next_to(axes.c2p(np.pi, 0), DOWN)
        zero_label = MathTex("0").next_to(axes.c2p(0, 0), DOWN)

        curve = axes.plot(lambda x: np.sin(x), x_range=[0, np.pi], color=YELLOW)
        curve_label = MathTex(r"y=\sin(x)", color=YELLOW, font_size=32).next_to(
            axes.c2p(np.pi / 2, 1), UP
        )

        self.play(Create(axes), Write(x_label), Write(y_label), Write(zero_label), Write(pi_label))
        self.play(Create(curve), Write(curve_label))
        self.wait(0.5)

        approx_text = MathTex(r"S_n = \sum_{i=1}^{n} \sin(x_i)\,\Delta x", font_size=36).to_corner(UL).shift(DOWN * 0.8)
        value_text = MathTex("S_n = 0.000", font_size=36).next_to(approx_text, DOWN, aligned_edge=LEFT)
        n_text = MathTex("n = 4", font_size=36).next_to(value_text, DOWN, aligned_edge=LEFT)
        self.play(Write(approx_text), Write(value_text), Write(n_text))

        def make_rects(n):
            dx = np.pi / n
            rects = VGroup()
            total = 0
            for i in range(n):
                x_left = i * dx
                x_mid = x_left + dx / 2
                h = np.sin(x_mid)
                total += h * dx
                p0 = axes.c2p(x_left, 0)
                p1 = axes.c2p(x_left + dx, h)
                rect = Rectangle(
                    width=p1[0] - p0[0],
                    height=p1[1] - p0[1],
                    stroke_color=BLUE,
                    stroke_width=2,
                    fill_color=BLUE,
                    fill_opacity=0.5,
                )
                rect.move_to((p0 + p1) / 2)
                rects.add(rect)
            return rects, total

        rects, total = make_rects(4)
        new_val = MathTex(f"S_n = {total:.4f}", font_size=36).move_to(value_text)
        self.play(Create(rects), Transform(value_text, new_val))
        self.wait(1)

        for n in [8, 16, 32, 64]:
            new_rects, total = make_rects(n)
            new_val = MathTex(f"S_n = {total:.4f}", font_size=36).move_to(value_text)
            new_n = MathTex(f"n = {n}", font_size=36).move_to(n_text)
            self.play(
                Transform(rects, new_rects),
                Transform(value_text, new_val),
                Transform(n_text, new_n),
                run_time=1.2,
            )
            self.wait(0.4)

        result = MathTex(r"\int_0^{\pi} \sin(x)\,dx = 2", font_size=44, color=GREEN).next_to(
            n_text, DOWN, aligned_edge=LEFT, buff=0.4
        )
        self.play(Write(result))
        self.wait(2)