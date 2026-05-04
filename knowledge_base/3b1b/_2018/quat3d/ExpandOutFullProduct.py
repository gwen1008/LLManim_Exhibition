# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示四元數乘積展開為旋轉的過程，教師向學生解釋公式的幾何意義。



from manim import *
class ExpandOutFullProduct(TeacherStudentsScene):
    def construct(self):
        product = MathTex(
            """
            (w_0 + x_0 i + y_0 j + z_0 k)
            (x_1 i + y_1 j + z_1 k)
            (w_0 - x_0 i - y_0 j - z_0 k)
            """,
            tex_to_color_map={
                "w_0": W_COLOR, "(": WHITE, ")": WHITE,
                "x_0": I_COLOR, "y_0": J_COLOR, "z_0": K_COLOR,
                "x_1": I_COLOR, "y_1": J_COLOR, "z_1": K_COLOR,
            }
        )
        product.set_width(config.frame_width - 1)
        product.to_edge(UP)

        n = 10
        q_brace = Brace(product[:n], DOWN)
        p_brace = Brace(product[n:-n], DOWN)
        q_inv_brace = Brace(product[-n:], DOWN)
        braces = VGroup(q_brace, p_brace, q_inv_brace)
        for brace, tex in zip(braces, ["q", "p", "q^{-1}"]):
            brace.add(brace.get_tex(tex))

        words = TexText("= Rotation of $p$")
        words.next_to(braces, DOWN)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(product, shift=DOWN)
        )
        self.play(
            LaggedStartMap(GrowFromCenter, braces),
            self.change_students(
                "confused", "horrified", "confused"
            )
        )
        self.wait(2)
        self.play(Write(words))
        self.play_student_changes(
            "pondering", "confused", "erm",
            look_at=words
        )
        self.wait(5)
