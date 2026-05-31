from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        matrix = [[3, 1], [0, 2]]
        np_matrix = np.array(matrix)

        title = MathTex(r"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}").to_corner(UL)
        self.add(title)

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane))

        # Unit vectors i, j
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED, stroke_width=6)
        i_label = MathTex(r"\hat{i}", color=GREEN).next_to(i_hat.get_end(), DOWN)
        j_label = MathTex(r"\hat{j}", color=RED).next_to(j_hat.get_end(), LEFT)

        self.play(GrowArrow(i_hat), GrowArrow(j_hat), Write(i_label), Write(j_label))
        self.wait(0.5)

        # Eigenvectors: λ=3 → (1,0); λ=2 → (1,-1) normalized direction (1,-1)
        # For A=[[3,1],[0,2]]: eigenvalues 3,2. v1=(1,0), v2=(-1,1) since (A-2I)v=0 → [[1,1],[0,0]] → v=(1,-1) or (-1,1)
        ev1_vec = np.array([1, 0, 0]) * 2
        ev2_vec = np.array([1, -1, 0]) * 1.5

        ev1 = Arrow(ORIGIN, ev1_vec, buff=0, color=YELLOW, stroke_width=5)
        ev2 = Arrow(ORIGIN, ev2_vec, buff=0, color=YELLOW, stroke_width=5)
        ev1_line = Line(-ev1_vec * 2, ev1_vec * 2, color=YELLOW, stroke_opacity=0.4)
        ev2_line = Line(-ev2_vec * 2, ev2_vec * 2, color=YELLOW, stroke_opacity=0.4)

        ev_label1 = MathTex(r"\lambda_1 = 3", color=YELLOW).scale(0.7).next_to(ev1.get_end(), UP)
        ev_label2 = MathTex(r"\lambda_2 = 2", color=YELLOW).scale(0.7).next_to(ev2.get_end(), DR)

        self.play(Create(ev1_line), Create(ev2_line))
        self.play(GrowArrow(ev1), GrowArrow(ev2), Write(ev_label1), Write(ev_label2))
        self.wait(1)

        info = Text("Eigenvectors: directions that only scale", font_size=24).to_edge(DOWN)
        self.play(Write(info))
        self.wait(1)

        # Apply transformation
        self.play(FadeOut(i_label), FadeOut(j_label), FadeOut(ev_label1), FadeOut(ev_label2))

        matrix_anim = plane.animate.apply_matrix(np_matrix)
        i_new = Arrow(ORIGIN, np_matrix @ np.array([1, 0]) @ np.eye(2), buff=0, color=GREEN, stroke_width=6)
        # Compute transformed endpoints
        def tf(v):
            r = np_matrix @ np.array([v[0], v[1]])
            return np.array([r[0], r[1], 0])

        i_target = Arrow(ORIGIN, tf([1, 0]), buff=0, color=GREEN, stroke_width=6)
        j_target = Arrow(ORIGIN, tf([0, 1]), buff=0, color=RED, stroke_width=6)
        ev1_target = Arrow(ORIGIN, tf([2, 0]), buff=0, color=YELLOW, stroke_width=5)
        ev2_target = Arrow(ORIGIN, tf([1.5, -1.5]), buff=0, color=YELLOW, stroke_width=5)
        ev1_line_target = Line(tf([-4, 0]), tf([4, 0]), color=YELLOW, stroke_opacity=0.4)
        ev2_line_target = Line(tf([-3, 3]), tf([3, -3]), color=YELLOW, stroke_opacity=0.4)

        self.play(
            matrix_anim,
            Transform(i_hat, i_target),
            Transform(j_hat, j_target),
            Transform(ev1, ev1_target),
            Transform(ev2, ev2_target),
            Transform(ev1_line, ev1_line_target),
            Transform(ev2_line, ev2_line_target),
            run_time=3,
        )
        self.wait(1)

        result = Text("Yellow vectors stayed on their lines!", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Transform(info, result))
        self.wait(2)