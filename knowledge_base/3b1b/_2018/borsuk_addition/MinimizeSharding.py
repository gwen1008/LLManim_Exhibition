# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示多組鋸齒狀圖形從緊密排列到左右分開並垂直排列的動畫過程。



from manim import *
class MinimizeSharding(Scene):
    def construct(self):
        piece_groups = VGroup(*[
            VGroup(*[
                self.get_piece()
                for x in range(3)
            ]).arrange(RIGHT, buff=SMALL_BUFF)
            for y in range(4)
        ]).arrange(RIGHT, buff=SMALL_BUFF)

        self.add(piece_groups)
        self.play(*[
            piece_groups[i].animate.space_out_submobjects(0.7)
            for i in range(len(piece_groups))
        ])
        self.wait()
        group1 = piece_groups[:2]
        group2 = piece_groups[2:]
        self.play(
            group1.animate.arrange(DOWN).next_to(ORIGIN, LEFT, LARGE_BUFF),
            group2.animate.arrange(DOWN).next_to(ORIGIN, RIGHT, LARGE_BUFF),
        )
        self.wait()

    def get_piece(self):
        jagged_spots = [
            ORIGIN, 2 * UP + RIGHT, 4 * UP + LEFT, 6 * UP,
        ]
        corners = list(itertools.chain(
            jagged_spots,
            [6 * UP + 10 * RIGHT],
            [
                p + 10 * RIGHT
                for p in reversed(jagged_spots)
            ],
            [ORIGIN]
        ))
        piece = VMobject().set_points_as_corners(corners)
        piece.set_width(1)
        piece.center()
        piece.set_stroke(WHITE, width=0.5)
        piece.set_fill(BLUE, opacity=1)
        return piece
