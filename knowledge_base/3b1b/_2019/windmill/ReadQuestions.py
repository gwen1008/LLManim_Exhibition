# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個背景圖片上，多組線段逐組出現並伴隨淡入的矩形高亮效果，然後淡出。



from manim import *
class ReadQuestions(Scene):
    def construct(self):
        background = ImageMobject("AskWhatsOnTest_final_image")
        background.set_height(config.frame_height)
        self.add(background)

        lines = SVGMobject("imo_2011_2_underline-01")
        lines.set_width(config.frame_width - 1)
        lines.move_to(0.1 * DOWN)
        lines.set_stroke(TEAL, 3)

        clump_sizes = [1, 2, 3, 2, 1, 2]
        partial_sums = list(np.cumsum(clump_sizes))
        clumps = VGroup(*[
            lines[i:j]
            for i, j in zip(
                [0] + partial_sums,
                partial_sums,
            )
        ])

        faders = []
        for clump in clumps:
            rects = VGroup()
            for line in clump:
                rect = Rectangle()
                rect.set_stroke(width=0)
                rect.set_fill(TEAL, 0.25)
                rect.set_width(line.get_width() + config.small_buff)
                rect.set_height(0.35, stretch=True)
                rect.move_to(line, DOWN)
                rects.add(rect)

            self.play(
                Create(clump, run_time=2),
                FadeIn(rects),
                *faders,
            )
            self.wait()
            faders = [
                FadeOut(clump),
                FadeOut(rects),
            ]
        self.play(*faders)
        self.wait()
