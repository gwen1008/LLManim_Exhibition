# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示兩個帶有標籤的大括號從縮小狀態恢復到原始大小，並在旁邊寫上文字標籤的動畫過程。



from manim import *
class ShowSegmentSplit(Scene):
    def __init__(self, include_image=True, **kwargs):
        super().__init__(**kwargs)
        self.include_image = include_image

    def construct(self):
        if self.include_image:
            image = ImageMobject("ShowCircleToCircleLine")
            image.set_height(config.frame_height)
            self.add(image)

        brace1 = Brace(Line(ORIGIN, 1.05 * UP), LEFT)
        brace2 = Brace(Line(1.7 * DOWN, ORIGIN), LEFT)
        braces = VGroup(brace1, brace2)
        braces.rotate(-14 * DEGREES)
        braces.move_to(0.85 * UP + 1.7 * LEFT)

        words = VGroup(
            Text("Top segment"),
            Text("Bottom segment")
        )
        for word, brace in zip(words, braces):
            word.next_to(
                brace.get_center(), LEFT,
                buff=0.35
            )
        words[0].set_color(PINK)
        words[1].set_color(GOLD)

        for mob in list(braces) + list(words):
            mob.add_to_back(mob.copy().set_stroke(BLACK, 5))

        for brace in braces:
            brace.save_state()
            brace.set_stroke(width=0)
            brace.scale(0)

        self.play(
            LaggedStart(
                *[Restore(brace) for brace in braces],
                lag_ratio=0.7
            ),
        )
        for word in words:
            self.play(Write(word, run_time=1))
        self.wait()
