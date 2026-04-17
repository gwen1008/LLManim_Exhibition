# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示圓周率前20位數字與超大質量黑洞質量的比較，並將數字轉換為逗號分隔的格式。



from manim import *
class CompareToGalacticMass(Scene):
    def construct(self):
        self.add_digits_of_pi()
        self.show_mass()
        self.show_galactic_black_holes()
        self.show_total_count()

    def add_digits_of_pi(self):
        # 20 digits of pi
        digits = MathTex("3.1415926535897932384...")
        digits.set_width(FRAME_WIDTH - 3)
        digits.to_edge(UP)

        highlighted_digits = VGroup(*[
            d.copy().set_stroke(color=BLUE, width=5, background=True)
            for d in [digits[0], *digits[2:-3]]
        ])
        counter = Integer(0)
        counter.scale(1.5)
        counter.set_color(BLUE)
        brace = VMobject()
        self.add(counter, brace)

        for k in range(len(highlighted_digits)):
            if k == 0:
                self.add(digits[0])
            else:
                self.remove(highlighted_digits[k - 1])
            self.add(digits[k + 1])
            self.add(highlighted_digits[k])
            counter.increment_value()
            brace.become(Brace(highlighted_digits[:k + 1], DOWN))
            counter.next_to(brace, DOWN)
            self.wait(0.1)
        self.add(digits)
        self.remove(*highlighted_digits)

        digits_word = Text("digits")
        digits_word.scale(1.5)
        digits_word.set_color(counter.get_color())
        counter.generate_target()
        group = VGroup(counter.target, digits_word)
        group.arrange(
            RIGHT,
            index_of_submobject_to_align=0,
            aligned_edge=DOWN,
            buff=0.7,
        )
        group.next_to(brace, DOWN)
        self.play(
            MoveToTarget(counter),
            FadeIn(digits_word, shift=LEFT),
        )
        self.wait()

        self.pi_digits_group = VGroup(
            digits, brace, counter, digits_word
        )

    def show_mass(self):
        # 注意：BlocksAndWallExample 需要自行定義或替換
        # 這裡保留原結構，但實際運行時需要調整
        bw_scene = BlocksAndWallExample(
            write_to_movie=False,
            skip_animations=True,
            count_clacks=False,
            show_flash_animations=False,
            floor_y=0,
            wall_x=-2,
            n_wall_ticks=8,
            sliding_blocks_config={
                "block1_config": {
                    "mass": 1e6,
                    "velocity": -0.01,
                    "distance": 4.5,
                    "label_text": "$100^{(20 - 1)}$ kg",
                    "fill_color": BLACK,
                },
                "block2_config": {
                    "distance": 1,
                    "velocity": 0,
                },
            }
        )
        block1 = bw_scene.blocks.block1
        block2 = bw_scene.blocks.block2
        group = VGroup(
            bw_scene.wall, bw_scene.floor,
            block1, block2
        )
        group.center()
        group.to_edge(DOWN)

        arrow = Arrow(start=ORIGIN, end=2 * LEFT, color=RED)
        arrow.shift(block1.get_center())
        group.add(arrow)

        brace = Brace(block1.label[:-2], UP, buff=SMALL_BUFF)
        number_words = Text(
            "100", *["billion"] * 4,
        )
        number_words.next_to(brace, UP, buff=SMALL_BUFF)
        VGroup(brace, number_words).set_color(YELLOW)

        self.play(Write(group))
        self.wait()
        last_word = number_words[0].copy()
        last_word.next_to(brace, UP, SMALL_BUFF)
        self.play(
            GrowFromCenter(brace),
            FadeIn(last_word, shift=DOWN),
        )
        for k in range(1, len(number_words) + 1):
            self.remove(last_word)
            last_word = number_words[:k].copy()
            last_word.next_to(brace, UP, SMALL_BUFF)
            self.add(last_word)
            self.wait(0.4)
        self.wait()
        self.remove(last_word)
        self.add(number_words)
        group.add(brace, number_words)
        self.play(group.animate.to_corner(DL))

        self.block1 = block1
        self.block2 = block2
        self.block_setup_group = group

    def show_galactic_black_holes(self):
        # 注意：SVGMobject 需要替換為 SVGMobject 或 ImageMobject
        # 這裡使用 Circle 作為替代
        black_hole = Circle(radius=0.5, color=BLACK, fill_opacity=1)
        black_hole.set_sheen(0.2, UL)
        black_hole.set_height(1)
        black_holes = VGroup(*[
            black_hole.copy() for k in range(10)
        ])
        black_holes.arrange_in_grid(5, 2)
        black_holes.to_corner(DR)
        import random
        random.shuffle(black_holes.submobjects)
        for bh in black_holes:
            bh.save_state()
            bh.scale(3)
            bh.set_fill(GREY_D, 0)

        equals = MathTex("=")
        equals.scale(2)
        equals.next_to(self.block1, RIGHT)

        words = Text("10x Sgr A$^*$ \\\\ supermassive \\\\ black hole")
        words.next_to(equals, RIGHT)
        self.add(words)

        self.play(
            Write(equals),
            Write(words),
            LaggedStartMap(
                Restore, black_holes,
                run_time=3
            )
        )
        self.wait()

        self.black_hole_words = VGroup(equals, words)
        self.black_holes = black_holes

    def show_total_count(self):
        digits = self.pi_digits_group[0]
        to_fade = self.pi_digits_group[1:]
        tex_string = "{:,}".format(31415926535897932384)
        number = MathTex(tex_string)
        number.scale(1.5)
        number.to_edge(UP)

        commas = VGroup(*[
            mob
            for c, mob in zip(tex_string, number)
            if c == ","
        ])
        dots = VGroup(*[
            mob
            for c, mob in zip(digits.tex_string, digits)
            if c == "."
        ])

        self.play(FadeOut(to_fade))
        self.play(
            ReplacementTransform(
                VGroup(*[m for m in digits if m not in dots]),
                VGroup(*[m for m in number if m not in commas]),
            ),
            ReplacementTransform(
                dots, commas,
                lag_ratio=0.5,
                run_time=2
            )
        )

        group0 = number[:2].copy()
        group1 = number[3:3 + 9 + 2].copy()
        group2 = number[-(9 + 2):].copy()
        for group in group0, group1, group2:
            group.set_stroke(color=BLUE, width=5, background=True)
            self.add(group)
            self.wait(0.5)
            self.remove(group)
