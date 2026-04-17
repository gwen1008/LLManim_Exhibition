# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯定理公式與視覺化圖表，並用箭頭和文字標註公式中的條件機率部分。



from manim import *
class BayesTheoremOnProportions(Scene):
    def construct(self):
        # Place on top of visuals from "HeartOfBayes"
        formula = get_bayes_formula()
        formula.scale(1.5)

        title = Text("Bayes' theorem")
        title.scale(2)
        title.next_to(formula, UP, buff=LARGE_BUFF)
        group = VGroup(formula, title)

        equals = MathTex("=")
        equals.next_to(formula, RIGHT)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(4)
        h_line.next_to(equals, RIGHT)
        h_line.set_stroke(WHITE, 3)

        self.add(group)
        self.wait()
        self.play(
            group.animate.to_edge(LEFT),
            MaintainPositionRelativeTo(equals, group),
            FadeIn(equals),
            MaintainPositionRelativeTo(h_line, group),
            FadeIn(h_line),
        )

        # People
        people = VGroup(*[Person() for x in range(7)])
        people.arrange(RIGHT)
        people.match_width(h_line)
        people.next_to(h_line, DOWN)
        people.set_color(BLUE_E)
        people[:3].set_color(GREEN)
        num_people = people[:3].copy()

        self.play(FadeIn(people, lag_ratio=0.1))
        self.play(num_people.animate.next_to(h_line, UP))
        self.wait(0.5)

        # Diagrams
        diagram = BayesDiagram(0.25, 0.5, 0.2)
        diagram.set_width(0.7 * h_line.get_width())
        diagram.next_to(h_line, DOWN)
        diagram.hne_rect.set_fill(opacity=0.1)
        diagram.nhne_rect.set_fill(opacity=0.1)
        num_diagram = diagram.deepcopy()
        num_diagram.next_to(h_line, UP)
        num_diagram.nhe_rect.set_fill(opacity=0.1)
        low_diagram_rects = VGroup(diagram.he_rect, diagram.nhe_rect)
        top_diagram_rects = VGroup(num_diagram.he_rect)

        self.play(
            FadeOut(people),
            FadeOut(num_people),
            FadeIn(diagram),
            FadeIn(num_diagram),
        )
        self.wait()

        # Circle each part
        E_part = VGroup(formula[4], *formula[19:]).copy()
        H_part = VGroup(formula[2], *formula[8:18]).copy()

        E_arrow = Arrow(ORIGIN, UP, color=BLUE)
        E_arrow.next_to(E_part[0], DOWN)
        E_words = Text(
            "...among cases where\n$E$ is True",
            color=BLUE,
            tex_to_color_map={"$E$": BLUE},
        )
        E_words.next_to(E_arrow, DOWN)
        H_arrow = Arrow(ORIGIN, DOWN, color=YELLOW)
        H_arrow.next_to(H_part[0], UP)
        H_words = Text(
            "How often is\n$H$ True...",
            color=YELLOW,
            tex_to_color_map={"$H$": YELLOW},
        )
        H_words.next_to(H_arrow, UP)

        denom_rect = SurroundingRectangle(E_part[1:], color=BLUE)
        numer_rect = SurroundingRectangle(H_part[1:], color=YELLOW)

        self.play(
            formula.animate.set_opacity(0.5),
            ApplyMethod(
                E_part.set_stroke, YELLOW, 3, {"background": True},
                rate_func=there_and_back,
            ),
            FadeIn(denom_rect),
            Create(E_arrow),
            FadeIn(E_words, shift=UP),
            low_diagram_rects.animate.set_stroke(TEAL, 3),
        )
        self.wait()
        self.play(
            FadeOut(E_part),
            FadeIn(H_part),
            FadeOut(denom_rect),
            FadeIn(numer_rect),
            Create(H_arrow),
            FadeIn(H_words, shift=DOWN),
            FadeOut(title, shift=UP),
            low_diagram_rects.animate.set_stroke(WHITE, 1),
            top_diagram_rects.animate.set_stroke(YELLOW, 3),
        )
        self.wait()
