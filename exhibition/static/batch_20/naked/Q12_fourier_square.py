from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        title = Text("Fourier 級數逼近方波", font_size=36).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-PI, PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4.5,
            axis_config={"include_tip": False, "stroke_width": 2},
        ).shift(DOWN*0.3)
        self.play(Create(axes))

        def square(x):
            x_mod = ((x + PI) % (2*PI)) - PI
            return 1 if x_mod > 0 else -1

        sq_graph = axes.plot(square, x_range=[-PI, PI, 0.001], color=YELLOW, use_smoothing=False, discontinuities=[-PI, 0, PI])
        sq_label = Text("目標方波", font_size=22, color=YELLOW).to_corner(UR).shift(DOWN*0.8)
        self.play(Create(sq_graph), FadeIn(sq_label))
        self.wait(0.5)

        def partial(N):
            def f(x):
                s = 0
                for k in range(1, N+1, 2):
                    s += np.sin(k*x)/k
                return (4/PI)*s
            return f

        formula = MathTex(r"f(x)=\frac{4}{\pi}\sum_{k\,odd}\frac{\sin(kx)}{k}", font_size=32).to_corner(UL).shift(DOWN*0.6)
        self.play(Write(formula))

        colors = [BLUE, GREEN, RED, PURPLE, ORANGE]
        n_values = [1, 3, 5, 11, 25]
        current = axes.plot(partial(1), x_range=[-PI, PI], color=colors[0])
        label = MathTex(r"N=1", font_size=30, color=colors[0]).next_to(formula, DOWN, buff=0.4)
        self.play(Create(current), Write(label))
        self.wait(1)

        for i, N in enumerate(n_values[1:], 1):
            new_graph = axes.plot(partial(N), x_range=[-PI, PI], color=colors[i])
            new_label = MathTex(f"N={N}", font_size=30, color=colors[i]).next_to(formula, DOWN, buff=0.4)
            self.play(Transform(current, new_graph), Transform(label, new_label), run_time=1.5)
            self.wait(0.8)

        conclusion = Text("項數越多 → 越接近方波", font_size=28, color=WHITE).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)