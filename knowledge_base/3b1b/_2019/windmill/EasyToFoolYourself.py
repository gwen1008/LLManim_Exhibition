# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個灰色 Pi 生物思考並產生思想泡泡，然後出現「Fool」文字和箭頭，最後 Pi 生物說話並出現紅色「No it's not!」文字的動畫過程。



from manim import *
class EasyToFoolYourself(PiCreatureScene):
    def __init__(self, default_pi_creature_kwargs=None, **kwargs):
        if default_pi_creature_kwargs is None:
            default_pi_creature_kwargs = {
                "color": GREY_BROWN,
            }
        super().__init__(default_pi_creature_kwargs=default_pi_creature_kwargs, **kwargs)

    def construct(self):
        morty = self.pi_creature
        morty.to_corner(DL)

        bubble = ThoughtBubble()
        for i, part in enumerate(bubble):
            part.shift(2 * i * SMALL_BUFF * DOWN)
        bubble.pin_to(morty)

        fool_word = Text("Fool")
        fool_word.scale(1.5)
        fool_arrow = Arrow(start=RIGHT, end=LEFT)
        fool_arrow.next_to(morty, RIGHT, buff=0)
        fool_word.next_to(fool_arrow, RIGHT)

        self.add(morty)
        self.play(
            Create(bubble),
            morty.animate.change("pondering"),
        )
        self.play(
            bubble[3].animate.set_fill(GREEN_SCREEN, 0.5),
        )
        self.wait()
        self.play(morty.animate.change("thinking"))
        self.play(
            FadeIn(fool_word, shift=LEFT),
            Create(fool_arrow),
        )
        self.wait()
        self.pi_creature_says(
            "Isn't it\\\\obvious?",
            target_mode="maybe",
            added_anims=[FadeOut(bubble)]
        )
        self.wait(4)

        #
        words = Text("No it's not!")
        words.scale(1.5)
        words.set_color(RED)
        words.next_to(morty.bubble, RIGHT, LARGE_BUFF)
        words.match_y(morty.bubble.content)

        self.play(
            FadeIn(words, scale=2),
            morty.animate.change("guilty"),
        )
        self.wait()
