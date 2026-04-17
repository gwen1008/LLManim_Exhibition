# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示正弦函數公式隨著角度從60度變化到0度再到90度時，數值動態更新的過程。



from manim import *
class ShowSineValues(Scene):
    def construct(self):
        angle_tracker = ValueTracker(60 * DEGREES)
        get_angle = angle_tracker.get_value
        formula = always_redraw(
            lambda: self.get_sine_formula(get_angle())
        )
        self.add(formula)

        self.play(
            angle_tracker.animate.set_value(0),
            run_time=3,
        )
        self.wait()
        self.play(
            angle_tracker.animate.set_value(90 * DEGREES),
            run_time=3,
        )
        self.wait()

    def get_sine_formula(self, angle):
        sin, lp, rp = MathTex(
            "\\sin", "(", ") = "
        )
        input_part = Integer(
            angle / DEGREES,
            unit="^\\circ",
        )
        input_part.set_color(YELLOW)
        output_part = DecimalNumber(
            np.sin(input_part.get_value() * DEGREES),
            num_decimal_places=3,
        )
        result = VGroup(
            sin, lp, input_part, rp, output_part
        )
        result.arrange(RIGHT, buff=SMALL_BUFF)
        sin.scale(1.1, about_edge=DOWN)
        lp.align_to(rp, UP)
        return result
