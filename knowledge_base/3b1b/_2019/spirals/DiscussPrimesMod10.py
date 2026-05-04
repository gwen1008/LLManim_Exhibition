# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示數字模10的餘數分類，並突顯質數在特定餘數類中的分佈。


from manim import *
import itertools as it
import operator as op
from functools import reduce

def read_in_primes(limit):
    # 假設的質數讀取函數，實際使用時需替換為真正的質數列表
    # 這裡返回一個小於等於limit的質數列表作為示例
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

class DiscussPrimesMod10(Scene):
    def construct(self):
        labels = VGroup(*[
            Text(f"{n} mod 10:", font_size=36)
            for n in range(10)
        ])
        labels.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        labels.to_edge(LEFT)
        # digits = VGroup(*[l[0] for l in labels])
        labels.set_color_by_gradient(YELLOW, BLUE)

        sequences = VGroup(*[
            VGroup(*[
                Integer(n).shift((n // 10) * RIGHT)
                for n in range(r, 100 + r, 10)
            ])
            for r in range(10)
        ])
        for sequence, label in zip(sequences, labels):
            sequence.next_to(label, RIGHT, buff=MED_LARGE_BUFF)
            for item in sequence:
                if item is sequence[-1]:
                    punc = MathTex("\\dots")
                else:
                    punc = Text(",", font_size=36)
                punc.next_to(item.get_corner(DR), RIGHT, buff=SMALL_BUFF)
                item.add(punc)

        # Introduce everything
        self.play(LaggedStart(*[
            FadeIn(label, shift=UP)
            for label in labels
        ]))
        self.wait()
        self.play(
            LaggedStart(*[
                LaggedStart(*[
                    FadeIn(item, shift=LEFT)
                    for item in sequence
                ])
                for sequence in sequences
            ])
        )
        self.wait()

        # Highlight 0's then 1's
        for sequence in sequences[:2]:
            lds = VGroup(*[item[-2] for item in sequence])
            rects = VGroup(*[
                SurroundingRectangle(ld, buff=0.05)
                for ld in lds
            ])
            rects.set_color(YELLOW)
            self.play(
                LaggedStartMap(
                    Create, rects,
                    lag_ratio=0.2
                )
            )
            self.play(FadeOut(rects))
            self.wait()

        # Eliminate certain residues
        two = sequences[2][0]
        five = sequences[5][0]
        evens = VGroup(*it.chain(*sequences[::2]))
        evens.remove(two)
        div5 = sequences[5][1:]
        prime_numbers = read_in_primes(100)

        primes = VGroup(*[
            item
            for seq in sequences
            for item in seq
            if int(item.get_value()) in prime_numbers
        ])
        non_primes = VGroup(*[
            item
            for seq in sequences
            for item in seq
            if reduce(op.and_, [
                int(item.get_value()) not in prime_numbers,
                item.get_value() % 2 != 0,
                item.get_value() % 5 != 0,
            ])
        ])

        for prime, group in [(two, evens), (five, div5)]:
            self.play(Create(SurroundingRectangle(prime)))
            self.play(FadeOut(SurroundingRectangle(prime)))
            self.play(LaggedStart(*[
                item.animate.set_opacity(0.2)
                for item in group
            ]))
            self.wait()

        # Highlight primes
        self.play(
            LaggedStart(*[
                prime.animate.scale(1.2).set_color(TEAL)
                for prime in primes
            ]),
            LaggedStart(*[
                non_prime.animate.scale(0.8).set_opacity(0.8)
                for non_prime in non_primes
            ]),
        )
        self.wait()

        # Highlight coprime residue classes
        rects = VGroup(*[
            SurroundingRectangle(VGroup(labels[r], sequences[r]))
            for r in [1, 3, 7, 9]
        ])
        for rect in rects:
            rect.reverse_points()

        fade_rect = FullScreenFadeRectangle()
        fade_rect.scale(1.1)
        new_fade_rect = fade_rect.copy()
        fade_rect.append_vectorized_mobject(rects[0])
        for rect in rects:
            new_fade_rect.append_vectorized_mobject(rect)

        self.play(Create(fade_rect))
        self.wait()
        self.play(
            FadeOut(fade_rect),
            FadeIn(new_fade_rect),
        )
        self.wait()
