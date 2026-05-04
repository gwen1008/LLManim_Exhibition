# Source: 3b1b/_2019/bayes/footnote.py
# Description: [3b1b translated] 展示貝葉斯定理的兩種視角，從韋恩圖過渡到兩個條件概率的矩形圖解，並動態揭示公式各部分對應的幾何區域。



from manim import *
class ShowTwoPerspectives(Scene):
    def __init__(self, pa=1/3, pb=1/4, p_both=1/6, diagram_height=4, **kwargs):
        super().__init__(**kwargs)
        self.pa = pa
        self.pb = pb
        self.p_both = p_both
        self.diagram_height = diagram_height

    def construct(self):
        # Ask about intersection
        formula = self.get_formula()

        venn_diagram = self.get_venn_diagram()
        venn_diagram.next_to(formula, DOWN, buff=LARGE_BUFF)

        arrow = Arrow(
            formula[3].get_bottom(),
            venn_diagram.get_center(),
        )

        self.add(formula)
        self.play(
            formula[:3].animate.set_opacity(0.2),
            formula[-3:].animate.set_opacity(0.2),
        )
        for i in (0, 1):
            self.play(
                FadeIn(venn_diagram[0][i]),
                Write(venn_diagram[1][i]),
                run_time=1,
            )
        self.play(Create(arrow))
        self.wait()

        # Think with respect to A
        diagram1 = self.get_diagram1()
        diagram1.evidence_split.set_opacity(0)
        diagram1.hypothesis_split.set_opacity(1)
        diagram1.to_edge(RIGHT, buff=LARGE_BUFF)
        diagram1.refresh_braces()

        d1_line = DashedLine(
            diagram1.h_rect.get_corner(UR),
            diagram1.h_rect.get_corner(DR),
        )
        d1_line.set_stroke(BLACK, 2)

        space_words = TexText(
            "Space of all\\\\possibilities"
        )
        space_words.match_width(diagram1.square)
        space_words.scale(0.9)
        space_words.move_to(diagram1.square)
        space_words.set_fill(BLACK)
        space_outline = SurroundingRectangle(diagram1.square, buff=0)
        space_outline.set_stroke(WHITE, 10)

        self.play(
            FadeOut(venn_diagram[0][1]),
            FadeOut(venn_diagram[1][1]),
            FadeOut(arrow),
            formula[4:6].animate.set_opacity(1),
        )
        diagram1.pa_label.update()
        self.play(
            FadeIn(diagram1.nh_rect),
            ReplacementTransform(
                venn_diagram[0][0],
                diagram1.h_rect,
            ),
            ReplacementTransform(
                venn_diagram[1][0],
                diagram1.pa_label.get_part_by_tex("A"),
            ),
            FadeIn(diagram1.h_brace),
            FadeIn(diagram1.pa_label[0]),
            FadeIn(diagram1.pa_label[2]),
            Create(d1_line),
        )
        self.add(diagram1.pa_label)
        self.wait()
        self.play(
            FadeIn(space_words),
            Create(space_outline),
        )
        self.play(
            FadeOut(space_words),
            FadeOut(space_outline),
        )
        self.wait()

        # Show B part
        B_rects = VGroup(diagram1.he_rect, diagram1.nhe_rect)
        B_rects.set_opacity(1)
        B_rects.set_sheen(0.2, UL)
        diagram1.nhe_rect.set_color(BLUE_D)
        diagram1.he_rect.set_color(MID_COLOR)
        diagram1.save_state()
        B_rects.stretch(0.001, 1, about_edge=DOWN)

        diagram1.he_brace.save_state()
        diagram1.he_brace.stretch(0.001, 1, about_edge=DOWN)

        self.add(diagram1.he_brace, diagram1.pba_label)
        self.add(diagram1, d1_line)
        self.play(
            Restore(diagram1),
            Restore(diagram1.he_brace),
            VFadeIn(diagram1.he_brace),
            VFadeIn(diagram1.pba_label),
            formula.pba.animate.set_opacity(1),
        )
        self.wait()

        # Show symmetric perspective
        diagram1_copy = diagram1.deepcopy()
        diagram2 = self.get_diagram2()
        d2_line = DashedLine(
            diagram2.b_rect.get_corner(UL),
            diagram2.b_rect.get_corner(UR),
        )
        d2_line.set_stroke(BLACK, 2)

        for rect in [diagram2.ba_rect, diagram2.nba_rect]:
            rect.save_state()
            rect.stretch(0.001, 0, about_edge=LEFT)

        self.play(
            diagram1_copy.animate.move_to(diagram2),
            formula.pb.animate.set_opacity(1),
        )
        self.play(
            diagram1_copy.set_likelihood(self.pb),
            diagram1_copy.set_antilikelihood(self.pb),
            VFadeOut(diagram1_copy),
            FadeIn(diagram2),
            TransformFromCopy(formula.pb, diagram2.pb_label),
            FadeIn(diagram2.pb_brace),
            Create(d2_line),
        )
        self.wait()
        self.play(
            formula.pab.animate.set_opacity(1),
            formula.eq1.animate.set_opacity(1),
        )
        self.play(
            TransformFromCopy(formula.pab, diagram2.pab_label),
            FadeIn(diagram2.pab_brace),
            Restore(diagram2.ba_rect),
            Restore(diagram2.nba_rect),
        )
        self.wait()

    def get_formula(self):
        kw = {
            "tex_to_color_map": {
                "A": YELLOW,
                "B": BLUE,
            }
        }
        parts = VGroup(*[
            MathTex(tex, **kw)
            for tex in [
                "P(B)", "P(A|B)", "=",
                "P(A \\text{ and } B)",
                "=", "P(A)", "P(B|A)",
            ]
        ])
        attrs = [
            "pb", "pab", "eq1", "p_both", "eq2", "pa", "pba"
        ]
        for attr, part in zip(attrs, parts):
            setattr(parts, attr, part)

        parts.arrange(RIGHT, buff=SMALL_BUFF)
        parts.set_width(FRAME_WIDTH - 1)
        parts.center().to_edge(UP)
        return parts

    def get_venn_diagram(self):
        c1 = Circle(
            radius=2.5,
            stroke_width=2,
            stroke_color=YELLOW,
            fill_opacity=0.5,
            fill_color=YELLOW,
        )
        c1.flip(RIGHT)
        c1.rotate(3 * TAU / 8)
        c2 = c1.copy()
        c2.set_color(BLUE)
        c1.shift(LEFT)
        c2.shift(RIGHT)
        circles = VGroup(c1, c2)

        titles = VGroup(
            MathTex("A"),
            MathTex("B"),
        )
        for title, circle, vect in zip(titles, circles, [UL, UR]):
            title.set_color(circle.get_color())
            title.scale(2)
            title.next_to(
                circle.get_boundary_point(vect),
                vect,
                buff=SMALL_BUFF
            )

        return VGroup(circles, titles)

    def get_diagram1(self):
        likelihood = (self.p_both / self.pa)
        antilikelihood = (self.pb - self.p_both) / (1 - self.pa)
        diagram = BayesDiagram(self.pa, likelihood, antilikelihood)
        diagram.set_height(self.diagram_height)

        diagram.add_brace_attrs()
        kw = {"tex_to_color_map": {"A": YELLOW, "B": BLUE}}
        diagram.pa_label = MathTex("P(A)", **kw)
        diagram.pba_label = MathTex("P(B|A)", **kw)
        diagram.pa_label.add_updater(
            lambda m: m.next_to(diagram.h_brace, DOWN, SMALL_BUFF),
        )
        diagram.pba_label.add_updater(
            lambda m: m.next_to(diagram.he_brace, LEFT, SMALL_BUFF),
        )

        return diagram

    def get_diagram2(self):
        pa = self.pa
        pb = self.pb
        p_both = self.p_both
        square = Square()
        square.set_stroke(WHITE, 1)
        square.set_fill(GREY_B, 1)
        square.set_height(self.diagram_height)

        b_rect = square.copy()
        b_rect.stretch(pb, 1, about_edge=DOWN)
        b_rect.set_fill(BLUE)
        b_rect.set_sheen(0.2, UL)

        nb_rect = square.copy()
        nb_rect.stretch(1 - pb, 1, about_edge=UP)

        ba_rect = b_rect.copy()
        ba_rect.stretch((p_both / pb), 0, about_edge=LEFT)
        ba_rect.set_fill(MID_COLOR)

        nba_rect = nb_rect.copy()
        nba_rect.stretch((pa - p_both) / (1 - pb), 0, about_edge=LEFT)
        nba_rect.set_fill(YELLOW)

        result = VGroup(
            square.set_opacity(0),
            b_rect, nb_rect,
            ba_rect, nba_rect,
        )
        result.b_rect = b_rect
        result.nb_rect = nb_rect
        result.ba_rect = ba_rect
        result.nba_rect = nba_rect

        pb_brace = Brace(b_rect, LEFT, buff=SMALL_BUFF)
        pab_brace = Brace(ba_rect, DOWN, buff=SMALL_BUFF)
        kw = {"tex_to_color_map": {"A": YELLOW, "B": BLUE}}
        pb_label = MathTex("P(B)", **kw)
        pab_label = MathTex("P(A|B)", **kw)
        pb_label.next_to(pb_brace, LEFT, SMALL_BUFF)
        pab_label.next_to(pab_brace, DOWN, SMALL_BUFF)

        result.pb_brace = pb_brace
        result.pab_brace = pab_brace
        result.pb_label = pb_label
        result.pab_label = pab_label

        VGroup(
            result,
            pb_brace, pab_brace,
            pb_label, pab_label,
        ).to_edge(LEFT)

        return result
