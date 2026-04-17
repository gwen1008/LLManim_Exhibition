# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯定理的核心概念，透過兩個矩形圖表（全體可能性 vs 符合證據的可能性）的轉換，並以幾何分數形式呈現條件機率。



from manim import *
class HeartOfBayesTheorem(Scene):
    def construct(self):
        title = Tex("Heart of Bayes' theorem")
        title.scale(1.5)
        title.add(Underline(title))
        title.to_edge(UP)

        # Bayes diagrams
        diagram = self.get_diagram(
            prior=0.1, likelihood=0.4, antilikelihood=0.1,
        )
        diagram.nh_rect.set_fill(GREEN_E)
        diagram.hypothesis_split.set_opacity(1)
        diagram.evidence_split.set_opacity(0)
        restricted_diagram = self.get_restricted_diagram(diagram)
        diagram_copy = diagram.copy()
        diagram_copy.move_to(restricted_diagram)

        diagrams = VGroup(diagram, restricted_diagram)

        label1 = TexText("All possibilities")
        label2 = TexText(
            "All possibilities\\\\", "fitting the evidence",
            tex_to_color_map={"evidence": BLUE},
        )
        labels = VGroup(label1, label2)
        labels.scale(diagram.get_width() / label1.get_width())

        for l, d in zip(labels, diagrams):
            l.next_to(d, UP)

        label2.save_state()
        label2[0].move_to(label2, DOWN)
        label2[1:].shift(0.25 * UP)
        label2[1:].set_opacity(0)

        # Final fraction written geometrically
        fraction = always_redraw(
            lambda: self.get_geometric_fraction(restricted_diagram)
        )
        frac_box = always_redraw(lambda: DashedVMobject(
            SurroundingRectangle(
                fraction,
                buff=MED_SMALL_BUFF,
                stroke_width=2,
                stroke_color=WHITE,
            ),
            num_dashes=100,
        ))
        prob = MathTex(
            "P\\left(",
            "{\\text{Librarian }",
            "\\text{given}", "\\over", "\\text{the evidence}}",
            "\\right)"
        )
        prob.set_color_by_tex("Librarian", YELLOW)
        prob.set_color_by_tex("evidence", BLUE)
        prob.get_part_by_tex("\\over").set_opacity(0)
        prob.match_width(frac_box)
        prob.next_to(frac_box, UP)

        updaters = VGroup(
            diagram, restricted_diagram, fraction, frac_box
        )
        updaters.suspend_updating()

        self.play(
            FadeIn(diagram),
            FadeIn(label1, shift=DOWN),
        )
        self.play(
            TransformFromCopy(diagram, diagram_copy),
            TransformFromCopy(label1[0], label2[0]),
        )
        self.play(
            Restore(label2),
            ReplacementTransform(diagram_copy, restricted_diagram)
        )
        self.wait()

        self.play(
            TransformFromCopy(
                restricted_diagram.he_rect,
                fraction[0],
            ),
            TransformFromCopy(
                restricted_diagram.he_rect,
                fraction[2][0],
            ),
            TransformFromCopy(
                restricted_diagram.nhe_rect,
                fraction[2][2],
            ),
            Create(fraction[1]),
            Write(fraction[2][1]),
        )
        self.add(fraction)
        self.play(
            Create(frac_box),
            FadeIn(prob)
        )
        self.wait()

        self.play(Write(title, run_time=1))
        self.wait()

        # Mess with some numbers
        updaters.resume_updating()
        self.play(*[
            ApplyMethod(d.set_prior, 0.4, run_time=2)
            for d in diagrams
        ])
        self.play(*[
            ApplyMethod(d.set_likelihood, 0.3, run_time=2)
            for d in diagrams
        ])
        self.play(*[
            ApplyMethod(d.set_antilikelihood, 0.6, run_time=2)
            for d in diagrams
        ])
        self.wait()
        updaters.suspend_updating()

        # Ask about a formula
        words = TexText("Write this more\\\\mathematically")
        words.scale(1.25)
        words.set_color(RED)
        words.to_corner(UR)
        arrow = Arrow(words.get_bottom(), frac_box.get_top(), buff=SMALL_BUFF)
        arrow.match_color(words)
        arrow.set_stroke(width=5)

        self.play(
            FadeIn(words, shift=DOWN),
            GrowArrow(arrow),
            FadeOut(prob),
            title.to_edge, LEFT
        )
        self.wait()

    def get_diagram(self, prior, likelihood, antilikelihood):
        # 注意：BayesDiagram 需要自行定義或替換
        diagram = BayesDiagram(
            prior, likelihood, antilikelihood,
            not_evidence_color1=GREY,
            not_evidence_color2=GREEN_E,
        )
        diagram.set_height(3)
        diagram.move_to(5 * LEFT + DOWN)

        diagram.add_brace_attrs()
        braces = VGroup(diagram.h_brace, diagram.nh_brace)
        diagram.add(*braces)
        
        # 替換 LibrarianIcon 和 FarmerIcon 為簡單形狀
        icons = VGroup(
            Square(fill_color=YELLOW_D, fill_opacity=1, stroke_width=0).scale(0.25),
            Circle(fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.25)
        )
        icons[0].set_color(YELLOW_D)
        for icon, brace in zip(icons, braces):
            icon.set_height(0.5)
            icon.brace = brace
            icon.add_updater(lambda m: m.next_to(m.brace, DOWN, SMALL_BUFF))
            diagram.add(icon)
        return diagram

    def get_restricted_diagram(self, diagram):
        restricted_diagram = diagram.copy()
        restricted_diagram.set_x(0)
        restricted_diagram.hypothesis_split.set_opacity(0)
        restricted_diagram.evidence_split.set_opacity(1)
        restricted_diagram.hne_rect.set_opacity(0.1)
        restricted_diagram.nhne_rect.set_opacity(0.1)
        return restricted_diagram

    def get_geometric_fraction(self, diagram):
        fraction = VGroup(
            diagram.he_rect.copy(),
            Line(LEFT, RIGHT),
            VGroup(
                diagram.he_rect.copy(),
                MathTex("+"),
                diagram.nhe_rect.copy(),
            ).arrange(RIGHT, buff=SMALL_BUFF)
        )
        fraction.arrange(DOWN)
        fraction[1].match_width(fraction)
        fraction.to_edge(RIGHT)
        fraction.align_to(diagram.square, UP)
        return fraction
