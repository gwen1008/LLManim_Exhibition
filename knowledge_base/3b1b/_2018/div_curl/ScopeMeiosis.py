# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個 PiCreature 角色在思考時，標題與線條動態生成並排列的過程。



from manim import *
class ScopeMeiosis(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "flip_at_start": True,
            "color": GREY_BROWN,
        },
        default_pi_creature_start_corner=DR,
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        morty = self.pi_creature
        section_titles = VGroup(*list(map(Text, [
            "Background on div/curl",
            "Conformal maps",
            "Conformal map $\\Rightarrow" +
            "\\text{div}\\textbf{F} = " +
            "\\text{curl}\\textbf{F} = 0$",
            "Complex derivatives",
        ])))
        sections = VGroup(*[
            VGroup(title, self.get_lines(title, 3))
            for title in section_titles
        ])
        sections.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        sections.to_edge(UP)

        top_title = section_titles[0]
        lower_sections = sections[1:]

        self.add(sections)
        modes = [
            "pondering",
            "pondering",
            "bump",
            "bump",
            "concerned_musician",
            "concerned_musician",
        ]

        for n, mode in zip(list(range(6)), modes):
            if n % 2 == 1:
                top_title = lines
                lines = self.get_lines(top_title, 4)
            else:
                lines = self.get_lines(top_title, 6)
            lower_sections.generate_target()
            lower_sections.target.next_to(
                lines, DOWN, MED_LARGE_BUFF, LEFT,
            )
            self.play(
                Create(lines),
                MoveToTarget(lower_sections),
                morty.change, mode, lines,
            )

    def get_lines(self, title, n_lines):
        lines = VGroup(*[
            Line(3 * LEFT, 3 * RIGHT, color=GREY_B)
            for x in range(n_lines)
        ])
        lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        lines.next_to(
            title, DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        # 模擬 pointwise_become_partial 效果：隨機縮短最後一條線
        last_line = lines[-1]
        random_factor = random.random()
        new_end = last_line.get_start() + random_factor * (last_line.get_end() - last_line.get_start())
        lines[-1] = Line(last_line.get_start(), new_end, color=GREY_B)
        return lines
