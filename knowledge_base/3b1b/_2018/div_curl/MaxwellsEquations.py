# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示馬克士威方程組的四個方程式，並依序用矩形框標示高斯定律、磁場散度為零、以及兩個旋度方程式，同時加入註解和角色動畫。



from manim import *
class MaxwellsEquations(Scene):
    def __init__(self, faded_opacity=0.3, **kwargs):
        super().__init__(**kwargs)
        self.faded_opacity = faded_opacity

    def construct(self):
        self.add_equations()
        self.circle_gauss_law()
        self.circle_magnetic_divergence()
        self.circle_curl_equations()

    def add_equations(self):
        title = Title("Maxwell's equations")
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        tex_to_color_map = {
            "\\textbf{E}": BLUE,
            "\\textbf{B}": YELLOW,
            "\\rho": WHITE,
        }

        equations = self.equations = VGroup(*[
            MathTex(
                tex, tex_to_color_map=tex_to_color_map
            )
            for tex in [
                """
                    \\text{div} \\, \\textbf{E} =
                    {\\rho \\over \\varepsilon_0}
                """,
                """\\text{div} \\, \\textbf{B} = 0""",
                """
                    \\text{curl} \\, \\textbf{E} =
                    -{\\partial \\textbf{B} \\over \\partial t}
                """,
                """
                    \\text{curl} \\, \\textbf{B} =
                    \\mu_0 \\left(
                        \\textbf{J} + \\varepsilon_0
                        {\\partial \\textbf{E} \\over \\partial t}
                    \\right)
                """,
            ]
        ])
        equations.arrange(
            DOWN, aligned_edge=LEFT,
            buff=MED_LARGE_BUFF
        )

        field_definitions = VGroup(*[
            MathTex(text, tex_to_color_map=tex_to_color_map)
            for text in [
                "\\text{Electric field: } \\textbf{E}",
                "\\text{Magnetic field: } \\textbf{B}",
            ]
        ])
        field_definitions.arrange(
            RIGHT, buff=MED_LARGE_BUFF
        )
        field_definitions.next_to(title, DOWN, MED_LARGE_BUFF)
        equations.next_to(field_definitions, DOWN, MED_LARGE_BUFF)
        field_definitions.shift(MED_SMALL_BUFF * UP)

        self.add(title)
        self.add(field_definitions)
        self.play(LaggedStart(
            *[FadeIn(eq) for eq in equations],
            run_time=3,
            lag_ratio=0.4
        ))
        self.wait()

    def circle_gauss_law(self):
        equation = self.equations[0]
        rect = SurroundingRectangle(equation)
        rect.set_color(RED)
        rho = equation.get_part_by_tex("\\rho")
        sub_rect = SurroundingRectangle(rho)
        sub_rect.match_color(rect)
        rho_label = TexText("Charge density")
        rho_label.next_to(sub_rect, RIGHT)
        rho_label.match_color(sub_rect)
        gauss_law = TexText("Gauss's law")
        gauss_law.next_to(rect, RIGHT)

        self.play(
            Create(rect),
            Write(gauss_law, run_time=1),
            self.equations[1:].animate.set_opacity(self.faded_opacity)
        )
        self.wait(2)
        self.play(
            ReplacementTransform(rect, sub_rect),
            FadeOut(gauss_law),
            FadeIn(rho_label),
            rho.animate.set_color(sub_rect.get_color()),
        )
        self.wait()
        self.play(
            self.equations.animate.to_edge(LEFT),
            rho_label.animate.next_to(sub_rect, RIGHT),
            sub_rect.animate.surround(rho),
            FadeOut(rho_label),
            FadeOut(sub_rect),
        )
        self.wait()

    def circle_magnetic_divergence(self):
        equations = self.equations
        rect = SurroundingRectangle(equations[1])

        self.play(
            equations[0].animate.set_opacity(self.faded_opacity),
            equations[1].animate.set_opacity(1.0),
        )
        self.play(Create(rect))
        self.wait(3)
        self.play(FadeOut(rect))

    def circle_curl_equations(self):
        equations = self.equations
        rect = SurroundingRectangle(equations[2:])
        randy = Randolph(height=2)
        randy.flip()
        randy.next_to(rect, RIGHT, aligned_edge=DOWN)
        randy.look_at(rect)

        self.play(
            equations[1].animate.set_opacity(self.faded_opacity),
            equations[2:].animate.set_opacity(1.0),
        )
        self.play(Create(rect))
        self.play(
            randy.animate.change("confused"),
            FadeIn(randy),
        )
        self.play(Blink(randy))
        self.play(randy.animate.look_at(2 * RIGHT))
        self.wait(3)
        self.play(
            FadeOut(rect),
            randy.animate.change("pondering"),
            randy.animate.look_at(rect),
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()
