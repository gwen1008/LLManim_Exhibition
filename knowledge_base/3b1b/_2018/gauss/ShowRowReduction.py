# Source: 3b1b/_2018/gauss.py
# Description: [3b1b translated] 展示一個矩陣透過列運算（縮放與相加）逐步化簡為單位矩陣的過程。


from manim import *
import numpy as np
from functools import reduce
import itertools as it

class ShowRowReduction(Scene):
    def __init__(
        self,
        matrices=[
            [
                [2, -1, -1],
                [0, 3, -4],
                [-3, 2, 1],
            ],
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ],
        ],
        h_spacing=2,
        extra_h_spacing=0.5,
        v_spacing=1,
        include_separation_lines=True,
        changing_row_color=YELLOW,
        reference_row_color=BLUE,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.matrices = matrices
        self.h_spacing = h_spacing
        self.extra_h_spacing = extra_h_spacing
        self.v_spacing = v_spacing
        self.include_separation_lines = include_separation_lines
        self.changing_row_color = changing_row_color
        self.reference_row_color = reference_row_color

    def construct(self):
        self.initialize_terms()

        self.apply_row_rescaling(0, 1/2)
        self.add_row_multiple_to_row(2, 0, 3)
        self.apply_row_rescaling(1, 1/3)
        self.add_row_multiple_to_row(2, 1, -1/2)
        self.apply_row_rescaling(2, 6)
        self.add_row_multiple_to_row(0, 1, 1/2)
        self.add_row_multiple_to_row(0, 2, 7/6)
        self.add_row_multiple_to_row(1, 2, 4/3)
        self.wait()

    def initialize_terms(self):
        full_matrix = reduce(
            lambda m, v: np.append(m, v, axis=1),
            self.matrices
        )
        mobject_matrix = np.vectorize(FractionMobject)(full_matrix)
        rows = self.rows = VGroup(*it.starmap(VGroup, mobject_matrix))
        for i, row in enumerate(rows):
            for j, term in enumerate(row):
                term.move_to(
                    i * self.v_spacing * DOWN +
                    j * self.h_spacing * RIGHT
                )

        # Visually separate distinct parts
        separation_lines = self.separation_lines = VGroup()
        lengths = [len(m[0]) for m in self.matrices]
        for partial_sum in np.cumsum(lengths)[:-1]:
            VGroup(*mobject_matrix[:, partial_sum:].flatten()).shift(
                self.extra_h_spacing * RIGHT
            )
            c1 = VGroup(*mobject_matrix[:, partial_sum - 1])
            c2 = VGroup(*mobject_matrix[:, partial_sum])
            line = DashedLine(c1.get_top(), c1.get_bottom())
            line.move_to(VGroup(c1, c2))
            separation_lines.add(line)

        if self.include_separation_lines:
            group = VGroup(rows, separation_lines)
        else:
            group = rows
        group.center().to_edge(DOWN, buff=2)
        self.add(group)

    def add_variables(self):
        # If it is meant to represent a system of equations
        pass

    def apply_row_rescaling(self, row_index, scale_factor):
        row = self.rows[row_index]
        new_row = VGroup()
        for element in row:
            target = FractionMobject(element.value * scale_factor)
            target.move_to(element)
            new_row.add(target)
        new_row.set_color(self.changing_row_color)

        label = VGroup(
            MathTex("r_%d" % (row_index + 1)),
            MathTex("\\rightarrow"),
            MathTex("("),
            FractionMobject(scale_factor),
            MathTex(")"),
            MathTex("r_%d" % (row_index + 1)),
        )
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.to_edge(UP)
        VGroup(label[0], label[-1]).set_color(self.changing_row_color)

        scalar_mob = FractionMobject(scale_factor)
        scalar_mob.add_to_back(
            MathTex("\\times").next_to(scalar_mob, LEFT, SMALL_BUFF)
        )
        scalar_mob.scale(0.5)
        scalar_mob.next_to(row[0], DR, SMALL_BUFF)

        # Do do, fancier illustrations here
        self.play(
            FadeIn(label),
            row.animate.set_color(self.changing_row_color),
        )
        self.play(FadeIn(scalar_mob))
        for elem, new_elem in zip(row, new_row):
            self.play(scalar_mob.animate.next_to(elem, DR, SMALL_BUFF))
            self.play(ReplacementTransform(elem, new_elem, path_arc=30 * DEGREES))
        self.play(FadeOut(scalar_mob))
        self.play(new_row.animate.set_color(WHITE))
        self.play(FadeOut(label))
        self.rows.submobjects[row_index] = new_row

    def add_row_multiple_to_row(self, row1_index, row2_index, scale_factor):
        row1 = self.rows[row1_index]
        row2 = self.rows[row2_index]
        new_row1 = VGroup()
        scaled_row2 = VGroup()
        for elem1, elem2 in zip(row1, row2):
            target = FractionMobject(elem1.value + scale_factor * elem2.value)
            target.move_to(elem1)
            new_row1.add(target)

            scaled_term = FractionMobject(scale_factor * elem2.value)
            scaled_term.move_to(elem2)
            scaled_row2.add(scaled_term)
        new_row1.set_color(self.changing_row_color)
        scaled_row2.set_color(self.reference_row_color)

        for elem1, elem2 in zip(row1, scaled_row2):
            elem2.add_plus_if_needed()
            elem2.scale(0.5)
            elem2.next_to(elem1, UL, buff=SMALL_BUFF)

        label = VGroup(
            MathTex("r_%d" % (row1_index + 1)),
            MathTex("\\rightarrow"),
            MathTex("r_%d" % (row1_index + 1)),
            MathTex("+"),
            MathTex("("),
            FractionMobject(scale_factor),
            MathTex(")"),
            MathTex("r_%d" % (row2_index + 1)),
        )
        label.arrange(RIGHT, buff=SMALL_BUFF)
        label.to_edge(UP)
        VGroup(label[0], label[2]).set_color(self.changing_row_color)
        label[-1].set_color(self.reference_row_color)

        self.play(
            FadeIn(label),
            row1.animate.set_color(self.changing_row_color),
            row2.animate.set_color(self.reference_row_color),
        )
        row1_target = row1.copy()
        row1_target.next_to(self.rows, UP, buff=2)
        row1_target.align_to(row1, LEFT)

        row2_target = row2.copy()
        row2_target.next_to(row1_target, DOWN, buff=MED_LARGE_BUFF)
        lp, rp = row2_parens = MathTex("()")
        row2_parens.set_height(row2.get_height() + 2 * SMALL_BUFF)
        lp.next_to(row2, LEFT, SMALL_BUFF)
        rp.next_to(row2, RIGHT, SMALL_BUFF)
        scalar = FractionMobject(scale_factor)
        scalar.next_to(lp, LEFT, SMALL_BUFF)
        scalar.add_plus_if_needed()

        self.play(
            FadeIn(row2_parens),
            Write(scalar),
        )
        self.play(TransformFromCopy(row2, scaled_row2))
        self.wait()
        for elem, new_elem, s_elem in zip(row1, new_row1, scaled_row2):
            self.play(
                FadeOut(elem),
                FadeIn(new_elem),
                Transform(s_elem, new_elem.copy().set_opacity(0), remover=True)
            )
        self.wait()
        self.play(
            FadeOut(label),
            FadeOut(row2_parens),
            FadeOut(scalar),
            new_row1.animate.set_color(WHITE),
            row2.animate.set_color(WHITE),
        )
        self.rows.submobjects[row1_index] = new_row1
