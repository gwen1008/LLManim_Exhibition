# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數中 j 與其他元素的乘法表，從上到下逐行動態生成並用矩形框強調。



from manim import *
class JMultiplicationChart(Scene):
    def construct(self):
        # Largely copy-pasted....what are you gonna do about it?
        product = MathTex("j", "\\cdot", "p")
        product[0].set_color(RED)
        product.scale(2)
        product.to_edge(UP)

        underline = Line(LEFT, RIGHT)
        underline.set_width(product.get_width() + MED_SMALL_BUFF)
        underline.next_to(product, DOWN)

        kwargs = {
            "tex_to_color_map": {
                "i": GREEN,
                "j": RED,
                "k": BLUE
            }
        }
        j_products = VGroup(
            MathTex("j", "\\cdot", "1", "=", "j", **kwargs),
            MathTex("j", "\\cdot", "j", "=", "-1", **kwargs),
            MathTex("j", "\\cdot", "i", "=", "-k", **kwargs),
            MathTex("j", "\\cdot", "k", "=", "i", **kwargs),
        )
        j_products.scale(2)
        j_products.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        j_products.next_to(underline, DOWN, buff=LARGE_BUFF)
        j_products.align_to(product, LEFT)

        self.play(FadeIn(product, shift=DOWN))
        self.play(Create(underline))
        self.wait()
        for j_product in j_products:
            self.play(TransformFromCopy(
                product, j_product[:3]
            ))
            self.wait()
            self.play(TransformFromCopy(
                j_product[:3], j_product[3:],
            ))
            self.wait()

        rect = SurroundingRectangle(
            VGroup(product, j_products),
            buff=MED_SMALL_BUFF
        )
        rect.set_stroke(WHITE, width=5)
        self.play(Create(rect))
        self.play(FadeOut(rect))
