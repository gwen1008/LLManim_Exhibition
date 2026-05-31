from manim import *


class MainScene(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("Taylor Series Approximation of sin(x)", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---------- Axes ----------
        axes = Axes(
            x_range=[-PI - 0.5, PI + 0.5, PI / 2],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": True, "color": GREY_B},
            tips=True,
        ).shift(DOWN * 0.4)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        self.play(Create(axes), FadeIn(x_label, y_label))
        self.wait(0.3)

        xr = [-PI - 0.3, PI + 0.3]

        # ---------- True sine curve ----------
        sine = axes.plot(lambda x: np.sin(x), x_range=xr, color=BLUE)
        sine_lbl = MathTex(r"\sin(x)", color=BLUE).scale(0.7)

        self.play(Create(sine), run_time=1.5)
        self.wait(0.3)

        # ---------- Legend setup ----------
        def legend_entry(color, text):
            line = Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=6)
            lbl = MathTex(text, color=color).scale(0.55)
            lbl.next_to(line, RIGHT, buff=0.15)
            return VGroup(line, lbl)

        legend = VGroup()
        e0 = legend_entry(BLUE, r"\sin(x)")
        legend.add(e0)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR).shift(DOWN * 0.8)
        self.play(FadeIn(legend))

        def add_legend(color, text):
            entry = legend_entry(color, text)
            entry.scale(1.0)
            new_legend = VGroup(*legend.submobjects, entry)
            new_legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            new_legend.to_corner(UR).shift(DOWN * 0.8)
            self.play(FadeIn(entry))
            return entry

        # ---------- T1 ----------
        t1 = axes.plot(lambda x: x, x_range=xr, color=YELLOW)
        cap1 = Text("Matches only near origin", font_size=24, color=YELLOW)
        cap1.to_edge(DOWN)
        self.play(Create(t1), run_time=1.2)
        add_legend(YELLOW, r"T_1 = x")
        self.play(FadeIn(cap1))
        self.wait(1.2)
        self.play(FadeOut(cap1))

        # ---------- T3 ----------
        t3 = axes.plot(lambda x: x - x**3 / 6, x_range=xr, color=GREEN)
        cap3 = Text("Better fit, wider range", font_size=24, color=GREEN)
        cap3.to_edge(DOWN)
        self.play(Create(t3), run_time=1.2)
        add_legend(GREEN, r"T_3 = x - \tfrac{x^3}{6}")
        self.play(FadeIn(cap3))
        self.wait(1.2)
        self.play(FadeOut(cap3))

        # ---------- T5 ----------
        t5 = axes.plot(
            lambda x: x - x**3 / 6 + x**5 / 120, x_range=xr, color=ORANGE
        )
        self.play(Create(t5), run_time=1.2)
        add_legend(ORANGE, r"T_5 = \dots + \tfrac{x^5}{120}")
        self.wait(1.0)

        # ---------- T7 ----------
        t7 = axes.plot(
            lambda x: x - x**3 / 6 + x**5 / 120 - x**7 / 5040,
            x_range=xr,
            color=RED,
        )
        cap7 = Text("Matches over a much wider range!", font_size=26, color=RED)
        cap7.to_edge(DOWN)
        self.play(Create(t7), run_time=1.4)
        add_legend(RED, r"T_7 = \dots - \tfrac{x^7}{5040}")
        self.play(FadeIn(cap7))
        self.wait(1.5)

        # ---------- Conclusion ----------
        self.play(FadeOut(cap7))
        conclusion = Text(
            "Higher-order Taylor polynomials match the function\nover a wider interval.",
            font_size=28,
            color=WHITE,
            line_spacing=0.8,
        )
        conclusion.to_edge(DOWN)
        box = SurroundingRectangle(conclusion, color=TEAL, buff=0.25)
        self.play(Write(conclusion), Create(box))
        self.wait(2.5)

        self.play(
            *[FadeOut(m) for m in self.mobjects]
        )
        self.wait(0.5)