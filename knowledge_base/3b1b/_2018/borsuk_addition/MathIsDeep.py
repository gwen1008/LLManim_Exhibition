# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示將單詞 "Math" 中的字母轉換為數字（A=1, B=2...），然後將這些數字相加得到總和的動畫過程，並有 PiCreature 角色在旁思考。



from manim import *
class MathIsDeep(PiCreatureScene):
    def construct(self):
        words = TexText("Math", "is", "deep")
        words.scale(2)
        words.to_edge(UP)
        math = words[0].copy()
        math[1].remove(math[1][1])
        math.set_fill(opacity=0)
        math.set_stroke(width=0, background=True)
        numbers = [13, 1, 20, 8]
        num_mobs = VGroup(*[Integer(d) for d in numbers])
        num_mobs.arrange(RIGHT, buff=MED_LARGE_BUFF)
        num_mobs.next_to(math, DOWN, buff=1.5)
        num_mobs.set_color(YELLOW)
        top_arrows = VGroup(*[
            Arrow(c.get_bottom(), n.get_top())
            for c, n in zip(math, num_mobs)
        ])
        n_sum = Integer(sum(numbers))
        n_sum.scale(1.5)
        n_sum.next_to(num_mobs, DOWN, buff=1.5)
        low_arrows = VGroup(*[
            Arrow(n.get_bottom(), n_sum.get_top())
            for n in num_mobs
        ])
        VGroup(top_arrows, low_arrows).set_color(WHITE)

        n_sum_border = n_sum.deepcopy()
        n_sum_border.set_fill(opacity=0)
        n_sum_border.set_stroke(YELLOW, width=1)
        n_sum_border.set_stroke(width=0, background=True)

        self.play(
            LaggedStartMap(
                FadeInFromLarge, words,
                scale_factor=1.5,
                run_time=0.6,
                lag_ratio=0.6,
            ),
            self.pi_creature.change, "pondering"
        )
        self.play(
            TransformFromCopy(math, num_mobs),
            *[GrowArrow(arrow) for arrow in top_arrows],
        )
        self.wait()
        self.play(
            TransformFromCopy(num_mobs, VGroup(n_sum)),
            self.pi_creature.change, "thinking",
            *[GrowArrow(arrow) for arrow in low_arrows],
        )
        self.play(LaggedStartMap(CreateThenUncreate, n_sum_border))
        self.play(Blink(self.pi_creature))
        self.wait()
