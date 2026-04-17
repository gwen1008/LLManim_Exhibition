# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示所有八種條件機率方程式的排列，並以角色對話建議獨立性假設。


from manim import *
import itertools as it

class ShowAllEightConditionals(Scene):
    def construct(self):
        self.show_all_conditionals()
        self.suggest_independence()

    def show_all_conditionals(self):
        equations = VGroup()
        filler_tex = "Filler"
        for bool_list in it.product(*[[True, False]]*3):
            equation = MathTex(
                "P(", filler_tex, ")", "=",
                "P(", filler_tex, ")",
                "P(", filler_tex, "|", filler_tex, ")",
                "P(", filler_tex, "|", filler_tex, ")",
            )
            sub_bool_lists = [
                bool_list[:n] for n in (3, 1, 2, 1, 3, 2)
            ]
            parts = equation.get_parts_by_tex(filler_tex)
            for part, sub_list in zip(parts, sub_bool_lists):
                slot_group = get_slot_group(
                    sub_list, 
                    buff = SMALL_BUFF,
                    include_qs = False
                )
                slot_group.replace(part, dim_to_match = 0)
                index = equation.index_of_part(part)
                equation.submobjects[index] = slot_group
            equations.add(equation)
        equations.arrange(DOWN, buff=0.5)

        rect = SurroundingRectangle(
            VGroup(*equations[0][7:], *equations[-1][7:]),
            buff = SMALL_BUFF
        )
        rect.shift(0.5*SMALL_BUFF*RIGHT)

        self.play(LaggedStart(
            *[FadeIn(eq) for eq in equations],
            run_time = 5,
            lag_ratio = 0.3
        ))
        self.wait()
        self.play(Create(rect, run_time = 2))
        self.play(FadeOut(rect))
        self.wait()

    def suggest_independence(self):
        full_screen_rect = FullScreenFadeRectangle()
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)

        self.play(
            FadeIn(full_screen_rect),
            FadeIn(randy)
        )
        self.play(PiCreatureSays(
            randy, "Let's just assume \\\\ independence.",
            target_mode = "shruggie"
        ))
        self.play(Blink(randy))
        self.wait()
