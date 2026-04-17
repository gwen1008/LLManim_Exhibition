# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示一個 PiCreature 從沉思到舉手思考，最後被一群隨機分佈的問號符號包圍的動畫過程。



from manim import *
class PrinciplesOverlay(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": GREY_BROWN,
            "flip_at_start": True,
        },
        default_pi_creature_start_corner=DR,
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        morty = self.pi_creature
        q_marks = VGroup(*[MathTex("?") for x in range(40)])
        q_marks.arrange_in_grid(4, 10)
        q_marks.space_out_submobjects(1.4)
        for mark in q_marks:
            mark.shift(
                random.random() * RIGHT,
                random.random() * UP,
            )
            mark.scale(1.5)
            mark.set_stroke(BLACK, 1)
        q_marks.next_to(morty, UP)
        q_marks.shift_onto_screen()
        q_marks.sort(
            lambda p: np.linalg.norm(p - morty.get_top())
        )

        self.play(morty.animate.change("pondering"))
        self.wait(2)
        self.play(morty.animate.change("raise_right_hand"))
        self.wait()
        self.play(morty.animate.change("thinking"))
        self.wait(4)
        self.play(FadeIn(q_marks[0], shift=DOWN))
        self.wait(2)
        self.play(LaggedStart(
            *[FadeIn(mark, shift=DOWN) for mark in q_marks[1:]],
            run_time=3
        ))
        self.wait(3)
