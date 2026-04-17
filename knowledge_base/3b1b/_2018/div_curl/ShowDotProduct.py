# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示兩個向量在平面上旋轉時，它們的點積值如何實時更新。


from manim import *
import numpy as np

class ShowDotProduct(MovingCameraScene):
    def __init__(self, prod_tex="\\cdot", **kwargs):
        super().__init__(**kwargs)
        self.prod_tex = prod_tex

    def construct(self):
        plane = NumberPlane()
        v1 = Vector(RIGHT, color=BLUE)
        v2 = Vector(UP, color=YELLOW)

        dot_product = MathTex(
            "\\vec{\\textbf{v}}", self.prod_tex,
            "\\vec{\\textbf{w}}", "="
        )
        dot_product.set_color_by_tex_to_color_map({
            "textbf{v}": BLUE,
            "textbf{w}": YELLOW,
        })
        dot_product.add_background_rectangle()
        dot_product.next_to(2.25 * UP, RIGHT)
        dot_product_value = DecimalNumber(
            1.0,
            include_background_rectangle=True,
        )
        dot_product_value.next_to(dot_product)
        
        # 在 ManimCE 中，我們使用 ValueTracker 和 Updater 來實現持續更新
        product_tracker = ValueTracker(self.get_product(v1, v2))
        dot_product_value.add_updater(
            lambda d: d.set_value(product_tracker.get_value())
        )

        self.camera.frame.set(height=4)
        self.camera.frame.move_to(DL + DL)
        self.add(plane)
        self.add(dot_product, dot_product_value)
        self.add(v1, v2)
        
        for n in range(5):
            self.play(
                Rotate(v1, 45 * DEGREES, about_point=ORIGIN),
                Rotate(v2, -45 * DEGREES, about_point=ORIGIN),
                product_tracker.animate.set_value(self.get_product(v1, v2)),
                run_time=3,
                rate_func=there_and_back
            )
            self.wait(0.5)

    def get_product(self, v1, v2):
        return np.dot(v1.get_vector(), v2.get_vector())
