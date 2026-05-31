from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        title = Tex("Newton's Method: $x^2 - 2 = 0$").to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-0.5, 3.5, 1],
            y_range=[-3, 8, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.3)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        f = lambda x: x**2 - 2
        graph = axes.plot(f, x_range=[-0.4, 3.2], color=BLUE)
        graph_label = MathTex("f(x)=x^2-2").scale(0.7).next_to(graph, UR, buff=-0.5).shift(LEFT*0.5)

        root_val = np.sqrt(2)
        root_dot = Dot(axes.c2p(root_val, 0), color=YELLOW)
        root_label = MathTex("\\sqrt{2}").scale(0.6).next_to(root_dot, DOWN, buff=0.15).set_color(YELLOW)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), Write(graph_label))
        self.play(FadeIn(root_dot, scale=0.5), Write(root_label))

        info_box = VGroup()
        info_title = MathTex("x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}").scale(0.65)
        info_title2 = MathTex("= \\tfrac{1}{2}\\left(x_n + \\tfrac{2}{x_n}\\right)").scale(0.65)
        info_box = VGroup(info_title, info_title2).arrange(DOWN, buff=0.15)
        info_box.to_corner(UL).shift(DOWN*0.6 + RIGHT*0.1)
        self.play(Write(info_box))

        x = 3.0
        colors = [RED, ORANGE, GREEN, PURPLE, TEAL]
        iter_text = VGroup().to_corner(UR).shift(DOWN*0.8 + LEFT*0.2)

        prev_tangent = None
        prev_vline = None
        prev_pt_curve = None
        prev_pt_axis = None

        for n in range(5):
            fx = f(x)
            slope = 2 * x
            x_new = x - fx / slope

            col = colors[n]
            pt_curve = Dot(axes.c2p(x, fx), color=col, radius=0.06)
            pt_axis = Dot(axes.c2p(x, 0), color=col, radius=0.06)
            vline = DashedLine(axes.c2p(x, 0), axes.c2p(x, fx), color=col, stroke_width=2)

            # tangent line
            x_left = max(-0.3, x - 2.5)
            x_right = min(3.3, x + 2.5)
            tangent = axes.plot(
                lambda t, x0=x, fx0=fx, m=slope: m * (t - x0) + fx0,
                x_range=[x_left, x_right],
                color=col,
                stroke_width=3,
            )

            x_label_tex = MathTex(f"x_{n}").scale(0.55).set_color(col).next_to(pt_axis, UP*0.5 if n%2==0 else DOWN, buff=0.1)

            line = MathTex(f"x_{n}={x:.4f} \\to x_{n+1}={x_new:.4f}").scale(0.4).set_color(col)
            iter_text.add(line)
            iter_text.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR).shift(DOWN*0.8 + LEFT*0.1)

            anims = [Create(vline), FadeIn(pt_curve), FadeIn(pt_axis), Write(x_label_tex)]
            if prev_tangent is not None:
                anims += [FadeOut(prev_tangent, run_time=0.5)]
            self.play(*anims, run_time=0.8)
            self.play(Create(tangent), run_time=0.9)
            self.play(Write(line), run_time=0.5)

            # show new x intercept
            new_axis_dot = Dot(axes.c2p(x_new, 0), color=col, radius=0.05)
            self.play(FadeIn(new_axis_dot, scale=2), run_time=0.4)

            prev_tangent = tangent
            x = x_new

        conclusion = MathTex(f"x_5 \\approx {x:.6f}", "\\;\\;\\sqrt{2}\\approx 1.414214").scale(0.55)
        conclusion.to_edge(DOWN).set_color(YELLOW)
        self.play(Write(conclusion))
        self.wait(2)