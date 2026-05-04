# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示三體問題中的位置和動量向量符號，並用動畫突顯各座標分量，最後計算並顯示總自由度數量。



from manim import *
class ThreeBodySymbols(Scene):
    def construct(self):
        self.init_coord_groups()
        self.introduce_coord_groups()
        self.count_coords()

    def init_coord_groups(self):
        kwargs = {
            "bracket_v_buff": 2 * SMALL_BUFF
        }
        positions = VGroup(*[
            get_vector_symbol(*[
                "{}_{}".format(s, i)
                for s in "xyz"
            ], **kwargs)
            for i in range(1, 4)
        ])
        velocities = VGroup(*[
            get_vector_symbol(*[
                "p^{}_{}".format(s, i)
                for s in "xyz"
            ], **kwargs)
            for i in range(1, 4)
        ])
        groups = VGroup(positions, velocities)
        colors = [GREEN, RED, BLUE]
        for group in groups:
            for matrix in group:
                matrix.coords = matrix.get_entries()
                for coord, color in zip(matrix.coords, colors):
                    coord.set_color(color)
            group.arrange(RIGHT)
        groups.arrange(DOWN, buff=LARGE_BUFF)
        groups.to_edge(LEFT)

        self.coord_groups = groups

    def introduce_coord_groups(self):
        groups = self.coord_groups
        x_group, p_group = groups
        x_word = Text("Positions")
        p_word = Text("Momenta")
        words = VGroup(x_word, p_word)
        for word, group in zip(words, groups):
            word.next_to(group, UP)

        rect_groups = VGroup()
        for group in groups:
            rect_group = VGroup(*[
                SurroundingRectangle(
                    VGroup(*[
                        tm.coords[i]
                        for tm in group
                    ]),
                    color=WHITE,
                    stroke_width=2,
                )
                for i in range(3)
            ])
            rect_groups.add(rect_group)

        self.play(
            *[
                LaggedStartMap(
                    FadeIn, group,
                    lambda m: (m, UP),
                    run_time=1,
                )
                for group in groups
            ],
            *[FadeIn(word, shift=DOWN) for word in words],
        )
        for rect_group in rect_groups:
            self.play(
                Create(rect_group),
                run_time=0.5
            )
            self.play(
                FadeOut(rect_group),
                run_time=0.5
            )
        self.wait()

    def count_coords(self):
        coord_copies = VGroup()
        for group in self.coord_groups:
            for tex_mob in group:
                for coord in tex_mob.coords:
                    coord_copy = coord.copy()
                    coord_copy.set_stroke(
                        WHITE, 2, background=True
                    )
                    coord_copies.add(coord_copy)

        count = Integer()
        count_word = MathTex("18", "degrees \\\\ of freedom")[1]
        count_group = VGroup(count, count_word)
        count_group.arrange(
            RIGHT,
            aligned_edge=DOWN,
        )
        count_group.scale(1.5)
        count_group.next_to(
            self.coord_groups, RIGHT,
            aligned_edge=DOWN,
        )
        count.add_updater(
            lambda m: m.set_value(len(coord_copies))
        )
        count.add_updater(
            lambda m: m.next_to(count_word[0][0], LEFT, aligned_edge=DOWN)
        )

        self.add(count_group)
        self.play(
            ShowIncreasingSubsets(coord_copies),
            run_time=1.5,
            rate_func=linear,
        )
        self.play(FadeOut(coord_copies))
