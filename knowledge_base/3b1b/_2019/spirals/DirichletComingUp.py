# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示 Dirichlet 的圖像從右側淡入，同時帶有黃色標題的文字從左側淡入的動畫。



from manim import *
class DirichletComingUp(Scene):
    def construct(self):
        image = ImageMobject("Dirichlet")
        image.set_height(3)
        words = TexText(
            "Coming up: \\\\", "Dirichlet's theorem",
            alignment="",
        )
        words.set_color_by_tex("Dirichlet's", YELLOW)
        words.scale(1.5)
        words.next_to(image, RIGHT)
        words.set_stroke(BLACK, 8, background=True)
        Group(words, image).center()

        self.play(
            FadeIn(image, shift=RIGHT),
            FadeIn(words, shift=LEFT),
        )
        self.wait()
