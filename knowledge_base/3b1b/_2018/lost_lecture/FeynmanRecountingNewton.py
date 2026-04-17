# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示費曼講課的畫面，然後從上方淡入牛頓畫像和《自然哲學的數學原理》圖像，並用白色邊框框住它們。



from manim import *
class FeynmanRecountingNewton(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_opacity = 1

    def construct(self):
        feynman_teaching = ImageMobject("Feynman_teaching")
        feynman_teaching.set_width(config.frame_width)

        newton = ImageMobject("Newton")
        principia = ImageMobject("Principia_equal_area")
        images = [newton, principia]
        for image in images:
            image.set_height(5)
        newton.to_corner(UL)
        principia.next_to(newton, RIGHT)
        for image in images:
            image.rect = SurroundingRectangle(
                image, color=WHITE, buff=0,
            )

        self.play(FadeIn(feynman_teaching, shift=DOWN, run_time=2))
        self.wait()
        self.play(
            FadeIn(newton, shift=DOWN),
            FadeIn(newton.rect, shift=DOWN),
        )
        self.wait()
        self.play(*[
            FadeIn(
                mob, shift=3 * LEFT
            )
            for mob in (principia, principia.rect)
        ])
        self.wait()
