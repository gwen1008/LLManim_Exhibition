# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示五個隨機分佈的點及其對應的主題標籤，然後用虛線連接所有點，最後聚焦於第一個主題。


from manim import *
import random
import itertools as it

class TopicsAndConnections(Scene):
    def __init__(self, random_seed=1, **kwargs):
        super().__init__(**kwargs)
        self.random_seed = random_seed

    def construct(self):
        random.seed(self.random_seed)
        
        dots = VGroup(*[
            Dot(8 * np.array([
                random.random(),
                random.random(),
                0
            ]))
            for n in range(5)
        ])
        topics = VGroup(*[
            Text(word).next_to(
                dot, RIGHT, buff=SMALL_BUFF
            )
            for dot, word in zip(dots, [
                "Divergence/curl",
                "Fluid flow",
                "Electricity and magnetism",
                "Conformal maps",
                "Complex numbers"
            ])
        ])
        for topic in topics:
            topic.add_to_back(
                topic.copy().set_stroke(BLACK, 2)
            )

        VGroup(dots, topics).center()
        for dot in dots:
            dot.save_state()
            dot.scale(3)
            dot.set_fill(opacity=0)

        connections = VGroup(*[
            DashedLine(d1.get_center(), d2.get_center())
            for d1, d2 in it.combinations(dots, 2)
        ])
        connections.set_stroke(YELLOW, 2)

        full_rect = FullScreenRectangle(
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0
        )

        self.play(
            LaggedStartMap(
                Restore, dots,
            ),
            LaggedStartMap(Write, topics),
        )
        self.wait()
        self.play(
            LaggedStartMap(Create, connections),
            Animation(topics),
            Animation(dots),
        )
        self.wait()
        self.play(
            FadeIn(full_rect),
            Animation(topics[0]),
            Animation(dots[0]),
        )
        self.wait()
