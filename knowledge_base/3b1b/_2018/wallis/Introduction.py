# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示沃利斯乘積的數值逼近過程，通過數線上的箭頭移動和矩形框選項來視覺化部分乘積收斂到 π/2 的過程。


from manim import *
import numpy as np

class Introduction(Scene):
    def construct(self):
        n_terms = 10

        number_line = NumberLine(
            x_range=[0, 2, 0.25],
            length=10,  # unit_size=5 對應 length=10 (5*2)
            include_numbers=True,
            numbers=[0, 1, 2],
            color=GREY_B,
        )
        number_line.move_to(DOWN)

        numerical_terms = get_wallis_product_numerical_terms(400)
        partial_products = np.cumprod(numerical_terms)
        curr_product = partial_products[0]

        arrow = Arrow(start=UP, end=DOWN, color=YELLOW, buff=0)

        def get_arrow_update():
            return arrow.animate.next_to(
                number_line.number_to_point(curr_product),
                UP, buff=SMALL_BUFF
            )
        get_arrow_update()
        decimal = DecimalNumber(
            curr_product, num_decimal_places=5, include_sign=False
        )
        decimal.add_updater(lambda d: d.next_to(arrow, UP, SMALL_BUFF))
        decimal.next_to(arrow, UP, SMALL_BUFF)

        product_mob = get_wallis_product(n_terms)
        product_mob.to_edge(UP)

        rects = VGroup(*[
            SurroundingRectangle(product_mob[:n])
            for n in list(range(3, 4 * n_terms, 4)) + [4 * n_terms]
        ])
        rect = rects[0].copy()

        pi_halves_arrow = Arrow(start=DOWN, end=UP, color=BLUE, buff=0)
        pi_halves_arrow.next_to(
            number_line.number_to_point(np.pi / 2), DOWN, SMALL_BUFF
        )
        pi_halves_term = MathTex("\\pi / 2")
        pi_halves_term.next_to(pi_halves_arrow, DOWN)

        self.add(product_mob, number_line, rect, arrow, decimal)
        self.add(pi_halves_arrow, pi_halves_term)
        for n in range(1, len(rects)):
            curr_product = partial_products[n]
            self.play(
                get_arrow_update(),
                Transform(rect, rects[n]),
                run_time=0.5
            )
            self.wait(0.5)

        for n in range(len(rects), len(numerical_terms), 31):
            curr_product = partial_products[n]
            self.play(
                get_arrow_update(),
                run_time=0.25
            )
        curr_product = np.pi / 2
        self.play(
            get_arrow_update(),
            run_time=0.5
        )
        self.wait()
