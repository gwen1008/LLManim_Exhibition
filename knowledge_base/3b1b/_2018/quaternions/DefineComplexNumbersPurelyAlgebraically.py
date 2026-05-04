# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示複數的純代數定義，透過分配律展開乘法，並強調結果仍保持相同形式。



from manim import *
class DefineComplexNumbersPurelyAlgebraically(Scene):
    def construct(self):
        self.add_linus()
        self.add_title()
        self.show_example_number()
        self.show_multiplication()
        self.emphsize_result_has_same_form()

    def add_linus(self):
        linus = self.linus = Linus()
        linus.move_to(3 * LEFT)

    def add_title(self):
        title = self.title = Title(
            "No spatial reasoning, just symbols"
        )
        self.play(
            FadeIn(title[:-1], shift=DOWN),
            Create(title[-1]),
            self.linus.look_at, title
        )

    def show_example_number(self):
        linus = self.linus

        number = MathTex("2.35", "+", "3.14", "i")
        number.next_to(self.title, DOWN, buff=1.5)
        number.shift(3 * RIGHT)
        real, imag = number[0], number[2]
        real_brace = Brace(real, UP)
        imag_brace = Brace(imag, DOWN)
        real_label = real_brace.get_text("Some real number")
        imag_label = imag_brace.get_text("Some other real number")
        VGroup(real, real_label).set_color(GREEN)
        VGroup(imag, imag_label).set_color(RED)

        i = number[-1]
        i_def = MathTex("i", "^2", "=", "-1")
        i_def.next_to(
            self.title, DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        i_def_rect = SurroundingRectangle(i_def, color=YELLOW, buff=MED_SMALL_BUFF)
        definition_label = Text("Definition")
        definition_label.next_to(i_def_rect, DOWN)
        definition_label.set_color(i_def_rect.get_color())

        self.play(Write(number, run_time=1))
        self.play(
            GrowFromCenter(real_brace),
            LaggedStartMap(FadeIn, real_label),
            linus.change, "confused", number,
            run_time=1
        )
        self.wait()
        self.play(
            GrowFromCenter(imag_brace),
            LaggedStartMap(FadeIn, imag_label),
            run_time=1
        )
        self.play(Blink(linus))
        self.play(
            linus.change, "erm", i_def,
            ReplacementTransform(
                i.copy(), i_def[0],
                path_arc=-30 * DEGREES
            ),
            FadeIn(i_def_rect),
            FadeIn(definition_label),
        )
        self.play(Write(i_def[1:]))
        self.wait()
        self.play(Blink(linus))

        self.to_fade = VGroup(
            real_brace, real_label,
            imag_brace, imag_label,
        )
        self.number = number

    def show_multiplication(self):
        linus = self.linus
        to_fade = self.to_fade
        z1 = self.number

        z2 = MathTex("4", "+", "5", "i")
        z2.set_color_by_tex_to_color_map(z1.get_color_map())

        for z in z1, z2:
            lp, rp = z.parens = MathTex("(", ")")
            lp.next_to(z, LEFT, SMALL_BUFF)
            rp.next_to(z, RIGHT, SMALL_BUFF)
            z.real = z[0]
            z.imag = z[2:]
            for part in z.real, z.imag:
                part.targets = [part.copy(), part.copy()]

        z1.generate_target()
        product = VGroup(
            VGroup(z1.target, z1.parens),
            VGroup(z2, z2.parens),
        )
        product.arrange(RIGHT, buff=SMALL_BUFF)
        product.move_to(2 * RIGHT + 2 * UP)

        foil = VGroup(*[Text(word) for word in [
            "First", "Outside", "Inside", "Last",
        ]])
        foil.arrange(
            DOWN, buff=MED_SMALL_BUFF,
            aligned_edge=LEFT
        )
        foil.scale(1.25)
        for word in foil:
            word[0].set_color(BLUE)
        foil.move_to(product).to_edge(DOWN, buff=LARGE_BUFF)

        def get_cdot():
            return MathTex("\\cdot")

        def get_lp():
            return MathTex("(")

        def get_rp():
            return MathTex(")")

        def get_plus():
            return MathTex("+")

        expansion = VGroup(
            z1.real.targets[0], get_cdot(), z2.real.targets[0], get_plus(),
            z1.real.targets[1], get_cdot(), z2.imag.targets[0], get_plus(),
            z1.imag.targets[0], get_cdot(), z2.real.targets[1], get_plus(),
            z1.imag.targets[1], get_cdot(), z2.imag.targets[1],
        )
        expansion.arrange(RIGHT, buff=0.15)
        expansion.next_to(product, DOWN, buff=LARGE_BUFF)
        expansion_parts = VGroup(*[
            expansion[4 * i: 4 * i + 3]
            for i in range(4)
        ])
        expansion_part_braces = VGroup(*[
            Brace(part, DOWN) for part in expansion_parts
        ])
        for word, brace in zip(foil, expansion_part_braces):
            word.next_to(brace, DOWN)

        final_product = VGroup(
            get_lp(),
            z1[0].copy(), get_cdot(), z2[0].copy(),
            MathTex("-"),
            z1[2].copy(), get_cdot(), z2[2].copy(),
            get_rp(), get_plus(),
            get_lp(),
            z1[0].copy(), get_cdot(), z2[2].copy(),
            get_plus(),
            z1[2].copy(), get_cdot(), z2[0].copy(),
            get_rp(), MathTex("i")
        )
        final_product.arrange(RIGHT, buff=0.15)
        final_product.next_to(expansion, DOWN, buff=2)
        final_arrows = VGroup()
        for i, brace in zip([1, 11, 15, 5], expansion_part_braces):
            target = final_product[i:i + 3]
            if i == 5:
                arrow = Line(
                    brace.get_bottom() + SMALL_BUFF * DOWN,
                    target.get_top() + MED_SMALL_BUFF * UP,
                )
                arrow.get_points()[1] = arrow.get_points()[0] + DOWN
                arrow.get_points()[2] = arrow.get_points()[3] + UP
                tip = RegularPolygon(3, start_angle=-100 * DEGREES)
                tip.set_height(0.2)
                tip.set_stroke(width=0)
                tip.set_fill(WHITE, opacity=1)
                tip.move_to(arrow.get_end())
                arrow.add(tip)
            else:
                arrow = Arrow(
                    brace.get_bottom(),
                    target.get_top(),
                )
            final_arrows.add(arrow)
        final_arrows.set_stroke(BLACK, width=6, background=True)

        # Move example number into product
        self.play(
            FadeOut(to_fade),
            MoveToTarget(z1),
            FadeIn(z1.parens),
            FadeIn(z2, shift=DOWN),
            FadeIn(z2.parens),
            linus.change, "happy", product,
        )
        self.wait()

        # Show distribution
        import itertools
        pairs = list(itertools.product([z1.real, z1.imag], [z2.real, z2.imag]))
        for i in range(4):
            left, right = pair = VGroup(*pairs[i])
            word = foil[i]
            dot = expansion[4 * i + 1]
            plus = expansion[4 * i + 3] if i < 3 else VMobject()
            brace = expansion_part_braces[i]

            self.play(pair.animate.shift(0.5 * DOWN))
            self.play(
                FadeIn(dot),
                GrowFromCenter(brace),
                FadeIn(word, shift=DOWN),
                linus.animate.move_to(4 * LEFT + DOWN),
                *[
                    ReplacementTransform(
                        part.copy(),
                        part.targets.pop(0)
                    )
                    for part in pair
                ]
            )
            self.play(
                pair.animate.shift(0.5 * UP),
                FadeIn(plus)
            )
        self.play(Blink(linus))

        self.play(
            FadeOut(foil),
            FadeIn(final_product, shift=DOWN),
            linus.look_at, final_product,
        )
        self.play(
            LaggedStartMap(Create, final_arrows),
            run_time=3,
        )
        self.play(linus.change, "confused")
        self.wait()

        self.final_product = final_product

    def emphsize_result_has_same_form(self):
        final_product = self.final_product
        real = final_product[1:1 + 7]
        imag = final_product[11:11 + 7]

        real_brace = Brace(real, DOWN)
        real_label = real_brace.get_text("Some real number")
        real_label.set_color(GREEN)
        imag_brace = Brace(imag, DOWN)
        imag_label = imag_brace.get_text(
            "Some other \\\\ real number"
        )
        imag_label.set_color(RED)
        braces = VGroup(real_brace, imag_brace)
        labels = VGroup(real_label, imag_label)
        self.play(
            LaggedStartMap(GrowFromCenter, braces),
            LaggedStartMap(Write, labels),
        )
        self.wait()
