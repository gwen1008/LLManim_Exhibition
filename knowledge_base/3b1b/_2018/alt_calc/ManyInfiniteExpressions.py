# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示三個無限表達式（連分數、嵌套根式和冪塔）從中心逐漸生長的動畫。



from manim import *
class ManyInfiniteExpressions(Scene):
    def construct(self):
        # 連分數表達式
        frac = get_phi_continued_fraction(10)
        frac.set_height(2)
        frac.to_corner(UL)

        # 嵌套根式表達式
        n = 9
        radical_str_parts = [
            "%d + \\sqrt{" % d
            for d in range(1, n + 1)
        ]
        radical_str_parts += ["\\cdots"]
        radical_str_parts += ["}"] * n
        radical = MathTex("".join(radical_str_parts))
        radical.to_corner(UR)
        radical.to_edge(DOWN)
        radical.set_color_by_gradient(YELLOW, RED)

        # 冪塔表達式
        n = 12
        power_tower = MathTex(
            *["\\sqrt{2}^{"] * n + ["\\dots"] + ["}"] * n
        )
        power_tower.to_corner(UR)
        power_tower.set_color_by_gradient(BLUE, GREEN)

        # 播放三個表達式從中心生長的動畫
        self.play(*[
            LaggedStart(
                *[GrowFromCenter(mob) for mob in group],
                lag_ratio=0.1,
                run_time=8,
            )
            for group in (frac, radical, power_tower)
        ])
        self.wait(2)
