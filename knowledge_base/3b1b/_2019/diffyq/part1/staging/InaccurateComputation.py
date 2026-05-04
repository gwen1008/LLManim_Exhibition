# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示實數、IEEE 754 表示法和誤差之間的對應關係，並以 π 和 e^(√163 π) 為例說明數值表示誤差。



from manim import *
class InaccurateComputation(Scene):
    def construct(self):
        h_line = DashedLine(LEFT_SIDE, RIGHT_SIDE)
        h_line.to_edge(UP, buff=1.5)
        words = VGroup(
            Text("Real number"),
            Text("IEEE 754\nrepresentation"),
            Text("Error"),
        )
        for i, word in zip([-1, 0, 1], words):
            word.next_to(h_line, UP)
            word.shift(i * FRAME_WIDTH * RIGHT / 3)

        lines = VGroup(*[
            DashedLine(TOP, BOTTOM)
            for x in range(4)
        ])
        lines.arrange(RIGHT)
        lines.stretch_to_fit_width(FRAME_WIDTH)

        self.add(h_line, lines[1:-1], words)

        numbers = VGroup(
            MathTex("\\pi").scale(2),
            MathTex("e^{\\sqrt{163}\\pi}").scale(1.5),
        )
        numbers.set_color(YELLOW)
        numbers.set_stroke(width=0, background=True)

        bit_strings = VGroup(
            MathTex(
                "01000000",
                "01001001",
                "00001111",
                "11011011",
            ),
            MathTex(
                "01011100",
                "01101001",
                "00101110",
                "00011001",
            )
        )
        for mob in bit_strings:
            mob.arrange(DOWN, buff=SMALL_BUFF)
            for word in mob:
                for submob, bit in zip(word, word.tex_string):
                    if bit == "0":
                        submob.set_color(GREY_B)
        errors = VGroup(
            MathTex(
                "\\approx 8.7422 \\times 10^{-8}"
            ),
            MathTex(
                "\\approx 5{,}289{,}803{,}032.00",
            ),
        )
        errors.set_color(RED)

        content = VGroup(numbers, bit_strings, errors)

        for group, word in zip(content, words):
            group[1].shift(3 * DOWN)
            group.move_to(DOWN)
            group.match_x(word)

        self.play(*[Write(num) for num in numbers])
        self.wait()
        self.play(
            TransformFromCopy(numbers, bit_strings),
            lag_ratio=0.01,
            run_time=2,
        )
        self.wait()
        self.play(FadeIn(errors, shift=3 * LEFT))
        self.wait()
