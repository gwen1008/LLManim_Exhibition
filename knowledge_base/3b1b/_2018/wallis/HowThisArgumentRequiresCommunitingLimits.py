# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示兩個角色討論極限交換的數學論證，包含分數乘積的極限與極限交換規則的視覺化。



from manim import *
class HowThisArgumentRequiresCommunitingLimits(PiCreatureScene):
    def construct(self):
        mathy, morty = self.pi_creatures

        scale_val = 0.7
        factors = MathTex(
            "{|L_1 - K|", "\\over", "|L_1 - S|}", "\\cdot",
            "{|L_{-1} - K|", "\\over", "|L_{-1} - S|}", "\\cdot",
            "{|L_2 - K|", "\\over", "|L_2 - S|}", "\\cdot",
            "{|L_{-2} - K|", "\\over", "|L_{-2} - S|}", "\\cdot",
            "{|L_3 - K|", "\\over", "|L_3 - S|}", "\\cdot",
            "{|L_{-3} - K|", "\\over", "|L_{-3} - S|}", "\\cdots",
        )
        factors.set_color_by_tex_to_color_map({
            "K": BLUE,
            "S": YELLOW,
        })
        equals = MathTex("=")
        result = MathTex(
            "{N", "{\\text{distance} \\choose \\text{between obs.}}",
            "\\over", "2}"
        )

        top_line = VGroup(factors, equals, result)
        top_line.arrange(RIGHT, buff=SMALL_BUFF)
        result.shift(SMALL_BUFF * UP)
        top_line.scale(scale_val)
        top_line.to_edge(UP)

        fractions = VGroup(*[
            factors[i:i + 3]
            for i in range(0, len(factors), 4)
        ])
        fraction_limit_arrows = VGroup(*[
            Arrow(start=UP, end=DOWN, buff=0.1).scale(0.5).next_to(fraction, DOWN)
            for fraction in fractions
        ])
        fraction_limit_arrows.set_color(WHITE)

        # 假設 get_wallis_product 函數已定義
        wallis_product = get_wallis_product(6)
        fraction_limits = VGroup(*[
            wallis_product[i:i + 3]
            for i in range(0, 4 * 6, 4)
        ])
        for lf, arrow in zip(fraction_limits, fraction_limit_arrows):
            lf.next_to(arrow, DOWN, buff=MED_SMALL_BUFF)

        result_limit_arrow = fraction_limit_arrows[0].copy()
        result_limit_arrow.next_to(result, DOWN)
        result_limit_arrow.align_to(fraction_limit_arrows[0])

        result_limit = wallis_product[-3:]
        result_limit.next_to(result_limit_arrow, DOWN, buff=MED_SMALL_BUFF)

        lower_equals = MathTex("=")
        lower_equals.next_to(result_limit, LEFT)

        mult_signs = VGroup()
        for f1, f2 in zip(fraction_limits, fraction_limits[1:]):
            mult_sign = MathTex("\\times")
            mult_sign.move_to(VGroup(f1, f2))
            mult_signs.add(mult_sign)
        cdots = MathTex("\\cdots")
        cdots.move_to(VGroup(fraction_limits[-1], lower_equals))
        mult_signs.add(cdots)

        # Pi creatures react
        self.play(
            PiCreatureSays(
                mathy,
                "Whoa whoa whoa \\\\ there buddy",
                look_at=morty.eyes,
                target_mode="sassy",
            ),
            morty.animate.change("guilty", mathy.eyes),
        )
        self.wait(2)

        # Write out commutative diagram
        self.play(
            RemovePiCreatureBubble(
                mathy,
                target_mode="raise_right_hand",
                look_at=factors,
            ),
            morty.animate.change("pondering", factors),
            LaggedStartMap(FadeIn, factors),
        )
        self.wait()
        self.play(
            FadeIn(equals),
            Write(result)
        )
        self.wait()
        self.play(
            LaggedStartMap(GrowArrow, fraction_limit_arrows),
            LaggedStartMap(
                FadeIn, fraction_limits,
                shift=UP
            ),
            run_time=4,
            lag_ratio=0.25,
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, mult_signs),
            FadeIn(lower_equals),
            mathy.animate.change("sassy"),
        )
        self.play(
            GrowArrow(result_limit_arrow),
            FadeIn(result_limit, shift=UP),
            morty.animate.change("confused"),
        )
        self.wait(2)

        # Write general limit rule
        limit_rule = MathTex(
            "\\left( \\lim_{N \\to \\infty} a_N^{(1)} \\right)",
            "\\left( \\lim_{N \\to \\infty} a_N^{(2)} \\right)",
            "\\cdots", "=",
            "\\lim_{N \\to \\infty} \\left( a_N^{(1)} a_N^{(2)} \\cdots \\right)"
        )
        limit_rule.next_to(self.pi_creatures, UP)
        q_marks = MathTex("???")
        q_marks.set_color(YELLOW)
        limit_equals = limit_rule.get_part_by_tex("=")
        q_marks.next_to(limit_equals, UP, buff=SMALL_BUFF)

        index_of_equals = limit_rule.index_of_part(limit_equals)
        lhs_brace = Brace(limit_rule[:index_of_equals], UP)
        rhs_brace = Brace(limit_rule[index_of_equals + 1:], UP)

        self.play(
            FadeIn(limit_rule, shift=DOWN),
            mathy.animate.change("angry"),
            morty.animate.change("erm"),
        )
        self.play(GrowFromCenter(lhs_brace))
        self.wait()
        self.play(ReplacementTransform(lhs_brace, rhs_brace))
        self.wait(2)
        self.play(FadeOut(rhs_brace), Write(q_marks))
        limit_rule.add(q_marks)
        self.wait(2)
        self.play(morty.animate.change("pondering"))
        self.play(mathy.animate.change("tease"))
        self.wait(3)
        self.play(
            Animation(limit_rule),
            morty.animate.change("pondering"),
            mathy.animate.change("pondering"),
        )
        self.wait(3)

        # Write dominated convergence
        mover = VGroup(
            top_line, fraction_limits, fraction_limit_arrows,
            mult_signs, lower_equals,
            result_limit, result_limit_arrow,
        )
        self.play(
            mover.animate.next_to(FRAME_HEIGHT * UP / 2, UP),
            limit_rule.animate.to_edge(UP),
        )
        dominated_convergence = Tex("``Dominated convergence''")
        dominated_convergence.set_color(BLUE)
        dominated_convergence.next_to(limit_rule, DOWN, buff=LARGE_BUFF)

        see_blog_post = Tex("(See supplementary blog post)")
        see_blog_post.next_to(dominated_convergence, DOWN)

        self.play(
            FadeIn(dominated_convergence, shift=DOWN),
            mathy.animate.change("raise_right_hand"),
        )
        self.play(morty.animate.change("thinking"))
        self.wait()
        self.play(Write(see_blog_post))
        self.wait(4)

    def create_pi_creatures(self):
        group = VGroup(PiCreature(color=GREY), Mortimer())
        group.set_height(2)
        group.arrange(RIGHT, buff=4)
        group.to_edge(DOWN)
        return group
