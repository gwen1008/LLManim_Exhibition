# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數乘法規則的視覺化過程，從解釋 q·p 的意義到具體 i 乘法的例子。



from manim import *
class RuleOfQuaternionMultiplicationOverlay(Scene):
    def construct(self):
        q_times_p = MathTex("q", "\\cdot", "p")
        q_times_p.scale(2)
        q_mob, times_mob, p_mob = q_times_p
        q_mob.set_color(MAROON_B)
        p_mob.set_color(YELLOW)
        q_arrow = Arrow(start=UP, end=DOWN, color=WHITE)
        q_arrow.next_to(q_mob, UP)
        p_arrow = Arrow(start=DOWN, end=UP, color=WHITE)
        p_arrow.next_to(p_mob, DOWN)

        q_words = Text("Think of as\nan action")
        q_words.next_to(q_arrow, UP)
        p_words = Text("Think of as\na point")
        p_words.next_to(p_arrow, DOWN)

        i_mob = MathTex("i")[0]
        i_mob.scale(2)
        i_mob.move_to(q_mob, RIGHT)
        i_mob.set_color(GREEN)

        self.add(q_times_p)
        self.play(
            FadeIn(q_words, shift=UP),
            GrowArrow(q_arrow),
        )
        self.play(
            FadeIn(p_words, shift=DOWN),
            GrowArrow(p_arrow),
        )
        self.wait()
        self.play(*map(FadeOut, [
            q_words, q_arrow,
            p_words, p_arrow,
        ]))
        self.play(
            FadeIn(i_mob, shift=DOWN),
            FadeOut(q_mob, shift=UP)
        )
        product = VGroup(i_mob, times_mob, p_mob)
        self.play(product.animate.to_edge(UP))

        # Show i products
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
        i_products = VGroup(
            MathTex("i", "\\cdot", "1", "=", "i", **kwargs),
            MathTex("i", "\\cdot", "i", "=", "-1", **kwargs),
            MathTex("i", "\\cdot", "j", "=", "k", **kwargs),
            MathTex("i", "\\cdot", "k", "=", "-j", **kwargs),
        )
        i_products.scale(2)
        i_products.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )
        i_products.next_to(underline, DOWN, buff=LARGE_BUFF)
        i_products.align_to(i_mob, LEFT)

        self.play(Create(underline))
        self.wait()
        for i_product in i_products:
            self.play(TransformFromCopy(
                product, i_product[:3]
            ))
            self.wait()
            self.play(TransformFromCopy(
                i_product[:3], i_product[3:],
            ))
            self.wait()

        rect = SurroundingRectangle(
            VGroup(product, i_products),
            buff=0.4
        )
        rect.set_stroke(WHITE, width=5)
        self.play(Create(rect))
        self.play(FadeOut(rect))
