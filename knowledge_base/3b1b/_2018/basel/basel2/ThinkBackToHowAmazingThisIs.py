# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示數線上的點對應到平方倒數和，並將數線變形成一個巨大的圓形。


from manim import *
import itertools as it
import numpy as np

class ThinkBackToHowAmazingThisIs(ThreeDScene):
    def __init__(self, x_radius=100, max_shown_n=20, **kwargs):
        super().__init__(**kwargs)
        self.x_radius = x_radius
        self.max_shown_n = max_shown_n

    def construct(self):
        self.show_sum()
        self.show_giant_circle()

    def show_sum(self):
        number_line = NumberLine(
            x_range = [-self.x_radius, self.x_radius, 1],
            numbers_with_elongated_ticks = list(range(-self.max_shown_n, self.max_shown_n)),
        )
        number_line.add_numbers()
        number_line.shift(2*DOWN)

        positive_dots, negative_dots = [
            VGroup(*[
                Dot(number_line.number_to_point(u*x))
                for x in range(1, int(self.x_radius), 2)
            ])
            for u in (1, -1)
        ]
        dot_pairs = list(it.starmap(VGroup, list(zip(positive_dots, negative_dots))))

        # Decimal
        decimal = DecimalNumber(0, num_decimal_places=6)
        decimal.to_edge(UP)
        terms = [2./(n**2) for n in range(1, 100, 2)]
        partial_sums = np.cumsum(terms)

        # pi^2/4 label
        brace = Brace(decimal, DOWN)
        pi_term = MathTex(r"\pi^2 \over 4")
        pi_term.next_to(brace, DOWN)

        term_mobjects = VGroup()
        for n in range(1, self.max_shown_n, 2):
            p_term = MathTex(r"\left(\frac{1}{%d}\right)^2"%n)
            n_term = MathTex(r"\left(\frac{-1}{%d}\right)^2"%n)
            group = VGroup(p_term, n_term)
            group.scale(0.7)
            p_term.next_to(number_line.number_to_point(n), UP, buff=LARGE_BUFF)
            n_term.next_to(number_line.number_to_point(-n), UP, buff=LARGE_BUFF)
            term_mobjects.add(group)
        term_mobjects.set_color_by_gradient(BLUE, YELLOW)
        plusses = VGroup(*[
            VGroup(*[
                MathTex("+").next_to(
                    number_line.number_to_point(u*n), UP, buff=1.25,
                )
                for u in (-1, 1)
            ])
            for n in range(0, self.max_shown_n, 2)
        ])

        # 在 ManimCE 中，相機控制方式不同
        # 這裡用移動整個場景來模擬縮放效果
        zoom_out = always_shift(
            self.camera.frame, 
            direction=OUT, rate=0.4
        )
        
        def update_decimal(decimal):
            # 使用相機的縮放來調整小數大小
            z = self.camera.frame.get_center()[2]
            decimal.set_height(0.07*z)
            decimal.move_to(0.7*z*UP)
        
        decimal.add_updater(update_decimal)

        self.add(number_line, *dot_pairs)
        self.add(zoom_out)
        decimal.add_updater(update_decimal)

        tuples = list(zip(term_mobjects, plusses, partial_sums))
        run_time = 1
        for term_mobs, plus_pair, partial_sum in tuples:
            self.play(
                FadeIn(term_mobs),
                Write(plus_pair, run_time=1),
                ChangeDecimalToValue(decimal, partial_sum),
                run_time=run_time
            )
            self.wait(run_time)
            run_time *= 0.9
        
        self.play(ChangeDecimalToValue(decimal, np.pi**2/4, run_time=5))
        
        # 停止縮放動畫
        zoom_out.begin_wind_down()
        self.wait()
        
        decimal.remove_updater(update_decimal)
        self.remove(zoom_out)
        
        self.play(*list(map(FadeOut, it.chain(
            term_mobjects, plusses, 
            number_line.numbers, [decimal]
        ))))

        self.number_line = number_line

    def show_giant_circle(self):
        # 在 ManimCE 中，NumberLine 沒有 insert_n_curves 方法
        # 我們直接使用現有的曲線
        everything = VGroup(*self.mobjects)
        circle = everything.copy()
        circle.move_to(ORIGIN)
        
        # 應用複數變換將數線變成圓形
        def complex_transform(point):
            x, y, z = point
            # 使用複數指數函數創建圓形
            complex_num = 7 * np.exp(complex(0, 0.0315 * x))
            return np.array([complex_num.real, complex_num.imag, z])
        
        circle.apply_function(complex_transform)
        circle.rotate(-TAU/4, about_point=ORIGIN)
        circle.center()

        self.play(Transform(everything, circle, run_time=6))
