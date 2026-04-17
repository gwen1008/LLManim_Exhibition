# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示橢圓的三種定義以列表形式出現，並依次高亮每種定義，同時淡化其他定義。



from manim import *
class MultipleDefinitionsOfAnEllipse(Scene):
    def construct(self):
        title = Title("Multiple definitions of ``ellipse''")
        self.add(title)

        definitions = VGroup(
            Text("1. Stretch a circle"),
            Text("2. Thumbtack \\\\ \\quad\\, construction"),
            Text("3. Slice a cone"),
        )
        definitions.arrange(
            DOWN, buff=LARGE_BUFF,
            aligned_edge=LEFT
        )
        definitions.next_to(title, DOWN, LARGE_BUFF)
        definitions.to_edge(LEFT)

        for definition in definitions:
            definition.saved_state = definition.copy()
            definition.saved_state.set_opacity(0.5)

        self.play(LaggedStart(
            *[FadeIn(definition, shift=RIGHT) for definition in definitions],
            run_time=4
        ))
        self.wait()
        for definition in definitions:
            others = [d for d in definitions if d is not definition]
            self.play(
                definition.animate.set_fill(WHITE, opacity=1).scale(1.2, about_edge=LEFT),
                *[Restore(other) for other in others]
            )
            self.wait(2)
