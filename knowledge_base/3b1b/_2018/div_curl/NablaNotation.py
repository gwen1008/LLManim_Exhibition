# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示散度和旋度的∇符號表示法，並將其展開為偏導數形式，最後鏡頭拉遠帶出更深層的含義。



from manim import *
class NablaNotation(PiCreatureScene, MovingCameraScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": GREY_BROWN,
        },
        default_pi_creature_start_corner=DL,
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        self.show_notation()
        self.show_expansion()
        self.zoom_out()

    def show_notation(self):
        morty = self.pi_creature

        tex_to_color_map = {
            "\\text{div}": BLUE,
            "\\nabla \\cdot": BLUE,
            "\\text{curl}": YELLOW,
            "\\nabla \\times": YELLOW,
        }
        div_equation = MathTex(
            "\\text{div} \\, \\textbf{F} = \\nabla \\cdot \\textbf{F}",
            tex_to_color_map=tex_to_color_map
        )
        div_nabla = div_equation.get_part_by_tex("\\nabla")
        curl_equation = MathTex(
            "\\text{curl} \\, \\textbf{F} = \\nabla \\times \\textbf{F}",
            tex_to_color_map=tex_to_color_map
        )
        curl_nabla = curl_equation.get_part_by_tex("\\nabla")
        equations = VGroup(div_equation, curl_equation)
        equations.arrange(DOWN, buff=LARGE_BUFF)
        equations.next_to(morty, UP, 2)
        equations.to_edge(LEFT)

        self.play(
            FadeIn(div_equation, shift=DOWN),
            morty.change, "raise_right_hand"
        )
        self.wait()
        self.play(WiggleOutThenIn(div_nabla, scale_value=1.5))
        self.wait()
        self.play(
            FadeIn(curl_equation, shift=DOWN),
            morty.change, "raise_left_hand"
        )
        self.wait()
        self.play(WiggleOutThenIn(curl_nabla, scale_value=1.5))
        self.wait()

        self.equations = equations

    def show_expansion(self):
        equations = self.equations
        morty = self.pi_creature

        nabla_vector = Matrix([
            ["\\partial \\over \\partial x"],
            ["\\partial \\over \\partial y"],
        ], v_buff=1.5)
        F_vector = Matrix([
            ["\\textbf{F}_x"],
            ["\\textbf{F}_y"],
        ], v_buff=1.2)
        nabla_vector.match_height(F_vector)

        div_lhs, curl_lhs = lhs_groups = VGroup(*[
            VGroup(
                nabla_vector.copy(),
                MathTex(tex).scale(1.5),
                F_vector.copy(),
                MathTex("=")
            )
            for tex in ("\\cdot", "\\times")
        ])
        colors = [BLUE, YELLOW]
        for lhs, color in zip(lhs_groups, colors):
            lhs.arrange(RIGHT, buff=MED_SMALL_BUFF)
            VGroup(lhs[0].get_brackets(), lhs[1]).set_color(color)
        div_lhs.to_edge(UP)
        curl_lhs.next_to(div_lhs, DOWN, buff=LARGE_BUFF)

        div_rhs = MathTex(
            "{\\partial F_x \\over \\partial x} + " +
            "{\\partial F_y \\over \\partial y}"
        )
        curl_rhs = MathTex(
            "{\\partial F_y \\over \\partial x} - " +
            "{\\partial F_x \\over \\partial y}"
        )
        rhs_groups = VGroup(div_rhs, curl_rhs)
        for rhs, lhs in zip(rhs_groups, lhs_groups):
            rhs.next_to(lhs, RIGHT)

        for rhs, tex, color in zip(rhs_groups, ["div", "curl"], colors):
            rhs.rect = SurroundingRectangle(rhs, color=color)
            rhs.label = MathTex(
                "\\text{%s}" % tex,
                "\\, \\textbf{F}"
            )
            rhs.label.set_color(color)
            rhs.label.next_to(rhs.rect, UP)

        for i in 0, 1:
            self.play(
                ReplacementTransform(
                    equations[i][2].copy(),
                    lhs_groups[i][0].get_brackets()
                ),
                ReplacementTransform(
                    equations[i][3].copy(),
                    lhs_groups[i][2],
                ),
                morty.change, "pondering",
                *[
                    GrowFromPoint(mob, equations[i].get_right())
                    for mob in [
                        lhs_groups[i][0].get_entries(),
                        lhs_groups[i][1],
                        lhs_groups[i][3]
                    ]
                ],
                run_time=2
            )
            self.wait()
        self.wait()
        for rhs in rhs_groups:
            self.play(
                Write(rhs),
                morty.change, 'confused'
            )
            self.play(
                Create(rhs.rect),
                FadeIn(rhs.label, shift=DOWN),
            )
            self.wait()
        self.play(morty.change, "erm")
        self.wait(3)

    def zoom_out(self):
        screen_rect = self.camera.frame.copy()
        screen_rect.set_stroke(WHITE, 3)
        screen_rect.scale(1.01)
        words = Tex("Something deeper at play...")
        words.scale(1.3)
        words.next_to(screen_rect, UP)

        self.add(screen_rect)
        self.play(
            self.camera.frame.animate.set_height(FRAME_HEIGHT + 3),
            Write(words, rate_func=lambda t: smooth(min(1, 0.3 + 0.7*t))),
            run_time=2,
        )
        self.wait()
