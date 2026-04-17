# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示巴塞爾問題的歐拉求和公式，從部分和逐步逼近 π²/6，並介紹歷史背景與其他 π 相關公式。


from manim import *
import itertools as it
import numpy as np

class IntroScene(PiCreatureScene):
    def __init__(self, rect_height=0.075, duration=1.0, eq_spacing=3*MED_LARGE_BUFF, n_rects_to_show=30, **kwargs):
        super().__init__(**kwargs)
        self.rect_height = rect_height
        self.duration = duration
        self.eq_spacing = eq_spacing
        self.n_rects_to_show = n_rects_to_show

    def construct(self):
        randy = self.pi_creature
        randy.scale(0.7).to_corner(DOWN+RIGHT)

        self.build_up_euler_sum()
        self.show_history()
        # self.other_pi_formulas()
        # self.refocus_on_euler_sum()

    def build_up_euler_sum(self):
        morty = self.pi_creature
        euler_sum = self.euler_sum = MathTex(
           "1", "+", 
           "{1 \\over 4}", "+",
           "{1 \\over 9}", "+",
           "{1 \\over 16}", "+",
           "{1 \\over 25}", "+",
           "\\cdots", "=",
            arg_separator = " \\, "
        )
        equals_sign = euler_sum.get_part_by_tex("=")
        plusses = euler_sum.get_parts_by_tex("+")
        term_mobjects = euler_sum.get_parts_by_tex("1")

        self.euler_sum.to_edge(UP)
        self.euler_sum.shift(2*LEFT)
       
        max_n = self.n_rects_to_show
        terms = [1./(n**2) for n in range(1, max_n + 1)]
        series_terms = list(np.cumsum(terms))
        series_terms.append(np.pi**2/6) ##Just force this up there

        partial_sum_decimal = self.partial_sum_decimal = DecimalNumber(
            series_terms[1],
            num_decimal_places = 2
        )
        partial_sum_decimal.next_to(equals_sign, RIGHT)

        ## Number line

        number_line = self.number_line = NumberLine(
            x_range = [0, 4, 0.2],
            color = WHITE,
            stroke_width = 1,
            length = 5,
            include_numbers = True,
            numbers_with_elongated_ticks = [0,1,2,3],
            numbers_to_include = np.arange(0,5),
            line_to_number_buff = MED_LARGE_BUFF
        )
        number_line.to_edge(LEFT)
        number_line.shift(MED_LARGE_BUFF*UP)

        # create slabs for series terms

        lines = VGroup()
        rects = self.rects = VGroup()
        rect_labels = VGroup()
        slab_colors = it.cycle([YELLOW, BLUE])
        rect_anims = []
        rect_label_anims = []

        for i, t1, t2 in zip(it.count(1), [0]+series_terms, series_terms):
            color = next(slab_colors)
            line = Line(*list(map(number_line.n2p, [t1, t2])))
            rect = Rectangle(
                stroke_width = 0,
                fill_opacity = 1,
                fill_color = color
            )
            rect.match_width(line)
            rect.stretch_to_fit_height(self.rect_height)
            rect.move_to(line)

            if i <= 5:
                if i == 1:
                    rect_label = MathTex("1")
                else:
                    rect_label = MathTex("\\frac{1}{%d}"%(i**2))
                    rect_label.scale(0.75)
                max_width = 0.7*rect.get_width()
                if rect_label.get_width() > max_width:
                    rect_label.set_width(max_width)
                rect_label.next_to(rect, UP, buff = MED_LARGE_BUFF/(i+1))

                term_mobject = term_mobjects[i-1]
                rect_anim = GrowFromPoint(rect, term_mobject.get_center())
                rect_label_anim = ReplacementTransform(
                    term_mobject.copy(), rect_label
                )
            else:
                rect_label = Dot(radius=0, color=BLACK)  # VectorizedPoint替代
                rect_anim = GrowFromPoint(rect, rect.get_left())
                rect_label_anim = FadeIn(rect_label)

            rects.add(rect)
            rect_labels.add(rect_label)
            rect_anims.append(rect_anim)
            rect_label_anims.append(rect_label_anim)
            lines.add(line)
        dots = MathTex("\\dots").scale(0.5)
        last_rect = rects[-1]
        dots.set_width(0.9*last_rect.get_width())
        dots.move_to(last_rect, UP+RIGHT)
        rects.submobjects[-1] = dots
        rect_anims[-1] = FadeIn(dots)

        self.add(number_line)
        self.play(FadeIn(euler_sum[0]))
        self.play(
            rect_anims[0],
            rect_label_anims[0]
        )
        for i in range(4):
            self.play(
                FadeIn(term_mobjects[i+1]),
                FadeIn(plusses[i]),
            )
            anims = [
                rect_anims[i+1],
                rect_label_anims[i+1],
            ]
            if i == 0:
                anims += [
                    FadeIn(equals_sign),
                    FadeIn(partial_sum_decimal)
                ]
            elif i <= 5:
                anims += [
                    ChangeDecimalToValue(
                        partial_sum_decimal,
                        series_terms[i+1], 
                        run_time = 1,
                        num_decimal_places = 6,
                    ).update_config(position_update_func = lambda m: m.next_to(equals_sign, RIGHT))
                ]
            self.play(*anims)

        for i in range(4, len(series_terms)-2):
            anims = [
                rect_anims[i+1],
                ChangeDecimalToValue(
                    partial_sum_decimal,
                    series_terms[i+1],
                    num_decimal_places = 6,
                ),
            ]
            if i == 5:
                anims += [
                    FadeIn(euler_sum[-3]), # +
                    FadeIn(euler_sum[-2]), # ...
                ]
            self.play(*anims, run_time = 2./i)

        brace = self.brace = Brace(partial_sum_decimal, DOWN)
        q_marks = self.q_marks = Text("???")
        q_marks.next_to(brace, DOWN)
        q_marks.set_color(LIGHT_GRAY)

        self.play(
            GrowFromCenter(brace),
            Write(q_marks),
            ChangeDecimalToValue(
                partial_sum_decimal,
                series_terms[-1],
                num_decimal_places = 6,
            ),
            morty.animate.change("confused"),
        )
        self.wait()

        self.number_line_group = VGroup(
            number_line, rects, rect_labels
        )

    def show_history(self):
        # Pietro Mengoli in 1644
        morty = self.pi_creature
        pietro = ImageMobject("Pietro_Mengoli")
        euler = ImageMobject("Euler")

        pietro_words = Text("Challenge posed by\nPietro Mengoli in 1644")
        pietro_words.scale(0.75)
        pietro_words.next_to(pietro, DOWN)
        pietro.add(pietro_words)

        euler_words = Text("Solved by Leonard\nEuler in 1735")
        euler_words.scale(0.75)
        euler_words.next_to(euler, DOWN)
        euler.add(euler_words)

        pietro.next_to(config.frame_width/2*LEFT, LEFT)
        euler.next_to(config.frame_width/2*RIGHT, RIGHT)

        pi_answer = self.pi_answer = MathTex("{\\pi^2 \\over 6}")
        pi_answer.set_color(YELLOW)
        pi_answer.move_to(self.partial_sum_decimal, LEFT)
        equals_sign = MathTex("=")
        equals_sign.next_to(pi_answer, RIGHT)
        pi_answer.shift(SMALL_BUFF*UP)
        self.partial_sum_decimal.generate_target()
        self.partial_sum_decimal.target.next_to(equals_sign, RIGHT)

        pi = pi_answer[0]
        pi_rect = SurroundingRectangle(pi, color = RED)
        pi_rect.save_state()
        pi_rect.set_height(config.frame_height)
        pi_rect.center()
        pi_rect.set_stroke(width = 0)
        squared = pi_answer[1]
        squared_rect = SurroundingRectangle(squared, color = BLUE)

        brace = Brace(
            VGroup(self.euler_sum, self.partial_sum_decimal.target),
            DOWN, buff = SMALL_BUFF
        )
        basel_text = brace.get_text("Basel problem", buff = SMALL_BUFF)

        self.number_line_group.save_state()
        self.play(
            pietro.animate.next_to(ORIGIN, LEFT, LARGE_BUFF),
            self.number_line_group.animate.next_to(config.frame_height/2*DOWN, DOWN),
            morty.animate.change("pondering"),
        )
        self.wait(2)
        self.play(euler.animate.next_to(ORIGIN, RIGHT, LARGE_BUFF))
        self.wait(2)
        self.play(
            ReplacementTransform(self.q_marks, pi_answer),
            FadeIn(equals_sign),
            FadeOut(self.brace),
            MoveToTarget(self.partial_sum_decimal)
        )
        self.wait()
        self.play(morty.animate.change("surprised"))
        self.play(Restore(pi_rect))
        self.wait()
        self.play(Transform(pi_rect, squared_rect))
        self.play(FadeOut(pi_rect))
        self.play(morty.animate.change("hesitant"))
        self.wait(2)
        self.play(
            GrowFromCenter(brace),
            euler.animate.to_edge(DOWN),
            pietro.animate.to_edge(DOWN),
            Restore(self.number_line_group),
            self.number_line_group.animate.shift(LARGE_BUFF*RIGHT),
        )
        self.play(Write(basel_text))
        self.play(morty.animate.change("happy"))
        self.wait(4)

    def other_pi_formulas(self):

        self.play(
            FadeOut(self.rects),
            FadeOut(self.number_line)
        )

        self.leibniz_sum = MathTex(
            "1-{1\\over 3}+{1\\over 5}-{1\\over 7}+{1\\over 9}-\\cdots",
            "=", "{\\pi \\over 4}")

        self.wallis_product = MathTex(
            "{2\\over 1} \\cdot {2\\over 3} \\cdot {4\\over 3} \\cdot {4\\over 5}" +
             "\\cdot {6\\over 5} \\cdot {6\\over 7} \\cdots",
             "=", "{\\pi \\over 2}")

        self.leibniz_sum.next_to(self.euler_sum.get_part_by_tex("="), DOWN,
            buff = self.eq_spacing,
            aligned_edge = self.leibniz_sum.get_part_by_tex("=")
        )

        self.wallis_product.next_to(self.leibniz_sum.get_part_by_tex("="), DOWN,
            buff = self.eq_spacing,
            aligned_edge = self.wallis_product.get_part_by_tex("=")
        )


        self.play(
            Write(self.leibniz_sum)
        )
        self.play(
            Write(self.wallis_product)
        )

    def refocus_on_euler_sum(self):

        self.euler_sum.add(self.pi_answer)

        self.play(
            FadeOut(self.leibniz_sum),
            FadeOut(self.wallis_product),
            self.euler_sum.animate.shift(
                ORIGIN + 2*UP - self.euler_sum.get_center())
        )

        # focus on pi squared
        pi_squared = self.euler_sum.get_part_by_tex("\\pi")[-3]
        self.play(
            pi_squared.animate.scale(2).set_rate_func(wiggle)
        )



        # Morty thinks of a circle

        q_circle = Circle(
            stroke_color = YELLOW,
            fill_color = YELLOW,
            fill_opacity = 0.5,
            radius = 0.4, 
            stroke_width = 10.0
        )
        q_mark = MathTex("?")
        q_mark.next_to(q_circle)

        thought = Group(q_circle, q_mark)
        q_mark.set_height(0.8 * q_circle.get_height())
        self.pi_creature_thinks(thought,target_mode = "confused",
            bubble_config = { "height" : 2, "width" : 3 })

        self.wait()
