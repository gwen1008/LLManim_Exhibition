# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示五個問題的預估平均分數與實際平均分數的柱狀圖對比，柱狀圖從底部向上動態生長。



from manim import *
class DifficultyEstimateVsReality(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1, 10],
            y_range=[-1, 5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_tip": False,
            },
        )
        axes.set_height(FRAME_HEIGHT - 1)
        axes.center()
        axes.x_axis.tick_marks.set_opacity(0)

        y_label = Tex("Average score")
        y_label.scale(1.25)
        y_label.rotate(90 * DEGREES)
        y_label.next_to(axes.y_axis, LEFT, SMALL_BUFF)
        y_label.shift(UP)

        estimated = [1.8, 2.6, 3, 4, 5]
        actual = [1.5, 0.5, 1, 1.2, 1.8]

        colors = [GREEN, RED]
        estimated_color, actual_color = colors

        estimated_bars = VGroup()
        actual_bars = VGroup()
        bar_pairs = VGroup()

        width = 0.25
        for a, e in zip(actual, estimated):
            bars = VGroup(
                Rectangle(width=width, height=e),
                Rectangle(width=width, height=a),
            )
            bars.set_stroke(width=1)
            bars[0].set_fill(estimated_color, 0.75)
            bars[1].set_fill(actual_color, 0.75)
            bars.arrange(RIGHT, buff=0, aligned_edge=DOWN)
            bar_pairs.add(bars)
            estimated_bars.add(bars[0])
            actual_bars.add(bars[1])

        bar_pairs.arrange(RIGHT, buff=1.5, aligned_edge=DOWN)
        bar_pairs.move_to(axes.c2p(5, 0), DOWN)
        for bp in bar_pairs:
            for bar in bp:
                bar.save_state()
                bar.stretch(0, 1, about_edge=DOWN)

        x_labels = VGroup(*[
            Tex("Q{}".format(i)).next_to(bp, DOWN)
            for i, bp in zip(it.count(1), bar_pairs)
        ])

        data_labels = VGroup(
            Tex("Estimated average"),
            Tex("Actual average"),
        )
        data_labels.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        data_labels.to_edge(UP)
        for color, label in zip(colors, data_labels):
            square = Square()
            square.set_height(0.5)
            square.set_fill(color, 0.75)
            square.set_stroke(WHITE, 1)
            square.next_to(label, LEFT, SMALL_BUFF)
            label.add(square)

        self.play(Write(axes))
        self.play(Write(y_label))

        self.play(
            LaggedStartMap(
                FadeIn, x_labels,
                lambda m: (m, UP),
                run_time=2,
            ),
            LaggedStartMap(
                Restore,
                estimated_bars,
                run_time=3,
            ),
            FadeIn(data_labels[0]),
        )
        self.wait()
        self.play(
            LaggedStartMap(
                Restore,
                actual_bars,
                run_time=3,
            ),
            FadeIn(data_labels[1]),
        )
        self.wait()
