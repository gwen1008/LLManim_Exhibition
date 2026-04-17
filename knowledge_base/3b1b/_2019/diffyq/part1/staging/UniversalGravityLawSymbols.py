# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示萬有引力定律公式的符號分解，並逐步引入位置和速度的導數關係。



from manim import *
class UniversalGravityLawSymbols(Scene):
    def construct(self):
        x1_tex = "\\vec{\\textbf{x}}_1"
        x2_tex = "\\vec{\\textbf{x}}_2"
        a1_tex = "\\vec{\\textbf{a}}_1"
        new_brown = interpolate_color(GREY_B, LIGHT_BROWN, 0.5)
        law = MathTex(
            "F_1", "=", "m_1", a1_tex, "=",
            "G", "m_1", "m_2",
            "\\left({", x2_tex, "-", x1_tex, "\\over",
            "||", x2_tex, "-", x1_tex, "||", "}\\right)",
            "\\left({", "1", "\\over",
            "||", x2_tex, "-", x1_tex, "||^2", "}\\right)",
            tex_to_color_map={
                x1_tex: BLUE_C,
                "m_1": BLUE_C,
                x2_tex: new_brown,
                "m_2": new_brown,
                a1_tex: YELLOW,
            }
        )
        law.to_edge(UP)

        force = law[:4]
        constants = law[4:8]
        unit_vect = law[8:19]
        inverse_square = law[19:]
        parts = VGroup(
            force, unit_vect, inverse_square
        )

        words = VGroup(
            Text("Force on\nmass 1"),
            Text("Unit vector\ntowards mass 2"),
            Text("Inverse square\nlaw"),
        )

        self.add(law)

        braces = VGroup()
        rects = VGroup()
        for part, word in zip(parts, words):
            brace = Brace(part, DOWN)
            word.scale(0.8)
            word.next_to(brace, DOWN)
            rect = SurroundingRectangle(part)
            rect.set_stroke(YELLOW, 1)
            braces.add(brace)
            rects.add(rect)

        self.play(
            Create(rects[0]),
            FadeOut(rects[0]),
            GrowFromCenter(braces[0]),
            FadeIn(words[0], shift=UP)
        )
        self.wait()
        self.play(
            Create(rects[1]),
            FadeOut(rects[1]),
            GrowFromCenter(braces[1]),
            FadeIn(words[1], shift=UP)
        )
        self.wait()
        self.play(
            Create(rects[2]),
            FadeOut(rects[2]),
            TransformFromCopy(braces[1], braces[2]),
            FadeIn(words[2], shift=UP),
        )
        self.wait()

        # Position derivative
        v1_tex = "\\vec{\\textbf{v}}_1"
        kw = {
            "tex_to_color_map": {
                x1_tex: BLUE_C,
                v1_tex: RED,
            }
        }
        x_deriv = MathTex(
            "{d", x1_tex, "\\over", "dt}", "=", v1_tex, **kw
        )
        x_deriv.to_corner(UL)
        v_deriv = MathTex(
            "{d", v1_tex, "\\over", "dt}", "=", **kw
        )

        # Make way
        law.generate_target()
        lt = law.target
        lt.to_edge(RIGHT)
        lt[6].set_opacity(0)
        lt[:6].align_to(lt[6], RIGHT)
        lt[:3].set_opacity(0)
        v_deriv.next_to(lt[3], LEFT)

        self.play(
            FadeIn(x_deriv, shift=DOWN),
            MoveToTarget(law),
            braces[1:].animate.align_to(lt, RIGHT),
            MaintainPositionRelativeTo(words[1:], braces[1:]),
            FadeOut(words[0]),
            FadeOut(braces[0]),
        )
        self.play(Indicate(x_deriv))

        self.play(
            TransformFromCopy(
                x_deriv.get_part_by_tex(v1_tex),
                v_deriv.get_part_by_tex(v1_tex),
            ),
            Write(VGroup(*filter(
                lambda m: m is not v_deriv.get_part_by_tex(v1_tex),
                v_deriv,
            )))
        )

        x_parts = VGroup(*[m for m in law if x1_tex in m.get_tex_string()])
        self.play(
            TransformFromCopy(
                VGroup(*[m for m in x_deriv if x1_tex in m.get_tex_string()]),
                x_parts.copy(),
                remover=True,
                path_arc=30 * DEGREES,
            )
        )
        self.play(
            LaggedStart(
                *[Indicate(part) for part in x_parts],
                lag_ratio=0.5
            )
        )
        self.wait()
