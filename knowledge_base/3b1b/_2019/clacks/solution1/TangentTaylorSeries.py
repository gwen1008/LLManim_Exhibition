# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示正切函數的泰勒級數展開，並用具體數值範例說明高階項的誤差影響。



from manim import *
class TangentTaylorSeries(TeacherStudentsScene):
    def construct(self):
        series = MathTex(
            r"\tan", r"(", r"\theta", r")", r"=", r"\theta", r"+",
            r"\frac{1}{3}", r"\theta", r"^3", r"+",
            r"\frac{2}{15}", r"\theta", r"^5", r"+", r"\cdots",
            tex_to_color_map={r"\theta": YELLOW},
        )
        series.move_to(2 * UP)
        series.move_to(self.hold_up_spot, DOWN)
        series_error = series[7:]
        series_error_rect = SurroundingRectangle(series_error)

        example = MathTex(
            r"\tan", r"\left(", r"\frac{1}{100}", r"\right)",
            r"=", r"\frac{1}{100}", r"+",
            r"\frac{1}{3}", r"\left(",
            r"\frac{1}{1{,}000{,}000}",
            r"\right)", r"+",
            r"\frac{2}{15}", r"\left(",
            r"\frac{1}{10{,}000{,}000{,}000}",
            r"\right)", r"+", r"\cdots",
        )
        example.set_color_by_tex(r"\frac{1}{1", BLUE)
        example.set_width(config.frame_width - 1)
        example.next_to(self.students, UP, buff=2)
        example.shift_onto_screen()
        error = example[7:]
        error_rect = SurroundingRectangle(error)
        error_rect.set_color(RED)
        error_decimal = DecimalNumber(
            np.tan(0.01) - 0.01,
            num_decimal_places=15,
        )
        error_decimal.next_to(error_rect, DOWN)
        approx = MathTex(r"\approx")
        approx.next_to(error_decimal, LEFT)
        error_decimal.add(approx)
        error_decimal.match_color(error_rect)

        self.play(
            FadeIn(series, shift=DOWN),
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play(
            Create(series_error_rect),
            self.change_students(*3 * ["pondering"])
        )
        self.play(FadeOut(series_error_rect))
        self.play(
            series.animate.center().to_edge(UP),
        )
        self.look_at(series)
        self.play(
            TransformFromCopy(series[:8], example[:8]),
            TransformFromCopy(series[8], example[9]),
            TransformFromCopy(series[10:12], example[11:13]),
            TransformFromCopy(series[12], example[14]),
            TransformFromCopy(series[14:], example[16:]),
            *[GrowFromCenter(example[i]) for i in (8, 10, 13, 15)]
        )
        self.play_student_changes("happy", "confused", "sad")
        self.play(Create(error_rect))
        self.play(ShowIncreasingSubsets(error_decimal))
        self.play_all_student_changes("hooray")
        self.wait(3)
