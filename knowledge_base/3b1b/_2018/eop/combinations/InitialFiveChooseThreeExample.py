# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示從 5 個元素中選擇 3 個的所有組合方式，並解釋二項式係數的概念和計算過程。


from manim import *
import itertools

class InitialFiveChooseThreeExample(Scene):
    def __init__(self, n=5, zero_color=BLUE, one_color=PINK, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.zero_color = zero_color
        self.one_color = one_color

    def construct(self):
        self.show_all_stacks()
        self.add_title()
        self.show_binomial_name()
        self.issolate_single_stack()
        self.count_chosen_stack()
        self.count_ways_to_fill_slots()
        self.walk_though_notation()
        self.emphasize_pattern_over_number()

    def show_all_stacks(self):
        stacks = get_stacks(
            self.get_obj1(), self.get_obj2(), self.n,
            vertical_buff=SMALL_BUFF
        )
        stacks.to_edge(DOWN, buff=MED_LARGE_BUFF)

        for stack in stacks:
            self.play(FadeIn(
                stack,
                run_time=0.2*len(stack),
                lag_ratio=0.5
            ))
        self.wait()

        self.stacks = stacks

    def add_title(self):
        n = self.n
        stacks = self.stacks

        n_choose_k = MathTex("n \\choose k")
        n_choose_k_words = Text("``n choose k''")
        nCk_group = VGroup(n_choose_k, n_choose_k_words)
        nCk_group.arrange(RIGHT)
        nCk_group.to_edge(UP)

        binomials = VGroup(*[
            MathTex(f"{n} \\choose {k}")
            for k in range(n+1)
        ])
        binomial_equations = VGroup()
        for k, binomial in enumerate(binomials):
            binomial.scale(0.75)
            number = MathTex(str(math.comb(n, k)))
            equation = VGroup(binomial, MathTex("="), number)
            equation.arrange(RIGHT, buff=SMALL_BUFF)
            equation.set_color(YELLOW)
            equation[1].set_color(WHITE)
            binomial_equations.add(equation)

        for stack, eq in zip(stacks, binomial_equations):
            eq.set_width(0.9*stack.get_width())
            eq.next_to(stack, UP)

        mover = VGroup()
        for eq in binomial_equations:
            point = Dot(radius=0).move_to(n_choose_k.get_center())
            group = VGroup(n_choose_k.copy(), point.copy(), point.copy())
            group.target = eq
            mover.add(group)

        self.play(FadeIn(nCk_group))
        self.play(LaggedStart(
            *[MoveToTarget(m) for m in mover],
            run_time=3,
        ))
        self.remove(*mover)
        self.add(binomial_equations)
        self.wait()

        self.n_choose_k = n_choose_k
        self.n_choose_k_words = n_choose_k_words
        self.binomial_equations = binomial_equations

    def show_binomial_name(self):
        new_words = Text("``Binomial coefficients''")
        new_words.move_to(self.n_choose_k_words, LEFT)

        self.play(Transform(self.n_choose_k_words, new_words))
        self.wait(2)

    def issolate_single_stack(self):
        stack = self.stacks[3]
        equation = self.binomial_equations[3]

        to_fade = VGroup(*self.stacks)
        to_fade.add(*self.binomial_equations)
        to_fade.add(self.n_choose_k, self.n_choose_k_words)
        to_fade.remove(stack, equation)

        self.play(
            FadeOut(to_fade),
            equation.animate.scale(1.5).move_to(
                equation.get_bottom() + (equation.get_top() - equation.get_bottom())/2
            ),
        )
        self.wait()
        for line in stack:
            ones = VGroup(*[mob for mob in line if "1" in mob.tex_string])
            line.ones = ones
            self.play(LaggedStart(
                *[ones[i].animate.set_color(YELLOW) for i in range(len(ones))],
                lag_ratio=0.7,
                run_time=1
            ))
            self.play(LaggedStart(
                *[ones[i].animate.set_color(self.one_color) for i in range(len(ones))],
                lag_ratio=0.7,
                run_time=1
            ))

    def count_chosen_stack(self):
        stack = self.stacks[3]
        for i, line in enumerate(stack):
            number = MathTex(str(i+1))
            number.next_to(stack, LEFT)
            brace = Brace(VGroup(*stack[:i+1]), LEFT)
            number.next_to(brace, LEFT)
            line.save_state()
            line.set_color(YELLOW)
            self.add(number, brace)
            self.wait(0.25)
            self.remove(number, brace)
            line.restore()
        self.add(number, brace)
        self.wait()

        self.stack_brace = brace
        self.stack_count = number

    def count_ways_to_fill_slots(self):
        lines = VGroup(*[Line(ORIGIN, 0.25*RIGHT) for x in range(5)])
        lines.arrange(RIGHT)
        lines.next_to(self.stacks[3], LEFT, LARGE_BUFF, UP)

        self.play(Create(lines))
        count = 1
        for indices in itertools.combinations(list(range(5)), 3):
            ones = VGroup(*[
                self.get_obj1().next_to(lines[i], UP)
                for i in indices
            ])
            num = MathTex(str(count))
            num.next_to(lines, DOWN)
            self.add(ones, num)
            self.wait(0.35)
            self.remove(ones, num)
            count += 1
        self.add(num, ones)
        self.wait()
        self.play(*[FadeOut(mob) for mob in [lines, num, ones]])

    def walk_though_notation(self):
        equation = self.binomial_equations[3]
        rect = SurroundingRectangle(equation[0])
        rect.set_color(WHITE)
        words = Text("``5 choose 3''")
        words.next_to(rect, UP)

        self.play(Write(words))
        self.play(Create(rect))
        self.play(FadeOut(rect))
        self.wait(2)

    def emphasize_pattern_over_number(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        words = Text("Remember the pattern \\\\ not the number")
        words.next_to(morty, UP)
        words.shift_onto_screen()

        self.play(FadeIn(morty))
        self.play(
            morty.animate.change("speaking"),
            Write(words, run_time=2)
        )
        self.play(
            Blink(morty),
            morty.animate.change("happy")
        )
        last_ones = VGroup()
        last_ones.save_state()
        for x in range(2):
            for line in self.stacks[3]:
                ones = line.ones
                ones.save_state()
                self.play(
                    ones.animate.set_color(YELLOW),
                    last_ones.animate.restore(),
                    morty.animate.look_at(ones),
                    run_time=0.25
                )
                last_ones = ones
            self.wait()

    ####

    def get_obj1(self):
        return MathTex("1").set_color(self.one_color)

    def get_obj2(self):
        return MathTex("0").set_color(self.zero_color)


# Helper function (需要從原始代碼中複製或重新實現)
def get_stacks(obj1, obj2, n, vertical_buff=SMALL_BUFF):
    stacks = VGroup()
    for k in range(n+1):
        stack = VGroup()
        for i in range(k+1):
            line = VGroup()
            for j in range(n):
                if j < k:
                    line.add(obj1.copy())
                else:
                    line.add(obj2.copy())
            line.arrange(RIGHT, buff=SMALL_BUFF)
            stack.add(line)
        stack.arrange(DOWN, buff=vertical_buff)
        stacks.add(stack)
    stacks.arrange(RIGHT, buff=LARGE_BUFF)
    return stacks
