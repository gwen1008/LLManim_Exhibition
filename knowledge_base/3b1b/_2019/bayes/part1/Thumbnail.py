# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯定理的視覺化圖表，包含機率區域、標籤和公式，作為影片縮圖使用。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        diagram = BayesDiagram(0.25, 0.4, 0.1)
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
            }
        }
        labels = VGroup(
            MathTex("P(H)", **kw),
            MathTex("P(E|H)", **kw),
            MathTex("P(E|\\neg H)", **kw),
        )
        labels.scale(1)

        for label, brace, vect in zip(labels, braces, [DOWN, LEFT, RIGHT]):
            label.next_to(brace, vect)

        diagram.add(*labels)

        diagram.to_edge(DOWN, buff=MED_SMALL_BUFF)
        diagram.shift(2 * LEFT)
        self.add(diagram)

        diagram.set_height(FRAME_HEIGHT - 1)
        diagram.center().to_edge(DOWN)
        for rect in diagram.evidence_split:
            rect.set_sheen(0.2, UL)
        
        # Formula
        formula = get_bayes_formula()
        formula.scale(1.5)
        formula.to_corner(UL)

        frac = VGroup(
            diagram.he_rect.copy(),
            Line(ORIGIN, 4 * RIGHT).set_stroke(WHITE, 3),
            VGroup(
                diagram.he_rect.copy(),
                MathTex("+"),
                diagram.nhe_rect.copy(),
            ).arrange(RIGHT)
        )
        frac.arrange(DOWN)
        equals = MathTex("=")
        equals.next_to(formula, RIGHT)
        frac.next_to(equals, RIGHT)

        self.add(formula)
        self.add(equals, frac)

        VGroup(formula, equals, frac).to_edge(UP, buff=SMALL_BUFF)
