# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一系列考慮事項從上方漸入並垂直排列的過程。



from manim import *
class VastSpaceOfConsiderations(Scene):
    def construct(self):
        considerations = VGroup(*[
            Text(phrase)
            for phrase in [
                "Define ``outer'' points",
                "Convex hulls",
                "Linear equations",
                "Sort points by when they're hit",
                "Sort points by some kind of angle?",
                "How does this permute the $n \\choose 2$ lines through pairs?",
                "Some points are hit more than others, can we quantify this?",
            ]
        ])
        considerations.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        considerations.to_edge(LEFT)

        self.play(LaggedStart(*[
            FadeIn(mob, shift=UP)
            for mob in considerations
        ], run_time=3, lag_ratio=0.2))
