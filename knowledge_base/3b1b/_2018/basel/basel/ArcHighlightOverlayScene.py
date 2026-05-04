# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個圓弧高亮疊加場景，其中多個標記圓弧圍繞圓心依序閃現，模擬光線掃過的效果。



from manim import *
class ArcHighlightOverlayScene(Scene):

    def construct(self):

        BASELINE_YPOS = -2.5
        OBSERVER_POINT = [0, BASELINE_YPOS, 0]
        LAKE0_RADIUS = 1.5
        INDICATOR_RADIUS = 0.6
        TICK_SIZE = 0.5
        LIGHTHOUSE_HEIGHT = 0.2
        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8
        DOT_COLOR = BLUE

        FLASH_TIME = 0.25

        def flash_arcs(n):

            angle = TAU / 2**n
            arcs = []
            arcs.append(LabeledArc(angle/2, start_angle = -TAU/4, radius = LAKE0_RADIUS, length = 1))

            for i in range(1, 2**n):
                arcs.append(LabeledArc(angle, start_angle = -TAU/4 + (i-0.5)*angle, radius = LAKE0_RADIUS, length = 2))
        
            arcs.append(LabeledArc(angle/2, start_angle = -TAU/4 - angle/2, radius = LAKE0_RADIUS, length = 1))

            self.play(
                FadeIn(arcs[0], run_time = FLASH_TIME)
            )

            for i in range(1, 2**n + 1):
                self.play(
                    FadeOut(arcs[i-1], run_time = FLASH_TIME),
                    FadeIn(arcs[i], run_time = FLASH_TIME)
                )

            self.play(
                FadeOut(arcs[2**n], run_time = FLASH_TIME),
            )
