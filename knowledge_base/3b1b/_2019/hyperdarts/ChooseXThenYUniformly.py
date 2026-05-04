# Source: 3b1b/_2019/hyperdarts.py
# Description: [3b1b translated] 展示在單位圓內隨機選取點的過程，先均勻選取 x 坐標，再均勻選取 y 坐標，最後顯示大量隨機點的分佈。


from manim import *
import numpy as np

class ChooseXThenYUniformly(Scene):
    def construct(self):
        # Setup
        unit_size = 3
        axes = Axes(
            x_range=[-1.25, 1.25, 0.25],
            y_range=[-1.25, 1.25, 0.25],
            x_length=unit_size * 2.5,
            y_length=unit_size * 2.5,
            axis_config={
                "include_numbers": True,
                "font_size": 24,
            }
        )
        # 手動添加數字標籤
        numbers = [-1, -0.5, 0.5, 1]
        for x in numbers:
            label = Text(f"{x:.1f}", font_size=24, color=WHITE)
            label.next_to(axes.c2p(x, 0), DOWN, buff=0.1)
            self.add(label)
        for y in numbers:
            label = Text(f"{y:.1f}", font_size=24, color=WHITE)
            label.next_to(axes.c2p(0, y), LEFT, buff=0.1)
            self.add(label)

        circle = Circle(radius=unit_size)
        circle.set_stroke(WHITE, 0)
        circle.set_fill(RED, 0.7)

        square = Square(side_length=unit_size * 2)
        square.move_to(circle.get_center())
        square.set_stroke(GREY_B, 1)
        square = DashedVMobject(square, num_dashes=101)

        self.add(square, circle)
        self.add(axes)

        # x and y stuff
        x_tracker = ValueTracker(-1)
        y_tracker = ValueTracker(-1)

        get_x = x_tracker.get_value
        get_y = y_tracker.get_value

        x_tip = ArrowTip(start_angle=PI / 2, color=BLUE)
        y_tip = ArrowTip(start_angle=0, color=YELLOW)
        for tip in [x_tip, y_tip]:
            tip.scale(0.5)
        x_tip.add_updater(lambda m: m.move_to(axes.c2p(get_x(), 0), UP))
        y_tip.add_updater(lambda m: m.move_to(axes.c2p(0, get_y()), RIGHT))

        x_eq = VGroup(MathTex("x = "), DecimalNumber(0))
        x_eq.arrange(RIGHT, buff=SMALL_BUFF)
        x_eq[1].match_y(x_eq[0][0][1])
        x_eq[1].add_updater(lambda m: m.set_value(get_x()))
        x_eq.set_color(BLUE)

        y_eq = VGroup(MathTex("y = "), DecimalNumber(0))
        y_eq.arrange(RIGHT, buff=SMALL_BUFF)
        y_eq[1].match_y(y_eq[0][0][1])
        y_eq[1].add_updater(lambda m: m.set_value(get_y()))
        y_eq.set_color(YELLOW)

        eqs = VGroup(x_eq, y_eq)
        eqs.arrange(DOWN, buff=MED_LARGE_BUFF)
        eqs.to_edge(UR)

        self.add(x_tip)
        self.add(x_eq)

        # Choose x
        self.play(
            x_tracker.animate.set_value(1),
            run_time=2,
        )
        self.play(
            x_tracker.animate.set_value(np.random.random()),
            run_time=1,
        )

        # Choose y
        self.play(
            FadeIn(y_tip, shift=UP),
            FadeIn(y_eq, shift=UP),
        )
        self.play(
            y_tracker.animate.set_value(1),
            run_time=2,
        )
        self.play(
            y_tracker.animate.set_value(np.random.random()),
            run_time=1,
        )

        point = axes.c2p(get_x(), get_y())
        dot = Dot(point)
        x_line = DashedLine(axes.c2p(0, get_y()), point)
        y_line = DashedLine(axes.c2p(get_x(), 0), point)
        lines = VGroup(x_line, y_line)
        lines.set_stroke(WHITE, 2)

        self.play(*[Create(line) for line in lines])
        self.play(DrawBorderThenFill(dot))
        self.wait()

        points = [
            axes.c2p(*np.random.uniform(-1, 1, size=2))
            for n in range(2000)
        ]
        dots = VGroup(*[
            Dot(point, radius=0.02)
            for point in points
        ])
        self.play(
            LaggedStart(*[FadeIn(dot, scale=3) for dot in dots]),
            run_time=3,
        )
        self.wait()
