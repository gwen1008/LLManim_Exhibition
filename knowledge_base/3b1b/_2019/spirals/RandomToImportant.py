# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個灰色 Pi 生物從左邊的「任意問題」轉向關注右邊的「深刻事實」，並用箭頭連接兩者。



from manim import *
class RandomToImportant(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": GREY_BROWN,
        },
        camera_config={
            "background_color": GREY_E,
        },
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            camera_config=camera_config,
            **kwargs
        )

    def construct(self):
        morty = self.pi_creature
        morty.center().to_edge(DOWN)

        left_comment = Text("Arbitrary question")
        left_comment.to_edge(UP)
        left_comment.shift(3.5 * LEFT)

        right_comment = Text("Deep fact")
        right_comment.to_edge(UP)
        right_comment.shift(3.5 * RIGHT)

        arrow = Arrow(
            left_comment.get_right(),
            right_comment.get_left(),
            buff=0.5,
        )

        self.play(
            morty.animate.change("raise_left_hand", left_comment),
            FadeIn(left_comment, shift=DOWN)
        )
        self.wait(2)
        self.play(
            morty.animate.change("raise_right_hand", right_comment),
            FadeIn(right_comment, shift=DOWN)
        )
        self.play(
            Create(arrow),
            morty.animate.look_at(right_comment),
        )
        self.wait(2)
