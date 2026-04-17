# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯定理的視覺化圖表，包含條件機率的矩形區域、標籤和公式，並用箭頭指向貝葉斯規則的公式表示。



from manim import *
class Thumbnail2(Scene):
    def construct(self):
        diagram = BayesDiagram(0.25, 0.4, 0.1)

        # Labels
        diagram.set_height(3)
        diagram.add_brace_attrs()
        braces = VGroup(
            diagram.h_brace,
            diagram.he_brace,
            diagram.nhe_brace,
        )
        diagram.add(*braces)

        kw = {
            "tex_to_color_map": {
                "H": YELLOW,
                "E": BLUE,
                "\\neg": RED,
            },
            "font_size": 24,
        }
        labels = VGroup(
            MathTex("P(H)", **kw),
            MathTex("P(E|H)", **kw),
            MathTex("P(E|\\neg H)", **kw),
        )

        for label, brace, vect in zip(labels, braces, [DOWN, LEFT, RIGHT]):
            label.next_to(brace, vect, buff=SMALL_BUFF)

        diagram.add(*labels)
        # End labels

        diagram.set_height(5)
        diagram.to_edge(LEFT)
        diagram.to_edge(DOWN)
        self.add(diagram)

        frac = VGroup(
            diagram.he_rect.copy(),
            Line(LEFT, RIGHT).set_width(7),
            VGroup(
                diagram.he_rect.copy(),
                MathTex("+", font_size=120),
                diagram.nhe_rect.copy(),
            ).arrange(RIGHT)
        ).arrange(DOWN, buff=0.5)

        frac.set_width(5)
        frac.move_to(diagram, UP)
        frac.to_edge(RIGHT)
        self.add(frac)

        right_arrow = Arrow(
            diagram.get_right(),
            frac[1].get_left(),
            thickness=0.1,
            color=GREEN
        )

        words = Tex("This is Bayes' rule", font_size=108)
        words.to_edge(UP)

        arrow = Arrow(
            words,
            frac,
            thickness=0.1,
        )
        arrow.scale(1.5, about_point=arrow.get_start())

        self.add(words, arrow)
