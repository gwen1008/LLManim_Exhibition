# Source: 3b1b/_2019/hyperdarts.py
# Description: [3b1b translated] 展示四個隨機變數在數線上的取樣過程，並即時計算其平方和是否小於1，視覺化概率問題。


from manim import *
import numpy as np

class SamplingFourRandomNumbers(Scene):
    def __init__(
        self,
        n_terms=4,
        title_tex="P\\left(x_0{}^2 + y_0{}^2 + x_1{}^2 + y_1{}^2 < 1\\right) = \\, ???",
        nl_to_nl_buff=0.75,
        to_floor_buff=0.5,
        tip_scale_factor=0.75,
        include_half_labels=True,
        include_title=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.n_terms = n_terms
        self.title_tex = title_tex
        self.nl_to_nl_buff = nl_to_nl_buff
        self.to_floor_buff = to_floor_buff
        self.tip_scale_factor = tip_scale_factor
        self.include_half_labels = include_half_labels
        self.include_title = include_title

    def construct(self):
        texs = ["x_0", "y_0", "x_1", "y_1", "x_2", "y_2"][:self.n_terms]
        colors = [BLUE, YELLOW, BLUE_B, YELLOW_B, BLUE_A, YELLOW_A][:self.n_terms]
        t2c = dict([(t, c) for t, c in zip(texs, colors)])

        # Title
        if self.include_title:
            title = MathTex(
                self.title_tex,
                tex_to_color_map=t2c
            )
            title.scale(1.5)
            title.to_edge(UP)

            h_line = DashedLine(title.get_left(), title.get_right())
            h_line.next_to(title, DOWN, buff=MED_SMALL_BUFF)

            self.add(title, h_line)

        # Number lines
        number_lines = VGroup(*[
            NumberLine(
                x_range=[-1, 1],
                length=6,  # unit_size=3 → length=3*2=6
                tick_size=0.1,
                numbers_with_elongated_ticks=[-1, 0, 1],
                include_numbers=True,
            )
            for x in range(self.n_terms)
        ])
        for line in number_lines:
            if self.include_half_labels:
                # 手動添加 -0.5 和 0.5 標籤
                for val in [-0.5, 0.5]:
                    label = DecimalNumber(val, num_decimal_places=1)
                    label.scale(0.5)
                    label.next_to(line.n2p(val), DOWN, buff=0.1)
                    line.add(label)
        
        number_lines.arrange(DOWN, buff=self.nl_to_nl_buff)
        number_lines.to_edge(LEFT, buff=0.5)
        number_lines.to_edge(DOWN, buff=self.to_floor_buff)

        self.add(number_lines)

        # Trackers
        trackers = Group(*[ValueTracker(0) for x in range(self.n_terms)])
        tips = VGroup(*[
            Triangle(
                start_angle=-PI / 2,
                color=color,
                fill_opacity=1,
                stroke_width=0
            ).scale(self.tip_scale_factor * 0.5)
            for color in colors
        ])
        labels = VGroup(*[
            MathTex(tex)
            for tex in texs
        ])

        for tip, tracker, line, label in zip(tips, trackers, number_lines, labels):
            tip.line = line
            tip.tracker = tracker
            tip.add_updater(lambda t: t.move_to(
                t.line.n2p(t.tracker.get_value()), DOWN
            ))

            label.tip = tip
            label.set_color(tip.color)
            label.add_updater(lambda l: l.next_to(l.tip, UP, buff=SMALL_BUFF))

        self.add(tips, labels)

        # Write bit sum
        summands = VGroup(*[
            MathTex("\\big(", "+0.00", "\\big)^2").set_color(color)
            for color in colors
        ])
        summands.arrange(DOWN)
        summands.to_edge(RIGHT, buff=3)
        for summand, tracker in zip(summands, trackers):
            dec = DecimalNumber(include_sign=True)
            dec.set_color(summand.get_color())
            dec.tracker = tracker
            dec.add_updater(lambda d: d.set_value(d.tracker.get_value()))
            dec.move_to(summand[1])
            summand.submobjects[1] = dec

        h_line = Line(LEFT, RIGHT)
        h_line.set_length(3)
        h_line.next_to(summands, DOWN, aligned_edge=RIGHT)
        plus = MathTex("+")
        plus.next_to(h_line.get_left(), UR)
        h_line.add(plus)

        total = DecimalNumber()
        total.scale(1.5)
        total.next_to(h_line, DOWN)
        total.align_to(summands, LEFT)
        total.add_updater(lambda d: d.set_value(np.sum([
            t.get_value()**2 for t in trackers
        ])))

        # Shift onto screen
        group = VGroup(summands, h_line, total)
        if group.get_bottom()[1] < -config.frame_height/2:
            group.shift(UP * (group.get_bottom()[1] + config.frame_height/2))
        self.add(summands, h_line, total)

        # < or > 1
        lt, gt = signs = VGroup(
            MathTex("< 1 \\quad \\checkmark"),
            MathTex("\\ge 1 \\quad"),
        )
        for sign in signs:
            sign.scale(1.5)
            sign.next_to(total, RIGHT, buff=MED_LARGE_BUFF)
        lt.set_color(GREEN)
        gt.set_color(RED)

        def update_signs(signs):
            i = int(total.get_value() > 1)
            signs[1 - i].set_opacity(0)
            signs[i].set_opacity(1)

        signs.add_updater(update_signs)

        self.add(signs)

        # Run simulation
        for x in range(9):
            trackers.generate_target()
            for t in trackers.target:
                t.set_value(np.random.uniform(-1, 1))

            if x == 8:
                for t in trackers.target:
                    t.set_value(np.random.uniform(-0.5, 0.5))

            self.remove(signs)
            self.play(MoveToTarget(trackers))
            self.add(signs)
            self.wait()

        # Less than 0.5
        nl = number_lines[0]
        line = Line(nl.n2p(-0.5), nl.n2p(0.5))
        rect = Rectangle(height=0.25)
        rect.set_stroke(width=0)
        rect.set_fill(GREEN, 0.5)
        rect.set_width(line.get_length(), stretch=True)
        rects = VGroup(*[
            rect.copy().move_to(line.n2p(0))
            for line in number_lines
        ])

        self.play(LaggedStartMap(GrowFromCenter, rects))
        self.wait()
        self.play(LaggedStartMap(FadeOut, rects))

        # Set one to 0.5
        self.play(trackers[0].animate.set_value(0.9))
        self.play(Create(Indicate(summands[0])))
        self.wait()
        self.play(LaggedStart(*[
            Create(Indicate(summand))
            for summand in summands[1:]
        ]))
        self.play(*[
            tracker.animate.set_value(0.1)
            for tracker in trackers[1:]
        ])
        self.wait(10)
