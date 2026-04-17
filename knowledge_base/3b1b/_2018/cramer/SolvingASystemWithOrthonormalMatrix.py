# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示如何使用正交矩陣求解線性系統，通過動態變換展示輸入向量與輸出向量的關係，並推導點積方程式。


from manim import *
import numpy as np

class SolvingASystemWithOrthonormalMatrix(LinearTransformationScene):
    def __init__(self, array_scale_factor=0.6, **kwargs):
        super().__init__(**kwargs)
        self.array_scale_factor = array_scale_factor

    def construct(self):
        # Setup system
        angle = TAU / 12
        matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        output_vect = [1, 2]
        symbolic_matrix = [
            ["\\cos(30^\\circ)", "-\\sin(30^\\circ)"],
            ["\\sin(30^\\circ)", "\\cos(30^\\circ)"],
        ]
        
        # 創建線性系統表示
        system = VGroup()
        # 創建矩陣
        matrix_mob = Matrix(
            symbolic_matrix,
            h_buff=2.5,
            element_to_mobject=MathTex,
            bracket_h_buff=SMALL_BUFF
        )
        matrix_mob.set_column_colors(X_COLOR, Y_COLOR)
        
        # 創建等號和輸出向量
        equals = MathTex("=")
        output_vect_mob = Matrix([[str(output_vect[0])], [str(output_vect[1])]])
        output_vect_mob.elements.set_color(WHITE)
        
        # 創建輸入向量佔位符
        input_vect_mob = Matrix([["x"], ["y"]])
        input_vect_mob.elements.set_color(WHITE)
        
        # 組合系統
        system.add(matrix_mob, input_vect_mob, equals, output_vect_mob)
        system.arrange(RIGHT, buff=SMALL_BUFF)
        system.scale(1.25)
        system.to_corner(UL)
        
        system_rect = BackgroundRectangle(system, buff=MED_SMALL_BUFF)

        matrix_brace = Brace(matrix_mob, DOWN, buff=SMALL_BUFF)
        orthonomal_label = Tex("Orthonormal")
        orthonomal_label.set_color(WHITE)
        orthonomal_label.next_to(matrix_brace, DOWN, SMALL_BUFF)
        orthonomal_label.add_background_rectangle()

        # Input and output vectors
        output_vect_mob_3d = self.get_vector(output_vect, color=GREEN)
        output_vect_label = output_vect_mob.copy()
        output_vect_label.add_background_rectangle()
        output_vect_label.scale(self.array_scale_factor)
        output_vect_label.next_to(
            output_vect_mob_3d.get_end(), RIGHT, buff=SMALL_BUFF)

        input_vect = np.dot(np.linalg.inv(matrix), output_vect)
        input_vect_mob_3d = self.get_vector(input_vect, color=BLUE)
        input_vect_label = Tex("Mystery input vector")
        input_vect_label.add_background_rectangle()
        input_vect_label.next_to(input_vect_mob_3d.get_end(), RIGHT, SMALL_BUFF)
        input_vect_label.match_color(input_vect_mob_3d)

        # Column arrays
        column_mobs = VGroup()
        for i, vect in zip(list(range(2)), [DR, DL]):
            elements = matrix_mob.deepcopy().get_columns()[i]
            column_mob = Matrix([[elem.get_tex_string()] for elem in elements])
            column_mob.add_background_rectangle()
            column_mob.scale(self.array_scale_factor)
            column_vector = self.get_vector(matrix[:, i])
            column_mob.next_to(
                column_vector.get_end(), vect,
                buff=SMALL_BUFF
            )
            column_mobs.add(column_mob)
        column_mobs[1].shift(SMALL_BUFF * UP)

        # Dot product lines
        x_point = self.plane.coords_to_point(input_vect[0], 0)
        y_point = self.plane.coords_to_point(0, input_vect[1])
        input_dashed_lines = VGroup(
            DashedLine(input_vect_mob_3d.get_end(), x_point),
            DashedLine(input_vect_mob_3d.get_end(), y_point),
        )
        output_dashed_lines = input_dashed_lines.copy()
        output_dashed_lines.apply_matrix(matrix)

        self.add_foreground_mobjects(system_rect, system)
        self.add_foreground_mobjects(matrix_brace, orthonomal_label)
        self.add_foreground_mobjects(output_vect_mob_3d, output_vect_label)
        self.plane.set_stroke(width=2)

        self.apply_matrix(matrix)
        self.wait()
        self.play(LaggedStartMap(Create, output_dashed_lines))
        self.play(*self.get_column_animations(matrix_mob, column_mobs))
        self.wait()
        self.remove(*output_dashed_lines)
        self.apply_inverse(matrix, added_anims=[
            FadeOut(column_mobs),
            ReplacementTransform(output_vect_mob_3d.copy(), input_vect_mob_3d),
            ReplacementTransform(
                output_dashed_lines.copy(), input_dashed_lines),
            FadeIn(input_vect_label),
        ])
        self.wait()
        self.remove(input_dashed_lines, input_vect_mob_3d)
        self.apply_matrix(matrix, added_anims=[
            FadeOut(input_vect_label),
            ReplacementTransform(input_vect_mob_3d.copy(), output_vect_mob_3d),
            ReplacementTransform(input_dashed_lines.copy(),
                                 output_dashed_lines),
            FadeIn(column_mobs),
        ])

        # Write dot product equations
        equations = VGroup()
        for i in 0, 1:
            moving_output_vect_label = output_vect_label.copy()
            moving_column_mob = column_mobs[i].copy()
            moving_var = input_vect_mob.get_entries()[i].copy()
            equation = VGroup(
                moving_var.generate_target(),
                MathTex("="),
                moving_output_vect_label.generate_target(),
                MathTex("\\cdot"),
                moving_column_mob.generate_target(use_deepcopy=True)
            )
            equation.movers = VGroup(
                moving_var, moving_output_vect_label, moving_column_mob
            )
            for element in moving_column_mob.target.get_family():
                if not isinstance(element, MathTex):
                    continue
                tex_string = element.tex_string
                if "sin" in tex_string or "cos" in tex_string:
                    element.set_stroke(width=1)
                    element.scale(1.25)
            equation.to_write = equation[1::2]
            equation[2].match_height(equation[4])
            equation.arrange(RIGHT, buff=SMALL_BUFF)
            equation.background_rectangle = BackgroundRectangle(equation)
            equation.add_to_back(equation.background_rectangle)
            equations.add(equation)
        equations.arrange(DOWN, buff=MED_LARGE_BUFF)
        equations.scale(1.25)
        equations.to_corner(UR, buff=MED_SMALL_BUFF)
        equations_rect = BackgroundRectangle(equations, buff=MED_LARGE_BUFF)
        equations_rect.set_fill(opacity=0.9)

        for i, equation in enumerate(equations):
            anims = [
                FadeIn(equation.background_rectangle),
                Write(equation.to_write),
                LaggedStartMap(
                    MoveToTarget, equation.movers,
                    path_arc=60 * DEGREES
                )
            ]
            if i == 0:
                anims.insert(0, FadeIn(equations_rect))
            self.play(*anims)
            self.wait()

    def get_column_animations(self, matrix_mobject, column_mobs):
        def get_kwargs(i):
            return {
                "rate_func": lambda t: smooth(min(max((t - 0.4 * i) / 0.6, 0), 1)),
                "run_time": 2,
            }
        animations = []
        for i, cm in enumerate(column_mobs):
            kwargs = get_kwargs(i)
            animations.append(FadeIn(cm.get_brackets(), **kwargs))
            animations.append(ReplacementTransform(
                matrix_mobject.get_brackets().copy(),
                cm.get_brackets(),
                **kwargs
            ))
            column_elements = matrix_mobject.get_columns()[i]
            animations.append(ReplacementTransform(
                VGroup(*column_elements).copy(),
                cm.get_entries(),
                **kwargs
            ))
        return animations
