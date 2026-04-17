# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示概率獨立性的視覺化，從樣本空間劃分到條件概率相等，再到獨立性假設與不獨立情況的對比。


from manim import *
import itertools as it

class MeaningOfIndependence(Scene):
    def __init__(self, sample_space_config=None, **kwargs):
        super().__init__(**kwargs)
        if sample_space_config is None:
            sample_space_config = {
                "height": 4,
                "width": 4,
            }
        self.sample_space_config = sample_space_config
        
    def construct(self):
        self.add_labeled_space()
        self.align_conditionals()
        self.relabel()
        self.assume_independence()
        self.no_independence()    

    def add_labeled_space(self):
        # 創建樣本空間（簡化實現）
        sample_space = Rectangle(
            height=self.sample_space_config["height"],
            width=self.sample_space_config["width"],
            stroke_color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.8
        )
        sample_space.shift(2*LEFT)
        
        # 水平分割
        line_h = Line(
            sample_space.get_left() + UP * self.sample_space_config["height"] * 0.3,
            sample_space.get_right() + UP * self.sample_space_config["height"] * 0.3
        )
        
        # 垂直分割
        top_rect = Rectangle(
            height=self.sample_space_config["height"] * 0.3,
            width=self.sample_space_config["width"],
            stroke_color=WHITE,
            fill_color=BLUE_D,
            fill_opacity=0.7
        )
        top_rect.move_to(sample_space.get_top() + DOWN * self.sample_space_config["height"] * 0.15)
        
        bottom_rect = Rectangle(
            height=self.sample_space_config["height"] * 0.7,
            width=self.sample_space_config["width"],
            stroke_color=WHITE,
            fill_color=BLUE_E,
            fill_opacity=0.7
        )
        bottom_rect.move_to(sample_space.get_bottom() + UP * self.sample_space_config["height"] * 0.35)
        
        # 添加標籤
        side_labels = VGroup(
            MathTex("P(A)").next_to(sample_space, LEFT),
            MathTex("P(\\overline A)").next_to(sample_space, LEFT, buff=2)
        )
        
        top_labels = VGroup(
            MathTex("P(B | A)").next_to(top_rect, UP, SMALL_BUFF),
            MathTex("P(\\overline B | A)").next_to(top_rect, DOWN, SMALL_BUFF)
        )
        
        bottom_labels = VGroup(
            MathTex("P(B | \\overline A)").next_to(bottom_rect, UP, SMALL_BUFF),
            MathTex("P(\\overline B | \\overline A)").next_to(bottom_rect, DOWN, SMALL_BUFF)
        )
        
        self.sample_space = VGroup(sample_space, line_h, top_rect, bottom_rect)
        self.sample_space_labels = VGroup(side_labels, top_labels, bottom_labels)
        
        self.add(self.sample_space)
        self.play(Write(self.sample_space_labels, run_time=4))
        
        # 保存引用以便後續使用
        self.top_rect = top_rect
        self.bottom_rect = bottom_rect
        self.top_labels = top_labels
        self.bottom_labels = bottom_labels

    def align_conditionals(self):
        line = Line(
            self.sample_space[0].get_corner(UP+LEFT) + RIGHT * self.sample_space_config["width"] * 0.3,
            self.sample_space[0].get_corner(DOWN+LEFT) + RIGHT * self.sample_space_config["width"] * 0.3
        )
        line.set_stroke(RED, 8)
        
        word = Text("Independence", font_size=48)
        word.next_to(self.sample_space, RIGHT, buff=LARGE_BUFF)
        word.set_color(RED)

        # 簡化條件概率變化動畫
        self.play(
            self.top_labels[0].animate.move_to(self.top_labels[0].get_center() + UP * 0.2),
            self.bottom_labels[0].animate.move_to(self.bottom_labels[0].get_center() + DOWN * 0.2)
        )
        
        self.play(
            Create(line),
            Write(word, run_time=1)
        )
        self.wait()

        self.independence_word = word
        self.independence_line = line

    def relabel(self):
        equation = MathTex("P(B | A) = P(B)", font_size=48)
        equation.move_to(self.independence_word)

        self.play(
            Transform(self.top_labels[0], MathTex("P(B)").move_to(self.top_labels[0])),
            FadeOut(self.bottom_labels),
        )
        self.play(
            self.independence_word.animate.next_to(equation, UP, MED_LARGE_BUFF),
            Write(equation)
        )
        self.wait()

        self.equation = equation

    def assume_independence(self):
        everything = VGroup(*self.mobjects)
        morty = SVGMobject("morty.svg")  # 假設有morty圖像
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)
        
        # 簡化思考泡泡
        bubble = Circle(radius=0.5, fill_color=WHITE, fill_opacity=0.3, stroke_color=WHITE)
        bubble.next_to(morty, LEFT, buff=SMALL_BUFF)

        self.play(
            FadeIn(morty),
            everything.animate.scale(0.5).move_to(bubble.get_center())
        )
        self.play(
            morty.animate.rotate(PI/12),  # 簡化表情變化
            Create(bubble)
        )
        self.wait(2)

        self.morty = morty

    def no_independence(self):
        self.play(
            self.top_labels[0].animate.move_to(self.top_labels[0].get_center() + DOWN * 0.2),
            self.independence_word.animate.set_opacity(0.3),
            self.equation.animate.set_opacity(0.3),
            self.morty.animate.rotate(-PI/12),  # 簡化困惑表情
            Uncreate(self.independence_line)
        )
        self.wait()
