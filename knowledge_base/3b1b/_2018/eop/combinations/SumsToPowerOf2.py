# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示組合數總和等於2的n次方，透過堆疊視覺化計數並轉換為二項式係數表示，最後顯示另一種n值的總和。


from manim import *
import itertools as it

class SumsToPowerOf2(Scene):
    def __init__(self, n=5, alt_n=7, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.alt_n = alt_n

    def construct(self):
        self.setup_stacks()
        self.count_32()
        self.show_sum_as_n_choose_k()
        self.show_alternate_sum()

    def setup_stacks(self):
        # 創建堆疊視覺化
        stacks = self.get_stacks(
            MathTex("1").set_color(PINK),
            MathTex("0").set_color(BLUE),
            n=self.n,
            vertical_buff=SMALL_BUFF,
        )
        stacks.to_corner(DL)
        
        # 創建組合數數字
        numbers = VGroup(*[
            MathTex(str(self.comb(self.n, k)))
            for k in range(self.n + 1)
        ])
        for number, stack in zip(numbers, stacks):
            number.next_to(stack, UP)

        self.play(
            LaggedStartMap(FadeIn, stacks),
            LaggedStartMap(FadeIn, numbers),
        )
        self.wait()

        self.stacks = stacks
        self.numbers = numbers

    def count_32(self):
        lines = VGroup(*it.chain(*self.stacks))
        rhs = MathTex("= 2^{%d}" % self.n)
        rhs.to_edge(UP, buff=LARGE_BUFF)
        rhs.to_edge(RIGHT, buff=2)

        numbers = self.numbers.copy()
        numbers.target = VGroup(*[
            MathTex("{%d \\choose %d}" % (self.n, k))
            for k in range(self.n + 1)
        ])
        plusses = VGroup(*[MathTex("+") for _ in numbers])
        plusses.remove(plusses[-1])
        plusses.add(MathTex("="))
        
        # 創建總和表達式
        sum_group = VGroup(*it.chain(*list(zip(
            numbers.target, plusses
        ))))
        sum_group.arrange(RIGHT, buff=SMALL_BUFF)
        sum_group.next_to(numbers, UP, LARGE_BUFF)
        sum_group.shift(MED_LARGE_BUFF * RIGHT)

        # 動態計數過程
        for i, line in zip(it.count(1), lines):
            line_copy = line.copy().set_color(YELLOW)
            number = Integer(i)
            number.scale(1.5)
            number.to_edge(UP)
            VGroup(number, line_copy).set_color(YELLOW)
            self.add(line_copy, number)
            self.wait(0.15)
            self.remove(line_copy, number)
        
        sum_result = number
        self.add(sum_result)
        self.wait()

        sum_result.target = MathTex(str(2**self.n))
        sum_result.target.set_color(sum_result.get_color())
        sum_result.target.next_to(sum_group, RIGHT)
        rhs.next_to(sum_result.target, RIGHT, aligned_edge=DOWN)
        
        self.play(
            MoveToTarget(sum_result),
            MoveToTarget(numbers),
            Write(plusses),
            Write(rhs),
        )
        self.wait()

        self.plusses = plusses
        self.sum_result = sum_result
        self.rhs = rhs
        self.n_choose_k_terms = numbers

    def show_sum_as_n_choose_k(self):
        numbers = self.numbers
        plusses = self.plusses
        n_choose_k_terms = self.n_choose_k_terms
        rhs = VGroup(self.sum_result, self.rhs)
        n = self.n

        fractions = self.get_fractions(n)
        plusses.generate_target()
        sum_group = VGroup(*it.chain(*list(zip(
            fractions, plusses.target
        ))))
        sum_group.arrange(RIGHT, buff=2*SMALL_BUFF)
        sum_group.next_to(rhs, LEFT)
        sum_group.shift(0.5*SMALL_BUFF*DOWN)

        self.play(
            Transform(n_choose_k_terms, fractions),
            MoveToTarget(plusses),
            lag_ratio=0.5,
            run_time=2
        )
        self.wait()

    def show_alternate_sum(self):
        fractions = self.get_fractions(self.alt_n)
        fractions.remove(*fractions[4:-1])
        fractions.submobjects.insert(4, MathTex("\\cdots"))
        plusses = VGroup(*[
            MathTex("+") for _ in fractions[:-1]
        ] + [MathTex("=")])
        
        sum_group = VGroup(*it.chain(*list(zip(
            fractions, plusses
        ))))
        sum_group.arrange(RIGHT)
        sum_group.next_to(
            self.n_choose_k_terms, DOWN,
            aligned_edge=LEFT, buff=LARGE_BUFF
        )
        sum_group.shift(SMALL_BUFF*DOWN)
        
        rhs = MathTex(
            str(2**self.alt_n), 
            "=", "2^{%d}" % (self.alt_n)
        )
        rhs[0].set_color(YELLOW)
        rhs.next_to(sum_group, RIGHT)

        self.play(
            LaggedStartMap(FadeOut, self.stacks),
            LaggedStartMap(FadeOut, self.numbers),
            LaggedStartMap(FadeIn, sum_group),
        )
        self.play(LaggedStartMap(FadeIn, rhs))
        self.wait(2)

    # 輔助函數
    def get_fractions(self, n):
        fractions = VGroup(MathTex("1"))
        dot_str = " \\!\\cdot\\! "
        for k in range(1, n+1):
            ts = str(n)
            bs = "1"
            for i in range(1, k):
                ts += dot_str + str(n-i)
                bs += dot_str + str(i+1)
            fraction = MathTex("{%s \\over %s}" % (ts, bs))
            fractions.add(fraction)
        return fractions

    def comb(self, n, k):
        """計算組合數 C(n, k)"""
        from math import comb
        return comb(n, k)

    def get_stacks(self, top, bottom, n, vertical_buff=SMALL_BUFF):
        """創建二進制堆疊視覺化"""
        stacks = VGroup()
        for k in range(n + 1):
            stack = VGroup()
            for _ in range(k):
                stack.add(top.copy())
            for _ in range(n - k):
                stack.add(bottom.copy())
            stack.arrange(DOWN, buff=vertical_buff)
            stacks.add(stack)
        stacks.arrange(RIGHT, buff=LARGE_BUFF)
        return stacks
