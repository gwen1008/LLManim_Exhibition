# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個 10x10 的數字矩陣，先高亮顯示其中的質數，然後淡出矩陣並顯示 22/7 和 355/113 對圓周率 π 的有理數逼近公式。



from manim import *
class PrimesAndPi(Scene):
    def construct(self):
        self.show_primes()
        self.show_rational_approximations()

    def show_primes(self):
        n_rows = 10
        n_cols = 10
        matrix = IntegerMatrix([
            [n_cols * x + y for y in range(n_cols)]
            for x in range(n_rows)
        ])
        numbers = matrix.get_entries()
        primes = VGroup(*filter(
            lambda m: is_prime(m.get_value()),
            numbers,
        ))
        non_primes = VGroup(*filter(
            lambda m: not is_prime(m.get_value()),
            numbers
        ))

        self.add(numbers)

        self.play(
            LaggedStart(*[
                ApplyFunction(
                    lambda m: m.set_color(TEAL).scale(1.2),
                    prime
                )
                for prime in primes
            ]),
            non_primes.animate.set_opacity(0.25),
            run_time=2,
        )
        self.wait()

        self.numbers = numbers

    def show_rational_approximations(self):
        numbers = self.numbers

        approxs = MathTex(
            "{22 \\over 7} &=", "{:.12}\\dots\\\\".format(22 / 7),
            "{355 \\over 113} &=", "{:.12}\\dots\\\\".format(355 / 113),
            "\\pi &=", "{:.12}\\dots\\\\".format(PI),
        )
        approxs[:2].shift(MED_LARGE_BUFF * UP)
        approxs[-2:].shift(MED_LARGE_BUFF * DOWN)
        approxs[-2:].set_color(YELLOW)
        approxs[1][:4].set_color(YELLOW)
        approxs[3][:8].set_color(YELLOW)
        approxs.scale(1.5)

        randy = Randolph(color=YELLOW, height=1)
        randy.move_to(approxs[-2][0], RIGHT)
        approxs[-2][0].set_opacity(0)

        self.play(
            LaggedStartMap(FadeOutAndShiftDown, numbers),
            LaggedStartMap(FadeIn, approxs),
            FadeIn(randy)
        )
        self.play(Blink(randy))
        self.play(randy.change, "pondering", UR)
        self.wait()
