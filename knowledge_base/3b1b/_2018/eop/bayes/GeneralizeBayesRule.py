# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示貝葉斯定理如何透過樣本空間分割與條件機率來更新信念，並逐步解釋先驗、後驗和似然項。


from manim import *
import itertools as it

class GeneralizeBayesRule(Scene):
    def construct(self):
        self.add_sample_space()
        self.add_title()
        self.add_posterior_rectangles()
        self.add_bayes_rule()
        self.talk_through_terms()
        self.name_likelihood()
        self.dont_memorize()
        self.show_space_restriction()

    def add_sample_space(self):
        # 創建樣本空間矩形
        sample_space = Rectangle(
            height=3, width=3,
            stroke_color=WHITE, fill_opacity=0
        )
        # 水平分割
        top_rect = Rectangle(
            height=3*0.4, width=3,
            stroke_color=WHITE, fill_opacity=0
        )
        bottom_rect = Rectangle(
            height=3*0.6, width=3,
            stroke_color=WHITE, fill_opacity=0
        )
        top_rect.next_to(sample_space.get_top(), DOWN, buff=0)
        bottom_rect.next_to(top_rect.get_bottom(), DOWN, buff=0)
        
        # 添加標籤
        labels = [
            MathTex("P(", "B", ")"),
            MathTex("P(\\text{not }", "B", ")"),
        ]
        for label in labels:
            label.scale(0.7)
            self.color_label(label)
        
        # 將標籤放在對應部分旁邊
        top_label = labels[0].next_to(top_rect, LEFT)
        bottom_label = labels[1].next_to(bottom_rect, LEFT)
        
        # 垂直分割
        parts = [top_rect, bottom_rect]
        values = [0.8, 0.4]
        given_strs = ["", "\\text{not }"]
        color_pairs = [(GREEN, BLUE), (GREEN_E, BLUE_E)]
        vects = [UP, DOWN]
        
        vertical_parts = []
        vertical_labels = []
        
        for part, value, given_str, colors, vect in zip(parts, values, given_strs, color_pairs, vects):
            # 創建垂直分割
            left_width = value * part.width
            right_width = (1-value) * part.width
            
            left_rect = Rectangle(
                height=part.height, width=left_width,
                stroke_color=WHITE, fill_color=colors[0], fill_opacity=0.8
            )
            right_rect = Rectangle(
                height=part.height, width=right_width,
                stroke_color=WHITE, fill_color=colors[1], fill_opacity=0.8
            )
            
            left_rect.move_to(part.get_left(), aligned_edge=LEFT)
            right_rect.next_to(left_rect, RIGHT, buff=0)
            
            # 添加標籤
            label = MathTex(
                "P(", "I", "|", given_str, "B", ")"
            )
            label.scale(0.7)
            self.color_label(label)
            
            if vect == UP:
                label.next_to(left_rect, UP, buff=SMALL_BUFF)
            else:
                label.next_to(left_rect, DOWN, buff=SMALL_BUFF)
            
            vertical_parts.extend([left_rect, right_rect])
            vertical_labels.append(label)
        
        # 組合所有元素
        self.sample_space = VGroup(
            sample_space, top_rect, bottom_rect,
            *vertical_parts, top_label, bottom_label, *vertical_labels
        )
        self.sample_space.to_edge(LEFT)
        
        self.add(self.sample_space)
        
        # 儲存參考以便後續使用
        self.top_rect = top_rect
        self.bottom_rect = bottom_rect
        self.vertical_parts = vertical_parts
        self.top_label = top_label
        self.bottom_label = bottom_label
        self.vertical_labels = vertical_labels

    def add_title(self):
        title = Text("Updating Beliefs from new Information")
        title.scale(0.8)
        title.to_corner(UP+LEFT)
        self.add(title)
        self.title = title

    def add_posterior_rectangles(self):
        # 創建後驗矩形（簡化版本）
        post_rects = Rectangle(
            height=1, width=2,
            stroke_color=WHITE, fill_color=YELLOW, fill_opacity=0.5
        )
        post_rects.next_to(self.sample_space, RIGHT, buff=LARGE_BUFF)
        
        label = MathTex("P(", "B", "|", "I", ")")
        label.scale(0.7)
        self.color_label(label)
        label.next_to(post_rects, UP)
        
        self.play(Create(post_rects))
        self.play(Write(label))
        
        self.post_rects = post_rects
        self.posterior_tex = label

    def add_bayes_rule(self):
        rule = MathTex(
             "=", "{P(", "B", ")", "P(", "I", "|", "B", ")",
            "\\over", "P(", "I", ")}",
        )
        self.color_label(rule)
        rule.scale(0.7)
        rule.next_to(self.posterior_tex, RIGHT)

        bayes_rule_words = Text("Bayes' rule")
        bayes_rule_words.scale(0.7)
        bayes_rule_words.next_to(rule[1:], UP, buff=LARGE_BUFF)
        
        self.play(FadeIn(rule))
        self.play(Write(bayes_rule_words))
        self.wait(2)

        self.bayes_rule_words = bayes_rule_words
        self.bayes_rule = rule

    def talk_through_terms(self):
        prior = self.top_label
        posterior = self.posterior_tex
        prior_target = VGroup(*self.bayes_rule[1:4])
        likelihood = VGroup(*self.bayes_rule[4:9])
        P_I = VGroup(*self.bayes_rule[-3:])

        prior_word = Text("Prior")
        posterior_word = Text("Posterior")
        words = [prior_word, posterior_word]
        for word in words:
            word.set_color(YELLOW)
            word.scale(0.7)
        
        prior_rect = SurroundingRectangle(prior, buff=SMALL_BUFF)
        posterior_rect = SurroundingRectangle(posterior, buff=SMALL_BUFF)
        for rect in [prior_rect, posterior_rect]:
            rect.set_stroke(YELLOW, 2)

        prior_word.next_to(prior, UP, buff=LARGE_BUFF)
        posterior_word.next_to(posterior, DOWN, buff=LARGE_BUFF)
        
        prior_arrow = Arrow(
            prior_word.get_bottom(), prior.get_top(),
            tip_length=0.15
        )
        posterior_arrow = Arrow(
            posterior_word.get_top(), posterior.get_bottom(),
            tip_length=0.15
        )

        self.play(
            Write(prior_word), 
            Create(prior_arrow), 
            Create(prior_rect),
        ) 
        self.wait()
        
        prior_copy = prior.copy()
        self.play(prior_copy.animate.move_to(prior_target).scale_to_fit_width(prior_target.width),
                  run_time=2,
                  path_arc=-PI/3)
        self.remove(prior_copy)
        self.wait()
        
        # 指示似然項
        self.play(
            Indicate(likelihood),
            Indicate(self.vertical_labels[0]),
        )
        self.wait()
        
        self.play(Indicate(P_I))
        self.wait()
        
        self.play(
            Write(posterior_word), 
            Create(posterior_arrow), 
            Create(posterior_rect),
        )

        self.prior_label = VGroup(prior_word, prior_arrow, prior_rect)
        self.posterior_label = VGroup(posterior_word, posterior_arrow, posterior_rect)
        self.likelihood = likelihood

    def name_likelihood(self):
        likelihoods = [
            self.vertical_labels[0],
            self.likelihood
        ]
        rects = [
            SurroundingRectangle(mob, buff=SMALL_BUFF)
            for mob in likelihoods
        ]
        name = Text("Likelihood")
        name.scale(0.7)
        name.next_to(self.posterior_tex, UP, buff=1.5*LARGE_BUFF)
        
        arrows = [
            Arrow(
                name, rect.get_edge_center(vect), 
                tip_length=0.15
            )
            for rect, vect in zip(rects, [RIGHT, UP])
        ]
        
        for mob in [name, *arrows, *rects]:
            mob.set_color(YELLOW)

        self.play(
            self.bayes_rule_words.animate.to_edge(UP),
            Write(name),
            *[Create(arrow) for arrow in arrows],
            *[Create(rect) for rect in rects]
        )
        self.wait(2)
        
        self.play(FadeOut(VGroup(name, *arrows, *rects)))
        self.play(FadeOut(self.posterior_label))
        self.play(FadeOut(self.prior_label))

    def dont_memorize(self):
        rule = VGroup(*self.bayes_rule[1:])
        word = Text("Memorize")
        word.scale(0.7)
        word.next_to(rule, DOWN)
        
        cross = VGroup(
            Line(UP+LEFT, DOWN+RIGHT),
            Line(UP+RIGHT, DOWN+LEFT),
        )
        cross.set_stroke(RED, 6)
        cross.replace(word, stretch=True)

        self.play(Write(word))
        self.wait()
        self.play(Create(cross))
        self.wait()
        
        self.play(FadeOut(VGroup(cross, word)))
        self.play(FadeOut(self.bayes_rule))
        self.play(FadeOut(self.post_rects),
                  FadeOut(self.posterior_tex))

    def show_space_restriction(self):
        # 簡化版本：重新顯示後驗矩形
        post_rects = Rectangle(
            height=1, width=2,
            stroke_color=WHITE, fill_color=YELLOW, fill_opacity=0.5
        )
        post_rects.next_to(self.sample_space, RIGHT, buff=LARGE_BUFF)
        
        label = MathTex("P(", "B", "|", "I", ")")
        label.scale(0.7)
        self.color_label(label)
        label.next_to(post_rects, UP)
        
        self.play(Create(post_rects))
        self.play(Write(label))
        self.wait(2)
        
        # 淡出非I部分
        non_I_parts = [self.vertical_parts[1], self.vertical_parts[3]]
        self.play(*[part.animate.set_opacity(0.3) for part in non_I_parts])
        self.wait()
        
        # 強調先驗部分
        self.play(
            self.top_rect.animate.set_stroke(YELLOW, 3),
            self.top_label.animate.set_color(YELLOW)
        )
        self.wait()
        
        self.play(
            self.top_rect.animate.set_stroke(WHITE, 1),
            self.top_label.animate.set_color(WHITE)
        )
        self.wait(3)

    def color_label(self, label):
        # 根據文本內容設置顏色
        for i, part in enumerate(label):
            if "B" in part.tex_string:
                part.set_color(RED)
            elif "I" in part.tex_string:
                part.set_color(GREEN)
