# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示 Steve 的性格描述文字與其職業概率條的對比動畫，突顯性格特徵與職業關聯性。



from manim import *
class DescriptionOfSteve(Scene):
    def construct(self):
        self.write_description()
        self.compare_probabilities()

    def write_description(self):
        steve = Steve(height=3)
        steve.to_corner(UR)

        description = self.get_description()
        description.to_edge(LEFT)
        description.align_to(steve, UP)

        mt_parts = VGroup(
            description.get_part_by_tex("meek"),
            description.get_part_by_tex("soul"),
        )
        mt_parts.set_color(WHITE)

        self.add(steve)
        self.play(
            FadeIn(description),
            run_time=3,
            lag_ratio=0.01,
            rate_func=linear,
        )
        self.wait(3)

        lines = VGroup(*[
            Line(mob.get_corner(DL), mob.get_corner(DR), color=YELLOW)
            for mob in mt_parts
        ])
        self.play(
            Create(lines),
            mt_parts.animate.set_color(YELLOW),
        )
        self.play(FadeOut(lines))
        self.wait()

    def compare_probabilities(self):
        bar = ProbabilityBar(
            0.5, width=10,
            include_braces=True,
            percentage_background_stroke_width=2,
        )
        icons = VGroup(
            LibrarianIcon(),
            FarmerIcon(),
        )
        for icon, text, half in zip(icons, ["Librarian", "Farmer"], bar.bars):
            icon.set_height(0.7)
            label = MathTex(text)
            label.next_to(icon, DOWN, buff=SMALL_BUFF)
            label.set_color(
                interpolate_color(half.get_color(), WHITE, 0.5)
            )
            icon.add(label)

        bar.add_icons(*icons)
        bar.move_to(1.75 * DOWN)

        bar.icons.set_opacity(0)

        q_marks = MathTex(*"???")
        q_marks.scale(1.5)
        q_marks.space_out_submobjects(1.5)
        q_marks.next_to(bar, DOWN)

        self.play(FadeIn(bar))
        self.wait()
        self.play(
            bar.p_tracker.set_value(0.9),
            bar.icons[0].animate.set_opacity(1),
        )
        self.wait()
        self.play(
            bar.p_tracker.set_value(0.1),
            bar.icons[1].animate.set_opacity(1),
        )
        self.play(
            LaggedStartMap(
                lambda m: FadeIn(m, shift=UP),
                q_marks,
                run_time=2,
            ),
            bar.p_tracker.animate.set_value(0.7),
            run_time=8,
        )
        for value in 0.3, 0.7:
            self.play(
                bar.p_tracker.animate.set_value(0.3),
                run_time=7,
            )

    def get_description(self):
        return Text(
            """
            Steve is very shy and withdrawn,\\\\
            invariably helpful but with very\\\\
            little interest in people or in the\\\\
            world of reality. A meek and tidy\\\\
            soul, he has a need for order and\\\\
            structure, and a passion for detail.\\\\
            """,
            color=WHITE,
        ).set_color_by_tex_to_color_map({
            "shy and withdrawn": BLUE,
            "meek and tidy": YELLOW,
            "soul": YELLOW,
        })
