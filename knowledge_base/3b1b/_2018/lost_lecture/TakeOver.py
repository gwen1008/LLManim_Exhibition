# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個 PiCreature 角色在漸變背景中，對著一個名為 Henry 的棍狀圖像說出邪惡台詞的場景。



from manim import *
class TakeOver(PiCreatureScene):
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
        # 使用 Rectangle 模擬漸變背景
        gradient = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=[WHITE, BLACK],
            fill_opacity=1,
            stroke_width=0
        )
        gradient.set_height(config.frame_height)
        self.add(gradient)

        morty = self.pi_creature
        # 使用 SVGMobject 替代 ImageMobject
        henry = SVGMobject("stick_figure")  # 假設有 stick_figure.svg
        henry.set_height(4)
        henry.to_edge(LEFT)
        henry.to_edge(DOWN)

        self.add(morty, henry)
        self.pi_creature_says(
            "Muahaha!  All \\\\ mine now.",
            bubble_config={"fill_opacity": 0.5},
            bubble_creation_class=FadeIn,
            target_mode="conniving",
            added_anims=[henry.animate.rotate(5 * DEGREES)]
        )
        self.wait(2)
