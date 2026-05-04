# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示三維坐標作為行列式體積的視覺化，通過動態替換矩陣列和坐標符號來演示。



from manim import *
class ThreeDCoordinatesAsVolumes(Scene):
    def construct(self):
        colors = [X_COLOR, Y_COLOR, Z_COLOR]
        x, y, z = coords = VGroup(*[Tex(c) for c in "xyz"])
        coords.set_color_by_gradient(*colors)
        matrix = IntegerMatrix(np.identity(3))
        matrix.set_column_colors(*colors)
        det_text = get_det_text(matrix)
        equals = MathTex("=")
        equals.next_to(det_text[0], LEFT)
        equals.shift(SMALL_BUFF * DOWN)
        coords.next_to(equals, LEFT)

        columns = VGroup(*[
            VGroup(*matrix.mob_matrix[:, i])
            for i in range(3)
        ])

        coord_column = coords.copy()
        for coord, m_elem in zip(coord_column, columns[2]):
            coord.move_to(m_elem)
        coord_column.set_color(WHITE)
        coord_column[2].set_color(BLUE)
        coord_column.generate_target()

        self.play(LaggedStartMap(FadeIn, VGroup(
            z, equals, det_text, matrix.brackets,
            VGroup(*matrix.mob_matrix[:, :2].flatten()),
            coord_column
        )))
        self.wait(2)
        coord_column.target.move_to(columns[1])
        coord_column.target.set_color_by_gradient(WHITE, Y_COLOR, WHITE)
        self.play(
            MoveToTarget(coord_column, path_arc=np.pi),
            FadeOut(columns[1]),
            FadeIn(columns[2]),
            FadeIn(y, shift=DOWN),
            z.animate.shift(UP),
            z.animate.set_opacity(0),
        )
        self.wait(2)
        coord_column.target.move_to(columns[0])
        coord_column.target.set_color_by_gradient(X_COLOR, WHITE, WHITE)
        self.play(
            MoveToTarget(coord_column, path_arc=np.pi),
            FadeOut(columns[0]),
            FadeIn(columns[1]),
            FadeIn(x, shift=DOWN),
            y.animate.shift(UP),
            y.animate.set_opacity(0),
        )
        self.wait(2)
