# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示在三維空間中，沿著圓弧上的三個點進行插值，並繪製連接它們的虛線段及其投影到圓上的過程。



from manim import *
class QuaternionInterpolationScematic(Scene):
    def construct(self):
        title = Tex("Slice of a hypersphere")
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(title)

        radius = 3
        circle = Circle(radius=radius)
        circle.set_stroke(GREY_B, 1)
        qs = [circle.point_from_proportion(p) for p in (0.55, 0.35, 0.15)]
        colors = [YELLOW, PINK, RED]
        q_dots = [Dot(q, color=c) for q, c in zip(qs, colors)]
        q_labels = [
            MathTex("q_{}".format(i + 1)).next_to(
                dot, normalize(dot.get_center()), SMALL_BUFF
            ).set_color(dot.get_color())
            for i, dot in enumerate(q_dots)
        ]

        q1, q2, q3 = qs
        lines = [
            DashedLine(q1, q2)
            for q1, q2 in zip(qs, qs[1:])
        ]
        for color, line in zip([GREEN, BLUE], lines):
            line.set_stroke(color, 3)
            line.proj = line.copy().apply_function(
                lambda p: radius * normalize(p)
            )
        dot = Dot(qs[0], color=WHITE)

        self.add(circle)
        self.add(dot)
        self.add(*q_dots + q_labels)

        self.wait(2)
        for line, q in zip(lines, qs[1:]):
            self.play(
                Create(line),
                Create(line.proj),
                dot.animate.move_to(q),
                run_time=4
            )
            self.wait(2)
