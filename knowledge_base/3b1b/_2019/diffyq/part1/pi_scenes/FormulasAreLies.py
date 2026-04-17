# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 展示一個 PiCreature 角色對物理公式提出質疑，並用對話框喊出「謊言！」的動畫場景。



from manim import *
class FormulasAreLies(PiCreatureScene):
    def construct(self):
        you = self.pi_creature
        t2c = {
            "{L}": BLUE,
            "{g}": YELLOW,
            "\\theta_0": WHITE,
            "\\sqrt{\\,": WHITE,
        }
        kwargs = {"tex_to_color_map": t2c}
        period_eq = MathTex(
            "\\text{Period} = 2\\pi \\sqrt{\\,{L} / {g}}",
            **kwargs
        )
        theta_eq = MathTex(
            "\\theta(t) = \\theta_0 \\cos\\left("
            "\\sqrt{\\,{L} / {g}} \\cdot t"
            "\\right)",
            **kwargs
        )
        equations = VGroup(theta_eq, period_eq)
        equations.arrange(DOWN, buff=LARGE_BUFF)

        for eq in [period_eq, theta_eq]:
            i = eq.index_of_part_by_tex("\\sqrt")
            eq.sqrt_part = eq[i:i + 4]

        theta0 = theta_eq.get_part_by_tex("\\theta_0")
        theta0_words = Text("Starting angle")
        theta0_words.next_to(theta0, UL)
        theta0_words.shift(UP + 0.5 * RIGHT)
        arrow = Arrow(
            theta0_words.get_bottom(),
            theta0,
            color=WHITE,
            tip_length=0.25,
        )

        bubble = SpeechBubble()
        bubble.pin_to(you)
        bubble_content = Text("Lies!")
        bubble_content.scale(2)
        bubble.add_content(bubble_content)

        self.add(period_eq)
        you.change("pondering", period_eq)
        self.wait()
        theta_eq.remove(*theta_eq.sqrt_part)
        self.play(
            TransformFromCopy(
                period_eq.sqrt_part,
                theta_eq.sqrt_part,
            ),
            FadeIn(theta_eq)
        )
        theta_eq.add(*theta_eq.sqrt_part)
        self.play(
            FadeIn(theta0_words, shift=LEFT),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(you.animate.change("confused"))
        self.wait()
        self.play(
            you.animate.change("angry"),
            Create(bubble),
            FadeIn(bubble_content, target_position=you.mouth),
            equations.animate.to_edge(LEFT),
            FadeOut(arrow),
            FadeOut(theta0_words),
        )
        self.wait()

    def create_pi_creature(self):
        return PiCreature(color=BLUE_C).flip().to_corner(DR)
