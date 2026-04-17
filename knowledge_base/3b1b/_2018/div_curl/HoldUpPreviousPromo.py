# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個灰色棕色的 PiCreature 舉起右手，同時一個螢幕矩形從上方淡入到左上角。



from manim import *
class HoldUpPreviousPromo(PiCreatureScene):
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
        screen_rect = ScreenRectangle(height=5)
        screen_rect.to_corner(UL)

        self.play(
            FadeIn(screen_rect, shift=DOWN),
            morty.animate.change("raise_right_hand"),
        )
        self.wait(5)
