from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = MathTex(r"\int_0^{\pi} \sin(x)\, dx").to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, PI + 0.3, PI / 4],
            y_range=[0, 1.3, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        curve = axes.plot(lambda x: np.sin(x), x_range=[0, PI], color=YELLOW)
        curve_label = MathTex(r"y=\sin(x)", color=YELLOW).scale(0.7).next_to(curve, UP, buff=0.1)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(curve), Write(curve_label))
        self.wait(0.5)

        approx_text = MathTex(r"S_n = \sum_{i=1}^{n} \sin(x_i)\,\Delta x").scale(0.7).to_edge(LEFT).shift(UP * 2)
        n_tracker = MathTex("n = 4").scale(0.8).next_to(approx_text, DOWN, aligned_edge=LEFT)
        val_tracker = MathTex("S_n \\approx 0.000").scale(0.8).next_to(n_tracker, DOWN, aligned_edge=LEFT)
        self.play(Write(approx_text), Write(n_tracker), Write(val_tracker))

        def make_rects(n):
            dx = PI / n
            rects = VGroup()
            total = 0
            for i in range(n):
                x_left = i * dx
                x_mid = x_left + dx / 2
                h = np.sin(x_mid)
                total += h * dx
                p1 = axes.c2p(x_left, 0)
                p2 = axes.c2p(x_left + dx, h)
                rect = Rectangle(
                    width=p2[0] - p1[0],
                    height=p2[1] - p1[1],
                    stroke_color=BLUE,
                    stroke_width=1,
                    fill_color=BLUE,
                    fill_opacity=0.5,
                ).move_to((p1 + p2) / 2)
                rects.add(rect)
            return rects, total

        rects, total = make_rects(4)
        new_val = MathTex(f"S_n \\approx {total:.3f}").scale(0.8).move_to(val_tracker, aligned_edge=LEFT)
        self.play(Create(rects), Transform(val_tracker, new_val))
        self.wait(1)

        for n in [8, 16, 32, 64]:
            new_rects, total = make_rects(n)
            new_n = MathTex(f"n = {n}").scale(0.8).move_to(n_tracker, aligned_edge=LEFT)
            new_val = MathTex(f"S_n \\approx {total:.3f}").scale(0.8).move_to(val_tracker, aligned_edge=LEFT)
            self.play(
                Transform(rects, new_rects),
                Transform(n_tracker, new_n),
                Transform(val_tracker, new_val),
                run_time=1.2,
            )
            self.wait(0.4)

        result = MathTex(r"\int_0^{\pi} \sin(x)\, dx = [-\cos(x)]_0^{\pi} = 2", color=GREEN).scale(0.9).to_edge(DOWN)
        self.play(Write(result))
        self.wait(2)