# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示貝葉斯更新在撲克牌情境下的視覺化過程，包括先驗概率、條件概率的變化，以及後驗概率的計算。



from manim import *
class UpdatePokerPrior(Scene):
    def __init__(self, double_heart_template="HH", cash_string="\\$\\$\\$", **kwargs):
        super().__init__(**kwargs)
        self.double_heart_template = double_heart_template
        self.cash_string = cash_string

    def construct(self):
        self.add_sample_space()
        self.add_top_conditionals()
        self.react_to_top_conditionals()
        self.add_bottom_conditionals()
        self.ask_where_conditionals_come_from()
        self.vary_conditionals()
        self.show_restricted_space()
        self.write_P_flush_given_bet()
        self.reshape_rectangles()
        self.compare_prior_to_posterior()
        self.preview_tweaks()
        self.tweak_non_flush_case()
        self.tweak_flush_case()
        self.tweak_prior()
        self.compute_posterior()

    def add_sample_space(self):
        p = 1./22
        sample_space = Rectangle(height=3, width=4, fill_opacity=0)
        sample_space.shift(LEFT)
        
        # 創建水平分割
        top_part = Rectangle(height=p*3, width=4, fill_color=RED, fill_opacity=0.7)
        bottom_part = Rectangle(height=(1-p)*3, width=4, fill_color=BLUE_E, fill_opacity=0.7)
        top_part.next_to(sample_space.get_top(), DOWN, buff=0)
        bottom_part.next_to(top_part.get_bottom(), DOWN, buff=0)
        
        sample_space_group = VGroup(top_part, bottom_part)
        sample_space_group.move_to(sample_space.get_center())
        
        labels = self.get_prior_labels(p)
        braces_and_labels = self.get_side_braces_and_labels(sample_space_group, labels)

        self.play(
            LaggedStartMap(FadeIn, sample_space_group),
            Write(braces_and_labels)
        )
        self.wait()

        sample_space_group.add(braces_and_labels)
        self.sample_space = sample_space_group
        self.horizontal_parts = [top_part, bottom_part]

    def add_top_conditionals(self):
        top_part = self.horizontal_parts[0]
        color = average_color(YELLOW, GREEN, GREEN)
        p = 0.97
        
        # 創建垂直分割
        left_part = Rectangle(height=top_part.height, width=p*4, fill_color=color, fill_opacity=0.7)
        right_part = Rectangle(height=top_part.height, width=(1-p)*4, fill_color=BLUE, fill_opacity=0.7)
        left_part.next_to(top_part.get_left(), RIGHT, buff=0)
        right_part.next_to(left_part.get_right(), RIGHT, buff=0)
        
        vertical_parts = VGroup(left_part, right_part)
        top_part.add(vertical_parts)
        
        label = self.get_conditional_label(p, True)
        brace = Brace(top_part, UP)
        label.next_to(brace, UP)

        explanation = Text(
            "Probability of high bet given flush",
            font_size=24
        )
        explanation.set_color_by_text("high bet", GREEN)
        explanation.set_color_by_text("flush", RED)
        explanation.next_to(label, UP)

        self.play(
            FadeIn(vertical_parts),
            FadeIn(label),
            GrowFromCenter(brace),
        )
        self.play(Write(explanation, run_time=3))
        self.wait(2)

        self.sample_space.add(brace, label)
        self.top_explanation = explanation
        self.top_conditional_rhs = label[-1]
        self.top_vertical_parts = vertical_parts

    def react_to_top_conditionals(self):
        her = SVGMobject("pi_creatures/plain").set_color(BLUE_B)
        her.flip(RIGHT)
        her.next_to(self.sample_space, RIGHT)
        her.to_edge(RIGHT)
        
        # 簡化眼鏡效果
        glasses = Rectangle(height=0.2, width=0.8, fill_color=BLACK, fill_opacity=0.5)
        glasses.move_to(her.eyes.get_center() if hasattr(her, 'eyes') else her.get_center())
        glasses.save_state()
        glasses.shift(UP)
        glasses.set_fill(opacity=0)
        her.glasses = glasses

        self.play(FadeIn(her))
        self.play(glasses.animate.restore())
        self.play(
            her.animate.set_color(GREEN),  # 簡化表情變化
            Animation(glasses)
        )
        self.wait(2)

        self.her = her
        
    def add_bottom_conditionals(self):
        her = self.her
        bottom_part = self.horizontal_parts[1]
        p = 0.3
        
        # 創建垂直分割
        left_part = Rectangle(height=bottom_part.height, width=p*4, fill_color=GREEN_E, fill_opacity=0.7)
        right_part = Rectangle(height=bottom_part.height, width=(1-p)*4, fill_color=BLUE_E, fill_opacity=0.7)
        left_part.next_to(bottom_part.get_left(), RIGHT, buff=0)
        right_part.next_to(left_part.get_right(), RIGHT, buff=0)
        
        vertical_parts = VGroup(left_part, right_part)
        bottom_part.add(vertical_parts)
        
        label = self.get_conditional_label(p, False)
        brace = Brace(bottom_part, DOWN)
        label.next_to(brace, DOWN)

        explanation = Text(
            "Probability of high bet given no flush",
            font_size=24
        )
        explanation.set_color_by_text("high bet", GREEN)
        explanation.set_color_by_text("no flush", RED)
        explanation.next_to(label, DOWN)

        self.play(DrawBorderThenFill(vertical_parts))
        self.play(
            GrowFromCenter(brace),
            FadeIn(label)
        )
        
        # 簡化表情變化
        self.play(
            her.animate.set_color(GRAY),
            MaintainPositionRelativeTo(her.glasses, her)
        )
        self.wait()
        
        # 簡化轉換動畫
        self.play(
            TransformFromCopy(label[:2], explanation[:2]),
            TransformFromCopy(label[2:4], explanation[2:4]),
            run_time=2
        )
        self.wait()
        self.play(Write(label[-2:]))
        self.wait(2)
        self.play(*list(map(FadeOut, [her, her.glasses])))

        self.sample_space.add(brace, label)
        self.bottom_explanation = explanation
        self.bottom_conditional_rhs = label[-1]
        self.bottom_vertical_parts = vertical_parts

    def ask_where_conditionals_come_from(self):
        randy = SVGMobject("pi_creatures/plain").set_color(GRAY)
        randy.flip(RIGHT)
        randy.scale(0.75)
        randy.to_edge(RIGHT)
        randy.shift(2*DOWN)
        
        words = Text("Where do these\nnumbers come from?", font_size=24)
        numbers_word = words.get_part_by_text("numbers")
        numbers_word.set_color(YELLOW)
        
        bubble = ThoughtBubble(height=3, width=4)
        bubble.pin_to(randy)
        bubble.shift(RIGHT*2)
        bubble.add_content(words)

        numbers = VGroup(
            self.top_conditional_rhs, 
            self.bottom_conditional_rhs
        )
        numbers.save_state()
        arrows = VGroup(*[
            Arrow(
                numbers_word.get_left(), 
                num.get_right(), 
                buff=0.1
            )
            for num in numbers
        ])

        questions = VGroup(*[
            Text(text, font_size=20)
            for text in [
                "Does she bluff?",
                "How much does she have?",
                "Does she take risks?",
                "What's her model of me?",
                "⋮"
            ]
        ])
        questions.arrange(DOWN, aligned_edge=LEFT)
        questions[-1].next_to(questions[-2], DOWN)
        questions.next_to(randy, UP)
        questions.shift(UP*0.5)

        self.play(
            randy.animate.set_color(BLUE),
            Create(bubble),
            Write(words, run_time=2)
        )
        self.play(*list(map(Create, arrows)))
        self.play(numbers.animate.set_color(YELLOW))
        self.wait()
        
        # 簡化眨眼動畫
        self.play(randy.animate.set_color(GREEN))
        self.play(*list(map(FadeOut, [bubble, words, arrows])))
        
        for question in questions:
            self.play(
                FadeIn(question),
                randy.animate.look_at(question)
            )
        self.wait()
        self.play(randy.animate.set_color(BLUE))
        self.wait()
        self.play(
            randy.animate.set_color(PURPLE),
            FadeOut(questions)
        )

        self.randy = randy

    def vary_conditionals(self):
        randy = self.randy
        rects = VGroup(*[
            SurroundingRectangle(
                explanation,
                buff=0.1,
            )
            for explanation, rhs in zip(
                [self.top_explanation, self.bottom_explanation],
                [self.top_conditional_rhs, self.bottom_conditional_rhs],
            )
        ])

        new_conditionals = [
            (0.91, 0.4),
            (0.83, 0.1),
            (0.99, 0.2),
            (0.97, 0.3),
        ]

        self.play(*list(map(Create, rects)))
        self.play(FadeOut(rects))
        
        import itertools
        for i, value in enumerate(itertools.chain(*new_conditionals)):
            self.play(
                randy.animate.look_at(rects[i%2]),
                *self.get_conditional_change_anims(i%2, value)
            )
            if i%2 == 1:
                self.wait()
        self.play(FadeOut(randy))

    def show_restricted_space(self):
        high_bet_space = VGroup(
            self.top_vertical_parts[0],
            self.bottom_vertical_parts[0]
        )
        low_bet_space = VGroup(
            self.top_vertical_parts[1],
            self.bottom_vertical_parts[1]
        )
        
        words = MathTex("P(", self.cash_string, ")")
        words.set_color_by_tex(self.cash_string, GREEN)
        words.next_to(self.sample_space, RIGHT)
        
        low_bet_space.generate_target()
        for submob in low_bet_space.target:
            submob.set_fill(opacity=0.3)
            
        arrows = VGroup(*[
            Arrow(
                words.get_left(),
                submob.get_center(),
                color=submob.get_color()
            )
            for submob in high_bet_space
        ])

        self.play(MoveToTarget(low_bet_space))
        self.play(
            Write(words),
            *list(map(Create, arrows))
        )
        self.wait()
        for rect in high_bet_space:
            self.play(Indicate(rect, scale_factor=1))
        self.play(*list(map(FadeOut, [words, arrows])))

        self.high_bet_space = high_bet_space

    def write_P_flush_given_bet(self):
        posterior_tex = MathTex(
            "P(", self.double_heart_template, 
            "|", self.cash_string, ")"
        )
        posterior_tex.scale(0.7)
        posterior_tex.set_color_by_tex(self.cash_string, GREEN)
        self.insert_double_heart(posterior_tex)
        
        rects = self.high_bet_space.copy()
        rects = [rects[0].copy()] + list(rects)
        for rect in rects:
            rect.generate_target()
            
        numerator = rects[0].target
        plus = MathTex("+")
        denominator = VGroup(rects[1].target, plus, rects[2].target)
        denominator.arrange(RIGHT, buff=0.1)
        
        frac_line = MathTex("\\over")
        frac_line.stretch_to_fit_width(denominator.get_width())
        fraction = VGroup(numerator, frac_line, denominator)
        fraction.arrange(DOWN)

        arrow = MathTex("\\downarrow")
        group = VGroup(posterior_tex, arrow, fraction)
        group.arrange(DOWN)
        group.to_corner(UP+RIGHT)

        self.play(LaggedStartMap(FadeIn, posterior_tex))
        self.play(Write(arrow))
        self.play(MoveToTarget(rects[0]))
        self.wait()
        self.play(*itertools.chain(
            list(map(Write, [frac_line, plus])),
            list(map(MoveToTarget, rects[1:]))
        ))
        self.wait(3)
        self.play(*list(map(FadeOut, [arrow, fraction] + rects)))

        self.posterior_tex = posterior_tex

    def reshape_rectangles(self):
        post_rects = self.get_posterior_rectangles()
        prior_rects = self.get_prior_rectangles()
        
        braces = Brace(post_rects, UP)
        labels = VGroup(self.posterior_tex.copy())
        labels.next_to(braces, UP)
        
        height_rect = SurroundingRectangle(braces)

        self.play(
            TransformFromCopy(
                prior_rects, post_rects,
                run_time=2,
            ),
        )
        self.wait(2)
        self.play(Transform(self.posterior_tex, labels[0]))
        self.posterior_tex = labels[0]
        self.play(GrowFromCenter(braces))
        self.wait()
        self.play(Create(height_rect))
        self.play(FadeOut(height_rect))
        self.wait()

        self.post_rects = post_rects
        self.post_rects.braces = braces
        self.post_rects.labels = labels

    def compare_prior_to_posterior(self):
        prior_tex = self.sample_space[2]  # 假設標籤在第三個元素
        post_tex = self.posterior_tex
        prior_rect, post_rect = [
            SurroundingRectangle(tex, stroke_width=2)
            for tex in [prior_tex, post_tex]
        ]

        post_words = Text("Posterior probability", font_size=24)
        post_words.to_corner(UP+RIGHT)
        post_arrow = Arrow(
            post_words.get_bottom(), post_tex.get_top(),
            color=WHITE
        )

        self.play(Create(prior_rect))
        self.wait()
        self.play(Transform(prior_rect, post_rect))
        self.wait()
        self.play(FadeOut(post_rect))
        self.play(Indicate(post_tex.get_part_by_tex(self.cash_string)))
        self.wait()
        self.play(
            Write(post_words),
            Create(post_arrow)
        )
        self.wait()
        self.play(post_words[1].animate.set_opacity(0.2))
        self.wait(2)
        self.play(*list(map(FadeOut, [post_words, post_arrow])))

    def preview_tweaks(self):
        post_rects = self.post_rects
        new_value_lists = [
            (0.85, 0.1, 0.11),
            (0.97, 0.3, 1./22),
        ]
        for new_values in new_value_lists:
            for i, value in zip(list(range(2)), new_values):
                self.play(*self.get_conditional_change_anims(
                    i, value, post_rects
                ))
            self.play(*self.get_prior_change_anims(
                new_values[-1], post_rects
            ))
        self.wait(2)

    def tweak_non_flush_case(self):
        her = self.her
        her.scale(0.7)
        her.set_color(GRAY)
        her.shift(DOWN)
        
        # 簡化眼鏡
        glasses = Rectangle(height=0.15, width=0.6, fill_color=BLACK, fill_opacity=0.5)
        glasses.move_to(her.get_center())
        her.glasses = glasses
        
        post_rects = self.post_rects
        posterior = VGroup(post_rects.braces, post_rects.labels)
        prior_rects = self.get_prior_rectangles()
        
        risk_averse_words = Text(
            "Suppose risk averse ...",
            font_size=20
        )
        risk_averse_words.next_to(her, DOWN)

        arrows = VGroup(*[
            Arrow(ORIGIN, LEFT, tip_length=0.1)
            for x in range(3)
        ])
        arrows.arrange(DOWN)
        arrows.next_to(prior_rects[1], RIGHT, buff=0.1)

        self.wait(2)
        self.play(*list(map(FadeIn, [her, her.glasses])))
        self.play(LaggedStartMap(FadeIn, risk_averse_words))
        self.play(her.animate.set_color(BLUE))
        self.wait()
        self.play(Create(arrows))
        self.play(
            *itertools.chain(
                self.get_conditional_change_anims(1, 0.1, post_rects),
                [Animation(arrows)]
            ),
            run_time=3
        )
        self.play(FadeOut(arrows))
        self.wait(2)
        post_surrounding_rect = SurroundingRectangle(posterior)
        self.play(Create(post_surrounding_rect))
        self.play(FadeOut(post_surrounding_rect))
        self.wait()
        self.play(
            FadeOut(risk_averse_words),
            *self.get_conditional_change_anims(1, 0.3, post_rects),
            run_time=2
        )

    def tweak_flush_case(self):
        her = self.her
        post_rects = self.post_rects

        self.play(
            her.animate.set_color(YELLOW)
        )
        self.play(
            *self.get_conditional_change_anims(0, 0.47, post_rects),
            run_time=3
        )
        self.wait(3)
        self.play(*self.get_conditional_change_anims(
            0, 0.97, post_rects
        ))
        self.wait()

    def tweak_prior(self):
        her = self.her
        post_rects = self.post_rects

        self.play(
            her.animate.set_color(GREEN)
        )
        self.play(
            *self.get_prior_change_anims(0.3, post_rects),
            run_time=2
        )
        self.wait(3)
        self.play(
            *self.get_prior_change_anims(1./22, post_rects),
            run_time=2
        )
        self.play(*list(map(FadeOut, [her, her.glasses])))

    def compute_posterior(self):
        prior_rects = self.get_prior_rectangles()
        post_tex = self.posterior_tex
        prior_rhs_group = self.get_prior_rhs_group()

        fraction = MathTex(
            "{(0.045)", "(0.97)", "\\over", 
            "(0.995)", "(0.3)", "+", "(0.045)", "(0.97)}"
        )
        
        # 簡化顏色設置
        fraction[0].set_color(prior_rects[0].get_color())
        fraction[1].set_color(prior_rects[0].get_color())
        fraction[3].set_color(prior_rects[1].get_color())
        fraction[4].set_color(prior_rects[1].get_color())
        fraction[6].set_color(prior_rects[0].get_color())
        fraction[7].set_color(prior_rects[0].get_color())
        
        fraction.scale(0.65)
        fraction.to_corner(UP+RIGHT, buff=0.2)
        
        arrow_kwargs = {
            "color": WHITE,
            "tip_length": 0.15,
        }
        rhs = MathTex("\\approx", "0.13")
        rhs.scale(0.8)
        rhs.next_to(post_tex, RIGHT)
        to_rhs_arrow = Arrow(
            fraction.get_bottom(), rhs.get_top(),
            **arrow_kwargs
        )

        pre_top_rect_products = VGroup(
            prior_rhs_group[0], self.top_conditional_rhs
        )
        pre_bottom_rect_products = VGroup(
            prior_rhs_group[1], self.bottom_conditional_rhs
        )

        self.play(Indicate(prior_rects[0], scale_factor=1))
        self.play(*[
            TransformFromCopy(
                mob, term,
                run_time=2,
            )
            for mob, term in zip(
                pre_top_rect_products, [fraction[0], fraction[1]]
            )
        ])
        self.play(Write(fraction[2]))  # over
        for pair in zip(pre_top_rect_products, [fraction[0], fraction[1]]):
            self.play(*list(map(Indicate, pair)))
            self.wait()
        self.wait()
        self.play(Indicate(prior_rects[1], scale_factor=1))
        self.play(*[
            TransformFromCopy(
                mob, term,
                run_time=2,
            )
            for mob, term in zip(
                pre_bottom_rect_products, [fraction[3], fraction[4]]
            )
        ])
        self.wait()
        for pair in zip(pre_bottom_rect_products, [fraction[3], fraction[4]]):
            self.play(*list(map(Indicate, pair)))
            self.wait()
        self.play(
            Write(fraction[5]),  # +
            TransformFromCopy(VGroup(fraction[0], fraction[1]), VGroup(fraction[6], fraction[7]))
        )
        self.wait()
        self.play(Create(to_rhs_arrow))
        self.play(Write(rhs))
        self.wait(3)

    # 輔助方法
    def get_prior_labels(self, value):
        p_str = f"{value:.3f}"
        q_str = f"{1-value:.3f}"
        labels = [
            MathTex(
                "P(", s, self.double_heart_template, ")",
                "= ", num
            )
            for s, num in (("", p_str), ("\\text{not }", q_str))
        ]
        for label in labels:
            label.scale(0.7)
            self.insert_double_heart(label)

        return labels

    def get_prior_rhs_group(self):
        # 簡化實現
        return VGroup(
            MathTex(f"{1./22:.3f}"),
            MathTex(f"{1-1./22:.3f}")
        )

    def get_conditional_label(self, value, given_flush=True):
        label = MathTex(
            "P(", self.cash_string, "|", 
            "" if given_flush else "\\text{not }",
            self.double_heart_template, ")",
            "=", str(value)
        )
        self.insert_double_heart(label)
        label.set_color_by_tex(self.cash_string, GREEN)
        label.scale(0.7)
        return label

    def insert_double_heart(self, tex_mob):
        # 簡化實現：用兩個紅心符號代替
        heart1 = Text("♥", color=RED)
        heart2 = Text("♥", color=RED)
        double_heart = VGroup(heart1, heart2)
        double_heart.arrange(RIGHT, buff=0.1)
        
        # 找到模板位置並替換
        for i, submob in enumerate(tex_mob):
            if hasattr(submob, 'tex_string') and self.double_heart_template in submob.tex_string:
                double_heart.move_to(submob.get_center())
                tex_mob.submobjects[i] = double_heart
                break
        return tex_mob

    def get_side_braces_and_labels(self, sample_space, labels):
        # 簡化實現
        brace_top = Brace(sample_space[0], LEFT)
        brace_bottom = Brace(sample_space[1], LEFT)
        label_top = labels[0].next_to(brace_top, LEFT)
        label_bottom = labels[1].next_to(brace_bottom, LEFT)
        return VGroup(brace_top, brace_bottom, label_top, label_bottom)

    def get_prior_rectangles(self):
        # 返回先驗矩形
        return VGroup(self.horizontal_parts[0], self.horizontal_parts[1])

    def get_posterior_rectangles(self):
        # 創建後驗矩形（簡化實現）
        rect1 = Rectangle(height=1, width=2, fill_color=RED, fill_opacity=0.7)
        rect2 = Rectangle(height=2, width=2, fill_color=BLUE_E, fill_opacity=0.7)
        rect1.next_to(ORIGIN, UP, buff=0)
        rect2.next_to(rect1, DOWN, buff=0)
        return VGroup(rect1, rect2)

    def get_horizontal_division_change_animations(self, value, new_label_kwargs):
        # 簡化實現：改變矩形高度
        new_top_height = value * 3
        new_bottom_height = (1-value) * 3
        
        anims = [
            self.horizontal_parts[0].animate.stretch_to_fit_height(new_top_height),
            self.horizontal_parts[1].animate.stretch_to_fit_height(new_bottom_height),
        ]
        
        if 'labels' in new_label_kwargs:
            new_labels = new_label_kwargs['labels']
            anims.append(Transform(self.sample_space[2:], new_labels))
            
        return anims

    def get_conditional_change_anims(self, sub_sample_space_index, value, post_rects=None):
        # 簡化實現：改變條件概率
        given_flush = (sub_sample_space_index == 0)
        label = self.get_conditional_label(value, given_flush)
        
        if sub_sample_space_index == 0:
            target = self.top_conditional_rhs
        else:
            target = self.bottom_conditional_rhs
            
        anims = [Transform(target, label[-1])]
        
        if post_rects is not None:
            # 簡化後驗矩形更新
            pass
            
        return anims

    def get_prior_change_anims(self, value, post_rects=None):
        anims = self.get_horizontal_division_change_animations(
            value, new_label_kwargs={
                'labels': self.get_prior_labels(value)
            }
        )
        if post_rects is not None:
            # 簡化後驗矩形更新
            pass
        return anims

    def get_posterior_rectangle_change_anims(self, post_rects):
        # 簡化實現
        return []
