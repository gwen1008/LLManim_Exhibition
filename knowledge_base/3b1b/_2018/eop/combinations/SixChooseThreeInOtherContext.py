# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示從 6 個步驟中選擇 3 個向右移動的路徑組合，以網格點和箭頭動畫呈現組合數的視覺化。


from manim import *
import itertools as it

class SixChooseThreeInOtherContext(Scene):
    def construct(self):
        self.add_dots()
        self.count_paths_to_three_three()

    def add_dots(self):
        n = 4
        dots = VGroup(*[Dot() for x in range(n**2)])
        dots.arrange_in_grid(n, n, buff=LARGE_BUFF)
        dots.next_to(ORIGIN, LEFT)
        self.add(dots)

        self.dots = dots
        self.dot_to_dot_distance = get_norm(
            dots[1].get_center() - dots[0].get_center()
        )

    def count_paths_to_three_three(self):
        dots = self.dots
        d = self.dot_to_dot_distance
        lower_left = dots.get_corner(DL)
        lower_left += dots[0].radius * (UP + RIGHT)

        right = Vector(d * RIGHT, color=PINK)
        up = Vector(d * UP, color=BLUE)

        last_rights = None
        last_ups = None
        last_line = None
        for indices in it.combinations(list(range(6)), 3):
            bools = [i in indices for i in range(6)]
            arrows = VGroup(*[
                right.copy() if b else up.copy()
                for b in bools
            ])
            last_point = np.array(lower_left)
            ups, rights = VGroup(), VGroup()
            for arrow, b in zip(arrows, bools):
                arrow.shift(last_point - arrow.get_start())
                last_point = arrow.get_end()
                group = rights if b else ups
                group.add(arrow)

            line = VGroup(*[arrow.tip.copy() for arrow in arrows])
            line.arrange(RIGHT, buff=0.5 * SMALL_BUFF)
            if last_line is None:
                line.shift(FRAME_WIDTH * RIGHT / 4)
                line.to_edge(UP)
                self.play(
                    Create(arrows),
                    Create(line)
                )
            else:
                line.next_to(last_line, DOWN, SMALL_BUFF)
                self.play(
                    FadeIn(line),
                    ReplacementTransform(last_rights, rights),
                    ReplacementTransform(last_ups, ups),
                )
            last_rights = rights
            last_ups = ups
            last_line = line
        self.wait()
