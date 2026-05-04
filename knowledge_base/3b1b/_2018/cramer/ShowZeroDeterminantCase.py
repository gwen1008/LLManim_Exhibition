# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示線性變換中行列式為零的情況，說明某些輸出向量沒有對應的輸入，而某些輸出向量對應多個輸入。


from manim import *
import numpy as np
import sympy

class ShowZeroDeterminantCase(LinearTransformationScene):
    def __init__(
        self,
        show_basis_vectors=True,
        matrix=[[3, -2.0], [1, -2.0 / 3]],
        tex_scale_factor=1.25,
        det_eq_symbol="=",
        **kwargs
    ):
        self.show_basis_vectors = show_basis_vectors
        self.matrix = matrix
        self.tex_scale_factor = tex_scale_factor
        self.det_eq_symbol = det_eq_symbol
        super().__init__(**kwargs)

    def construct(self):
        self.add_equation()
        self.show_det_zero()

    def add_equation(self):
        equation = self.equation = MathTex(
            "A", "\\vec{\\textbf{x}}", "=", "\\vec{\\textbf{v}}"
        )
        equation.scale(self.tex_scale_factor)
        # 使用 set_color_by_tex 的替代方法
        for tex in equation:
            if "x" in tex.tex_string:
                tex.set_color(INPUT_COLOR)
            if "v" in tex.tex_string:
                tex.set_color(OUTPUT_COLOR)
        equation.add_background_rectangle()
        equation.to_corner(UL)
        self.add(equation)
        self.add_foreground_mobject(equation)

    def show_det_zero(self):
        matrix = self.matrix

        vect_in_span = [2, 2.0 / 3]
        vect_off_span = [1, 2]
        vect_in_span_mob = self.get_vector(vect_in_span, color=OUTPUT_COLOR)
        vect_off_span_mob = self.get_vector(vect_off_span, color=OUTPUT_COLOR)

        for vect_mob in [vect_in_span_mob, vect_off_span_mob]:
            circle = Circle(color=WHITE, radius=0.15, stroke_width=2)
            circle.move_to(vect_mob.get_end())
            vect_mob.circle = circle

        vect_off_span_words = Tex("No input lands here")
        vect_off_span_words.next_to(vect_off_span_mob.circle, UP)
        vect_off_span_words.add_background_rectangle()

        vect_in_span_words = Tex("Many inputs lands here")
        vect_in_span_words.next_to(vect_in_span_mob.circle, DR)
        vect_in_span_words.shift_onto_screen()
        vect_in_span_words.add_background_rectangle()

        moving_group = VGroup(self.plane, self.basis_vectors)
        moving_group.save_state()

        solution = np.dot(np.linalg.pinv(matrix), vect_in_span)
        null_space_basis = np.array(sympy.Matrix(matrix).nullspace())
        null_space_basis = null_space_basis.flatten().astype(float)
        solution_vectors = VGroup(*[
            self.get_vector(
                solution + x * null_space_basis,
                rectangular_stem_width=0.025,
                tip_length=0.2,
            )
            for x in np.linspace(-4, 4, 20)
        ])
        solution_vectors.set_color_by_gradient(YELLOW, MAROON_B)

        self.apply_matrix(matrix, path_arc=0)
        self.wait()
        self.show_det_equation()
        self.wait()

        # Mention zero determinants
        self.play(GrowArrow(vect_off_span_mob))
        self.play(
            Create(vect_off_span_mob.circle),
            Write(vect_off_span_words),
        )
        self.wait()
        self.play(
            FadeOut(vect_off_span_mob.circle),
            ReplacementTransform(vect_off_span_mob, vect_in_span_mob),
            ReplacementTransform(vect_off_span_words, vect_in_span_words),
            ReplacementTransform(vect_off_span_mob.circle,
                                 vect_in_span_mob.circle),
        )
        self.wait(2)
        self.play(
            FadeOut(vect_in_span_words),
            FadeOut(vect_in_span_mob.circle),
            moving_group.animate.restore(run_time=2),
            ReplacementTransform(
                VGroup(vect_in_span_mob),
                solution_vectors,
                run_time=2,
            ),
        )
        self.wait()

    # Helpers

    def show_det_equation(self):
        equation = self.equation
        det_equation = MathTex(
            "\\det(", "A", ")", self.det_eq_symbol, "0"
        )
        det_equation.scale(self.tex_scale_factor)
        det_equation.next_to(
            equation, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        det_rect = BackgroundRectangle(det_equation)
        self.play(
            FadeIn(det_rect),
            Write(det_equation[0]),
            ReplacementTransform(
                equation.get_part_by_tex("A").copy(),
                det_equation.get_part_by_tex("A").copy(),
            ),
            Write(det_equation[2:]),
        )
        self.add_foreground_mobject(det_rect, det_equation)
