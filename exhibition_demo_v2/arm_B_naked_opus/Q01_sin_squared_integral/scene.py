from manim import *


class MainScene(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("Evaluating ∫₀^π sin²x dx", font_size=44, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---------- Plot of sin^2(x) with shaded area ----------
        axes = Axes(
            x_range=[0, PI, PI / 4],
            y_range=[0, 1.2, 0.5],
            x_length=6,
            y_length=3,
            tips=False,
            axis_config={"color": GREY_B, "include_numbers": False},
        ).to_corner(DR, buff=0.6)

        x_labels = VGroup(
            MathTex("0").next_to(axes.c2p(0, 0), DOWN, buff=0.2),
            MathTex(r"\pi").next_to(axes.c2p(PI, 0), DOWN, buff=0.2),
        )

        curve = axes.plot(lambda x: np.sin(x) ** 2, x_range=[0, PI], color=BLUE)
        curve_label = MathTex(r"\sin^2 x", color=BLUE).next_to(
            axes.c2p(PI / 2, 1), UP, buff=0.15
        ).scale(0.8)

        area = axes.get_area(curve, x_range=[0, PI], color=TEAL, opacity=0.5)

        self.play(Create(axes), FadeIn(x_labels))
        self.play(Create(curve), Write(curve_label))
        self.play(FadeIn(area))
        self.wait(0.5)

        # ---------- Step container on the left ----------
        steps = VGroup()

        s1 = MathTex(r"I = \int_{0}^{\pi} \sin^2 x \, dx", font_size=40)
        s1.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        self.play(Write(s1))
        steps.add(s1)
        self.wait(0.5)

        s2 = MathTex(
            r"\sin^2 x = \frac{1 - \cos 2x}{2}", font_size=38, color=GREEN
        ).next_to(s1, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(s2))
        self.wait(0.5)

        s3 = MathTex(
            r"I = \frac{1}{2}\int_{0}^{\pi} 1\, dx - \frac{1}{2}\int_{0}^{\pi}\cos 2x\, dx",
            font_size=34,
        ).next_to(s2, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(s3))
        self.wait(0.5)

        s4 = MathTex(
            r"I = \left[\frac{x}{2} - \frac{\sin 2x}{4}\right]_{0}^{\pi}",
            font_size=36,
            color=ORANGE,
        ).next_to(s3, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(s4))
        self.wait(0.5)

        s5 = MathTex(
            r"= \left(\frac{\pi}{2} - \frac{\sin 2\pi}{4}\right) - \left(0 - 0\right)",
            font_size=34,
        ).next_to(s4, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(s5))
        self.wait(0.5)

        s6 = MathTex(
            r"= \frac{\pi}{2} - 0 = \frac{\pi}{2}",
            font_size=38,
        ).next_to(s5, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(s6))
        self.wait(0.5)

        # ---------- Final boxed answer ----------
        answer = MathTex(r"\boxed{I = \dfrac{\pi}{2}}", font_size=46, color=YELLOW)
        answer.next_to(axes, UP, buff=0.5)
        self.play(
            Indicate(area, color=YELLOW, scale_factor=1.05),
            FadeIn(answer, shift=UP),
        )
        self.play(Circumscribe(answer, color=YELLOW))
        self.wait(2)