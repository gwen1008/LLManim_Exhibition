# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示三個等價關係箭頭在矩形之間形成三角形，然後淡出其中兩個箭頭的動畫過程。



from manim import *
class TriangleOfEquivalences(Scene):
    def construct(self):
        title = Title("How do you prove this\\textinterrobang.")
        self.add(title)
        rects = VGroup(*[ScreenRectangle() for x in range(3)])
        rects.set_height(2)
        rects[:2].arrange(RIGHT, buff=2)
        rects[2].next_to(rects[:2], DOWN, buff=1.5)
        rects.next_to(title, DOWN)

        arrows = VGroup(*[
            MathTex("\\Leftrightarrow")
            for x in range(3)
        ])
        arrows.scale(2)
        arrows[0].move_to(rects[:2])
        arrows[1].rotate(60 * DEGREES)
        arrows[1].move_to(rects[1:])
        arrows[2].rotate(-60 * DEGREES)
        arrows[2].move_to(rects[::2])
        arrows[1:].shift(0.5 * DOWN)

        self.play(LaggedStart(
            *[DrawBorderThenFill(arrow) for arrow in arrows],
            lag_ratio=0.7,
            run_time=3,
        ))
        self.wait()
        self.play(FadeOut(arrows[1:]))
        self.wait()
