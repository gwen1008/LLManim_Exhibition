# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示從「現在」到「未來」的時間線，並透過貝葉斯公式的三個理解層次（含圖示與人物）逐步解釋其意義。



from manim import *
class StateGoal(Scene):
    def __init__(self, default_pi_creature_kwargs=None, **kwargs):
        super().__init__(**kwargs)
        if default_pi_creature_kwargs is None:
            default_pi_creature_kwargs = {
                "color": BLUE_B,
                "height": 2,
            }
        self.default_pi_creature_kwargs = default_pi_creature_kwargs

    def construct(self):
        # Zoom to later
        you = PiCreature(**self.default_pi_creature_kwargs)
        line = NumberLine(
            x_range=[-2, 12],
            include_tip=True
        )
        line.to_edge(DOWN, buff=1.5)
        line.to_edge(LEFT, buff=-0.5)

        you.next_to(line.n2p(0), UP)

        you_label = Text("you")
        you_label.next_to(you, RIGHT, buff=MED_LARGE_BUFF)
        you_arrow = Arrow(you_label.get_left(), you.get_right() + 0.5 * LEFT, buff=0.1)

        now_label = Text("Now")
        later_label = Text("Later")
        now_label.next_to(line.n2p(0), DOWN)
        later_label.next_to(line.n2p(10), DOWN)

        self.add(line, now_label)
        self.add(you)
        self.play(
            FadeIn(you_label, shift=LEFT),
            GrowArrow(you_arrow),
            you.animate.change("pondering"),
        )
        self.wait()
        you_label.add(you_arrow)
        self.play(
            you.animate.change("horrified"),
            you.animate.look(DOWN),
            you.animate.next_to(line.n2p(10), UP),
            MaintainPositionRelativeTo(you_label, you),
            FadeIn(later_label, shift=DOWN, scale=0.5),
        )
        self.wait()

        # Add bubble
        bubble = you.get_bubble(
            height=4,
            width=6,
        )
        bubble.set_fill(opacity=0)
        formula = self.get_bayes_formula()
        bubble.position_mobject_inside(formula)

        self.play(
            you.animate.change("confused", bubble),
            Create(bubble),
        )
        self.play(FadeIn(formula))
        self.play(you.animate.change("hooray", formula))
        self.wait(2)

        # Show examples
        icons = VGroup(
            SVGMobject(file_name="science"),
            SVGMobject(file_name="robot"),
        )
        for icon in icons:
            icon.set_stroke(width=0)
            icon.set_fill(GREY)
            icon.set_sheen(1, UL)
            icon.set_height(1.5)
        icons[0].set_stroke(GREY, 3, background=True)
        gold = self.get_gold()
        icons.add(gold)

        icons.arrange(DOWN, buff=MED_LARGE_BUFF)
        icons.to_corner(UL)

        for icon in icons[:2]:
            self.play(
                Write(icon, run_time=2),
                you.animate.change("thinking", icon),
            )
        self.play(
            Blink(you),
            FadeOut(VGroup(
                line, now_label, later_label,
                you_label, you_arrow
            )),
        )
        self.play(
            FadeIn(gold, shift=LEFT),
            you.animate.change("erm", gold),
        )
        self.play(Blink(you))

        # Brief Thompson description
        words = VGroup(
            Text("1988").scale(1.5),
            Text("Tommy Thompson\nand friends"),
        )
        words.arrange(DOWN, buff=0.75)

        ship = ImageMobject("ss_central_america")
        ship.set_width(4)
        ship.move_to(gold, DL)
        ship_title = Text("SS Central America")
        ship_title.next_to(ship, UP)

        words.next_to(ship, RIGHT)

        self.play(
            FadeIn(words[0], shift=LEFT),
            you.animate.change("tease", words),
            FadeOut(icons[:2]),
        )
        self.play(FadeIn(words[1], shift=UP))
        self.wait()

        self.add(ship, gold)
        self.play(
            FadeIn(ship),
            gold.animate.scale(0.2),
            gold.animate.move_to(ship),
        )
        self.play(FadeIn(ship_title, shift=DOWN))
        self.play(you.animate.change("thinking", ship))

        amount = MathTex("> \\$700{,}000{,}000")
        amount.scale(1.5)
        amount.next_to(ship, DOWN, buff=MED_LARGE_BUFF)
        amount.to_edge(LEFT, buff=2)
        amount.set_color(YELLOW)

        gold_copy = gold.copy()
        self.play(
            gold_copy.animate.scale(3),
            gold_copy.animate.next_to(amount, LEFT),
            FadeIn(amount),
        )
        self.play(Blink(you))
        self.wait()
        self.play(LaggedStart(*[
            FadeOut(mob, shift=DOWN)
            for mob in [*words, ship_title, ship, gold, gold_copy, amount]
        ]))

        # Levels of understanding
        # Turn bubble into level points
        level_points = VGroup(*[bubble.copy() for x in range(3)])
        for n, point in enumerate(level_points):
            point.set_width(0.5)
            point.set_height(0.5, stretch=True)
            point.add(*[
                point[-1].copy().scale(1.2**k)
                for k in range(1, n + 1)
            ])
            point[:3].scale(1.2**n, about_point=point[3].get_center())
            point.set_stroke(width=2)
            point.set_fill(opacity=0)
        level_points.arrange(DOWN, buff=LARGE_BUFF)

        title = Text("Levels of understanding")
        title.scale(1.5)
        title.to_corner(UL)
        underline = Line()
        underline.match_width(title)
        underline.move_to(title, DOWN)
        title.add(underline)

        level_points.next_to(title, DOWN, buff=1.5)
        level_points.to_edge(LEFT)
        level_points.set_color_by_gradient(GREEN, YELLOW, RED)

        self.remove(bubble)
        self.play(
            formula.animate.to_corner(UR),
            FadeOut(you),
            *[
                ReplacementTransform(bubble.copy(), point)
                for point in level_points
            ],
        )
        self.play(Write(title, run_time=1))
        self.wait()

        # Write level 1
        level_labels = VGroup(
            Text("What is it saying?"),
            Text("Why is it true?"),
            Text("When is it useful?"),
        )
        for lp, ll in zip(level_points, level_labels):
            ll.scale(1.25)
            ll.set_color(lp.get_color())
            ll.next_to(lp, RIGHT)

        formula_parts = VGroup(
            formula.prior,
            formula.likelihood,
            formula.p_evidence,
            formula.posterior,
        ).copy()
        formula_parts.generate_target()
        formula_parts.target.scale(1.5)
        formula_parts.target.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        formula_parts.target.next_to(formula, DOWN, buff=LARGE_BUFF)
        formula_parts.target.shift(3 * LEFT)

        equal_signs = VGroup(*[
            Text("=").next_to(fp, RIGHT)
            for fp in formula_parts.target
        ])

        kw = {
            "tex_to_color_map": {
                "hypothesis": BLUE,
                "evidence": GREEN,
            },
            "alignment": "",
        }
        meanings = VGroup(
            Text("Probability a hypothesis is true\n(before any evidence)", **kw),
            Text("Probability of seeing the evidence \\quad \\\\if the hypothesis is true", **kw),
            Text("Probability of seeing the evidence", **kw),
            Text("Probability a hypothesis is true\ngiven some evidence", **kw),
        )
        for meaning, equals in zip(meanings, equal_signs):
            meaning.scale(0.5)
            meaning.next_to(equals, RIGHT)

        self.play(
            FadeIn(level_labels[0], lag_ratio=0.1),
            MoveToTarget(formula_parts),
            LaggedStart(*[FadeIn(eq, shift=RIGHT) for eq in equal_signs]),
            LaggedStart(*[FadeIn(m) for m in meanings]),
        )
        self.wait()

        # Write level 2
        diagram = self.BayesDiagram(0.35, 0.5, 0.2, height=2.5)
        diagram.next_to(formula, DOWN, aligned_edge=LEFT)

        braces = VGroup(*[
            Brace(diagram.he_rect, vect, buff=SMALL_BUFF)
            for vect in [DOWN, LEFT]
        ])

        formula_parts.generate_target()
        formula_parts.target[:2].scale(0.5)
        formula_parts.target[0].next_to(braces[0], DOWN, buff=SMALL_BUFF)
        formula_parts.target[1].next_to(braces[1], LEFT, buff=SMALL_BUFF)

        pe_picture = VGroup(
            diagram.he_rect.copy(),
            MathTex("+"),
            diagram.nhe_rect.copy()
        )
        pe_picture.arrange(RIGHT, buff=SMALL_BUFF)
        pe_picture.next_to(equal_signs[2], RIGHT)

        phe_picture = VGroup(
            diagram.he_rect.copy(),
            Line().match_width(pe_picture),
            pe_picture.copy(),
        )
        phe_picture.arrange(DOWN, buff=MED_SMALL_BUFF)
        phe_picture.next_to(equal_signs[3], RIGHT)

        pe_picture.scale(0.5, about_edge=LEFT)
        phe_picture.scale(0.3, about_edge=LEFT)

        self.play(
            FadeOut(meanings),
            FadeOut(equal_signs[:2]),
            MoveToTarget(formula_parts),
            FadeIn(diagram),
            LaggedStart(*[GrowFromCenter(b) for b in braces]),
            FadeIn(level_labels[1], lag_ratio=0.1),
            level_labels[0].animate.set_opacity(0.5),
        )
        self.play(
            TransformFromCopy(diagram.he_rect, pe_picture[0]),
            TransformFromCopy(diagram.nhe_rect, pe_picture[2]),
            FadeIn(pe_picture[1]),
        )
        self.play(
            TransformFromCopy(pe_picture, phe_picture[2]),
            TransformFromCopy(pe_picture[0], phe_picture[0]),
            Create(phe_picture[1])
        )
        self.wait()

        # Write level 3
        steve = self.Steve(height=3)
        steve.to_edge(RIGHT, buff=2)

        arrow = Arrow(level_points.get_bottom(), level_points.get_top(), buff=0)
        arrow.shift(0.25 * LEFT)

        self.play(
            LaggedStart(*[
                FadeOut(mob, shift=3*RIGHT)
                for mob in [
                    VGroup(diagram, braces, formula_parts[:2]),
                    VGroup(formula_parts[2], equal_signs[2], pe_picture),
                    VGroup(formula_parts[3], equal_signs[3], phe_picture),
                ]
            ]),
            FadeIn(level_labels[2], lag_ratio=0.1),
            level_labels[1].animate.set_opacity(0.5),
        )
        self.wait()
        self.play(
            GrowArrow(arrow),
            level_points.animate.shift(0.5 * RIGHT),
            level_labels.animate.shift(0.5 * RIGHT),
            level_labels.animate.set_opacity(1),
        )
        self.wait()
        self.play(Write(steve, run_time=3))
        self.wait()

        # Transition to next scene
        self.play(
            steve.animate.to_corner(UR),
            Uncreate(arrow),
            LaggedStart(*[
                FadeOut(mob, shift=DOWN)
                for mob in [
                    title,
                    formula,
                    *level_points,
                    *level_labels,
                ]
            ]),
        )
        self.wait()

    def get_gold(self):
        gold = SVGMobject(file_name="gold_bars")[0]
        gold.set_stroke(width=0)
        gold.set_fill(GOLD)
        gold.set_sheen(0.5, UP)
        gold.flip(UP)
        gold_copy = gold.copy()
        gold_copy.shift(2 * OUT)

        rects = VGroup()
        for curve in gold:
            p1 = curve.get_points()[0]
            p2 = curve.get_points()[-1]
            rect = Polygon(p1, p2, p2 + 2 * OUT, p1 + 2 * OUT)
            rect.match_style(gold)
            rects.add(rect)
        rects.sort(lambda p: p[1])
        gold.add(*rects)
        gold.add(gold_copy)

        gold.rotate(2 * DEGREES, UP)
        gold.rotate(2 * DEGREES, RIGHT)
        gold.set_shade_in_3d(True)
        gold.set_height(1.5)
        gold.set_stroke(BLACK, 0.5)
        return gold

    def get_bayes_formula(self):
        # 簡化的貝葉斯公式表示
        formula = MathTex(
            "P(H|E) = \\frac{P(E|H) \\cdot P(H)}{P(E)}"
        )
        formula.prior = formula[0][6:8]  # P(H)
        formula.likelihood = formula[0][9:13]  # P(E|H)
        formula.p_evidence = formula[0][14:16]  # P(E)
        formula.posterior = formula[0][0:4]  # P(H|E)
        return formula

    class BayesDiagram:
        def __init__(self, h_width, e_height, overlap, height=2.5):
            self.height = height
            self.h_width = h_width
            self.e_height = e_height
            self.overlap = overlap
            
            # 創建矩形表示假設和證據
            self.h_rect = Rectangle(
                width=h_width * height,
                height=height,
                color=BLUE,
                fill_opacity=0.3
            )
            self.e_rect = Rectangle(
                width=height,
                height=e_height * height,
                color=GREEN,
                fill_opacity=0.3
            )
            
            # 重疊區域
            self.he_rect = Rectangle(
                width=overlap * height,
                height=e_height * height,
                color=YELLOW,
                fill_opacity=0.5
            )
            
            # 非重疊區域
            self.nhe_rect = Rectangle(
                width=(h_width - overlap) * height,
                height=e_height * height,
                color=BLUE,
                fill_opacity=0.3
            )
            
            # 定位
            self.h_rect.move_to(ORIGIN)
            self.e_rect.move_to(ORIGIN)
            self.he_rect.move_to(ORIGIN)
            self.nhe_rect.next_to(self.he_rect, LEFT, buff=0)
            
            self.group = VGroup(self.h_rect, self.e_rect, self.he_rect, self.nhe_rect)

    class Steve:
        def __init__(self, height=3):
            self.group = VGroup()
            # 創建簡單的人物表示
            head = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            body = Rectangle(width=0.6, height=0.8, color=BLUE, fill_opacity=1)
            body.next_to(head, DOWN, buff=0)
            
            self.group.add(head, body)
            self.group.set_height(height)
