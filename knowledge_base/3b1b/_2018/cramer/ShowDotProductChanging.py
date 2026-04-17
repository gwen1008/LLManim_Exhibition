# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示線性變換前後兩個向量的點積符號從正變負的過程，並在右上角顯示對應的數學方程式。



from manim import *
class ShowDotProductChanging(LinearTransformationScene):
    def __init__(
        self,
        matrix=[[2, -5.0 / 3], [-5.0 / 3, 2]],
        v=[1, 2],
        w=[2, 1],
        v_label="v",
        w_label="w",
        v_color=YELLOW,
        w_color=MAROON_B,
        rhs1="> 0",
        rhs2="< 0",
        foreground_plane_kwargs={
            "x_radius": 2 * FRAME_WIDTH,
            "y_radius": 2 * FRAME_HEIGHT,
        },
        equation_scale_factor=1.5,
        **kwargs
    ):
        self.matrix = matrix
        self.v = v
        self.w = w
        self.v_label = v_label
        self.w_label = w_label
        self.v_color = v_color
        self.w_color = w_color
        self.rhs1 = rhs1
        self.rhs2 = rhs2
        self.foreground_plane_kwargs = foreground_plane_kwargs
        self.equation_scale_factor = equation_scale_factor
        super().__init__(**kwargs)

    def construct(self):
        v_mob = self.add_vector(self.v, color=self.v_color, animate=False)
        w_mob = self.add_vector(self.w, color=self.w_color, animate=False)
        kwargs = {
            "transformation_name": "T",
            "at_tip": True,
            "animate": False,
        }
        v_label = self.add_transformable_label(v_mob, self.v_label, **kwargs)
        w_label = self.add_transformable_label(w_mob, self.w_label, **kwargs)

        start_equation = self.get_equation(v_label, w_label, self.rhs1)
        start_equation.to_corner(UR)
        self.play(
            Write(start_equation[0::2]),
            ReplacementTransform(v_label.copy(), start_equation[1]),
            ReplacementTransform(w_label.copy(), start_equation[3]),
        )
        self.wait()
        self.add_foreground_mobject(start_equation)
        self.apply_matrix(self.matrix)
        self.wait()

        end_equation = self.get_equation(v_label, w_label, self.rhs2)
        end_equation.next_to(start_equation, DOWN, aligned_edge=RIGHT)
        self.play(
            FadeIn(end_equation[0]),
            ReplacementTransform(
                start_equation[2::2].copy(),
                end_equation[2::2],
            ),
            ReplacementTransform(v_label.copy(), end_equation[1]),
            ReplacementTransform(w_label.copy(), end_equation[3]),
        )
        self.wait(2)

    def get_equation(self, v_label, w_label, rhs):
        equation = VGroup(
            v_label.copy(),
            MathTex("\\cdot"),
            w_label.copy(),
            MathTex(rhs),
        )
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.add_to_back(BackgroundRectangle(equation))
        equation.scale(self.equation_scale_factor)
        return equation
