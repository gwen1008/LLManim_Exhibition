# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示帕斯卡三角形從頂部逐行生成，解釋三角形中每個數字代表組合數的意義，並以 9 選 4 為例說明其概率計算。


from manim import *
import itertools
import random

class IntroducePascalsTriangle(Scene):
    def __init__(self, max_n=9, **kwargs):
        super().__init__(**kwargs)
        self.max_n = max_n

    def construct(self):
        self.show_triangle()
        self.show_sum_of_two_over_rule()
        self.keep_in_mind_what_these_mean()
        self.issolate_9_choose_4_term()
        self.show_9_choose_4_pattern()
        self.cap_off_triangle()

    def show_triangle(self):
        rows = PascalsTriangle(n_rows=self.max_n+1)
        self.play(FadeIn(rows[1]))
        for last_row, curr_row in zip(rows[1:], rows[2:]):
            self.play(*[
                Transform(
                    last_row.copy(), VGroup(*mobs),
                    remover=True
                )
                for mobs in (curr_row[1:], curr_row[:-1])
            ])
            self.add(curr_row)
        self.wait()

        self.rows = rows

    def show_sum_of_two_over_rule(self):
        rows = self.rows

        example = rows[5][3]
        ex_top1 = rows[4][2]
        ex_top2 = rows[4][3]

        rects = VGroup()
        for mob, color in (example, GREEN), (ex_top1, BLUE), (ex_top2, YELLOW):
            mob.rect = SurroundingRectangle(mob, color=color)
            rects.add(mob.rect)

        rows_to_fade = VGroup(*rows[1:4], *rows[6:])
        rows_to_fade.save_state()

        top_row = rows[4]
        low_row = rows[5]
        top_row_copy = top_row.copy()
        top_row.save_state()
        top_row.add(ex_top2.rect)
        top_row_copy.add(ex_top1.rect)
        h_line = Line(LEFT, RIGHT)
        h_line.stretch_to_fit_width(low_row.get_width() + 2)
        h_line.next_to(low_row, UP, 1.5*SMALL_BUFF)
        plus = MathTex("+")
        plus.next_to(h_line.get_left(), UP+RIGHT, buff=1.5*SMALL_BUFF)

        self.play(Create(example.rect))
        self.play(
            ReplacementTransform(example.rect.copy(), ex_top1.rect),
            ReplacementTransform(example.rect.copy(), ex_top2.rect),
        )
        self.wait(2)
        self.play(rows_to_fade.animate.set_opacity(0.3))
        self.play(
            top_row.animate.align_to(low_row, LEFT),
            top_row_copy.animate.next_to(top_row, UP),
            top_row_copy.animate.align_to(low_row, RIGHT),
        )
        self.play(
            Create(h_line),
            Write(plus)
        )
        self.wait(2)
        for row in top_row, top_row_copy:
            row.remove(row[-1])
        self.play(
            rows_to_fade.animate.restore(),
            top_row.animate.restore(),
            Transform(
                top_row_copy, top_row.saved_state,
                remover=True
            ),
            FadeOut(VGroup(h_line, plus)),
            FadeOut(rects),
        )
        self.wait()

    def keep_in_mind_what_these_mean(self):
        morty = Mortimer().flip()
        morty.scale(0.7)
        morty.to_edge(LEFT)
        morty.shift(DOWN)

        numbers = VGroup(*itertools.chain(*self.rows[1:]))
        random.shuffle(numbers.submobjects)

        self.play(FadeIn(morty))
        self.play(PiCreatureSays(
            morty, "Keep in mind \\\\ what these mean.",
            bubble_config={
                "width": 3.5,
                "height": 2.5,
            }
        ))
        self.play(
            Blink(morty),
            LaggedStartMap(
                Indicate, numbers,
                rate_func=wiggle,
                color=PINK,
            )
        )
        self.play(*list(map(FadeOut, [
            morty, morty.bubble, morty.bubble.content
        ])))

    def issolate_9_choose_4_term(self):
        rows = self.rows

        for n in range(1, self.max_n+1):
            num = rows[n][0]
            line = get_stack(Female(), Male(), n, 0)[0]
            if n < self.max_n:
                line.next_to(num, LEFT)
            else:
                line.next_to(num, DOWN, MED_LARGE_BUFF)
            self.set_color_num(num)
            self.add(line)
            if n < self.max_n:
                self.wait(0.25)
            else:
                self.wait(1.25)
            self.dehighlight_num(num)
            self.remove(line)
        for k in range(1, 5):
            num = rows[self.max_n][k]
            line = get_stack(Female(), Male(), self.max_n, k)[0]
            line.next_to(num, DOWN, MED_LARGE_BUFF)
            self.set_color_num(num)
            self.add(line)
            self.wait(0.5)
            self.dehighlight_num(num)
            self.remove(line)
        num.set_color(YELLOW)
        num.scale(1.2)
        self.add(line)
        self.wait()

        self.nine_choose_four_term = num
        self.nine_choose_four_line = line

    def show_9_choose_4_pattern(self):
        rows = VGroup(*self.rows[1:])
        all_stacks = get_stacks(Female(), Male(), 9)
        stack = all_stacks[4]
        all_lines = VGroup(*itertools.chain(*all_stacks))

        self.play(
            rows.animate.shift(3*UP),
            self.nine_choose_four_line.animate.shift(2.5*UP),
        )
        self.remove(self.nine_choose_four_line)

        for n, line in enumerate(stack):
            line.next_to(self.nine_choose_four_term, DOWN, LARGE_BUFF)
            num = Integer(n+1)
            num.next_to(line, DOWN, MED_LARGE_BUFF)
            self.add(line, num)
            self.wait(0.1)
            self.remove(line, num)
        self.add(line, num)
        self.wait()
        self.curr_line = line

        #Probability
        expr = MathTex(
            "P(4", "\\female", "\\text{ out of }", "9", ")", "="
        )
        expr.move_to(num.get_left())
        expr.set_color_by_tex("female", MAROON_B)
        nine_choose_four_term = self.nine_choose_four_term.copy()
        nine_choose_four_term.generate_target()
        nine_choose_four_term.target.scale(1./1.2)
        over_512 = MathTex("\\quad \\over 2^9")
        frac = VGroup(nine_choose_four_term.target, over_512)
        frac.arrange(DOWN, buff=SMALL_BUFF)
        frac.next_to(expr, RIGHT, SMALL_BUFF)
        eq_result = MathTex("\\approx 0.246")
        eq_result.next_to(frac, RIGHT)

        def show_random_lines(n, wait_time=1):
            for x in range(n):
                if x == n-1:
                    wait_time = 0
                new_line = random.choice(all_lines)
                new_line.move_to(self.curr_line)
                self.remove(self.curr_line)
                self.curr_line = new_line
                self.add(self.curr_line)
                self.wait(wait_time)

        self.play(FadeOut(num), FadeIn(expr))
        show_random_lines(4)
        self.play(
            MoveToTarget(nine_choose_four_term),
            Write(over_512)
        )
        show_random_lines(4)
        self.play(Write(eq_result))
        show_random_lines(6)
        self.play(
            self.nine_choose_four_term.animate.scale(1./1.2),
            self.nine_choose_four_term.animate.set_color(WHITE),
            *list(map(FadeOut, [
                expr, nine_choose_four_term,
                over_512, eq_result, self.curr_line
            ]))
        )
        self.play(rows.animate.shift(3*DOWN))

    def cap_off_triangle(self):
        top_row = self.rows[0]
        circle = Circle(color=YELLOW)
        circle.replace(top_row, dim_to_match=1)
        circle.scale(1.5)

        line_groups = VGroup()
        for n in range(4, -1, -1):
            line = VGroup(*[
                random.choice([Male, Female])()
                for k in range(n)
            ])
            if n == 0:
                line.add(Line(LEFT, RIGHT).scale(0.1).set_stroke(BLACK, 0))
            line.arrange(RIGHT, SMALL_BUFF)
            line.shift(FRAME_X_RADIUS*RIGHT/2 + FRAME_Y_RADIUS*UP/2)
            brace = Brace(line, UP)
            if n == 1:
                label = "1 Person"
            else:
                label = "%d People"%n
            brace_text = brace.get_text(label)
            line_group = VGroup(line, brace, brace_text)
            line_groups.add(line_group)

        self.play(Create(circle))
        self.play(Write(top_row))
        self.wait()
        curr_line_group = line_groups[0]
        self.play(FadeIn(curr_line_group))
        for line_group in line_groups[1:]:
            self.play(ReplacementTransform(
                curr_line_group, line_group
            ))
            curr_line_group = line_group
        self.wait()

    ###

    def set_color_num(self, num):
        num.set_color(YELLOW)
        num.scale(1.2)

    def dehighlight_num(self, num):
        num.set_color(WHITE)
        num.scale(1.0/1.2)
