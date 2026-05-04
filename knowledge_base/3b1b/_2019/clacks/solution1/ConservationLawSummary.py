# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示能量守恆和動量守恆的方程式，並用圖形和動畫效果強調能量守恆的概念。



from manim import *
class ConservationLawSummary(Scene):
    def construct(self):
        energy_eq = MathTex(
            "\\frac{1}{2}", "m_1", "(", "v_1", ")", "^2", "+",
            "\\frac{1}{2}", "m_2", "(", "v_2", ")", "^2", "=",
            "\\text{const.}",
        )
        energy_word = Text("Energy")
        energy_word.scale(2)
        circle = Circle(color=YELLOW, radius=2)
        energy_group = VGroup(energy_word, energy_eq, circle)
        
        momentum_eq = MathTex(
            "m_1", "v_1", "+", "m_2", "v_2", "=",
            "\\text{const.}",
        )
        momentum_word = Text("Momentum")
        momentum_word.scale(2)
        line = Line(ORIGIN, RIGHT + np.sqrt(10) * DOWN)
        line.set_color(GREEN)
        momentum_group = VGroup(momentum_word, momentum_eq, line)

        equations = VGroup(energy_eq, momentum_eq)
        words = VGroup(energy_word, momentum_word)

        for equation in equations:
            # ManimCE 中 set_color_by_tex 用法略有不同
            for tex in ["m_1", "m_2"]:
                equation.set_color_by_tex(tex, BLUE)
            for tex in ["v_1", "v_2"]:
                equation.set_color_by_tex(tex, RED)

        words.arrange(
            DOWN, buff=3,
        )
        words.to_edge(LEFT, buff=1.5)

        for group in [energy_group, momentum_group]:
            arrow = Arrow(
                LEFT, 2 * RIGHT,
                stroke_width=0.1,  # 替代 rectangular_stem_width
                tip_length=0.5,
                color=WHITE
            )
            arrow.next_to(group[0], RIGHT)
            group[1].next_to(group[0], DOWN)
            group[2].next_to(arrow, RIGHT)
            group[2].set_stroke(width=6)
            group.add(arrow)
        
        red_energy_word = energy_word.copy()
        red_energy_word.set_fill(opacity=0)
        red_energy_word.set_stroke(RED, 2)

        self.add(energy_group, momentum_group)
        self.wait()
        
        # ShowCreationThenDestruction 在 ManimCE 中沒有直接對應
        # 使用 Create 和 Uncreate 組合來模擬
        self.play(
            LaggedStart(
                *[Create(red_energy_word, run_time=0.5) for _ in range(3)],
                lag_ratio=0.3
            )
        )
        self.play(Uncreate(red_energy_word))
        
        for color in [RED, BLUE, PINK, YELLOW]:
            circle_copy = circle.copy().set_color(color)
            self.play(Create(circle_copy))
            self.play(FadeOut(circle_copy))
