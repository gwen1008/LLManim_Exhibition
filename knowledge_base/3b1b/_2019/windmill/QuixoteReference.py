# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示風車和唐吉訶德剪影從無到有繪製出來的動畫過程，背景為漸變灰色。



from manim import *
class QuixoteReference(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        rect.set_fill([GREY_D, GREY])

        windmill = SVGMobject("windmill")
        windmill.set_fill([GREY_BROWN, WHITE], 1)
        windmill.set_stroke(width=0)
        windmill.set_height(6)
        windmill.to_edge(RIGHT)

        quixote = SVGMobject("quixote")
        quixote.flip()
        quixote.set_height(4)
        quixote.to_edge(LEFT)
        quixote.set_stroke(BLACK, width=0)
        quixote.set_fill(BLACK, 1)
        quixote.align_to(windmill, DOWN)

        self.add(rect)
        self.play(LaggedStart(
            DrawBorderThenFill(windmill),
            DrawBorderThenFill(
                quixote,
                stroke_width=1,
            ),
            lag_ratio=0.4,
            run_time=3
        ))
        self.wait()
