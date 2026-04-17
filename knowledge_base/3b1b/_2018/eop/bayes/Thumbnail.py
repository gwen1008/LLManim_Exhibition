# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示貝葉斯定理的視覺化圖解，包含先驗機率與後驗機率的彩色區塊和標籤。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        title = Tex("Bayes' rule")
        title.scale(2)
        title.to_edge(UP)
        self.add(title)

        prior_label = MathTex("P(", "H", ")")
        post_label = MathTex("P(", "H", "|", "D", ")")
        for label in [prior_label, post_label]:
            label.set_color_by_tex("H", YELLOW)
            label.set_color_by_tex("D", GREEN)
            label.scale(1.5)

        # 由於 SampleSpaceScene 是自定義類別，這裡用最接近的視覺元素替代
        # 創建一個矩形來代表樣本空間
        sample_space = Rectangle(height=4.5, width=6, color=WHITE)
        sample_space.set_fill(opacity=0)  # 透明填充
        
        # 水平分割（30% 和 70%）
        left_rect = Rectangle(
            height=4.5, 
            width=6*0.3, 
            color=WHITE
        ).set_fill(color=BLUE, opacity=0.7)
        left_rect.align_to(sample_space, LEFT)
        
        right_rect = Rectangle(
            height=4.5, 
            width=6*0.7, 
            color=WHITE
        ).set_fill(color=RED, opacity=0.7)
        right_rect.next_to(left_rect, RIGHT, buff=0)
        
        # 垂直分割左矩形（80% 和 20%）
        left_top = Rectangle(
            height=4.5*0.8, 
            width=6*0.3, 
            color=WHITE
        ).set_fill(color=GREEN, opacity=0.9)
        left_top.align_to(left_rect, UP)
        
        left_bottom = Rectangle(
            height=4.5*0.2, 
            width=6*0.3, 
            color=WHITE
        ).set_fill(color=BLUE, opacity=0.9)
        left_bottom.next_to(left_top, DOWN, buff=0)
        
        # 垂直分割右矩形（30% 和 70%）
        right_top = Rectangle(
            height=4.5*0.3, 
            width=6*0.7, 
            color=WHITE
        ).set_fill(color=GREEN_E, opacity=0.9)
        right_top.align_to(right_rect, UP)
        
        right_bottom = Rectangle(
            height=4.5*0.7, 
            width=6*0.7, 
            color=WHITE
        ).set_fill(color=BLUE_E, opacity=0.9)
        right_bottom.next_to(right_top, DOWN, buff=0)
        
        # 組合樣本空間
        sample_space_group = VGroup(
            sample_space,
            left_rect, right_rect,
            left_top, left_bottom,
            right_top, right_bottom
        )
        
        # 添加先驗機率標籤
        prior_label.next_to(sample_space, LEFT, buff=0.5)
        
        # 創建後驗機率矩形（用高亮邊框表示）
        post_rects = VGroup()
        # 假設後驗機率對應左上的綠色區域
        post_rect = Rectangle(
            height=4.5*0.8, 
            width=6*0.3, 
            color=YELLOW, 
            stroke_width=8
        ).set_fill(opacity=0)
        post_rect.move_to(left_top)
        post_rects.add(post_rect)
        
        # 添加後驗機率標籤
        post_label.next_to(post_rect, RIGHT, buff=0.5)
        post_group = VGroup(post_rect, post_label)
        
        # 組合所有元素
        all_elements = VGroup(sample_space_group, prior_label, post_group)
        all_elements.next_to(title, DOWN, buff=LARGE_BUFF)
        
        self.add(sample_space_group, prior_label, post_group)
