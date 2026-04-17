# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示三組渦流標籤（大、中、小）以淡入淡出的方式依次出現和消失。



from manim import *
class EddyLabels(Scene):
    def construct(self):
        labels = VGroup(
            Text("Large eddy"),
            Text("Medium eddy"),
            Text("Small eddy"),
        )
        for label in labels:
            self.play(FadeIn(
                label,
                rate_func=there_and_back_with_pause,
                run_time=3
            ))
