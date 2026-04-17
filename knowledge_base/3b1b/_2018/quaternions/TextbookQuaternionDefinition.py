# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數乘法的定義公式，以及其基礎乘法規則，並呈現教師與學生對此複雜公式的反應動畫。



from manim import *
class TextbookQuaternionDefinition(TeacherStudentsScene):
    def __init__(self, random_seed=1, **kwargs):
        super().__init__(random_seed=random_seed, **kwargs)

    def construct(self):
        equation = MathTex(
            """
            (w_1 + x_1 i + y_1 j + z_1 k)
            (w_2 + x_2 i + y_2 j + z_2 k) =
            &(w_1 w_2 - x_1 x_2 - y_1 y_2 - z_1 z_2) \\, +\\\\
            &(w_1 x_2 + x_1 w_2 + y_1 z_2 - z_1 y_2)i \\, +\\\\
            &(w_1 y_2 + y_1 w_2 + z_1 x_2 - x_1 z_2)j \\, +\\\\
            &(w_1 z_2 + z_1 w_2 + x_1 y_2 - y_1 x_2)k \\\\
            """,
            tex_to_color_map={
                "w_1": YELLOW,
                "w_2": YELLOW,
                "x_1": GREEN,
                "x_2": GREEN,
                "y_1": RED,
                "y_2": RED,
                "z_1": BLUE,
                "z_2": BLUE,
            }
        )
        equation.set_width(FRAME_WIDTH - 1)
        equation.to_edge(UP)

        defining_products = VGroup(*[
            MathTex(
                tex,
                tex_to_color_map={
                    "i": GREEN,
                    "j": RED,
                    "k": BLUE,
                }
            )
            for tex in [
                "i^2 = j^2 = k^2 = -1",
                "ij = -ji = k",
                "ki = -ik = j",
                "jk = -kj = i",
            ]
        ])
        defining_products.arrange(DOWN)
        defining_products.next_to(self.students, UP, LARGE_BUFF)
        def_rect = SurroundingRectangle(defining_products)

        self.play(
            LaggedStartMap(FadeIn, defining_products, shift=DOWN),
            self.change_students(*3 * ["confused"]),
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play(Create(def_rect))
        self.play(
            Write(equation, run_time=4, lag_ratio=0.2),
            self.change_students(
                "horrified", "pleading", "sick",
                equation
            ),
            self.teacher.animate.change("erm", equation),
        )
        self.blink()
        self.look_at(equation.get_corner(UL))
        self.blink()
        self.look_at(equation.get_corner(UR))
        self.play(self.teacher.animate.change("sassy", equation))
        self.wait(2)
        self.play_all_student_changes("pondering")
        self.look_at(equation)
        self.wait()
        self.play(self.teacher.animate.change("thinking", equation))
        self.wait(8)
