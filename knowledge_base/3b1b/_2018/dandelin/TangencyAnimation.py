# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示五個黃色圓環從中心縮放出現的動畫效果。



from manim import *
class TangencyAnimation(Scene):
    def construct(self):
        rings = VGroup(*[
            Circle(color=YELLOW, stroke_width=3, radius=0.5)
            for x in range(5)
        ])
        for ring in rings:
            ring.save_state()
            ring.scale(0)
            ring.saved_state.set_stroke(width=0)

        self.play(LaggedStart(
            *[Restore(ring) for ring in rings],
            run_time=2,
            lag_ratio=0.7
        ))
