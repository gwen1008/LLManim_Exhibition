from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        title = Text("黃金螺旋 (費氏數列)", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Fibonacci squares: (x_min, y_min, side)
        squares_data = [
            (0, 0, 1),      # S1
            (1, 0, 1),      # S2
            (0, -2, 2),     # S3
            (-3, -2, 3),    # S4
            (-3, 1, 5),     # S5
            (2, -2, 8),     # S6
        ]
        # Arc params: (center, radius, start_angle)  all angle = -PI/2
        arcs_data = [
            ((1, 0), 1, PI),
            ((1, 0), 1, PI/2),
            ((0, 0), 2, 0),
            ((0, 1), 3, -PI/2),
            ((2, 1), 5, PI),
            ((2, -2), 8, PI/2),
        ]

        scale = 0.5
        shift = np.array([-3.5, -2.0, 0]) * scale

        colors = [BLUE_C, TEAL_C, GREEN_C, YELLOW_C, ORANGE, RED_C]

        def transform_point(p):
            return np.array([p[0]*scale, p[1]*scale, 0]) + shift

        group = VGroup()
        labels_group = VGroup()
        arcs_group = VGroup()

        for i, ((x, y, s), col) in enumerate(zip(squares_data, colors)):
            sq = Square(side_length=s*scale, color=col, stroke_width=2)
            sq.set_fill(col, opacity=0.15)
            center_pt = transform_point((x + s/2, y + s/2))
            sq.move_to(center_pt)

            lbl = Text(str(s), font_size=int(18 + s*2), color=WHITE).move_to(center_pt)

            (cx, cy), r, sa = arcs_data[i]
            arc = Arc(
                radius=r*scale,
                start_angle=sa,
                angle=-PI/2,
                arc_center=transform_point((cx, cy)),
                color=GOLD,
                stroke_width=4,
            )

            self.play(Create(sq), FadeIn(lbl), run_time=0.6)
            self.play(Create(arc), run_time=0.8)
            group.add(sq)
            labels_group.add(lbl)
            arcs_group.add(arc)

        caption = Text("邊長: 1, 1, 2, 3, 5, 8", font_size=28).to_edge(DOWN)
        self.play(Write(caption))
        self.play(arcs_group.animate.set_stroke(width=6), run_time=1)
        self.wait(2)