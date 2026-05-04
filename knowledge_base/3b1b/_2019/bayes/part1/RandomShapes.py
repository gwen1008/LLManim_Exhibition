# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一系列隨機形狀（矩形、圓形、三角形、符號）依次淡入淡出，形成連續變換的視覺效果。



from manim import *
class RandomShapes(Scene):
    def construct(self):
        # 假設 BayesDiagram 是自定義類別，這裡保留原樣
        diagram = BayesDiagram(0.1, 0.4, 0.1)
        diagram.set_height(3)

        e_part = VGroup(diagram.he_rect, diagram.nhe_rect).copy()
        e_part.set_fill(BLUE, opacity=1)

        circle = Circle()
        circle.set_fill(RED, opacity=0.5)
        circle.set_stroke(RED, width=2)
        circle.move_to(diagram)

        tri = Polygon(UP, ORIGIN, RIGHT)
        tri.match_height(diagram)
        tri.set_fill(PURPLE, opacity=0.5)
        tri.set_stroke(PURPLE, width=2)
        tri.move_to(diagram)

        h_rect = diagram.h_rect
        h_rect.set_fill(YELLOW, opacity=1)

        pi = MathTex("\\pi")
        pi.set_height(2)
        pi.set_stroke(GREEN, width=2)
        pi.set_fill(GREEN, opacity=0.5)

        events = VGroup(
            e_part,
            h_rect,
            circle,
            pi,
            tri,
        )

        last = VMobject()
        for event in events:
            self.play(
                FadeIn(event),
                FadeOut(last)
            )
            self.wait()
            last = event
