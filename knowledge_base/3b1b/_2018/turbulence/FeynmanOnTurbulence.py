# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示費曼的照片、名字和關於湍流重要性的引言，以淡入和書寫動畫呈現。



from manim import *
class FeynmanOnTurbulence(Scene):
    def construct(self):
        feynman = ImageMobject("Feynman_Woods", height=4)
        name = Text("Richard Feynman")
        name.next_to(feynman, DOWN)
        quote = Tex(
            "``", "Turbulence", "is the most\\\\"
            "important", "unsolved problem\\\\",
            "of classical physics.''",
            tex_to_color_map={
                "Turbulence": BLUE,
                "unsolved problem\\\\": YELLOW,
            },
        )
        quote[0].shift(SMALL_BUFF * RIGHT)
        quote.next_to(feynman, RIGHT)
        Group(feynman, name, quote).center()

        self.play(
            FadeIn(feynman, shift=UP),
            FadeIn(name, shift=DOWN),
            Write(quote, run_time=4)
        )
        self.wait()
