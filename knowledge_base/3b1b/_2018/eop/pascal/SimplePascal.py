# Source: 3b1b/_2018/eop/pascal.py
# Description: [3b1b translated] 展示帕斯卡三角形從單一單元格開始，通過複製和變換動態生成新行的過程。



from manim import *
class SimplePascal(Scene):

    def build_new_pascal_row(self, old_pt):
        lowest_row_copy = old_pt.get_lowest_row().copy()
        self.add(lowest_row_copy)

        n = old_pt.nrows - 1
        lowest_row_copy1 = old_pt.get_lowest_row()
        lowest_row_copy2 = lowest_row_copy1.copy()

        start_mob = VGroup(lowest_row_copy1, lowest_row_copy2)
        self.add(start_mob)

        new_pt = old_pt.copy()
        cell_height = old_pt.height / old_pt.nrows
        cell_width = old_pt.width / old_pt.nrows
        new_pt.nrows += 1
        new_pt.height = new_pt.nrows * cell_height
        new_pt.width = new_pt.nrows * cell_width

        new_pt.init_points()
        # align with original (copy got centered on screen)
        c1 = new_pt.coords_to_mobs[0][0].get_center()
        c2 = old_pt.coords_to_mobs[0][0].get_center()
        v = c2 - c1
        new_pt.shift(v)

        new_row_left_copy = VGroup(*[
            new_pt.coords_to_mobs[n+1][k]
            for k in range(0, n+1)
        ])

        new_row_right_copy = VGroup(*[
            new_pt.coords_to_mobs[n+1][k]
            for k in range(1, n+2)
        ]).copy()

        target_mob = VGroup(new_row_left_copy, new_row_right_copy)
        self.play(Transform(start_mob, target_mob))

        return new_pt

    def construct(self):
        cell_height = 1
        cell_width = 1
        nrows = 1
        pt = GeneralizedPascalsTriangle(
            nrows=nrows,
            height=nrows * cell_height,
            width=nrows * cell_width,
            submob_class=graded_square,
            portion_to_fill=0.9
        )
        pt.shift(3 * UP)
        self.add(pt)
        lowest_row_copy = pt.get_lowest_row().copy()
        self.add(lowest_row_copy)
        for i in range(7):
            pt = self.build_new_pascal_row(pt)
