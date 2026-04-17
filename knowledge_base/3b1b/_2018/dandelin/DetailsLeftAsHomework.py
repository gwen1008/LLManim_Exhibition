# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個灰色棕色的 PiCreature 角色在左下角說出「Details left as homework」的對話框，並帶有歡呼的表情。



from manim import *
class DetailsLeftAsHomework(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": GREY_BROWN,
            "flip_at_start": False,
        },
        default_pi_creature_start_corner=DL,
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        # morty = self.pi_creature
        self.pi_creature_says(
            "Details left \\\\ as homework",
            target_mode="hooray"
        )
        self.wait(3)
