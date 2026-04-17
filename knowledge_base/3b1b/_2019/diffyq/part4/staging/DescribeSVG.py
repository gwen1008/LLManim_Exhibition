# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一個從 SVG 檔案讀取的高音譜號路徑，並用一個移動的點追蹤其參數化曲線，最後將路徑分解為貝茲曲線段並顯示其控制點。



from manim import *
class DescribeSVG(Scene):
    def construct(self):
        plane = ComplexPlane(
            axis_config={"unit_size": 2}
        )
        plane.add_coordinates()
        self.add(plane)

        svg_mob = SVGMobject("TrebleClef")
        path = svg_mob.family_members_with_points()[0]
        path.set_fill(opacity=0)
        path.set_stroke(YELLOW, 2)
        path.set_height(6)
        path.shift(0.5 * RIGHT)
        path_parts = CurvesAsSubmobjects(path)
        path_parts.set_stroke(GREEN, 3)
        self.add(path)

        dot = Dot()
        dot.set_color(PINK)
        ft_label = MathTex("f(t) = ")
        ft_label.to_corner(UL)
        z_decimal = DecimalNumber(num_decimal_places=3)
        z_decimal.next_to(ft_label, RIGHT)
        z_decimal.add_updater(lambda m: m.set_value(
            plane.p2n(dot.get_center())
        ))
        z_decimal.set_color(interpolate_color(PINK, WHITE, 0.25))
        rect = BackgroundRectangle(VGroup(ft_label, z_decimal))

        brace = Brace(rect, DOWN)
        question = Text("Where is this defined?")
        question.add_background_rectangle()
        question.next_to(brace, DOWN)

        answer = Text("Read in some .svg")
        answer.add_background_rectangle()
        answer.next_to(question, DOWN, buff=LARGE_BUFF)

        self.add(rect, ft_label, z_decimal)
        self.add(question, brace)
        self.play(UpdateFromAlphaFunc(
            dot,
            lambda d, a: d.move_to(path.point_from_proportion(a)),
            run_time=5,
            rate_func=lambda t: 0.3 * there_and_back(t)
        ))
        self.wait()
        self.play(FadeIn(answer, shift=UP))
        self.play(
            FadeOut(path),
            FadeOut(dot),
            FadeIn(path_parts),
        )

        path_parts.generate_target()
        path_parts.save_state()
        path_parts.target.space_out_submobjects(1.3)
        for part in path_parts.target:
            part.shift(0.2 * part.get_center()[0] * RIGHT)
        path_parts.target.move_to(path_parts)
        self.play(
            MoveToTarget(path_parts)
        )

        indicators = self.get_bezier_point_indicators(path_parts)
        self.play(Create(
            indicators,
            lag_ratio=0.5,
            run_time=3,
        ))
        self.wait()
        self.play(
            FadeOut(indicators),
            Restore(path_parts),
        )

    def get_bezier_point_indicators(self, path):
        dots = VGroup()
        lines = VGroup()
        for part in path.family_members_with_points():
            for tup in part.get_cubic_bezier_tuples():
                a1, h1, h2, a2 = tup
                dots.add(
                    Dot(a1),
                    Dot(a2),
                    Dot(h2, color=YELLOW),
                    Dot(h1, color=YELLOW),
                )
                lines.add(
                    Line(a1, h1),
                    Line(a2, h2),
                )
        for dot in dots:
            dot.set_width(0.05)
        lines.set_stroke(WHITE, 1)
        return VGroup(dots, lines)
