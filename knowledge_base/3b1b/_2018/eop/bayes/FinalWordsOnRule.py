# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示貝葉斯定理的視覺化樣本空間，包含先驗機率、條件機率、後驗機率的動態調整，以及機器學習和科學推論的應用說明。


from manim import *
import itertools as it

class FinalWordsOnRule(Scene):
    def construct(self):
        self.add_sample_space()
        self.add_uses()
        self.tweak_values()

    def add_sample_space(self):
        # 注意：SampleSpace 類別在 ManimCE 中不存在
        # 這裡使用 Rectangle 和 VGroup 來模擬樣本空間
        sample_space = self.sample_space = Rectangle(width=6, height=4)
        prior = 0.2
        top_conditional = 0.8
        bottom_conditional = 0.3
        
        # 水平分割
        top_rect = Rectangle(width=6, height=4*prior)
        bottom_rect = Rectangle(width=6, height=4*(1-prior))
        top_rect.move_to(sample_space.get_top())
        bottom_rect.move_to(sample_space.get_bottom())
        
        # 垂直分割
        top_left = Rectangle(width=6*top_conditional, height=4*prior)
        top_right = Rectangle(width=6*(1-top_conditional), height=4*prior)
        top_left.move_to(top_rect.get_left())
        top_right.move_to(top_rect.get_right())
        
        bottom_left = Rectangle(width=6*bottom_conditional, height=4*(1-prior))
        bottom_right = Rectangle(width=6*(1-bottom_conditional), height=4*(1-prior))
        bottom_left.move_to(bottom_rect.get_left())
        bottom_right.move_to(bottom_rect.get_right())
        
        # 設置顏色
        top_left.set_color(GREEN)
        top_right.set_color(RED)
        bottom_left.set_color(GREEN_E)
        bottom_right.set_color(RED_E)
        
        # 創建樣本空間組
        sample_space_group = VGroup(
            VGroup(top_left, top_right),
            VGroup(bottom_left, bottom_right)
        )
        
        # 淡出部分區域
        for i in range(2):
            sample_space_group[i][1].set_opacity(0.3)
        
        # 創建標籤
        B = "\\text{Belief}"
        D = "\\text{Data}"
        P_B = MathTex("P(", B, ")")
        P_D_given_B = MathTex("P(", D, "|", B, ")")
        P_D_given_not_B = MathTex(
            "P(", D, "|", "\\text{not }", B, ")"
        )
        P_B_given_D = MathTex("P(", B, "|", D, ")")
        labels = VGroup(P_B, P_D_given_B, P_D_given_not_B, P_B_given_D)
        for label in labels:
            label.scale(0.7)
            # 設置顏色
            for tex in label:
                if tex.tex_string == B:
                    tex.set_color(BLUE)
                elif tex.tex_string == D:
                    tex.set_color(GREEN)
        
        # 創建大括號（簡化版本）
        braces = VGroup()
        # 先驗機率大括號
        brace1 = Brace(sample_space_group[0], LEFT)
        brace1_label = P_B.copy().next_to(brace1, LEFT)
        braces.add(brace1)
        labels.add(brace1_label)
        
        # 條件機率大括號
        brace2 = Brace(top_left, UP)
        brace2_label = P_D_given_B.copy().next_to(brace2, UP)
        braces.add(brace2)
        labels.add(brace2_label)
        
        brace3 = Brace(bottom_left, DOWN)
        brace3_label = P_D_given_not_B.copy().next_to(brace3, DOWN)
        braces.add(brace3)
        labels.add(brace3_label)
        
        # 後驗機率矩形（簡化）
        post_rects = VGroup(
            Rectangle(width=2, height=1, color=BLUE),
            Rectangle(width=4, height=1, color=RED)
        )
        post_rects.arrange(RIGHT, buff=0)
        post_rects.next_to(sample_space_group, DOWN, buff=0.5)
        
        # 後驗機率大括號
        brace4 = Brace(post_rects, UP)
        brace4_label = P_B_given_D.copy().next_to(brace4, UP)
        braces.add(brace4)
        labels.add(brace4_label)
        
        # 組合所有元素
        group = VGroup(sample_space_group, braces, labels, post_rects)
        group.to_corner(DL)
        self.add(group)
        
        self.post_rects = post_rects
        self.sample_space_group = sample_space_group

    def add_uses(self):
        uses = Text(
            "Machine learning, scientific inference, ...",
            font_size=36
        )
        uses.to_edge(UP)
        for word in uses:
            self.play(Write(word, run_time=2))
        self.wait()

    def tweak_values(self):
        post_rects = self.post_rects
        new_value_lists = [
            (0.85, 0.1, 0.11),
            (0.3, 0.9, 0.4),
            (0.97, 0.3, 1./22),
        ]
        
        for new_values in new_value_lists:
            # 簡化：只調整後驗矩形寬度
            for i, value in enumerate(new_values[:2]):
                new_width = value * 6
                self.play(
                    post_rects[i].animate.stretch_to_fit_width(new_width),
                    run_time=1
                )
                self.wait()
            
            # 調整水平分割
            new_prior = new_values[2]
            self.play(
                self.sample_space_group[0].animate.stretch_to_fit_height(4*new_prior),
                self.sample_space_group[1].animate.stretch_to_fit_height(4*(1-new_prior)),
                run_time=1
            )
            self.wait()
        
        self.wait(2)
