# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示兩個角色（Randolph 和 Mortimer）的互動，其中一個角色思考數學公式，另一個角色困惑地看著，並出現一個混亂的思維泡泡。



from manim import *
class FailureToEmpathize(PiCreatureScene):
    def construct(self):
        randy, morty = self.pi_creatures

        # What a mess...
        big_bubble = ThoughtBubble(height=4, width=5)
        big_bubble.scale(1.75)
        big_bubble.flip(UR)
        for part in big_bubble:
            part.rotate(90 * DEGREES)
        big_bubble[:3].rotate(-30 * DEGREES)
        for i, part in enumerate(big_bubble[:3]):
            part.rotate(30 * DEGREES)
            part.shift((3 - i) * SMALL_BUFF * DOWN)
        big_bubble[0].shift(MED_SMALL_BUFF * RIGHT)
        big_bubble[:3].next_to(big_bubble[3], LEFT)
        big_bubble[:3].shift(0.3 * DOWN)
        big_bubble.set_fill(GREY_E)
        big_bubble.to_corner(UR)

        equation = MathTex(
            "\\sum_{k=1}^n (2k - 1) = n^2"
        )
        self.pi_creature_thinks(
            randy, equation,
            target_mode="confused",
            look_at=equation,
        )
        randy_group = VGroup(
            randy, randy.bubble,
            randy.bubble.content
        )
        self.wait()
        self.play(
            DrawBorderThenFill(big_bubble),
            morty.change, "confused",
            randy_group.animate.scale(0.5),
            randy_group.animate.move_to(big_bubble.get_bubble_center()),
            randy_group.animate.shift(0.5 * DOWN + RIGHT),
        )
        self.wait()
        self.play(morty.change("maybe"))
        self.wait(2)

        # Zoom out
        morty_group = VGroup(morty, big_bubble)
        ap = 5 * RIGHT + 2.5 * UP
        self.add(morty_group, randy_group)
        self.play(
            morty_group.animate.scale(2, about_point=ap),
            morty_group.animate.set_opacity(0),
            randy_group.animate.scale(2, about_point=ap),
            run_time=2
        )
        self.wait()

    def create_pi_creatures(self):
        randy = Randolph()
        morty = Mortimer()
        randy.flip().to_corner(DR)
        morty.flip().to_corner(DL)

        return (randy, morty)
