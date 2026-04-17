# Source: 3b1b/_2019/aliquot.py
# Description: [3b1b translated] 展示數字 28 的所有因數矩形排列，每個因數用不同顏色表示，並旋轉排列在畫面中。


from manim import *
import itertools

class AmicableNumbers(Scene):
    def __init__(self, n1=28, n2=284, colors=None, **kwargs):
        super().__init__(**kwargs)
        if colors is None:
            colors = [
                BLUE_C,
                BLUE_B,
                BLUE_D,
                GREY_BROWN,
                GREEN_C,
                GREEN_B,
                GREEN_D,
                GREY,
            ]
        self.n1 = n1
        self.n2 = n2
        self.colors = colors

    def construct(self):
        self.show_n1()
        self.show_n1_factors()
        self.show_n1_factor_sum()
        self.show_n2_factors()
        self.show_n2_factor_sum()

    def show_n1(self):
        dots = VGroup(*[Dot() for x in range(self.n1)])
        dots.set_color(BLUE)
        dots.set_sheen(0.2, UL)
        dots.arrange(RIGHT, buff=SMALL_BUFF)
        dots.set_width(config.frame_width - 1)

        rects = self.get_all_factor_rectangles(dots)
        rects.rotate(90 * DEGREES)
        rects.arrange(RIGHT, buff=MED_SMALL_BUFF, aligned_edge=DOWN)
        for rect in rects:
            rect.first_col.set_stroke(WHITE, 3)
        rects.set_height(config.frame_height - 1)

        self.add(rects)

    def show_n1_factors(self):
        pass

    def show_n1_factor_sum(self):
        pass

    def show_n2_factors(self):
        pass

    def show_n2_factor_sum(self):
        pass

    def show_factors(self, dot_group):
        pass

    def get_all_factor_rectangles(self, dot_group):
        n = len(dot_group)
        factors = self.get_factors(n)
        colors = itertools.cycle(self.colors)
        result = VGroup()
        for k, color in zip(factors, colors):
            group = dot_group.copy()
            group.set_color(color)
            group.arrange_in_grid(rows=k, buff=SMALL_BUFF)
            group.first_col = group[::(n // k)]
            result.add(group)
        return result

    def get_factors(self, n):
        # 簡單的因數計算函數
        factors = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                factors.append(i)
                if i != n // i:
                    factors.append(n // i)
        factors.sort()
        return factors
