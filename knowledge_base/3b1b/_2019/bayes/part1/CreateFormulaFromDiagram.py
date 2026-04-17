# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 從貝葉斯圖表逐步推導出貝葉斯公式，並解釋先驗、似然、反似然和後驗等概念。



from manim import *
class CreateFormulaFromDiagram(Scene):
    def __init__(
        self,
        tex_to_color_map=None,
        bayes_diagram_config=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        if tex_to_color_map is None:
            tex_to_color_map = {
                "P": WHITE,
                "H": BLUE,
                "E": GREEN,
                "\\neg": RED,
            }
        self.tex_to_color_map = tex_to_color_map
        
        if bayes_diagram_config is None:
            bayes_diagram_config = {
                "prior": 1 / 21,
                "likelihood": 0.4,
                "antilikelihood": 0.1,
                "not_evidence_color1": GREY,
                "not_evidence_color2": GREY_D,
                "prior_rect_direction": UP,
            }
        self.bayes_diagram_config = bayes_diagram_config

    def construct(self):
        t2c = self.tex_to_color_map

        # Add posterior
        posterior = MathTex("P(H|E)", tex_to_color_map=t2c)
        posterior.to_corner(UR)
        posterior_words = Text("Goal: ")
        posterior_words.next_to(posterior, LEFT, aligned_edge=UP)
        self.add(posterior)
        self.add(posterior_words)

        # Show prior
        diagram = self.get_diagram()

        prior_label = MathTex("P(H)", tex_to_color_map=t2c)
        prior_label.add_updater(
            lambda m: m.next_to(diagram.h_brace, UP, SMALL_BUFF)
        )

        prior_example = MathTex("= 1 / 21")
        prior_example.add_updater(
            lambda m: m.next_to(prior_label, RIGHT).shift(0.03 * UP)
        )

        prior_arrow = Arrow(0.7 * RIGHT, color=WHITE)
        prior_arrow.next_to(prior_label, LEFT, SMALL_BUFF)
        prior_word = Text("``Prior''")
        prior_word.next_to(prior_arrow, LEFT, SMALL_BUFF)
        prior_word.align_to(prior_label[0], DOWN)
        prior_word.set_color(BLUE)

        self.add(diagram)
        self.play(ShowIncreasingSubsets(diagram.people, run_time=2))
        self.wait()
        self.play(
            diagram.hypothesis_split.set_opacity, 1,
            FadeIn(diagram.h_brace),
            FadeIn(prior_label, shift=DOWN),
        )
        self.wait()
        self.play(FadeIn(prior_example))
        self.play(
            LaggedStartMap(
                Indicate, diagram.people[::10],
                color=BLUE,
            )
        )
        self.wait()
        self.play(
            FadeIn(prior_word, RIGHT),
            GrowArrow(prior_arrow)
        )
        self.wait()
        prior_group = VGroup(
            prior_word, prior_arrow,
            prior_label, prior_example,
            diagram.h_brace,
        )

        # First likelihood split
        like_example = MathTex("= 0.4")
        like_example.add_updater(
            lambda m: m.next_to(diagram.he_brace, LEFT)
        )
        like_example.update()

        like_label = MathTex("P(E|H)", tex_to_color_map=t2c)
        like_label.add_updater(
            lambda m: m.next_to(like_example, LEFT)
        )
        like_label.update()

        like_word = Text("``Likelihood''")
        like_word.next_to(like_label, UP, buff=LARGE_BUFF, aligned_edge=LEFT)
        like_arrow = Arrow(
            like_word.get_bottom(),
            like_label.get_top(),
            buff=0.2,
            color=WHITE
        )

        limit_arrow = Arrow(0.5 * UP, color=WHITE)
        limit_arrow.next_to(like_label.get_part_by_tex("|"), UP, SMALL_BUFF)
        limit_arrow.set_stroke(WHITE, 4)
        limit_word = Text("Limit\nyour\nview")
        limit_word.next_to(limit_arrow, UP)

        hne_people = diagram.people[:6]
        he_people = diagram.people[6:10]
        nhe_people = diagram.people[19::10]
        nhne_people = diagram.people[10:]
        nhne_people.remove(*nhe_people)

        for group in [hne_people, nhne_people]:
            group.generate_target()
            group.target.set_opacity(0.25)
            group.target.set_stroke(BLACK, 0, background=True)

        self.play(
            diagram.he_rect.set_opacity, 1,
            diagram.hne_rect.set_opacity, 1,
            MoveToTarget(hne_people),
            GrowFromCenter(diagram.he_brace),
            FadeIn(like_label, RIGHT),
            FadeIn(like_example, RIGHT),
        )
        self.wait()
        self.play(
            ShowCreationThenFadeAround(
                like_label.get_part_by_tex("E"),
                surrounding_rectangle_config={
                    "color": GREEN
                }
            ),
        )
        self.play(WiggleOutThenIn(like_label.get_part_by_tex("|")))
        self.play(
            ShowCreationThenFadeAround(
                like_label.get_part_by_tex("H")
            ),
        )
        self.wait()
        self.play(
            diagram.people[10:].set_opacity, 0.2,
            diagram.nh_rect.set_opacity, 0.2,
            FadeIn(limit_word, DOWN),
            GrowArrow(limit_arrow),
            rate_func=there_and_back_with_pause,
            run_time=6,
        )
        self.wait()
        self.play(
            Write(like_word, run_time=1),
            GrowArrow(like_arrow),
        )
        self.wait()

        # Show anti-likelihood
        anti_label = MathTex("P(E| \\neg H)", tex_to_color_map=t2c)
        anti_label.add_updater(
            lambda m: m.next_to(diagram.nhe_brace, RIGHT)
        )

        anti_example = MathTex("= 0.1")
        anti_example.add_updater(
            lambda m: m.next_to(anti_label, RIGHT).align_to(anti_label[0], DOWN)
        )

        neg_sym = anti_label.get_part_by_tex("\\neg").copy()
        neg_sym.generate_target()
        neg_sym.target.scale(2.5)
        not_word = Text("means ", "``not''")
        not_word[1].set_color(RED)
        neg_group = VGroup(neg_sym.target, not_word)
        neg_group.arrange(RIGHT)
        neg_group.next_to(anti_label, UP, LARGE_BUFF)
        neg_group.to_edge(RIGHT, buff=MED_SMALL_BUFF)

        diagram.nhe_rect.set_opacity(1)
        diagram.nhe_rect.save_state()
        diagram.nhe_rect.become(diagram.nh_rect)
        self.play(
            Restore(diagram.nhe_rect),
            GrowFromCenter(diagram.nhe_brace),
            MoveToTarget(nhne_people),
            FadeIn(anti_label, LEFT),
            FadeIn(anti_example, LEFT),
        )
        diagram.nhne_rect.set_opacity(1)
        self.wait()
        self.play(
            ShowCreationThenFadeAround(
                anti_label[2],
                surrounding_rectangle_config={"color": GREEN},
            )
        )
        self.play(
            ShowCreationThenFadeAround(
                anti_label[4:6],
                surrounding_rectangle_config={"color": RED},
            )
        )
        self.wait()
        self.play(
            MoveToTarget(neg_sym),
            FadeIn(not_word)
        )
        self.wait()
        self.play(
            FadeOut(not_word),
            Transform(neg_sym, anti_label.get_part_by_tex("\\neg"))
        )
        self.remove(neg_sym)

        # Recall final answer, geometrically
        he_group = VGroup(diagram.he_rect, he_people)
        nhe_group = VGroup(diagram.nhe_rect, nhe_people)

        denom = VGroup(
            he_group.copy(),
            MathTex("+"),
            nhe_group.copy(),
        )
        denom.arrange(RIGHT)
        answer = VGroup(
            he_group.copy(),
            Underline(denom, stroke_width=2),
            denom,
        )
        answer.arrange(DOWN)
        answer.scale(0.5)
        answer.to_edge(UP, MED_SMALL_BUFF)
        answer.shift(LEFT)

        equals = MathTex("=")
        posterior.generate_target()

        post_group = VGroup(posterior.target, equals, answer)
        post_group.arrange(RIGHT)
        post_group.to_corner(UL)

        post_word = Text("``Posterior''")
        post_word.set_color(YELLOW)
        post_word.to_corner(UL, buff=MED_SMALL_BUFF)

        post_arrow = Arrow(
            post_word.get_bottom(),
            posterior.target[1].get_top(),
            buff=0.2,
            color=WHITE
        )
        post_arrow.set_stroke(WHITE, 5)

        dividing_line = DashedLine(ORIGIN, FRAME_WIDTH * RIGHT)
        dividing_line.set_stroke(WHITE, 1)
        dividing_line.next_to(answer, DOWN)
        dividing_line.set_x(0)

        diagram.add(
            diagram.h_brace,
            diagram.he_brace,
            diagram.nhe_brace,
        )
        diagram.generate_target(use_deepcopy=True)
        diagram.target.scale(0.5, about_edge=DL)
        diagram.target.refresh_braces()

        like_group = VGroup(like_word, like_arrow)
        like_vect = like_group.get_center() - like_label.get_center()
        self.play(
            Create(dividing_line),
            MoveToTarget(diagram),
            MaintainPositionRelativeTo(like_group, like_label),
            MaintainPositionRelativeTo(
                VGroup(prior_word, prior_arrow),
                prior_label,
            ),
            MoveToTarget(posterior),
            ReplacementTransform(posterior_words, equals),
        )
        like_group.move_to(like_label.get_center() + like_vect)
        self.wait()
        self.play(TransformFromCopy(he_group, answer[0]))
        self.play(Create(answer[1]))
        self.play(LaggedStart(
            TransformFromCopy(he_group, answer[2][0]),
            GrowFromCenter(answer[2][1]),
            TransformFromCopy(nhe_group, answer[2][2]),
        ))
        self.wait()

        # Write final answer, as a formula
        formula = MathTex(
            "=", "{P(H) P(E | H)", "\\over",
            "P(H) P(E | H) + P(\\neg H) P(E | \\neg H)}",
            tex_to_color_map=t2c
        )
        formula.scale(0.9)
        formula.next_to(answer, RIGHT)

        ph = formula[2:6]
        peh = formula[6:12]
        over = formula.get_part_by_tex("\\over")
        ph2 = formula[13:17]
        peh2 = formula[17:23]
        pnh = formula[23:28]
        penh = formula[28:]

        parts = VGroup(ph, peh, ph2, peh2, pnh, penh)
        parts.save_state()

        np1 = MathTex("(\\# I )")[0]
        person = self.create_person()
        person.replace(np1[2], dim_to_match=1)
        person.scale(1.5)
        np1.submobjects[2] = person

        np1.match_height(ph)
        np1.next_to(ph, LEFT, SMALL_BUFF)
        VGroup(np1, ph, peh).match_x(over)

        np2 = np1.copy()
        np2.next_to(ph2, LEFT, SMALL_BUFF)
        VGroup(np2, ph2, peh2).match_width(
            VGroup(ph2, peh2), about_edge=RIGHT
        )

        np3 = np1.copy()
        np3.next_to(pnh, LEFT, SMALL_BUFF)
        VGroup(np3, pnh, penh).match_width(
            VGroup(pnh, penh), about_edge=RIGHT
        )

        nps = VGroup(np1, np2, np3)
        crosses = VGroup(*[Cross(np) for np in nps])

        top_brace = Brace(np1, UP, buff=SMALL_BUFF)
        top_count = Integer(210)
        top_count.add_updater(lambda m: m.next_to(top_brace, UP, SMALL_BUFF))

        low_brace = Brace(np3, DOWN, buff=SMALL_BUFF)
        low_count = Integer(210)
        low_count.add_updater(lambda m: m.next_to(low_brace, DOWN, SMALL_BUFF))

        h_rect = Rectangle(  # Highlighting rectangle
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.25,
        )
        h_rect.replace(diagram.square, stretch=True)

        s_rect = SurroundingRectangle(answer[0])

        diagram.refresh_braces()
        nh_group = VGroup(
            diagram.nh_brace,
            MathTex("P(\\neg H)", tex_to_color_map=t2c),
            MathTex("= 20 / 21"),
        )
        nh_group[1].next_to(nh_group[0], UP, SMALL_BUFF)
        nh_group[2].next_to(nh_group[1], RIGHT, SMALL_BUFF)

        self.play(
            Write(formula.get_part_by_tex("=")),
            Write(formula.get_part_by_tex("\\over")),
            run_time=1
        )
        self.play(Create(s_rect))
        self.wait()
        self.play(
            FadeIn(np1),
            FadeIn(top_brace),
            FadeIn(top_count),
        )
        self.wait()
        self.play(h_rect.replace, diagram.h_rect, {"stretch": True})
        self.play(
            TransformFromCopy(prior_label, ph),
            top_brace.become, Brace(VGroup(np1, ph), UP, buff=SMALL_BUFF),
            ChangeDecimalToValue(top_count, 10),
        )
        self.wait()
        self.play(h_rect.replace, diagram.he_rect, {"stretch": True})
        self.play(
            TransformFromCopy(like_label, peh),
            top_brace.become, Brace(VGroup(np1, peh), UP, buff=SMALL_BUFF),
            ChangeDecimalToValue(top_count, 4)
        )
        self.wait()

        self.play(
            s_rect.move_to, answer[2][0],
            TransformFromCopy(np1, np2),
            TransformFromCopy(ph, ph2),
            TransformFromCopy(peh, peh2),
        )
        self.wait()

        self.play(
            FadeOut(h_rect),
            s_rect.become, SurroundingRectangle(answer[2][2]),
            FadeOut(prior_group),
            FadeIn(nh_group),
        )
        self.wait()
        h_rect.replace(diagram.square, stretch=True)
        self.play(
            FadeIn(np3),
            FadeIn(low_brace),
            FadeIn(low_count),
        )
        self.play(h_rect.replace, diagram.nh_rect, {"stretch": True})
        self.play(
            TransformFromCopy(nh_group[1], pnh),
            low_brace.become, Brace(VGroup(np3, pnh), DOWN, buff=SMALL_BUFF),
            ChangeDecimalToValue(low_count, 200),
        )
        self.play(h_rect.replace, diagram.nhe_rect, {"stretch": True})
        self.play(
            TransformFromCopy(anti_label, penh),
            low_brace.become, Brace(VGroup(np3, penh), DOWN, buff=SMALL_BUFF),
            ChangeDecimalToValue(low_count, 20),
        )
        self.wait()

        # Clean up
        self.play(
            FadeOut(nh_group),
            FadeOut(s_rect),
            FadeOut(h_rect),
            FadeIn(prior_group),
        )
        self.wait()

        self.play(
            Create(crosses),
            FadeOut(low_brace),
            FadeOut(top_brace),
            FadeOut(low_count),
            FadeOut(top_count),
        )
        self.wait()
        self.play(
            Restore(parts),
            FadeOut(crosses),
            FadeOut(nps),
            answer.set_opacity, 0.2
        )
        self.wait()

        # Write Bayes' theorem
        formula_rect = SurroundingRectangle(formula[1:])
        formula_rect.set_stroke(TEAL, 2)

        bayes_words = Text("Bayes' theorem")
        bayes_words.scale(1.5)
        bayes_words.next_to(formula_rect, UP, SMALL_BUFF)
        bayes_words.match_color(formula_rect)

        self.play(Create(formula_rect))
        self.play(FadeIn(bayes_words, shift=DOWN))
        self.wait()

        # Simplify denominator
        simpler_form = self.get_bayes_formula()[7:]
        simpler_form.move_to(answer)
        pe = simpler_form[-4:].copy()
        pe.save_state()

        big_denom_rect = SurroundingRectangle(VGroup(ph2, penh))
        lil_denom_rect = SurroundingRectangle(pe)
        for rect in big_denom_rect, lil_denom_rect:
            rect.set_stroke(BLUE, 0)
            rect.set_fill(BLUE, 0.25)
        pe.move_to(big_denom_rect)
        pe.set_opacity(0)

        self.play(
            FadeOut(answer),
            FadeIn(simpler_form[:-4])
        )
        self.play(TransformFromCopy(formula_rect, big_denom_rect))
        self.wait()
        self.play(
            Restore(pe),
            ReplacementTransform(big_denom_rect, lil_denom_rect),
            Transform(
                formula_rect,
                SurroundingRectangle(simpler_form, color=TEAL),
            ),
            bayes_words.match_x, simpler_form,
        )
        self.remove(pe)
        self.add(simpler_form)
        self.wait()

        # Show all evidence cases
        he_group_copy = he_group.copy()
        nhe_group_copy = nhe_group.copy()
        copies = VGroup(he_group_copy, nhe_group_copy)

        self.play(
            copies.arrange, RIGHT, {"buff": LARGE_BUFF},
            copies.move_to, DOWN,
            copies.to_edge, RIGHT, LARGE_BUFF,
        )
        self.wait()
        self.play(
            he_group_copy.next_to, VGroup(ph2, peh2), DOWN,
        )
        self.play(
            nhe_group_copy.next_to, VGroup(pnh, penh), DOWN,
        )
        self.wait()
        self.play(
            FadeOut(copies),
            FadeOut(lil_denom_rect),
        )
        self.wait()

        # Name posterior
        self.play(
            GrowArrow(post_arrow),
            FadeIn(post_word, RIGHT),
            FadeOut(formula_rect),
            FadeOut(bayes_words),
        )
        self.wait()

        # Show confusion
        randy = self.create_randolph()
        randy.flip()
        randy.next_to(dividing_line, DOWN)
        randy.to_edge(RIGHT)

        prior_rect = SurroundingRectangle(prior_word)
        post_rect = SurroundingRectangle(post_word)
        VGroup(prior_rect, post_rect).set_stroke(WHITE, 2)

        self.play(FadeIn(randy))
        self.play(randy.animate.change("confused", formula))
        self.play(Blink(randy))
        self.play(randy.animate.change("horrified", formula))
        self.play(randy.animate.look_at(diagram))
        self.play(Blink(randy))
        self.play(randy.animate.look_at(formula))
        self.play(randy.animate.change("tired"))
        self.wait(2)
        self.play(
            randy.animate.change("pondering", prior_label),
            Create(prior_rect)
        )
        self.play(Blink(randy))
        self.play(
            ReplacementTransform(prior_rect, post_rect),
            randy.animate.look_at(post_rect),
        )
        self.play(randy.animate.change("thinking"))
        self.play(FadeOut(post_rect))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.animate.look_at(formula))
        self.play(Blink(randy))
        self.wait()

        # Transition to next scene
        return  # Skip
        to_move = VGroup(posterior, formula)
        self.remove(to_move, *to_move, *to_move[1])
        to_move.generate_target()
        to_move.target[1].scale(1 / 0.9)
        to_move.target.arrange(RIGHT)
        to_move.target.to_corner(UL)

        everything = Group(*self.mobjects)

        self.play(
            LaggedStartMap(FadeOutAndShiftDown, everything),
            MoveToTarget(to_move, rate_func=squish_rate_func(smooth, 0.5, 1)),
            run_time=2,
        )

    def get_diagram(self, include_people=True):
        # 簡化的貝葉斯圖表實現
        diagram = self.create_bayes_diagram()
        diagram.set_height(5.5)
        diagram.set_width(5.5, stretch=True)
        diagram.move_to(0.5 * DOWN)
        self.add_brace_attrs(diagram)

        diagram.evidence_split.set_opacity(0)
        diagram.hypothesis_split.set_opacity(0)
        diagram.nh_rect.set_fill(GREY_D)

        if include_people:
            people = VGroup(*[self.create_person() for x in range(210)])
            people.set_color(interpolate_color(GREY_B, WHITE, 0.5))
            people.arrange_in_grid(rows=10, cols=21)
            people.set_width(diagram.get_width() - SMALL_BUFF)
            people.set_height(diagram.get_height() - SMALL_BUFF, stretch=True)
            people.move_to(diagram)
            people[10:].set_color(GREEN_D)
            people.set_stroke(BLACK, 2, background=True)

            diagram.add(people)
            diagram.people = people

        return diagram

    def create_bayes_diagram(self):
        # 創建簡化的貝葉斯圖表
        square = Square(side_length=5)
        square.set_fill(BLUE_E, opacity=0.5)
        
        # 創建分割線
        h_line = Line(square.get_left(), square.get_right())
        h_line.shift(UP * square.height * (1 - self.bayes_diagram_config["prior"]))
        
        v_line = Line(square.get_top(), square.get_bottom())
        v_line.shift(RIGHT * square.width * self.bayes_diagram_config["likelihood"])
        
        # 創建矩形區域
        h_rect = Rectangle(
            width=square.width,
            height=square.height * self.bayes_diagram_config["prior"],
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_color=BLUE
        )
        h_rect.align_to(square, UP)
        
        he_rect = Rectangle(
            width=square.width * self.bayes_diagram_config["likelihood"],
            height=square.height * self.bayes_diagram_config["prior"],
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_color=GREEN
        )
        he_rect.align_to(square, UP + LEFT)
        
        nhe_rect = Rectangle(
            width=square.width * self.bayes_diagram_config["antilikelihood"],
            height=square.height * (1 - self.bayes_diagram_config["prior"]),
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_color=GREEN
        )
        nhe_rect.align_to(square, DOWN + LEFT)
        
        # 創建括號
        h_brace = Brace(h_rect, UP)
        he_brace = Brace(he_rect, LEFT)
        nhe_brace = Brace(nhe_rect, RIGHT)
        nh_brace = Brace(
            Rectangle(
                width=square.width,
                height=square.height * (1 - self.bayes_diagram_config["prior"])
            ),
            DOWN
        )
        
        diagram = VGroup(square, h_line, v_line, h_rect, he_rect, nhe_rect)
        diagram.square = square
        diagram.h_line = h_line
        diagram.v_line = v_line
        diagram.h_rect = h_rect
        diagram.he_rect = he_rect
        diagram.nhe_rect = nhe_rect
        diagram.nh_rect = Rectangle(
            width=square.width,
            height=square.height * (1 - self.bayes_diagram_config["prior"]),
            fill_color=GREY_D,
            fill_opacity=0.3,
            stroke_color=GREY_D
        ).align_to(square, DOWN)
        
        diagram.h_brace = h_brace
        diagram.he_brace = he_brace
        diagram.nhe_brace = nhe_brace
        diagram.nh_brace = nh_brace
        
        diagram.hypothesis_split = h_line
        diagram.evidence_split = v_line
        diagram.hne_rect = Rectangle(
            width=square.width * (1 - self.bayes_diagram_config["likelihood"]),
            height=square.height * self.bayes_diagram_config["prior"],
            fill_color=GREY,
            fill_opacity=0.3,
            stroke_color=GREY
        ).next_to(he_rect, RIGHT, buff=0)
        
        diagram.nhne_rect = Rectangle(
            width=square.width * (1 - self.bayes_diagram_config["antilikelihood"]),
            height=square.height * (1 - self.bayes_diagram_config["prior"]),
            fill_color=GREY,
            fill_opacity=0.3,
            stroke_color=GREY
        ).next_to(nhe_rect, UP, buff=0)
        
        return diagram

    def add_brace_attrs(self, diagram):
        # 添加括號屬性
        pass

    def create_person(self):
        # 創建簡化的人物圖形
        head = Circle(radius=0.1, color=WHITE, fill_opacity=1)
        body = Line(ORIGIN, DOWN * 0.2, color=WHITE)
        person = VGroup(head, body)
        return person

    def create_randolph(self):
        # 創建簡化的角色
        return SVGMobject(
            "https://raw.githubusercontent.com/ManimCommunity/manim/main/assets/svg/thinking.svg",
            color=BLUE
        ).scale(0.5)

    def get_bayes_formula(self):
        # 返回貝葉斯公式
        return MathTex(
            "P(H|E) = \\frac{P(H)P(E|H)}{P(E)}",
            tex_to_color_map=self.tex_to_color_map
        )
