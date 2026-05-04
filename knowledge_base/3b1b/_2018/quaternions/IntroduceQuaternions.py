# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數的介紹，比較三種數字系統，顯示四個垂直軸，並分解四元數的實部和虛部。



from manim import *
class IntroduceQuaternions(Scene):
    def construct(self):
        self.compare_three_number_systems()
        self.mention_four_perpendicular_axes()
        self.bring_back_complex()
        self.show_components_of_quaternion()

    def compare_three_number_systems(self):
        numbers = self.get_example_numbers()
        labels = VGroup(
            Text("Complex number"),
            Text("Not-actually-a-number-system 3d number"),
            Text("Quaternion"),
        )

        for number, label in zip(numbers, labels):
            label.next_to(number, UP, aligned_edge=LEFT)

            self.play(
                FadeIn(number, shift=DOWN),
                Write(label),
            )
            self.play(CreateThenFadeAround(
                number[2:],
                surrounding_rectangle_config={"color": BLUE}
            ))
            self.wait()

        shift_size = config.frame_height / 2 - labels[2].get_top()[1] - 0.8
        self.play(
            numbers.animate.shift(shift_size * UP),
            labels.animate.shift(shift_size * UP),
        )

        self.numbers = numbers
        self.labels = labels

    def mention_four_perpendicular_axes(self):
        number = self.numbers[2]
        three_axes = VGroup(*[
            self.get_simple_axes(label, color)
            for label, color in zip(
                ["i", "j", "k"],
                [GREEN, RED, BLUE],
            )
        ])
        three_axes.arrange(RIGHT, buff=LARGE_BUFF)
        three_axes.next_to(number, DOWN, LARGE_BUFF)

        self.play(LaggedStart(*[
            FadeIn(ax, scale=2) for ax in three_axes
        ]))
        self.wait(2)

        self.three_axes = three_axes

    def bring_back_complex(self):
        numbers = self.numbers
        labels = self.labels
        numbers[0].move_to(numbers[1], LEFT)
        labels[0].move_to(labels[1], LEFT)
        numbers.remove(numbers[1])
        labels.remove(labels[1])

        group = VGroup(numbers, labels)
        self.play(
            group.animate.to_edge(UP),
            FadeOut(self.three_axes, shift=DOWN)
        )
        self.wait()

    def show_components_of_quaternion(self):
        quat = self.numbers[-1]
        real_part = quat[0]
        imag_part = quat[2:]
        real_brace = Brace(real_part, DOWN)
        imag_brace = Brace(imag_part, DOWN)
        real_word = Text("Real\npart")
        imag_word = Text("Imaginary\npart")
        scalar_word = Text("Scalar\npart")
        vector_word = Text("``Vector''\npart")
        for word in real_word, scalar_word:
            word.next_to(real_brace, DOWN, SMALL_BUFF)
        for word in imag_word, vector_word:
            word.next_to(imag_brace, DOWN, SMALL_BUFF)
        braces = VGroup(real_brace, imag_brace)
        VGroup(scalar_word, vector_word).set_color(YELLOW)

        self.play(
            LaggedStart(*[GrowFromCenter(brace) for brace in braces]),
            LaggedStart(*[
                FadeIn(word, shift=UP) for word in [real_word, imag_word]
            ])
        )
        self.wait()
        self.play(
            FadeOut(real_word, shift=DOWN),
            FadeIn(scalar_word, shift=DOWN),
        )
        self.wait(2)
        self.play(real_part.animate.set_value(0))
        self.wait()
        self.play(
            FadeOut(imag_word, shift=DOWN),
            FadeIn(vector_word, shift=DOWN)
        )
        self.wait(2)

    def get_example_numbers(self):
        number_2d = VGroup(
            DecimalNumber(3.14),
            MathTex("+"),
            DecimalNumber(1.59),
            MathTex("i")
        )
        number_3d = VGroup(
            DecimalNumber(2.65),
            MathTex("+"),
            DecimalNumber(3.58),
            MathTex("i"),
            MathTex("+"),
            DecimalNumber(9.79),
            MathTex("j"),
        )
        number_4d = VGroup(
            DecimalNumber(3.23),
            MathTex("+"),
            DecimalNumber(8.46),
            MathTex("i"),
            MathTex("+"),
            DecimalNumber(2.64),
            MathTex("j"),
            MathTex("+"),
            DecimalNumber(3.38),
            MathTex("k"),
        )
        numbers = VGroup(number_2d, number_3d, number_4d)
        for number in numbers:
            number.arrange(RIGHT, buff=SMALL_BUFF)
            for part in number:
                if isinstance(part, MathTex):
                    if part.get_tex_string() == "j":
                        part.shift(0.5 * SMALL_BUFF * DL)
            number[2].set_color(GREEN)
            if len(number) > 5:
                number[5].set_color(RED)
            if len(number) > 8:
                number[8].set_color(BLUE)
        numbers.arrange(
            DOWN, buff=2, aligned_edge=LEFT
        )
        numbers.center()
        numbers.shift(LEFT)
        return numbers

    def get_simple_axes(self, label, color):
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
        )
        axes.set_height(2.5)
        label_mob = MathTex(label)
        label_mob.set_color(color)
        label_mob.next_to(axes.c2p(0, 1.5), RIGHT, SMALL_BUFF)
        reals_label_mob = Text("Reals")
        reals_label_mob.next_to(
            axes.c2p(1, 0), DR, SMALL_BUFF
        )
        axes.add(label_mob, reals_label_mob)
        return axes
