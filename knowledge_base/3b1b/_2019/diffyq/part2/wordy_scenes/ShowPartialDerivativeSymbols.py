# Source: 3b1b/_2019/diffyq/part2/wordy_scenes.py
# Description: [3b1b translated] 展示偏微分符號從 d 到 ∂ 的轉換過程，並解釋每個符號的意義。


from manim import *
import itertools as it

class ShowPartialDerivativeSymbols(Scene):
    def construct(self):
        t2c = {
            "{x}": GREEN,
            "{t}": YELLOW,
        }
        d_derivs, del_derivs = VGroup(*[
            VGroup(*[
                MathTex(
                    "{" + sym, "T", "\\over", sym, var + "}",
                    "(", "{x}", ",", "{t}", ")",
                ).set_color_by_tex_to_color_map(t2c)
                for var in ("{x}", "{t}")
            ])
            for sym in ("d", "\\partial")
        ])
        dTdx, dTdt = d_derivs
        delTdelx, delTdelt = del_derivs
        dels = VGroup(*it.chain(*[
            del_deriv.get_parts_by_tex("\\partial")
            for del_deriv in del_derivs
        ]))

        dTdx.to_edge(UP)
        self.play(FadeIn(dTdx, shift=DOWN))
        self.wait()
        self.play(CreateThenFadeOut(SurroundingRectangle(dTdx[3:5])))
        self.play(CreateThenFadeOut(SurroundingRectangle(dTdx[:2])))
        self.wait()

        dTdt.move_to(dTdx)
        self.play(
            dTdx.animate.next_to(dTdt, RIGHT, buff=1.5),
            dTdx.animate.set_opacity(0.5),
            FadeIn(dTdt, shift=DOWN)
        )
        self.wait()

        for m1, m2 in zip(d_derivs, del_derivs):
            m2.move_to(m1)

        pd_words = Text("Partial derivatives")
        pd_words.next_to(del_derivs, DOWN, buff=MED_LARGE_BUFF)

        self.play(
            Write(pd_words),
            dTdx.animate.set_opacity(1),
            run_time=1,
        )
        self.wait()
        self.play(
            ReplacementTransform(d_derivs, del_derivs)
        )
        self.play(
            LaggedStart(*[
                CreateThenFadeOut(
                    SurroundingRectangle(
                        d,
                        color=BLUE,
                        buff=0.5 * SMALL_BUFF,
                        stroke_width=2,
                    )
                )
                for d in dels
            ])
        )
        self.wait()

        num_words = VGroup(*[
            Text(
                "Change in $T$\ncaused by ",
                "$\\partial$", "${}$".format(var),
            ).set_color_by_tex_to_color_map(t2c)
            for var in ("{x}", "{t}")
        ])
        num_words.scale(0.8)
        for word, deriv in zip(num_words, del_derivs):
            num = deriv[:2]
            word.move_to(num, UP)
            word.to_edge(UP, buff=MED_SMALL_BUFF)
            deriv.rect = SurroundingRectangle(
                num,
                buff=SMALL_BUFF,
                stroke_width=2,
                color=word[-1].get_color(),
            )
            deriv.rect.mob = num
            deriv.rect.add_updater(lambda r: r.move_to(r.mob))

        self.play(
            Write(num_words[1]),
            VGroup(del_derivs, pd_words).animate.shift(DOWN),
            Create(del_derivs[1].rect),
        )
        self.play(
            Write(num_words[0]),
            Create(del_derivs[0].rect),
        )
        self.wait()
