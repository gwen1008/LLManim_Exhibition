# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示一個黃色角色看著筆記本電腦，思考巴塞爾問題與沃利斯乘積之間的數學關係，並用思想泡泡和箭頭連接兩個公式。



from manim import *
class SridharWatchingScene(PiCreatureScene):
    def __init__(self, default_pi_creature_kwargs=None, **kwargs):
        if default_pi_creature_kwargs is None:
            default_pi_creature_kwargs = {
                "color": YELLOW_E,
                "flip_at_start": False,
            }
        super().__init__(default_pi_creature_kwargs=default_pi_creature_kwargs, **kwargs)

    def construct(self):
        laptop = Laptop()
        laptop.scale(1.8)
        laptop.to_corner(DR)
        sridhar = self.pi_creature
        sridhar.next_to(laptop, LEFT, SMALL_BUFF, DOWN)
        bubble = ThoughtBubble()
        bubble.flip()
        bubble.pin_to(sridhar)

        basel = MathTex(
            "{1", "\\over", "1^2}", "+",
            "{1", "\\over", "2^2}", "+",
            "{1", "\\over", "3^2}", "+", "\\cdots",
            "= \\frac{\\pi^2}{6}"
        )
        wallis = get_wallis_product(n_terms=4)
        VGroup(basel, wallis).scale(0.7)
        basel.move_to(bubble.get_bubble_center())
        basel.to_edge(UP, buff=MED_SMALL_BUFF)
        wallis.next_to(basel, DOWN, buff=0.75)
        arrow = MathTex("\\updownarrow")
        arrow.move_to(VGroup(basel, wallis))
        basel.set_color(YELLOW)
        wallis.set_color(BLUE)

        self.play(LaggedStartMap(DrawBorderThenFill, laptop))
        self.play(sridhar.change, "pondering", laptop.screen)
        self.wait()
        self.play(Create(bubble))
        self.play(LaggedStartMap(FadeIn, basel))
        self.play(
            ReplacementTransform(basel.copy(), wallis),
            GrowFromPoint(arrow, arrow.get_top())
        )
        self.wait(4)
        self.play(sridhar.change, "thinking", wallis)
        self.wait(4)
        self.play(LaggedStartMap(
            ApplyFunction,
            VGroup(*list(laptop) + [bubble, basel, arrow, wallis, sridhar]),
            lambda mob: (lambda m: m.set_color(BLACK).set_opacity(0).scale(0.8), mob),
            run_time=3,
        ))
