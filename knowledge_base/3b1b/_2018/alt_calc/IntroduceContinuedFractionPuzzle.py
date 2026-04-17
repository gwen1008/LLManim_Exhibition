# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個連分數謎題，並透過角色對話和動畫逐步解釋其數學意義，最終導出固定點的概念。



from manim import *
class IntroduceContinuedFractionPuzzle(PiCreatureScene):
    def __init__(self, remove_initial_rhs=True, **kwargs):
        super().__init__(**kwargs)
        self.remove_initial_rhs = remove_initial_rhs

    def construct(self):
        self.ask_question()
        self.set_equal_to_x()

    def create_pi_creatures(self):
        morty = Mortimer(height=2)
        morty.to_corner(DR)

        friend = PiCreature(color=GREEN, height=2)
        friend.to_edge(DOWN)
        friend.shift(LEFT)

        group = VGroup(morty, friend)
        group.shift(2 * LEFT)

        return morty, friend

    def ask_question(self):
        morty, friend = self.pi_creatures
        frac = get_phi_continued_fraction(9)
        frac.scale(0.8)
        rhs = DecimalNumber(
            (1 - np.sqrt(5)) / 2.0,
            num_decimal_places=5,
            show_ellipsis=True,
        )
        rhs.set_color(YELLOW)
        equals = MathTex("=")
        equals.next_to(frac.get_part_by_tex("\\over"), RIGHT)
        rhs.next_to(equals, RIGHT)
        group = VGroup(frac, equals, rhs)
        group.scale(1.5)
        group.to_corner(UR)

        self.play(
            LaggedStartMap(
                Write, frac,
                run_time=15,
                lag_ratio=0.15,
            ),
            FadeIn(equals, shift=DOWN),
            FadeIn(rhs, shift=DOWN),
            PiCreatureSays(
                friend, "Would this be valid? \\\\ If not, why not?",
                target_mode="confused",
                look_at=frac,
                bubble_config={
                    "direction": RIGHT,
                    "width": 4,
                    "height": 3,
                }
            ),
            morty.animate.change("pondering"),
        )
        self.wait()

        anims = [
            RemovePiCreatureBubble(
                friend, target_mode="pondering",
                look_at=frac
            ),
        ]
        if self.remove_initial_rhs:
            anims += [
                Animation(frac),
                FadeOut(equals),
                rhs.animate.scale(0.5).to_corner(DL),
            ]
        self.play(*anims)

        self.neg_one_over_phi = rhs
        self.equals = equals
        self.frac = frac

    def set_equal_to_x(self):
        frac = self.frac
        morty, friend = self.pi_creatures

        inner_frac = frac[4:]
        inner_frac_rect = SurroundingRectangle(
            inner_frac, stroke_width=2, buff=0.5 * SMALL_BUFF
        )
        inner_frac_group = VGroup(inner_frac, inner_frac_rect)

        equals = MathTex("=")
        equals.next_to(frac[3], RIGHT)
        x, new_x = [MathTex("x") for i in range(2)]
        xs = VGroup(x, new_x)
        xs.set_color(YELLOW)
        xs.scale(1.3)
        x.next_to(equals, RIGHT)
        new_x.next_to(frac[3], DOWN, 2 * SMALL_BUFF)

        fixed_point_words = VGroup(
            Text("Fixed point of"),
            MathTex(
                "f(x) = 1 + \\frac{1}{x}",
                tex_to_color_map={"x": YELLOW}
            )
        )
        fixed_point_words.arrange(DOWN)

        self.play(Write(x), Write(equals))
        self.wait()
        self.play(Create(inner_frac_rect))
        self.wait()
        self.play(
            inner_frac_group.animate.scale(0.75).center().to_edge(LEFT),
            ReplacementTransform(
                x.copy(), new_x,
                path_arc=-90 * DEGREES
            )
        )
        self.wait()
        self.play(
            frac[3].animate.stretch(0.1, 0, about_edge=RIGHT),
            MaintainPositionRelativeTo(
                VGroup(frac[2], new_x), frac[3]
            ),
            UpdateFromFunc(
                frac[:2], lambda m: m.next_to(frac[3], LEFT)
            )
        )
        self.wait()
        fixed_point_words.next_to(VGroup(frac[0], xs), DOWN, LARGE_BUFF)
        self.play(
            Write(fixed_point_words),
            morty.animate.change("hooray"),
            friend.animate.change("happy")
        )
        self.wait(3)
