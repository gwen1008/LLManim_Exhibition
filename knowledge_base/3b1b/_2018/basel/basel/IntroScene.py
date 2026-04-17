# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示巴塞爾問題（歐拉求和）的動畫推導，包括數線上的級數累加、π²/6 的答案呈現，以及其他與 π 相關的公式。



from manim import *
class IntroScene(PiCreatureScene):
    def __init__(self, rect_height=0.2, duration=0.5, eq_spacing=6*MED_LARGE_BUFF, **kwargs):
        super().__init__(**kwargs)
        self.rect_height = rect_height
        self.duration = duration
        self.eq_spacing = eq_spacing

    def construct(self):
        randy = self.pi_creature
        randy.scale(0.7).to_corner(DOWN+RIGHT)

        self.build_up_euler_sum()
        self.build_up_sum_on_number_line()
        self.show_pi_answer()
        self.other_pi_formulas()
        self.refocus_on_euler_sum()

    def build_up_euler_sum(self):
        self.euler_sum = MathTex(
            "1", "+", 
            "{1 \\over 4}", "+",
            "{1 \\over 9}", "+",
            "{1 \\over 16}", "+",
            "{1 \\over 25}", "+",
            "\\cdots", "=",
            arg_separator=" \\, "
        )
        self.euler_sum.to_edge(UP)
        self.euler_sum.shift(2*LEFT)
       
        terms = [1./n**2 for n in range(1,6)]
        partial_results_values = np.cumsum(terms)

        self.play(
            FadeIn(self.euler_sum[0], run_time=self.duration)
        )

        equals_sign = self.euler_sum.get_part_by_tex("=")

        self.partial_sum_decimal = DecimalNumber(
            partial_results_values[1],
            num_decimal_places=2
        )
        self.partial_sum_decimal.next_to(equals_sign, RIGHT)

        for i in range(4):
            if i == 0:
                self.play(
                    FadeIn(self.euler_sum[1], run_time=self.duration),
                    FadeIn(self.euler_sum[2], run_time=self.duration),
                    FadeIn(equals_sign, run_time=self.duration),
                    FadeIn(self.partial_sum_decimal, run_time=self.duration)
                )
            else:
                self.play(
                    FadeIn(self.euler_sum[2*i+1], run_time=self.duration),
                    FadeIn(self.euler_sum[2*i+2], run_time=self.duration),
                    ChangeDecimalToValue(
                        self.partial_sum_decimal,
                        partial_results_values[i+1], 
                        run_time=self.duration,
                        num_decimal_places=6,
                        position_update_func=lambda m: m.next_to(equals_sign, RIGHT)
                    )
                )
            self.wait()

        self.q_marks = Text("???").set_color(LIGHT_COLOR)
        self.q_marks.move_to(self.partial_sum_decimal)

        self.play(
            FadeIn(self.euler_sum[-3], run_time=self.duration),  # +
            FadeIn(self.euler_sum[-2], run_time=self.duration),  # ...
            ReplacementTransform(self.partial_sum_decimal, self.q_marks)
        )
        self.wait()

    def build_up_sum_on_number_line(self):
        self.number_line = NumberLine(
            x_range=[0, 4, 0.2],
            length=5,
            color=WHITE,
            stroke_width=1,
            include_numbers=True,
            numbers_to_include=np.arange(0, 5),
            font_size=24,
            label_direction=DOWN,
        ).shift(LEFT)
        
        self.number_line_labels = self.number_line.get_number_mobjects()
        self.play(
            FadeIn(self.number_line),
            FadeIn(self.number_line_labels)
        )
        self.wait()

        # create slabs for series terms
        max_n1 = 10
        max_n2 = 100

        terms = [0] + [1./(n**2) for n in range(1, max_n2 + 1)]
        series_terms = np.cumsum(terms)
        lines = VGroup()
        self.rects = VGroup()
        slab_colors = [YELLOW, BLUE] * (max_n2 // 2)

        for t1, t2, color in zip(series_terms, series_terms[1:], slab_colors):
            line = Line(
                self.number_line.number_to_point(t1),
                self.number_line.number_to_point(t2)
            )
            rect = Rectangle(
                height=self.rect_height,
                width=0.5 * line.get_width(),
                stroke_width=0,
                fill_opacity=1,
                color=color
            )
            rect.move_to(line)
            self.rects.add(rect)
            lines.add(line)

        self.little_euler_terms = VGroup()
        for i in range(1,7):
            if i == 1:
                term = MathTex("1", color=slab_colors[i-1])
            else:
                term = MathTex(f"{{1\\over {i**2}}}", color=slab_colors[i-1])
            term.scale(0.4)
            self.little_euler_terms.add(term)

        for i in range(5):
            self.play(
                GrowFromPoint(
                    self.rects[i],
                    self.euler_sum[2*i].get_center(),
                    run_time=1
                )
            )
            term = self.little_euler_terms[i]
            term.next_to(self.rects[i], UP)
            self.play(FadeIn(term))

        self.ellipsis = MathTex("\\cdots").scale(0.4)
        for i in range(5, max_n1):
            if i == 5:
                self.ellipsis.next_to(self.rects[i+3], UP)
                self.play(
                    FadeIn(self.ellipsis),
                    GrowFromPoint(
                        self.rects[i],
                        self.euler_sum[10].get_center(),
                        run_time=0.5
                    )
                )
            else:
                self.play(
                    GrowFromPoint(
                        self.rects[i],
                        self.euler_sum[10].get_center(),
                        run_time=0.5
                    )
                )
        
        for i in range(max_n1, max_n2):
            self.play(
                GrowFromPoint(
                    self.rects[i],
                    self.euler_sum[10].get_center(),
                    run_time=0.01
                )
            )

        self.wait()

        PI = TAU/2
        P = self.q_marks.get_center() + 0.5 * DOWN + 0.5 * LEFT
        Q = self.rects[-1].get_center() + 0.2 * UP
        self.arrow = CurvedArrow(
            P, Q,
            angle=TAU/12,
            color=YELLOW
        )
        self.play(FadeIn(self.arrow))
        self.wait()

    def show_pi_answer(self):
        self.pi_answer = MathTex("{\\pi^2 \\over 6}").set_color(YELLOW)
        self.pi_answer.move_to(self.partial_sum_decimal)
        self.pi_answer.next_to(
            self.euler_sum[-1], 
            RIGHT, 
            buff=1,
            aligned_edge=DOWN
        )
        self.play(ReplacementTransform(self.q_marks, self.pi_answer))
        self.wait()

    def other_pi_formulas(self):
        self.play(
            FadeOut(self.rects),
            FadeOut(self.number_line_labels),
            FadeOut(self.number_line),
            FadeOut(self.little_euler_terms),
            FadeOut(self.ellipsis),
            FadeOut(self.arrow)
        )

        self.leibniz_sum = MathTex(
            "1-{1\\over 3}+{1\\over 5}-{1\\over 7}+{1\\over 9}-\\cdots",
            "=", "\\quad\\,\\,{\\pi \\over 4}", 
            arg_separator=" \\, "
        )

        self.wallis_product = MathTex(
            "{2\\over 1} \\cdot {2\\over 3} \\cdot {4\\over 3} \\cdot {4\\over 5}" +
            "\\cdot {6\\over 5} \\cdot {6\\over 7} \\cdots",
            "=", "\\quad\\,\\, {\\pi \\over 2}", 
            arg_separator=" \\, "
        )

        equals_sign = self.euler_sum.get_part_by_tex("=")
        self.leibniz_sum.next_to(
            equals_sign, 
            DOWN,
            buff=2,
            aligned_edge=LEFT
        )

        self.wallis_product.next_to(
            self.leibniz_sum.get_part_by_tex("="), 
            DOWN,
            buff=2,
            aligned_edge=LEFT
        )

        self.play(Write(self.leibniz_sum))
        self.play(Write(self.wallis_product))

    def refocus_on_euler_sum(self):
        self.euler_sum.add(self.pi_answer)

        self.play(
            FadeOut(self.leibniz_sum),
            FadeOut(self.wallis_product),
            self.euler_sum.animate.shift(
                ORIGIN + 2*UP - self.euler_sum.get_center()
            )
        )

        # focus on pi squared
        pi_squared = self.euler_sum.get_part_by_tex("\\pi")[-3]
        self.play(
            Wiggle(
                pi_squared,
                scale_value=4,
                rotation_angle=0.003 * TAU,
                run_time=2
            )
        )

        # Morty thinks of a circle
        q_circle = Circle(
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.25,
            radius=0.5, 
            stroke_width=3.0
        )
        q_mark = MathTex("?")
        q_mark.next_to(q_circle)
        q_mark.set_height(0.6 * q_circle.get_height())

        thought = Group(q_circle, q_mark)
        
        self.pi_creature_says(
            thought,
            target_mode="confused",
            bubble_config={"height": 2.5, "width": 5}
        )
        self.wait()
